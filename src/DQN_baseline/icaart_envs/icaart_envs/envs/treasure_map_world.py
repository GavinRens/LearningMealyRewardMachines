import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import environs.treasure_map_world as env

import random

# import src.Learning_MRMs_FormalMethods_3 as L_MRM_FM



class TreasureMapWorld(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):

        #Change this
        self.episode_length = 300 # a default value, to be modified after construction of the Env object



        # Do not change these
        self.env = env
        self.A = env.A + ['reset']
        self.O = env.O + ['null']
        self.state_size = (2 + (len(self.O))*2,)
        self.steps = 0
        self.history = []
        self.reset()


    def state_translation_function(self, input):
        state, obs = input
        if isinstance(state, set):
            v = [0, 0]
            for i in state:
                if "r" in i:
                    v[0] = int(i.split("r")[1])
                else:
                    v[1] = int(i.split("c")[1])
            state = np.array(v, dtype=np.float32)
        else:
            raise NotImplementedError()
        if isinstance(obs, str):
            i = (self.O).index(obs)
            obs = np.eye(len(self.O))[i]
        return state, obs

    def action_translation_function(self, action):
        if isinstance(action, str):
            return self.A.index(action)
        else:
            return self.A[action]
        
    def _state(self):

        return np.concatenate((self.current_state, self.current_obs, self.current_history), axis=-1)

    def step(self, action):

        self.steps += 1
        a = self.action_translation_function(action)
        if a == 'reset':
            self._reset()
            r = env.RESET_COST
        else:
            next_state = self.current_state_env = self.env.SampleNextState(self.current_state_env, a)
            next_obs = self.env.labelingFunc(next_state, a)
            self.current_state, self.current_obs = self.state_translation_function((next_state, next_obs))
            # self.current_history = self.current_history + self.current_obs - self.current_history * self.current_obs
            self.current_history = self.current_history + self.current_obs #- self.current_history * self.current_obs
            r = self.env.EnvironReward(next_obs)

        self.history.append((self.current_state, a, r))

        return self._state(), r, self.steps == self.episode_length, {}



    def _reset(self):
        self.current_state, self.current_obs = self.state_translation_function((self.env.initial, 'null'))
        self.current_state_env = self.env.initial
        self.current_history = [0. for _ in range(len(env.O) + 1)]
        self.env.activeNode_UnderlyingRT = self.env.UnderlyingRT

    def reset(self):
        self.history = []
        self.steps = 0
        self._reset()
        return self._state()


    def render(self, mode='human', close=False):
        # print(self.history[-1])
        pass

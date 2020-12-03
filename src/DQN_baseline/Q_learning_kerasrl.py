import numpy as np
import gym
# import icaart_envs
import tensorflow as tf
import icaart_envs
# import src.DQN_baseline.icaart_envs
# import src.DQN_baseline.icaart_envs.icaart_envs.envs
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

# import src.Learning_MRMs_FormalMethods_3 as L_MRM_FM

NUOF_EPISODES = 1#1200
RESOLUTION = 1#10
# RESOLUTION = L_MRM_FM.RESOLUTION
STEPS_PER_EPISODE = 10#13 * 13 * 3 * 8
# STEPS_PER_EPISODE = L_MRM_FM.STEPS_PER_EPISODE * 8
NUOF_TRIALS = 1#4#10 # also defined in src.Experiments
BATCH_SIZE = 128


# ENV_NAME = 'TreasureMapWorld-v0'
ENV_NAME = 'Cube-v0'
# ENV_NAME = 'OfficeBot-v0'


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
env.episode_length = STEPS_PER_EPISODE
np.random.seed(123)
env.seed(123)
nb_actions = len(env.A)
warmup_episodes = BATCH_SIZE // env.episode_length + 1

# Next, we build a very simple model.
def create_model():
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.state_size))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    return model
# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!



trials = []
for t in range(NUOF_TRIALS):
    model = create_model()
    memory = SequentialMemory(limit=10000, window_length=1)
    policy = EpsGreedyQPolicy(eps=0.1)
    dqn = DQNAgent(model=model, batch_size=BATCH_SIZE, enable_double_dqn=True, nb_actions=nb_actions, memory=memory,
                   nb_steps_warmup=warmup_episodes * env.episode_length,
                   target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    h = dqn.fit(env, nb_steps=(NUOF_EPISODES + warmup_episodes) * env.episode_length , visualize=True, verbose=1)
    trials.append(h.history['episode_reward'][warmup_episodes:])
    # trials.append(h.history['episode_reward'][warmup_episodes::2])

# You can replace DISTINGUISHER with some info to distinguish results for different experiments
with open("results/d_q_learning_baseline_"+ENV_NAME+"_DISTINGUISHER", "w") as file:
# with open("/Users/gavinrens/PycharmProjects/LearningMealyRewardMachines/results/d_q_learning_baseline_"+ENV_NAME+"_DISTINGUISHER", "w") as file:
    file.write("Episodes/{},Return\n".format(RESOLUTION))
    for trial in trials:
        cumulative_reward = 0
        i = 0
        for s, reward in enumerate(trial):
            cumulative_reward += reward
            if s % RESOLUTION == 0:
                i += 1
                file.write("{},{}\n".format(i, cumulative_reward))




#
# # After training is done, we save the final weights.
# dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
# dqn.load_weights('dqn_{}_weights.h5f'.format(ENV_NAME))

# Finally, evaluate our algorithm for 5 episodes.
# dqn.test(env, nb_episodes=10, visualize=True)
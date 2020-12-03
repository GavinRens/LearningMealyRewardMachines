# Assumes null observations are not to be learnt.
# Agent plans to get to required states for required observations (for answering membership queries).
# Agent ignores rewards received for intermediate (non-null) observations.
# Given hypothesis MRM, generate the cross-product and perform MCTS planning on the resulting MDP for exploitation

import environs.treasure_map_world as env
# import environs.office_bot as env
# import environs.cube as env
# import environs.treasure_map_world_small as env

from src.ARM_Learning_MRMs.getExperience import getExperience
from src.ARM_Learning_MRMs.getExperience import MODE_MIN
from src.ARM_Learning_MRMs.getExperience import getActionScheduler
from src.ARM_Learning_MRMs.getExperience import TMP_MODEL_PATH
# import src.MRM_learning_tools as mlt

import stormpy
import stormpy.core

from pylstar.ObservationTable import ObservationTable
from pylstar.Letter import Letter
from pylstar.Word import Word
from pylstar.KnowledgeBase import KnowledgeBase

import random
import time
import re

observation_trace = []
reward_trace = []
# traces_for_comparison = []  # trace records to use for comparison with Tabu RM (Toro Icarte et al. 2019)
rewards = 0
nuof_MQs = 0
nuof_CEs_explor = 0
nuof_CEs_lowReward = 0
total_learning_time = 0
total_exploring_time = 0
actionsExecuted = 0
actionsForLearning = 0
OT = None
RM = None

rewardPerEpisode = 0
RewardPerResolutionVector = []

NUOF_EPISODES = 20
RESOLUTION = 10
STEPS_PER_EPISODE = env.Width * env.Height * 3
# STEPS_PER_EPISODE = env.Width * env.Height * 2 # for tmw, but 3 also works, just takes much longer
# STEPS_PER_EPISODE = 40

# ActionsToExecute = 1000e3 # for treasure-map world when using random exploitation for MRM learning
# MODE = MODE_MAX
MODE = MODE_MIN

# Value given by expert
# Value_expert = 6 #small treasure-map
Value_expert = 9 #treasure-map, < 9.885844748499585
# Value_expert = 0.3 # office-bot, < 0.38327526913557464
# Value_expert = 0.15 # cube, < 0.16239316069874632

# To record the parameters; used in Experiments.py
params = ['FMs', env.Name, NUOF_EPISODES, STEPS_PER_EPISODE, env.APF, ["MIN", "MAX"][MODE], Value_expert, env.C, env.RESET_COST]


class MRMActiveKnowledgeBase(KnowledgeBase):
    """
    The class that implements the main mechanism of an active Mealy Reward Machine knowledge base.
    """

    # def __init__(self, cache_file_path=None):
    #     super(MRMActiveKnowledgeBase, self).__init__(cache_file_path=cache_file_path)

    def __init__(self):
        super(MRMActiveKnowledgeBase, self).__init__()

    # LEARNING BY PLANNING
    def _execute_word(self, input_word):
        # Executes the specified input word.
        global nuof_MQs
        global actionsForLearning
        global actionsExecuted
        global rewards
        global MODE
        global NUOF_EPISODES, RESOLUTION, STEPS_PER_EPISODE
        global RewardPerResolutionVector

        if input_word is None:
            raise Exception("Word cannot be None")
        # print("MQ:", input_word)
        resetUnderlyingMRM()
        reward_trace = []
        nuof_MQs += 1
        env.current_state = env.initial
        scheduler = getExperience(env.current_state, input_word, MODE, env.RESET_COST)  # Create the scheduler

        i = 0
        while i < len(input_word):
            letter = input_word.letters[i]
            reset = False
            a = getActionScheduler(scheduler, env.current_state, i)  # ask for the next action to execute
            next_state = env.SampleNextState(env.current_state, a)  # get the next state
            actionsExecuted += 1
            actionsForLearning += 1
            # Rewards receive while learning are recorded
            if actionsExecuted % (STEPS_PER_EPISODE * RESOLUTION) == 0:
                RewardPerResolutionVector.append(rewards)
            # To catch cases when agent starts in state with first observation letter
            if Letter(env.labelingFunc(next_state, a)) == letter:
                i += 1
                r = env.EnvironReward(env.labelingFunc(next_state, a))
                rewards += r
                reward_trace.append(r)
                env.current_state = next_state
                continue

            while Letter(env.labelingFunc(next_state, a)) != letter:
                if env.labelingFunc(next_state, a) == "null":  # if we observe nothing, execute a new action
                    a = getActionScheduler(scheduler, env.current_state, i)
                    next_state = env.SampleNextState(env.current_state, a)
                    actionsExecuted += 1
                    actionsForLearning += 1
                    r = env.C # Do not use EnvironReward, because then activeNode_UnderlyingRT is updated
                    rewards += r
                    # Rewards receive while learning are recorded
                    if actionsExecuted % (STEPS_PER_EPISODE * RESOLUTION) == 0:
                        RewardPerResolutionVector.append(rewards)
                    env.current_state = next_state
                else:  # if we observe something we don't want, reset
                    reset = True
                    break

            if reset:
                i = 0
                reward_trace = []
                resetUnderlyingMRM()
                rewards += env.RESET_COST
                env.current_state = env.initial
            else:  # if we observe what we want
                i += 1
                r = env.EnvironReward(env.labelingFunc(next_state, a))
                rewards += r
                reward_trace.append(r)

        output_word = Word([Letter(r) for r in reward_trace])
        return output_word


def BuildOT():
    consistent = False
    closed = False
    iteration4OT = 0

    while not consistent or not closed:
        iteration4OT += 1
        print('Building the OT', 'iteration', iteration4OT)
        if not OT.is_closed():
            OT.close_table()
            closed = False
        else:
            closed = True

        inconsistency = OT.find_inconsistency()
        if inconsistency is not None:
            OT.make_consistent(inconsistency)
            consistent = False
        else:
            consistent = True


def getStateInHypothesis(states_h, state):
    for i in states_h:
        if int(i.name) == int(state):
            return i

# For office-bot
'''def buildProductAutomaton(h):

    # Given a hypothesis of the angluin algo, build the product between the gird and this hypothesis. The init state is {'c1','r1','null'} with no obs already made
    rewards = "rewards\n"
    labels = ''
    out_file = open(TMP_MODEL_PATH, 'w')
    # module
    out_file.write("mdp\n\nmodule tmp\n\n")

    # number of state and initial state
    new_states = []
    for s in env.S:
        for o in range(len(h.get_states())):
            labels += 'label "r' + str(env.getRow(s)) + '_c' + str(env.getColumn(s)) + '_' + str(o) + '" = s=' + str(
                len(new_states)) + ' ;\n'
            new_states.append((s, o))

    out_file.write("\ts : [0.." + str(len(new_states)) + "] init " + str(new_states.index((env.initial, 0))) + ";\n\n")

    # transitions
    for s in new_states:
        for a in env.A:
            obs = env.labelingFunc(s[0], a)
            out_file.write("\t[" + a + "] s=" + str(new_states.index(s)) + "-> ")

            temp_list = []
            destList = env.GetTransitions(s[0], a)

            if obs == 'null':
                rewards += "\t[" + a + "] (s=" + str(new_states.index(s)) + ") : " + str(env.C) + ";\n"

                for (dest, prob) in destList:
                    index_dest = str(new_states.index((dest, s[1])))
                    temp_list.append(str(prob) + " : (s'=" + index_dest + ")")
            else:
                tr_val = h.play_word(Word([Letter(obs)]), getStateInHypothesis(h.get_states(), s[1]))
                state_in_h = int(tr_val[1][-1].name)
                rewards += "\t[" + a + "] (s=" + str(new_states.index(s)) + ") : " + str(
                    tr_val[0].last_letter().name) + ";\n"
                for (dest, prob) in destList:
                    index_dest = str(new_states.index((dest, state_in_h)))
                    temp_list.append(str(prob) + " : (s'=" + index_dest + ")")

            out_file.write(" + ".join(temp_list))
            out_file.write(";\n")

        a = "reset"
        out_file.write("\t[" + a + "] s=" + str(new_states.index(s)) + "-> 1.0 : (s'=" + str(
            new_states.index((env.initial, 0))) + ");\n")
        rewards += "\t[" + a + "] (s=" + str(new_states.index(s)) + ") : " + str(env.RESET_COST) + ";\n"

    out_file.write("\nendmodule\n\n")
    out_file.write(labels)

    rewards += "endrewards\n"
    out_file.write(rewards)
    out_file.close()'''


# For environs besides office-bot
def buildProductAutomaton(h):

    # Given a hypothesis of the angluin algo, build the product between the gird and this hypothesis. The init state is {'c1','r1','null'} with no obs already made
    rewards = "rewards\n"
    labels = ''
    out_file = open(TMP_MODEL_PATH, 'w')
    # module
    out_file.write("mdp\n\nmodule tmp\n\n")

    # number of state and initial state
    new_states = []
    for s in env.S:
        for o in range(len(h.get_states())):
            labels += 'label "r' + str(env.getRow(s)) + '_c' + str(env.getColumn(s)) + '_' + str(o) + '" = s=' + str(
                len(new_states)) + ' ;\n'
            new_states.append((s, o))

    out_file.write("\ts : [0.." + str(len(new_states)) + "] init " + str(new_states.index((env.initial, 0))) + ";\n\n")

    # transitions
    for s in new_states:
        for a in env.A:
            dest = env.SampleNextState(s[0], a, False)
            out_file.write("\t[" + a + "] s=" + str(new_states.index(s)) + "-> " + str(env.APF) + " : (s'=")
            # if {'null'}.issubset(dest): #CHANGE
            if env.labelingFunc(dest, a) == 'null':
                out_file.write(str(new_states.index((dest, s[1]))))
                rewards += "\t[" + a + "] (s=" + str(new_states.index(s)) + ") : " + str(env.C) + ";\n"
            else:
                for o in env.O:
                    # if {o}.issubset(dest): #CHANGE
                    if env.labelingFunc(dest, a) == o:
                        tr_val = h.play_word(Word([Letter(o)]), getStateInHypothesis(h.get_states(), s[1]))
                        state_in_h = int(tr_val[1][-1].name)
                        out_file.write(str(new_states.index((dest, state_in_h))))
                        rewards += "\t[" + a + "] (s=" + str(new_states.index(s)) + ") : " + str(
                            tr_val[0].last_letter().name) + ";\n"
                        break
            out_file.write(") + " + str(1 - env.APF) + " :(s'=" + str(new_states.index(s)) + ");\n")
        a = "reset"
        out_file.write("\t[" + a + "] s=" + str(new_states.index(s)) + "-> 1.0 : (s'=" + str(
            new_states.index((env.initial, 0))) + ");\n")
        rewards += "\t[" + a + "] (s=" + str(new_states.index(s)) + ") : " + str(env.RESET_COST) + ";\n"

    out_file.write("\nendmodule\n\n")
    out_file.write(labels)

    rewards += "endrewards\n"
    out_file.write(rewards)
    out_file.close()


def getIndexStateHFromMap(states, state, node):
    for s in range(len(states)):
        if {"r" + str(env.getRow(state)) + "_c" + str(env.getColumn(state)) + '_' + str(node)}.issubset(
                states[s].labels):
            return s


def getRewardH(state, action, rewards):
    return rewards[state * (len(env.A) + 1) + int(action.__str__())]  # +1 because we have the reset action


def getNextSateH(state, action):
    action = state.actions[action]
    r = random.random()
    c = 0
    for transition in action.transitions:
        c += transition.value()
        if r < c:
            break
    return transition.column


def fromIdStateHToStateM(sh, states_h):
    pattern = re.compile("r[0-9]+_c[0-9]+_[0-9]+")
    for i in states_h[sh].labels:
        if pattern.match(i):
            return {'r' + str(i[1]), 'c' + str(i[4])}


def executeOneStepExploration(current_state_h, states_h, action, rewards_h):
    next_state_h = getNextSateH(states_h[current_state_h], action) # Sample next state from product MDP
    r_h = getRewardH(current_state_h, action, rewards_h.state_action_rewards)
    next_state_m = fromIdStateHToStateM(next_state_h, states_h)
    # next_state_m = env.SampleNextState(env.current_state, env.A[int(action.__str__())])
    obs = env.labelingFunc(next_state_m, action)
    r_m = None
    if obs == 'null':
        r_m = env.C
    else:
        r_m = env.EnvironReward(obs)
    return (r_h, r_m, next_state_h, next_state_m, obs)


def findCounterExample(model):
    global actionsExecuted
    global STEPS_PER_EPISODE
    global rewards
    resetUnderlyingMRM()
    observation_trace = []
    reward_trace = []
    env.current_state = env.initial
    current_state_h = getIndexStateHFromMap(model.states, env.current_state, 0)
    while True:
        a = int(random.random() // (1 / len(env.A)))
        (r_h, r_m, next_state_h, next_state_m, obs) = executeOneStepExploration(current_state_h, model.states,
                                                                                    a, model.reward_models[''])
        actionsExecuted += 1
        rewards += r_m
        # Rewards receive while learning are recorded
        if actionsExecuted % (STEPS_PER_EPISODE * RESOLUTION) == 0:
            RewardPerResolutionVector.append(rewards)

        env.current_state = next_state_m
        current_state_h = next_state_h
        if obs != 'null':
            observation_trace.append(obs)
            reward_trace.append(r_m)
            if r_m != r_h: # a counter example has been encountered
                return observation_trace, reward_trace
        if actionsExecuted % STEPS_PER_EPISODE == 0:
            resetUnderlyingMRM()
            observation_trace = []
            reward_trace = []
            # Initialize agent's state
            env.current_state = env.initial
            current_state_h = getIndexStateHFromMap(model.states, env.current_state, 0)


def resetUnderlyingMRM():
    env.activeNode_UnderlyingRT = env.UnderlyingRT


def BuildHyp(OT):
    consistent = False
    closed = False

    while not consistent or not closed:
        if not OT.is_closed():
            OT.close_table()
            closed = False
        else:
            closed = True

        inconsistency = OT.find_inconsistency()
        if inconsistency is not None:
            OT.make_consistent(inconsistency)
            consistent = False
        else:
            consistent = True
    return OT.build_hypothesis()


results = []  # To record the results; used in Experiments.py


def main(iteration):
    # if __name__ == '__main__':
    global rewards
    global rewardPerEpisode
    global RewardPerResolutionVector
    global total_learning_time
    global total_exploring_time
    global actionsExecuted
    global actionsForLearning
    global nuof_MQs
    global nuof_CEs_explor
    global nuof_CEs_lowReward
    global OT
    global RM
    global results
    global NUOF_EPISODES, RESOLUTION, STEPS_PER_EPISODE

    rewards = 0
    RewardPerResolutionVector = []
    nuof_MQs = 0
    nuof_CEs_explor = 0
    nuof_CEs_lowReward = 0
    total_learning_time = 0
    total_exploring_time = 0
    actionsExecuted = 0
    actionsForLearning = 0
    OT = None
    RM = None
    print('\n\n')
    print('------------------------------------')
    print('Running trial', iteration, '...')
    print('------------------------------------')
    StartExperimentTime = time.time()

    # initialize MRM / Observation Table
    input_vocabulary = env.O  # the input vocabulary is the set of observations
    in_letters = [Letter(symbol) for symbol in input_vocabulary]
    kbase = MRMActiveKnowledgeBase()
    OT = ObservationTable(input_letters=in_letters, knowledge_base=kbase)

    print()
    print('Initializing the OT ...')
    OT.initialize()

    RM = BuildHyp(OT)
    print(RM.build_dot_code())
    print('Building product automaton')
    buildProductAutomaton(RM)
    program = stormpy.parse_prism_program(TMP_MODEL_PATH)
    properties = stormpy.parse_properties_for_prism_program("Rmax=? [ LRA ]", program)
    options = stormpy.BuilderOptions(True, True)  # To keep rewards and labels
    model = stormpy.build_sparse_model_with_options(program, options)
    result = stormpy.model_checking(model, properties[0], extract_scheduler=True)
    print('Value of policy wrt H:', result.at(0))

    for e in range(NUOF_EPISODES):
        print('------------------------------------')
        print('EPISODE NUMBER ', e+1)
        print('------------------------------------')

        # Reset system
        resetUnderlyingMRM()
        observation_trace = []
        reward_trace = []
        env.current_state = env.initial
        current_state_h = getIndexStateHFromMap(model.states, env.current_state, 0)

        for step in range(STEPS_PER_EPISODE):
            if result.at(0) < Value_expert:
                print(result.at(0), " < Value_expert, looking for counter-example...")
                StartTime1 = time.time()
                observation_trace, reward_trace = findCounterExample(model)
                nuof_CEs_lowReward += 1
                input_word = Word([Letter(symbol) for symbol in observation_trace])
                output_word = Word([Letter(symbol) for symbol in reward_trace])
                print('Adding counter-example (case 1) ...')
                print('observation_trace:', observation_trace)
                print('reward_trace:', reward_trace)
                OT.add_counterexample(input_word, output_word)
                EndTime1 = time.time()
                total_learning_time += EndTime1 - StartTime1
                RM = BuildHyp(OT)
                print(RM.build_dot_code())
                print('Building product automaton')
                buildProductAutomaton(RM)
                program = stormpy.parse_prism_program(TMP_MODEL_PATH)
                properties = stormpy.parse_properties_for_prism_program("Rmax=? [ LRA ]", program)
                options = stormpy.BuilderOptions(True, True)  # To keep rewards and labels
                model = stormpy.build_sparse_model_with_options(program, options)
                result = stormpy.model_checking(model, properties[0], extract_scheduler=True)
                print('Value of policy wrt H:', result.at(0))
            else:
                StartTime2 = time.time()
                scheduler = result.scheduler
                a = scheduler.get_choice(current_state_h)
                a = a.get_deterministic_choice()
                if int(a.__str__()) == len(env.A): # a is the reset action
                    # But still in same episode
                    (r_h, r_m, next_state_h, next_state_m, obs) = (env.RESET_COST, env.RESET_COST, model.initial_states[0], env.initial, "null")
                    # Reset system
                    resetUnderlyingMRM()
                    observation_trace = []
                    reward_trace = []
                    env.current_state = env.initial
                    current_state_h = getIndexStateHFromMap(model.states, env.current_state, 0)
                    rewards += r_m
                    actionsExecuted += 1
                else:
                    (r_h, r_m, next_state_h, next_state_m, obs) = executeOneStepExploration(current_state_h, model.states,
                                                                                            a, model.reward_models[''])
                    current_state_h = next_state_h
                    env.current_state = next_state_m
                    rewards += r_m
                    actionsExecuted += 1
                if actionsExecuted % (STEPS_PER_EPISODE*RESOLUTION) == 0:
                    RewardPerResolutionVector.append(rewards)
                EndTime2 = time.time()
                total_exploring_time += EndTime2 - StartTime2
                if obs != 'null':
                    observation_trace.append(obs)
                    reward_trace.append(r_m)
                    # if r_m != r_h, a counter example has been encountered
                    if r_m != r_h:
                        print('r_m:', r_m, 'r_h:', r_h)
                        nuof_CEs_explor += 1
                        StartTime3 = time.time()
                        input_word = Word([Letter(symbol) for symbol in observation_trace])
                        output_word = Word([Letter(symbol) for symbol in reward_trace])
                        print('Adding counter-example (case 2) ...')
                        print('observation_trace:', observation_trace)
                        print('reward_trace:', reward_trace)
                        OT.add_counterexample(input_word, output_word)
                        RM = BuildHyp(OT)
                        print(RM.build_dot_code())
                        print('Building product automaton')
                        buildProductAutomaton(RM)
                        program = stormpy.parse_prism_program(TMP_MODEL_PATH)
                        properties = stormpy.parse_properties_for_prism_program("Rmax=? [ LRA ]", program)
                        options = stormpy.BuilderOptions(True, True)  # To keep rewards and labels
                        model = stormpy.build_sparse_model_with_options(program, options)
                        result = stormpy.model_checking(model, properties[0], extract_scheduler=True)
                        print('Value of policy wrt H:', result.at(0))
                        EndTime3 = time.time()
                        total_learning_time += EndTime3 - StartTime3
                        continue


    EndExperimentTime = time.time()
    EperimentTime = EndExperimentTime - StartExperimentTime

    print()
    print(RM.build_dot_code())

    print()
    print('STEPS_PER_EPISODE:', STEPS_PER_EPISODE)
    print('APF:', env.APF)
    print('Optimization problem:', ["MIN", "MAX"][MODE])
    print()

    print('rewards:', rewards)
    print('nuof actions executed:', actionsExecuted)
    print('nuof actions for learning:', actionsForLearning)
    print('nuof MQs:', nuof_MQs)
    print('nuof counter examples found during exploration:', nuof_CEs_explor)
    print('nuof counter examples found due to value < expert value:', nuof_CEs_lowReward)
    print('total learning time:', total_learning_time)
    print('total exploring time:', total_exploring_time)
    print('total experiment time (mins):', EperimentTime // 60)

    results = [rewards, actionsExecuted, nuof_MQs, nuof_CEs_explor, nuof_CEs_lowReward,
               total_learning_time, total_exploring_time, (total_learning_time + total_exploring_time)]

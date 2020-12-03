import stormpy
import stormpy.core
import re
from pylstar.Letter import Letter
from pylstar.Word import Word

import environs.treasure_map_world as env
# import environs.office_bot as env
# import environs.cube as env
# import environs.treasure_map_world_small as env

TMP_MODEL_PATH = "tmp.nm"
MODE_MAX = 1
MODE_MIN = 0


def mappingState(s):
    return env.S.index(s)


def inverseMappingState(s):
    return env.S[s]


def mappingAction(a):
    return env.A.index(a)


def inverseMappingAction(a):
    try:
        return env.A[a]
    except IndexError:
        return a


def getStateInNRMDP(lbls):
    """Given the labels of a state in G, return the corresponding state and observation in M"""
    pattern = re.compile("s[0-9]+_obs[0-9]+")
    for i in lbls:
        if pattern.match(i):
            return [int(i[1:i.index('_')]), int(i[i.index('obs') + 3:])]


def printScheduler(sch):
    for i in range(len(sch)):
        c = -1
        f = False

        for j in range(len(sch[i])):
            if sch[i][j] != -1 and c != -1 and c != sch[i][j]:
                f = True
                break
            if sch[i][j] != -1 and c != sch[i][j]:
                c = sch[i][j]

        print("\nIn state ", inverseMappingState(i), "|", i, ":")
        if f:
            for j in range(len(sch[i])):
                if sch[i][j] != -1:
                    if j == 0:
                        print("\tIf observation", 0, "do action", inverseMappingAction(sch[i][j]))
                    else:
                        print("\tIf observation", env.O[j - 1], "do action", inverseMappingAction(sch[i][j]))
        else:
            for j in sch[i]:
                if j != -1:
                    print("\tDo action", inverseMappingAction(j))
                    break
            if j == -1:
                print("\tIt doen't matter")


def createPrismModel(states, transitions, target, mode, nr_actions, reset_transitions, reset_cost):
    """Create a prism file describing the temporary model (G in the notes)"""
    out_file = open(TMP_MODEL_PATH, 'w')
    # module
    out_file.write("mdp\n\nmodule tmp\n\n")

    # number of state and initial state
    out_file.write("\ts : [0.." + str(len(states)) + "] init " + str(abs(mode)) + ";\n\n")

    # transitions
    for state in range(len(transitions)):
        for action in range(len(transitions[state])):
            if sum(transitions[state][action]) != 0:
                out_file.write("\t[" + chr(97 + action) + "] s=" + str(state) + "-> ")
                destinations = []
                for dest in range(len(transitions[state][action])):
                    if transitions[state][action][dest] != 0:
                        destinations.append(str(transitions[state][action][dest]) + ":(s'=" + str(dest) + ")")
                out_file.write(" + ".join(destinations))
                out_file.write(";\n")
    out_file.write("\nendmodule\n\n")

    # label target
    out_file.write('label "target" = ')
    target = list(set(target))
    target = ["(s=" + str(x) + ")" for x in target]
    if len(target) == 0:
        out_file.write("(s=" + str(len(states) + 1) + ");\n")
    else:
        out_file.write(" | ".join(target))
        out_file.write(";\n")

    # label states
    if mode == MODE_MAX:
        out_file.write('label "sink" = (s=0);\n')

    for i in range(mode, len(states)):
        out_file.write('label "s' + str(states[i][0]) + '_obs' + str(states[i][1]) + '" = (s=' + str(i) + ');\n')

    if mode == MODE_MIN:
        out_file.write("\nrewards\n")
        if reset_cost == 1:
            out_file.write("\ttrue:1;\n")
        else:
            for i in range(len(states)):
                for j in range(nr_actions):
                    if j in reset_transitions[i]:
                        out_file.write("\t[" + chr(97 + j) + "] (s=" + str(i) + ") : " + str(reset_cost) + ";\n")
                    else:
                        out_file.write("\t[" + chr(97 + j) + "] (s=" + str(i) + ") : 1;\n")

        out_file.write("endrewards\n")

    out_file.close()


def createNewState(new_state, states, transitions, reset_transitions):
    """Create a new state in the temporary model (G in the notes)"""
    states.append(new_state)
    transitions.append([])
    nr_actions = len(env.A)

    # create new row in self.transitions for the new state
    for i in range(nr_actions):
        transitions[-1].append([])
        for j in range(len(states)):
            transitions[-1][-1].append(0)
    # add new cell in self.transitions old rows (for old self.states)
    for i in range(len(states) - 1):
        for j in range(nr_actions):
            transitions[i][j].append(0)

    reset_transitions.append([])


def addNewTransition(new_state, tr_from, tr_action, tr_prob, states, transitions, reset_transitions):
    """add a new transition in the temporary model (G in the notes)"""
    if not new_state in states:
        createNewState(new_state, states, transitions, reset_transitions)

    i = states.index(new_state)
    tr_from = states.index(tr_from)
    if transitions[tr_from][tr_action][i] == tr_prob:  # We are looping
        return False
    transitions[tr_from][tr_action][i] = tr_prob
    return True


def createNewMdp(states, transitions, state, observations, current_obs, target, reset_transitions):
    """Function which build the temporary MDP"""
    to_add = []
    for action in env.A:
        seen_obs = env.labelingFunc(state, action)

        destList = env.GetTransitions(state, action)
        for (next_state, proba) in destList:

            if seen_obs == "null":  # we observe nothing
                new_state = (mappingState(next_state), current_obs)

                if addNewTransition(new_state, (mappingState(state), current_obs), mappingAction(action), proba, states,
                                    transitions, reset_transitions):
                    to_add.append((next_state, current_obs))

            elif Letter(seen_obs) == observations.letters[current_obs]:  # we observe what we want
                current_obs += 1
                new_state = (mappingState(next_state), current_obs)
                if addNewTransition(new_state, (mappingState(state), current_obs - 1), mappingAction(action), proba,
                                    states, transitions, reset_transitions):
                    if len(observations) == current_obs:  # we have done
                        target.append(states.index(new_state))
                    else:  # continue in every direction
                        to_add.append((next_state, current_obs))

                current_obs -= 1

            else:  # we observe something we don't want
                transitions[states.index((mappingState(state), current_obs))][mappingAction(action)][0] = 1.0
                reset_transitions[states.index((mappingState(state), current_obs))].append(mappingAction(action))

    return to_add


def initializeTransitions(states, transitions, nr_actions):
    """initialize the transitions matrix of the new mdp"""
    for k in range(len(states)):
        transitions.append([])
        for i in range(nr_actions):
            transitions[-1].append([])
            for j in range(len(states)):
                transitions[-1][-1].append(0)


def getExperience(initial_state, observations, mode, reset_cost):
    """
	Args:
		initial_state (member of env.S): the initial state of our env
		observations (pylstar.Word): the observations we want to reach (in the wanted order)
		mode (int): MODE_MAX to maximize the prob to see the observations in one try (currently not working)
					MODE_MIN to minimize the number of actions executed to see the observations
	
	Returns:
		python matrix: matrix representing the scheduler (bounded memory strategy)
	"""
    nr_actions = len(env.A)

    # create New Model-----------------------------------------------------------
    if mode == MODE_MAX:
        states = [(-1, -1), (mappingState(initial_state), 0)]
    if mode == MODE_MIN:
        states = [(mappingState(initial_state), 0)]
    transitions = []
    target = []
    reset_transitions = [[]]
    if mode == MODE_MAX:
        reset_transitions.append([])
    initializeTransitions(states, transitions, nr_actions)
    to_add = [(initial_state, 0)]
    while len(to_add) > 0:
        next_add = to_add.pop(0)
        to_add += createNewMdp(states, transitions, next_add[0], observations, next_add[1], target, reset_transitions)
    createPrismModel(states, transitions, target, mode, nr_actions, reset_transitions, -reset_cost)

    # build new model------------------------------------------------------------
    program = stormpy.parse_prism_program(TMP_MODEL_PATH)
    if mode == MODE_MAX:
        prop = 'Pmax=? [F "target"]'
    if mode == MODE_MIN:
        prop = 'Rmin=? [F "target"]'
    properties = stormpy.parse_properties_for_prism_program(prop, program)
    options = stormpy.BuilderOptions(True, True)  # To keep rewards and labels
    model = stormpy.build_sparse_model_with_options(program, options)

    # compute prop---------------------------------------------------------------
    result = stormpy.model_checking(model, properties[0], extract_scheduler=True)

    # extract scheduler----------------------------------------------------------
    scheduler = result.scheduler
    scheduler_nrmdp = []
    for i in range(len(env.S)):
        scheduler_nrmdp.append([])
        for j in range(len(observations) + 1):
            scheduler_nrmdp[-1].append(-1)
    for state in model.states:
        if not "sink" in state.labels:
            state_lbl = getStateInNRMDP(state.labels)
            scheduler_nrmdp[state_lbl[0]][state_lbl[1]] = scheduler.get_choice(state).get_deterministic_choice()
    return scheduler_nrmdp


def getActionScheduler(sch, state, index_wanted_obs):
    state = mappingState(state)
    return inverseMappingAction(sch[state][index_wanted_obs])


if __name__ == '__main__':
    w = []
    for i in env.O:
        w.append(Letter(i))
    w = Word(w)
    getExperience(env.S[0], w, MODE_MAX, 1)
    print("-----------------------------------------")
# getExperience(env.S[0],w,MODE_MIN,1)

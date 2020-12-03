from environs.treasure_map_world import labelingFunc
# from environs.office_bot import labelingFunc
# from environs.cube import labelingFunc
# from environs.treasure_map_world_small import labelingFunc


def getSymbolFromLetter(letter):
    return list(letter.symbols)[0]


def extractStateTrace(i_a_trace):
    # assuming interaction_trace = [action_1, state_1, reward_1, ..., action_k, state_k, reward_k]
    sttTrace = []
    for i in range(len(i_a_trace)):
        if i % 3 == 1:
            sttTrace.append(i_a_trace[i])
    return sttTrace


def extractObservationTrace(i_a_trace):
    # assuming interaction_trace = [action_1, state_1, reward_1, ..., action_k, state_k, reward_k]
    obsTrace = []
    for i in range(len(i_a_trace)):
        if i % 3 == 1:
            obsTrace.append(labelingFunc(i_a_trace[i],i_a_trace[i-1]))
    return obsTrace


def extractRewTrace(interaction_trace):
    # assuming interaction_trace = [action_1, state_1, reward_1, ..., action_k, state_k, reward_k]
    rewTrace = []
    for i in range(len(interaction_trace)):
        if i % 3 == 2:
            rewTrace.append(interaction_trace[i])
    return rewTrace


def sttTrace2obsSeq(state_trace):
    obsSeq = []
    for s in state_trace:
        obsSeq.append(labelingFunc(s))
    return obsSeq

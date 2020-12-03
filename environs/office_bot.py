import random
import copy

Name = 'OfficeBot'
print(Name)
'''This is the specification of an MDP for a Width by Height gridworld.
The objective is to visit cells in a particular order, so that observations are made in a particular order.'''

# Number of grid columns
Width = 3

# Number of grid rows
Height = 7

# Default reward
C = -0.1

# Reset cost
RESET_COST = -2


# Action Precision Factor
APF = 0.95
# APF = 1

Obstacles = [(2,1),(2,2),(2,3),(2,5),(2,6),(2,7),(3,1),(3,2),(3,6),(3,7)]


# States
S = []
for col in range(1, Width + 1):
    for row in range(1, Height + 1):
        if (col, row) not in Obstacles:
            S.append({'c' + str(col), 'r' + str(row)})


# Initialize agent's state
# initial = None
# current_state = None
# while initial == None:
#     x = random.choice([i for i in range(1, Width + 1)])
#     y = random.choice([j for j in range(1, Height + 1)])
#     for s in S:
#         if (x, y) not in Obstacles and {'c' + str(x), 'r' + str(y)}.issubset(s):
#             initial = s
#             break

initial = {'c2','r4'}

current_state = initial


ids = 0

class UMRMNode:
    def __init__(self, name=None):
        self.name = name
        self.edges = []

    def addEdge(self, edge):
        self.edges.append(edge)


# Edge of the underlying MRM
class UMRMEdge:
    def __init__(self, transition_condition, output_reward, arrival_node):
        self.transcond = transition_condition
        self.reward = output_reward
        self.node = arrival_node

    # Method to return the RT rooted at this node as a string (i.t.o. only rewards).
    # def __str__(self):
    #     X = 'id: ' + str(self.id) + ' | ' + 'visits: ' + str(self.visits) + ': <' + str(self.transcond) + ' | ' + str(
    #         self.reward) + '>' + ', children: ' + str(self.children)
    #     for idd in self.children:
    #         X += '\n' + '   ' + str(UnderlyingRTNodes[idd])
    #     return X


# Actions
A = ['n', 'e', 'w', 's', 'ask', 'pickMailA', 'pickDonutA', 'dropItemA', 'pickMailB', 'pickDonutB', 'dropItemB']
# north, east, west, south, ask what person wants, pmX = pickup mail for X, pd = pickup donut, dX = dropoff item for X

# Observations
O = ['mailRequestA', 'donutRequestA', 'haveMailA', 'haveDonutA', 'mailRequestB', 'donutRequestB', 'haveMailB', 'haveDonutB', 'itemDelivered']
# mail requested, donut requested, have mail, have donut, item delivered


def labelingFunc(s, a=None):
    if type(a) == type(0):
        a = A[a]

    # Office of A
    if a == 'ask':
        if {'c1', 'r7'}.issubset(s):
            return 'mailRequestA'
        if {'c1', 'r6'}.issubset(s):
            return 'donutRequestA'
    if a == 'dropItemA':
        if {'c1', 'r7'}.issubset(s) or {'c1', 'r6'}.issubset(s):
            return 'itemDelivered'

    # Office of B
    if a == 'ask':
        if {'c1', 'r2'}.issubset(s):
            return 'donutRequestB'
        if {'c1', 'r1'}.issubset(s):
            return 'mailRequestB'
    if a == 'dropItemB':
        if {'c1', 'r1'}.issubset(s) or {'c1', 'r2'}.issubset(s):
            return 'itemDelivered'

    # Mail Room
    if {'c3', 'r5'}.issubset(s):
        if a == 'pickMailA':
            return 'haveMailA'
        if a == 'pickMailB':
            return 'haveMailB'

    # Kitchen
    if {'c3', 'r3'}.issubset(s) :
        if a == 'pickDonutA':
            return 'haveDonutA'
        if a == 'pickDonutB':
            return 'haveDonutB'

    return 'null'


# Defining the underlying reward model of the running example

Node_0 = UMRMNode('Node_0')
Node_1 = UMRMNode('Node_1')
Node_2 = UMRMNode('Node_2')
Node_3 = UMRMNode('Node_3')
Node_4 = UMRMNode('Node_4')
Node_5 = UMRMNode('Node_5')
Node_6 = UMRMNode('Node_6')
Node_7 = UMRMNode('Node_5')
Node_8 = UMRMNode('Node_6')


Edge_mailRequestA03 = UMRMEdge('mailRequestA', 1, Node_3)
# Edge_mailRequestA03 = UMRMEdge('mailRequestA', C, Node_3)
Edge_donutRequestA01 = UMRMEdge('donutRequestA', 1, Node_1)
# Edge_donutRequestA01 = UMRMEdge('donutRequestA', C, Node_1)
Edge_mA00 = UMRMEdge('haveMailA', C, Node_0)
Edge_dA00 = UMRMEdge('haveDonutA', C, Node_0)
Edge_mailRequestB04 = UMRMEdge('mailRequestB', 1, Node_4)
# Edge_mailRequestB04 = UMRMEdge('mailRequestB', C, Node_4)
Edge_donutRequestB02 = UMRMEdge('donutRequestB', 1, Node_2)
# Edge_donutRequestB02 = UMRMEdge('donutRequestB', C, Node_2)
Edge_mB00 = UMRMEdge('haveMailB', C, Node_0)
Edge_dB00 = UMRMEdge('haveDonutB', C, Node_0)
Edge_del00 = UMRMEdge('itemDelivered', C, Node_0)
Node_0.addEdge(Edge_mailRequestA03)
Node_0.addEdge(Edge_donutRequestA01)
Node_0.addEdge(Edge_mA00)
Node_0.addEdge(Edge_dA00)
Node_0.addEdge(Edge_mailRequestB04)
Node_0.addEdge(Edge_donutRequestB02)
Node_0.addEdge(Edge_mB00)
Node_0.addEdge(Edge_dB00)
Node_0.addEdge(Edge_del00)

Edge_mailRequestA11 = UMRMEdge('mailRequestA', C, Node_1)
Edge_donutRequestA11 = UMRMEdge('donutRequestA', C, Node_1)
Edge_mA11 = UMRMEdge('haveMailA', C, Node_1)
Edge_dA15 = UMRMEdge('haveDonutA', 2, Node_5)
Edge_mailRequestB11 = UMRMEdge('mailRequestB', C, Node_1)
Edge_donutRequestB11 = UMRMEdge('donutRequestB', C, Node_1)
Edge_mB11 = UMRMEdge('haveMailB', C, Node_1)
Edge_dB11 = UMRMEdge('haveDonutB', C, Node_1)
Edge_del11 = UMRMEdge('itemDelivered', C, Node_1)
Node_1.addEdge(Edge_mailRequestA11)
Node_1.addEdge(Edge_donutRequestA11)
Node_1.addEdge(Edge_mA11)
Node_1.addEdge(Edge_dA15)
Node_1.addEdge(Edge_mailRequestB11)
Node_1.addEdge(Edge_donutRequestB11)
Node_1.addEdge(Edge_mB11)
Node_1.addEdge(Edge_dB11)
Node_1.addEdge(Edge_del11)

Edge_mailRequestA22 = UMRMEdge('mailRequestA', C, Node_2)
Edge_donutRequestA22 = UMRMEdge('donutRequestA', C, Node_2)
Edge_mA22 = UMRMEdge('haveMailA', C, Node_2)
Edge_dA22 = UMRMEdge('haveDonutA', C, Node_2)
Edge_mailRequestB22 = UMRMEdge('mailRequestB', C, Node_2)
Edge_donutRequestB22 = UMRMEdge('donutRequestB', C, Node_2)
Edge_mB22 = UMRMEdge('haveMailB', C, Node_2)
Edge_dB27 = UMRMEdge('haveDonutB', 2, Node_7)
Edge_del22 = UMRMEdge('itemDelivered', C, Node_2)
Node_2.addEdge(Edge_mailRequestA22)
Node_2.addEdge(Edge_donutRequestA22)
Node_2.addEdge(Edge_mA22)
Node_2.addEdge(Edge_dA22)
Node_2.addEdge(Edge_mailRequestB22)
Node_2.addEdge(Edge_donutRequestB22)
Node_2.addEdge(Edge_mB22)
Node_2.addEdge(Edge_dB27)
Node_2.addEdge(Edge_del22)

Edge_mailRequestA33 = UMRMEdge('mailRequestA', C, Node_3)
Edge_donutRequestA33 = UMRMEdge('donutRequestA', C, Node_3)
Edge_mA36 = UMRMEdge('haveMailA', 2, Node_6)
Edge_dA33 = UMRMEdge('haveDonutA', C, Node_3)
Edge_mailRequestB33 = UMRMEdge('mailRequestB', C, Node_3)
Edge_donutRequestB33 = UMRMEdge('donutRequestB', C, Node_3)
Edge_mB33 = UMRMEdge('haveMailB', C, Node_3)
Edge_dB33 = UMRMEdge('haveDonutB', C, Node_3)
Edge_del33 = UMRMEdge('itemDelivered', C, Node_3)
Node_3.addEdge(Edge_mailRequestA33)
Node_3.addEdge(Edge_donutRequestA33)
Node_3.addEdge(Edge_mA36)
Node_3.addEdge(Edge_dA33)
Node_3.addEdge(Edge_mailRequestB33)
Node_3.addEdge(Edge_donutRequestB33)
Node_3.addEdge(Edge_mB33)
Node_3.addEdge(Edge_dB33)
Node_3.addEdge(Edge_del33)

Edge_mailRequestA44 = UMRMEdge('mailRequestA', C, Node_4)
Edge_donutRequestA44 = UMRMEdge('donutRequestA', C, Node_4)
Edge_mA44 = UMRMEdge('haveMailA', C, Node_4)
Edge_dA44 = UMRMEdge('haveDonutA', C, Node_4)
Edge_mailRequestB44 = UMRMEdge('mailRequestB', C, Node_4)
Edge_donutRequestB44 = UMRMEdge('donutRequestB', C, Node_4)
Edge_mB48 = UMRMEdge('haveMailB', 2, Node_8)
Edge_dB44 = UMRMEdge('haveDonutB', C, Node_4)
Edge_del44 = UMRMEdge('itemDelivered', C, Node_4)
Node_4.addEdge(Edge_mailRequestA44)
Node_4.addEdge(Edge_donutRequestA44)
Node_4.addEdge(Edge_mA44)
Node_4.addEdge(Edge_dA44)
Node_4.addEdge(Edge_mailRequestB44)
Node_4.addEdge(Edge_donutRequestB44)
Node_4.addEdge(Edge_mB48)
Node_4.addEdge(Edge_dB44)
Node_4.addEdge(Edge_del44)

Edge_mailRequestA55 = UMRMEdge('mailRequestA', C, Node_5)
Edge_donutRequestA55 = UMRMEdge('donutRequestA', C, Node_5)
Edge_mA55 = UMRMEdge('haveMailA', C, Node_5)
Edge_dA55 = UMRMEdge('haveDonutA', C, Node_5)
Edge_mailRequestB55 = UMRMEdge('mailRequestB', C, Node_5)
Edge_donutRequestB55 = UMRMEdge('donutRequestB', C, Node_5)
Edge_mB55 = UMRMEdge('haveMailB', C, Node_5)
Edge_dB55 = UMRMEdge('haveDonutB', C, Node_5)
Edge_del50 = UMRMEdge('itemDelivered', 3, Node_0)
Node_5.addEdge(Edge_mailRequestA55)
Node_5.addEdge(Edge_donutRequestA55)
Node_5.addEdge(Edge_mA55)
Node_5.addEdge(Edge_dA55)
Node_5.addEdge(Edge_mailRequestB55)
Node_5.addEdge(Edge_donutRequestB55)
Node_5.addEdge(Edge_mB55)
Node_5.addEdge(Edge_dB55)
Node_5.addEdge(Edge_del50)

Edge_mailRequestA66 = UMRMEdge('mailRequestA', C, Node_6)
Edge_donutRequestA66 = UMRMEdge('donutRequestA', C, Node_6)
Edge_mA66 = UMRMEdge('haveMailA', C, Node_6)
Edge_dA66 = UMRMEdge('haveDonutA', C, Node_6)
Edge_mailRequestB66 = UMRMEdge('mailRequestB', C, Node_6)
Edge_donutRequestB66 = UMRMEdge('donutRequestB', C, Node_6)
Edge_mB66 = UMRMEdge('haveMailB', C, Node_6)
Edge_dB66 = UMRMEdge('haveDonutB', C, Node_6)
Edge_del60 = UMRMEdge('itemDelivered', 4, Node_0)
Node_6.addEdge(Edge_mailRequestA66)
Node_6.addEdge(Edge_donutRequestA66)
Node_6.addEdge(Edge_mA66)
Node_6.addEdge(Edge_dA66)
Node_6.addEdge(Edge_mailRequestB66)
Node_6.addEdge(Edge_donutRequestB66)
Node_6.addEdge(Edge_mB66)
Node_6.addEdge(Edge_dB66)
Node_6.addEdge(Edge_del60)

Edge_mailRequestA77 = UMRMEdge('mailRequestA', C, Node_7)
Edge_donutRequestA77 = UMRMEdge('donutRequestA', C, Node_7)
Edge_mA77 = UMRMEdge('haveMailA', C, Node_7)
Edge_dA77 = UMRMEdge('haveDonutA', C, Node_7)
Edge_mailRequestB77 = UMRMEdge('mailRequestB', C, Node_7)
Edge_donutRequestB77 = UMRMEdge('donutRequestB', C, Node_7)
Edge_mB77 = UMRMEdge('haveMailB', C, Node_7)
Edge_dB77 = UMRMEdge('haveDonutB', C, Node_7)
Edge_del70 = UMRMEdge('itemDelivered', 3, Node_0)
Node_7.addEdge(Edge_mailRequestA77)
Node_7.addEdge(Edge_donutRequestA77)
Node_7.addEdge(Edge_mA77)
Node_7.addEdge(Edge_dA77)
Node_7.addEdge(Edge_mailRequestB77)
Node_7.addEdge(Edge_donutRequestB77)
Node_7.addEdge(Edge_mB77)
Node_7.addEdge(Edge_dB77)
Node_7.addEdge(Edge_del70)

Edge_mailRequestA88 = UMRMEdge('mailRequestA', C, Node_8)
Edge_donutRequestA88 = UMRMEdge('donutRequestA', C, Node_8)
Edge_mA88 = UMRMEdge('haveMailA', C, Node_8)
Edge_dA88 = UMRMEdge('haveDonutA', C, Node_8)
Edge_mailRequestB88 = UMRMEdge('mailRequestB', C, Node_8)
Edge_donutRequestB88 = UMRMEdge('donutRequestB', C, Node_8)
Edge_mB88 = UMRMEdge('haveMailB', C, Node_8)
Edge_dB88 = UMRMEdge('haveDonutB', C, Node_8)
Edge_del80 = UMRMEdge('itemDelivered', 4, Node_0)
Node_8.addEdge(Edge_mailRequestA88)
Node_8.addEdge(Edge_donutRequestA88)
Node_8.addEdge(Edge_mA88)
Node_8.addEdge(Edge_dA88)
Node_8.addEdge(Edge_mailRequestB88)
Node_8.addEdge(Edge_donutRequestB88)
Node_8.addEdge(Edge_mB88)
Node_8.addEdge(Edge_dB88)
Node_8.addEdge(Edge_del80)

UnderlyingRT = Node_0

################################################################################
def printUMRM(strt_nd):
    for edge in strt_nd.edges:
        print('edge.transcond:', edge.transcond, 'edge.reward:', edge.reward, 'edge.node.name:', edge.node.name)
        #printUMRM(edge.node)

# printUMRM(Node_0)
# print()
# printUMRM(Node_1)


# Initialize underlying RT to its start node
activeNode_UnderlyingRT = Node_0


# Used in createNewMdp() in getExperience.py to create a product MDP
def GetTransitions(s, a):
    global APF
    col = getColumn(s)
    row = getRow(s)

    if moveAgainstSide(col, row, a) or moveAgainstObstacle(col, row, a):
        return [(s, 1)]
    else:
        if a == 'n':
            return [(getState({'r' + str(row + 1), 'c' + str(col)}), APF), (s, 1-APF)]
        if a == 'e':
            return [(getState({'r' + str(row), 'c' + str(col + 1)}), APF), (s, 1-APF)]
        if a == 'w':
            return [(getState({'r' + str(row), 'c' + str(col - 1)}), APF), (s, 1-APF)]
        if a == 's':
            return [(getState({'r' + str(row - 1), 'c' + str(col)}), APF), (s, 1-APF)]
        if a == 'ask':
            # OFFICE A
            if {'c1', 'r6'}.issubset(s) or {'c1', 'r7'}.issubset(s):
                return [(getState({'c1', 'r7'}), 0.5), (getState({'c1', 'r6'}), 0.5)]
            # OFFICE B
            if {'c1', 'r1'}.issubset(s) or {'c1', 'r2'}.issubset(s):
                return [(getState({'c1', 'r1'}), 0.5), (getState({'c1', 'r2'}), 0.5)]
        if a in ['dropItemA', 'pickMailA', 'pickDonutA', 'dropItemB', 'pickMailB', 'pickDonutB']:
            return [(getState({'r' + str(row), 'c' + str(col)}), 1)]
        return [(s, 1)] # required!


# To keep things easy, we model stochasticity by making the agent get stuck (1-APF)% of the time
def SampleNextState(s, a):
    global APF
    p = APF
    col = getColumn(s)
    row = getRow(s)

    if moveAgainstSide(col, row, a) or moveAgainstObstacle(col, row, a):
        return s
    else:
        rand = random.uniform(0, 1)
        if a == 'n':
            if rand <= p:
                return getState({'r' + str(row + 1), 'c' + str(col)})
            else:
                return s
        if a == 'e':
            if rand <= p:
                return getState({'r' + str(row), 'c' + str(col + 1)})
            else:
                return s
        if a == 'w':
            if rand <= p:
                return getState({'r' + str(row), 'c' + str(col - 1)})
            else:
                return s
        if a == 's':
            if rand <= p:
                return getState({'r' + str(row - 1), 'c' + str(col)})
            else:
                return s
        if a == 'ask': # When robot asks what the person wants, the robot might be placed into a neighboring cell;
            # different cells in an office result in the person giving different answers (mail or donut)
            rand = random.uniform(0, 1)
            # OFFICE A
            if {'c1', 'r6'}.issubset(s) or {'c1', 'r7'}.issubset(s):
            # if {'c1', 'r5'}.issubset(s) or {'c1', 'r6'}.issubset(s) or {'c1', 'r7'}.issubset(s):
                if rand <= 0.5:
                    return getState({'c1', 'r7'})
                else:
                    return getState({'c1', 'r6'})
            # OFFICE B
            if {'c1', 'r1'}.issubset(s) or {'c1', 'r2'}.issubset(s):
            # if {'c1', 'r1'}.issubset(s) or {'c1', 'r2'}.issubset(s) or {'c1', 'r3'}.issubset(s):
                if rand <= 0.5:
                    return getState({'c1', 'r1'})
                else:
                    return getState({'c1', 'r2'})
        if a in ['dropItemA', 'pickMailA', 'pickDonutA', 'dropItemB', 'pickMailB', 'pickDonutB']:
            return getState({'r' + str(row), 'c' + str(col)})

        return s


def getColumn(s):
    for f in s:
        if f[0] == 'c':
            return int(f[1:])


def getRow(s):
    for f in s:
        if f[0] == 'r':
            return int(f[1:])


def getState(sub):
    global S
    for s in S:
        if sub.issubset(s):
            return s


def moveAgainstSide(col, row, a):
    if a == 'n' and row == Height: return True
    if a == 'e' and col == Width: return True
    if a == 'w' and col == 1: return True
    if a == 's' and row == 1: return True
    return False


def moveAgainstObstacle(col, row, a):
    global Obstacles
    if a == 'n' and (col, row + 1) in Obstacles: return True
    if a == 'e' and (col + 1, row) in Obstacles: return True
    if a == 'w' and (col - 1, row) in Obstacles: return True
    if a == 's' and (col, row - 1) in Obstacles: return True
    return False


def EnvironReward(obs):
    if obs == 'null': return C
    global activeNode_UnderlyingRT
    for edge in activeNode_UnderlyingRT.edges:
        if obs == edge.transcond:
            activeNode_UnderlyingRT = edge.node
            return edge.reward


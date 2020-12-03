import random

Name = 'TreasureMapSmall2'
print(Name)

'''This is the specification of an MDP for a Width by Height gridworld.
The objective is to visit cells in a particular order, so that observations are made in a particular order.'''

# Number of grid columns
Width = 5

# Number of grid rows
Height = 5

# Default reward
C = -1

# Action Precision Factor
APF = 0.95


Obstacles = []

Corners = [(1,1),(1,5),(5,1),(5,5)]

# Actions
A = ['n', 'e', 'w', 's', 'buy', 'sell', 'collect']

# Observations
O = ['m', 'e', 't', 'j']

# States
S = []
for col in range(1, Width + 1):
    for row in range(1, Height + 1):
        if (col, row) not in Obstacles:
            S.append({'c' + str(col), 'r' + str(row)})  # agent is not here

# Initialize agent's state
initial = None
current_state = None

while initial == None:
    x = random.choice([i for i in range(1, Width + 1)])
    y = random.choice([j for j in range(1, Height + 1)])
    for s in S:
        if (x, y) in Corners and {'c' + str(x), 'r' + str(y)}.issubset(s):
            initial = s
            break

# initial = {'c8','r6'}

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


def labelingFunc(s, a=None):
    if type(a) == type(0):
        a = A[a]

    if {'c3', 'r2'} == s:
        if a == 'buy': return 'm'
    if {'c2', 'r2'} == s:
        if a == 'buy': return 'e'
    if {'c3', 'r3'} == s:
        if a == 'collect': return 't'
    if {'c4', 'r4'} == s:
        if a == 'sell': return 'j'
    return 'null'

# Defining the underlying reward model of the running example

Node_0 = UMRMNode('Node_0')
Node_1 = UMRMNode('Node_1')
Node_2 = UMRMNode('Node_2')
Node_3 = UMRMNode('Node_3')
Node_4 = UMRMNode('Node_4')

Edge_m01 = UMRMEdge('m', 10, Node_1)
Edge_e00 = UMRMEdge('e', C, Node_0)
Edge_t00 = UMRMEdge('t', C, Node_0)
Edge_j00 = UMRMEdge('j', C, Node_0)
Node_0.addEdge(Edge_m01)
Node_0.addEdge(Edge_e00)
Node_0.addEdge(Edge_t00)
Node_0.addEdge(Edge_j00)

Edge_m11 = UMRMEdge('m', C, Node_1)
Edge_e12 = UMRMEdge('e', 80, Node_2)
Edge_t11 = UMRMEdge('t', C, Node_1)
Edge_j11 = UMRMEdge('j', C, Node_1)
Node_1.addEdge(Edge_m11)
Node_1.addEdge(Edge_e12)
Node_1.addEdge(Edge_t11)
Node_1.addEdge(Edge_j11)

Edge_m22 = UMRMEdge('m', C, Node_2)
Edge_e22 = UMRMEdge('e', C, Node_2)
Edge_t24 = UMRMEdge('t', 80, Node_4)
Edge_j22 = UMRMEdge('j', C, Node_2)
Node_2.addEdge(Edge_m22)
Node_2.addEdge(Edge_e22)
Node_2.addEdge(Edge_t24)
Node_2.addEdge(Edge_j22)

Edge_m33 = UMRMEdge('m', C, Node_3)
Edge_e33 = UMRMEdge('e', C, Node_3)
Edge_t34 = UMRMEdge('t', 95, Node_4)
Edge_j33 = UMRMEdge('j', C, Node_3)
Node_3.addEdge(Edge_m33)
Node_3.addEdge(Edge_e33)
Node_3.addEdge(Edge_t34)
Node_3.addEdge(Edge_j33)

Edge_m44 = UMRMEdge('m', C, Node_4)
Edge_e44 = UMRMEdge('e', C, Node_4)
Edge_t44 = UMRMEdge('t', C, Node_4)
Edge_j41 = UMRMEdge('j', 180, Node_1)
Node_4.addEdge(Edge_m44)
Node_4.addEdge(Edge_e44)
Node_4.addEdge(Edge_t44)
Node_4.addEdge(Edge_j41)

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
        if a == 'buy' or a == 'sell' or a == 'collect':
            return [(s, 1)]



# Transition Oracle
# To keep things easy, we model stochasticity by making the agent get stuck (1-APF)% of the time
def SampleNextState(s, a):
    global APF
    p = APF
    col = getColumn(s)
    row = getRow(s)
    # s = [(col, row)]
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
        return s


# State transition function
'''def T(s, a, ss):
    global APF
    col = getColumn(s)
    row = getRow(s)
    if s == ss:
        if moveAgainstSide(col, row, a) or moveAgainstObstacle(col, row, a) or a == 'buy' or a == 'sell' or a == 'collect':
            return 1
        else:
            return 1 - APF
    if a == 'n':
        if {'r' + str(row + 1), 'c' + str(col)}.issubset(ss):
            return APF
    if a == 'e':
        if {'r' + str(row), 'c' + str(col + 1)}.issubset(ss):
            return APF
    if a == 'w':
        if {'r' + str(row), 'c' + str(col - 1)}.issubset(ss):
            return APF
    if a == 's':
        if {'r' + str(row - 1), 'c' + str(col)}.issubset(ss):
            return APF
    return 0'''


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

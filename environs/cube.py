import random

Name = 'Cube Problem'
print(Name)
'''This is the specification of an MDP for a Width by Height gridworld.
The objective is to visit cells in a particular order, so that observations are made in a particular order.'''

# Number of grid columns
Width = 5

# Number of grid rows
Height = 5

# Default reward
C = 0
# C = -0.01

# Reset cost
RESET_COST = -1

# Action Precision Factor
APF = 0.95

# Obstacles
#Obstacles = [(3, 4), (3, 5), (4, 8), (4, 9), (8, 3), (8, 4), (9, 7), (9, 8)]
Obstacles = []

# Actions
A = ['n', 'e', 'w', 's']

# Observations
O = ['a', 'b']
# O = ['a', 'b', 'c', 'd']

# States
S = []
for col in range(1, Width + 1):
    for row in range(1, Height + 1):
        if (col, row) not in Obstacles:
            S.append({'c' + str(col), 'r' + str(row)})  # agent is not here

# Initialize agent's state
# initial = None
# while initial == None:
#     x = random.choice([i for i in range(1, Width + 1)])
#     y = random.choice([j for j in range(1, Height + 1)])
#     for s in S:
#         if (x, y) not in Obstacles and {'c' + str(x), 'r' + str(y)}.issubset(s):
#             initial = s
#             print('Initial environ state:', s)
#             break

initial = {'c5','r1'}

current_state = initial

# For version submitted to ECML
def labelingFunc(s, a):
    if type(a) == type(0):
        a = A[a]

    if s == {'c2', 'r1'}:
        if a == 's':
            return 'a'
        else:
            return 'null'
    if s == {'c1', 'r3'}:
        if a == 'w':
            return 'a'
        else:
            return 'null'
    if s == {'c4', 'r3'}:
        if a == 'e':
            return 'b'
        else:
            return 'null'
    if s == {'c4', 'r5'}:
        if a == 'n':
            return 'b'
        else:
            return 'null'
    return 'null'


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


# Defining an underlying reward model that will be used for evaluation and experimentation

Node_0 = UMRMNode('Node_0')
Node_1 = UMRMNode('Node_1')
Node_2 = UMRMNode('Node_2')
Node_3 = UMRMNode('Node_3')
Node_4 = UMRMNode('Node_4')
Node_5 = UMRMNode('Node_5')
Node_6 = UMRMNode('Node_6')


Edge_a01 = UMRMEdge('a', C, Node_1)
Edge_b00 = UMRMEdge('b', C, Node_0)
Node_0.addEdge(Edge_a01)
Node_0.addEdge(Edge_b00)

Edge_a12 = UMRMEdge('a', C, Node_2)
Edge_b11 = UMRMEdge('b', C, Node_1)
Node_1.addEdge(Edge_a12)
Node_1.addEdge(Edge_b11)

Edge_a23 = UMRMEdge('a', C, Node_3)
Edge_b25 = UMRMEdge('b', 2, Node_5)
Node_2.addEdge(Edge_a23)
Node_2.addEdge(Edge_b25)

Edge_a34 = UMRMEdge('a', C, Node_4)
Edge_b33 = UMRMEdge('b', C, Node_3)
Node_3.addEdge(Edge_a34)
Node_3.addEdge(Edge_b33)

Edge_a41 = UMRMEdge('a', C, Node_1)
Edge_b46 = UMRMEdge('b', 1, Node_6)
Node_4.addEdge(Edge_a41)
Node_4.addEdge(Edge_b46)

Edge_a55 = UMRMEdge('a', C, Node_5)
Edge_b55 = UMRMEdge('b', C, Node_0)
Node_5.addEdge(Edge_a55)
Node_5.addEdge(Edge_b55)

Edge_a66 = UMRMEdge('a', C, Node_6)
Edge_b66 = UMRMEdge('b', C, Node_0)
Node_6.addEdge(Edge_a66)
Node_6.addEdge(Edge_b66)

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
        return [(s, 1)]  # required?


# Transition Oracle
# To keep things easy, i model stochasticity by making the agent get stuck (1-APF)% of the time
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


# State transition function
def T(s, a, ss):
    global APF
    col = getColumn(s)
    row = getRow(s)
    if s == ss:
        if moveAgainstSide(col, row, a) or moveAgainstObstacle(col, row, a):
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
    return 0


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

def ExecuteInEnviron(s, a, ss):
    # required for cookie domain
    pass


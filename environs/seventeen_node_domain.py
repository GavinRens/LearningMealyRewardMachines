import random

Name = '17-nodes'
print(Name)
'''This is the specification of an MDP for a Width by Height gridworld.
The objective is to visit cells in a particular order, so that observations are made in a particular order.'''

# Number of grid columns
Width = 10

# Number of grid rows
Height = 10

# Default reward
C = 0

# Action Precision Factor
APF = 0.95

# Obstacles
Obstacles = [(3, 4), (3, 5), (4, 8), (4, 9), (8, 3), (8, 4), (9, 7), (9, 8)]

# Actions
A = ['n', 'e', 'w', 's']

# Observations
O = ['a', 'b']

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

initial = {'c1','r1'}

current_state = initial


# Define which observations are made in which states after which actions
ObsAssign = dict()
def DefinePerception():
    global S
    global A
    global O
    for s in S:
        rand = random.uniform(0, 1)
        if rand <= 0.25: # something is perceived in s
            for a in A:
                ObsAssign[frozenset(s), a] = random.choice(O)
        else: # nohing is perceived in s
            for a in A:
                ObsAssign[frozenset(s), a] = 'null'

# Add things of interest to the cells; these are the thing which will be observed
DefinePerception()

# The function that labels states with observations depending on actions
def labelingFunc(s, a):
    if type(a) == type(0):
        a = A[a]
    global ObsAssign
    return ObsAssign[frozenset(s), a]


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
Node_7 = UMRMNode('Node_7')
Node_8 = UMRMNode('Node_8')
Node_9 = UMRMNode('Node_9')
Node_10 = UMRMNode('Node_10')
Node_11 = UMRMNode('Node_11')
Node_12 = UMRMNode('Node_12')
Node_13 = UMRMNode('Node_13')
Node_14 = UMRMNode('Node_14')
Node_15 = UMRMNode('Node_15')
Node_16 = UMRMNode('Node_16')

Edge_a01 = UMRMEdge('a', 1, Node_1)
Edge_b016 = UMRMEdge('b', 1, Node_16)
Edge_n00 = UMRMEdge('null', C, Node_0)
Node_0.addEdge(Edge_a01)
Node_0.addEdge(Edge_b016)
Node_0.addEdge(Edge_n00)

Edge_a12 = UMRMEdge('a', 2, Node_2)
Edge_b11 = UMRMEdge('b', C, Node_1)
Edge_n11 = UMRMEdge('null', C, Node_1)
Node_1.addEdge(Edge_a12)
Node_1.addEdge(Edge_b11)
Node_1.addEdge(Edge_n11)

Edge_a23 = UMRMEdge('a', 3, Node_3)
Edge_b22 = UMRMEdge('b', C, Node_2)
Edge_n22 = UMRMEdge('null', C, Node_2)
Node_2.addEdge(Edge_a23)
Node_2.addEdge(Edge_b22)
Node_2.addEdge(Edge_n22)

Edge_a34 = UMRMEdge('a', 4, Node_4)
Edge_b33 = UMRMEdge('b', C, Node_3)
Edge_n33 = UMRMEdge('null', C, Node_3)
Node_3.addEdge(Edge_a34)
Node_3.addEdge(Edge_b33)
Node_3.addEdge(Edge_n33)

Edge_a45 = UMRMEdge('a', 5, Node_5)
Edge_b413 = UMRMEdge('b', 1, Node_13)
Edge_n44 = UMRMEdge('null', C, Node_4)
Node_4.addEdge(Edge_a45)
Node_4.addEdge(Edge_b413)
Node_4.addEdge(Edge_n44)

Edge_a56 = UMRMEdge('a', 6, Node_6)
Edge_b55 = UMRMEdge('b', C, Node_5)
Edge_n55 = UMRMEdge('null', C, Node_5)
Node_5.addEdge(Edge_a56)
Node_5.addEdge(Edge_b55)
Node_5.addEdge(Edge_n55)

Edge_a67 = UMRMEdge('a', 7, Node_7)
Edge_b66 = UMRMEdge('b', C, Node_6)
Edge_n66 = UMRMEdge('null', C, Node_6)
Node_6.addEdge(Edge_a67)
Node_6.addEdge(Edge_b66)
Node_6.addEdge(Edge_n66)

Edge_a78 = UMRMEdge('a', 8, Node_8)
Edge_b77 = UMRMEdge('b', C, Node_7)
Edge_n77 = UMRMEdge('null', C, Node_7)
Node_7.addEdge(Edge_a78)
Node_7.addEdge(Edge_b77)
Node_7.addEdge(Edge_n77)

Edge_a88 = UMRMEdge('a', C, Node_8)
Edge_b89 = UMRMEdge('b', 1, Node_9)
Edge_n88 = UMRMEdge('null', C, Node_8)
Node_8.addEdge(Edge_a88)
Node_8.addEdge(Edge_b89)
Node_8.addEdge(Edge_n88)

Edge_a1616 = UMRMEdge('a', C, Node_16)
Edge_b1615 = UMRMEdge('b', 2, Node_15)
Edge_n1616 = UMRMEdge('null', C, Node_16)
Node_16.addEdge(Edge_a1616)
Node_16.addEdge(Edge_b1615)
Node_16.addEdge(Edge_n1616)

Edge_a152 = UMRMEdge('a', 1, Node_2)
Edge_b1514 = UMRMEdge('b', 3, Node_14)
Edge_n1515 = UMRMEdge('null', C, Node_15)
Node_15.addEdge(Edge_a152)
Node_15.addEdge(Edge_b1514)
Node_15.addEdge(Edge_n1515)

Edge_a1414 = UMRMEdge('a', C, Node_14)
Edge_b1413 = UMRMEdge('b', 4, Node_13)
Edge_n1414 = UMRMEdge('null', C, Node_14)
Node_14.addEdge(Edge_a1414)
Node_14.addEdge(Edge_b1413)
Node_14.addEdge(Edge_n1414)

Edge_a1313 = UMRMEdge('a', C, Node_13)
Edge_b1312 = UMRMEdge('b', 5, Node_12)
Edge_n1313 = UMRMEdge('null', C, Node_13)
Node_13.addEdge(Edge_a1313)
Node_13.addEdge(Edge_b1312)
Node_13.addEdge(Edge_n1313)

Edge_a1212 = UMRMEdge('a', C, Node_12)
Edge_b1211 = UMRMEdge('b', 6, Node_11)
Edge_n1212 = UMRMEdge('null', C, Node_12)
Node_12.addEdge(Edge_a1212)
Node_12.addEdge(Edge_b1211)
Node_12.addEdge(Edge_n1212)

Edge_a116 = UMRMEdge('a', 1, Node_6)
Edge_b1110 = UMRMEdge('b', 7, Node_10)
Edge_n1111 = UMRMEdge('null', C, Node_11)
Node_11.addEdge(Edge_a116)
Node_11.addEdge(Edge_b1110)
Node_11.addEdge(Edge_n1111)

Edge_a1010 = UMRMEdge('a', C, Node_10)
Edge_b109 = UMRMEdge('b', 8, Node_9)
Edge_n1010 = UMRMEdge('null', C, Node_10)
Node_10.addEdge(Edge_a1010)
Node_10.addEdge(Edge_b109)
Node_10.addEdge(Edge_n1010)

Edge_a90 = UMRMEdge('a', C, Node_9)
Edge_b99 = UMRMEdge('b', C, Node_9)
Edge_n99 = UMRMEdge('null', C, Node_9)
Node_9.addEdge(Edge_a90) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Node_9.addEdge(Edge_b99)
Node_9.addEdge(Edge_n99)

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


# Transition Oracle
# To keep things easy, i model stochasticity by making the agent get stuck (1-APF)% of the time
def SampleNextState(s, a, stoc=True):
    global APF
    p = APF
    if not stoc:
        p = 1.0
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
        if a == 'reset':
            return getState(initial)


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
    if a == 'reset':
        if ss == initial:
            return 1
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


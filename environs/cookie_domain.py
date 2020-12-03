'''
An alternative version of the cookie domain of Toro Icart 2018/2019
'''

Name = 'Cookie'
print(Name)
import random

# Number of grid columns
Width = 4

# Number of grid rows
Height = 5

# Default reward
C = 0

# Reset reward
R = -0.1

# Action Precision Factor
APF = 0.95

# Obstacles
Obstacles = [(2, 2), (2, 4),    (3, 1), (3, 2), (3, 4), (3, 5),     (4, 1), (4, 2), (4, 4), (4, 5)]

# States
S = []
for col in range(1, Width + 1):
    for row in range(1, Height + 1):
        if (col, row) not in Obstacles:
            S.append({'c' + str(col), 'r' + str(row)})  # agent is not here

# Initialize agent's state
initial = {'c1', 'r3'}
current_state = initial

# Actions
A = ['n', 'e', 'w', 's', 'pb', 'eat']

# Observations
O = ['red_n', 'blu_n', 'yel_y', 'yel_n', 'red_c', 'blu_c']

cookie_in_blue_room = False
cookie_in_red_room = False

def labelingFunc(s, a):
    global cookie_in_blue_room
    global cookie_in_red_room

    if type(a) == type(0):
        a = A[a]

    # if in blue room
    if {'c1', 'r5'}.issubset(s) or {'c2', 'r5'}.issubset(s):
        if cookie_in_blue_room:
            if {'c2', 'r5'}.issubset(s) and a == 'eat':
                return 'blu_n' # cookine was eaten
            else:
                return 'blu_c' # cookine was not eaten
        else:
            return 'blu_n' # there was no cookie in the room

    # if in red room
    if {'c1', 'r1'}.issubset(s) or {'c2', 'r1'}.issubset(s):
        if cookie_in_red_room:
            if {'c2', 'r1'}.issubset(s) and a == 'eat':
                return 'red_n' # cookine was eaten
            else:
                return 'red_c' # cookine was not eaten
        else:
            return 'red_n' # there was no cookie in the room

    # if in yellow room
    if {'c3', 'r3'}.issubset(s) or {'c4', 'r3'}.issubset(s):
            if {'c4', 'r3'}.issubset(s) and a == 'pb':
                return 'yel_y' # button was pressed
            else:
                return 'yel_n' # button was not pressed

    # else in hallway
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




# Defining the underlying reward model that will be used for evaluation and experimentation
#UnderlyingRTNodes = {}

Node_0 = UMRMNode('Node_0')
Node_1 = UMRMNode('Node_1')
Node_2 = UMRMNode('Node_2')
Node_3 = UMRMNode('Node_3')

Edge_red_n00 = UMRMEdge('red_n', C, Node_0)
Edge_red_c00 = UMRMEdge('red_c', C, Node_0)
Edge_blu_n00 = UMRMEdge('blu_n', C, Node_0)
Edge_blu_c00 = UMRMEdge('blu_c', C, Node_0)
Edge_yel_y01 = UMRMEdge('yel_y', 0.000001, Node_1)
Edge_yel_n00 = UMRMEdge('yel_n', C, Node_0)
Edge_null00 = UMRMEdge('null', C, Node_0)
Node_0.addEdge(Edge_red_n00)
Node_0.addEdge(Edge_red_c00)
Node_0.addEdge(Edge_blu_n00)
Node_0.addEdge(Edge_blu_c00)
Node_0.addEdge(Edge_yel_y01)
Node_0.addEdge(Edge_yel_n00)
Node_0.addEdge(Edge_null00)

Edge_red_n11 = UMRMEdge('red_n', C, Node_1)
Edge_red_c12 = UMRMEdge('red_c', 0, Node_2)
Edge_blu_n11 = UMRMEdge('blu_n', C, Node_1)
Edge_blu_c13 = UMRMEdge('blu_c', 0, Node_3)
Edge_yel_y11 = UMRMEdge('yel_y', C, Node_1)
Edge_yel_n11 = UMRMEdge('yel_n', C, Node_1)
Edge_null11 = UMRMEdge('null', C, Node_1)
Node_1.addEdge(Edge_red_n11)
Node_1.addEdge(Edge_red_c12)
Node_1.addEdge(Edge_blu_n11)
Node_1.addEdge(Edge_blu_c13)
Node_1.addEdge(Edge_yel_y11)
Node_1.addEdge(Edge_yel_n11)
Node_1.addEdge(Edge_null11)

Edge_red_n20 = UMRMEdge('red_n', 1, Node_0)
Edge_red_c22 = UMRMEdge('red_c', C, Node_2)
Edge_blu_n22 = UMRMEdge('blu_n', C, Node_2)
Edge_blu_c23 = UMRMEdge('blu_c', C, Node_2)
Edge_yel_y21 = UMRMEdge('yel_y', C, Node_1)
Edge_yel_n22 = UMRMEdge('yel_n', C, Node_2)
Edge_null22 = UMRMEdge('null', C, Node_2)
Node_2.addEdge(Edge_red_n20)
Node_2.addEdge(Edge_red_c22)
Node_2.addEdge(Edge_blu_n22)
Node_2.addEdge(Edge_blu_c23)
Node_2.addEdge(Edge_yel_y21)
Node_2.addEdge(Edge_yel_n22)
Node_2.addEdge(Edge_null22)

Edge_red_n33 = UMRMEdge('red_n', C, Node_3)
Edge_red_c33 = UMRMEdge('red_c', C, Node_3)
Edge_blu_n30 = UMRMEdge('blu_n', 1, Node_0)
Edge_blu_c33 = UMRMEdge('blu_c', C, Node_3)
Edge_yel_y31 = UMRMEdge('yel_y', C, Node_1)
Edge_yel_n33 = UMRMEdge('yel_n', C, Node_3)
Edge_null33 = UMRMEdge('null', C, Node_3)
Node_3.addEdge(Edge_red_n33)
Node_3.addEdge(Edge_red_c33)
Node_3.addEdge(Edge_blu_n30)
Node_3.addEdge(Edge_blu_c33)
Node_3.addEdge(Edge_yel_y31)
Node_3.addEdge(Edge_yel_n33)
Node_3.addEdge(Edge_null33)

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
    global initial

    p = APF
    if not stoc:
        p = 1.0
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
        if a == 'pb':
            return s
        if a == 'eat':
            return s


# State transition function
def T(s, a, ss):
    global APF
    global initial

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
    if a == 'pb':
        if s == ss:
            return 1
    if a == 'eat':
        if s == ss:
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


def ExecuteInEnviron(s, a, ss=None):
    global cookie_in_blue_room
    global cookie_in_red_room
    # print(a)
    if a == 'pb':
        if {'c4', 'r3'}.issubset(s):
            # rand = random.uniform(0, 1)
            rand = 0.6
            if rand <= 0.5:
                cookie_in_blue_room = True;
                cookie_in_red_room = False
            else:
                cookie_in_blue_room = False;
                cookie_in_red_room = True
    if a == 'eat':
        if cookie_in_blue_room and {'c2', 'r5'}.issubset(s):
            cookie_in_blue_room = False
        if cookie_in_red_room and {'c2', 'r1'}.issubset(s):
            cookie_in_red_room = False

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        foodScore = 0
        if newFood.count() != 0:
            foodScore = 1/(min([manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]))

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostDistances = []
        for i in range(len(newGhostStates)):
            distance = manhattanDistance(newPos, newGhostStates[i].getPosition()) + newScaredTimes[i]
            if distance != 0:
                ghostDistances.append(1/distance)
            else:
                ghostDistances.append(distance)
        return foodScore - max(ghostDistances) + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        legalMoves = gameState.getLegalActions()
        scores = [self.value(gameState.generateSuccessor(0, action), 1, self.depth) for action in legalMoves]
        '''
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        '''
        return legalMoves[scores.index(max(scores))]

    # helper function, returns minimax value
    def value(self, currentGameState, agentIndex, depth):
        if currentGameState.isWin() or currentGameState.isLose() or depth == 0:
            return self.evaluationFunction(currentGameState)
        legalMoves = currentGameState.getLegalActions(agentIndex)
        newIndex = (agentIndex + 1) % currentGameState.getNumAgents()
        if newIndex == 0:
            depth -= 1
        scores = [self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth) for action in legalMoves]
        if agentIndex == 0:
            return max(scores)
        return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        legalMoves = gameState.getLegalActions()
        value = alpha = float("-inf")
        bestAction = legalMoves[0]
        for action in legalMoves:
            currentValue = self.value(gameState.generateSuccessor(0, action), 1, self.depth, alpha, float("inf"))
            if value < currentValue:
                bestAction = action
                value = currentValue
            alpha = max(alpha, value)
        # scores = [self.value(gameState.generateSuccessor(0, action), 1, self.depth, float("-inf"), float("inf")) for action in legalMoves]
        # return legalMoves[scores.index(max(scores))]
        return bestAction

    # helper function, returns minimax value in Alpha-Beta implementation
    def value(self, currentGameState, agentIndex, depth, alpha, beta):
        if currentGameState.isWin() or currentGameState.isLose() or depth == 0:
            return self.evaluationFunction(currentGameState)
        legalMoves = currentGameState.getLegalActions(agentIndex)
        newIndex = (agentIndex + 1) % currentGameState.getNumAgents()
        if newIndex == 0:
            depth -= 1
        if agentIndex == 0:
            value = float("-inf")
            for action in legalMoves:
                value = max(value, self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth, alpha, beta))
                if value > beta:
                    return value
                alpha = max(alpha, value)
        else:
            value = float("inf")
            for action in legalMoves:
                value = min(value, self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth, alpha, beta))
                if value < alpha:
                    return value
                beta = min(beta, value)

        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        legalMoves = gameState.getLegalActions()
        scores = [self.value(gameState.generateSuccessor(0, action), 1, self.depth) for action in legalMoves]
        return legalMoves[scores.index(max(scores))]

    # helper function, returns expectimax value
    def value(self, currentGameState, agentIndex, depth):
        if currentGameState.isWin() or currentGameState.isLose() or depth == 0:
            return self.evaluationFunction(currentGameState)
        legalMoves = currentGameState.getLegalActions(agentIndex)
        newIndex = (agentIndex + 1) % currentGameState.getNumAgents()
        if newIndex == 0:
            depth -= 1
        scores = [self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth) for action in legalMoves]
        if agentIndex == 0:
            return max(scores)
        return sum(scores)/len(scores)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Similar to the evaluation function for the reflex agent,
    the returned score is determined by considering the following 3 values:
    1. the reciprocal of the approximated distance between the pacman to the nearest food
    2. the reciprocal of the approximated distance between the pacman to the nearest ghost
    (also considering the scaredTime)
    3. the score of currentGameState
    """
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodScore = 0
    if food.count() != 0:
        foodScore = 1 / (min([manhattanDistance(pos, foodPos) for foodPos in food.asList()]))

    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostDistances = []
    for i in range(len(ghostStates)):
        distance = manhattanDistance(pos, ghostStates[i].getPosition()) + scaredTimes[i]
        if distance != 0:
            ghostDistances.append(1 / distance)
        else:
            ghostDistances.append(distance)
    return foodScore - 10*max(ghostDistances) + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

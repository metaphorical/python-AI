import sys 

class Node():
    def __init__(self, state, parent, action):
        self.state=state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
         self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty:
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):

        # Read the file
        with open(filename) as f:
            contents = f.read()
        
        # Validate maze
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one starting point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal/exit")
        
        # determine hight and width of the maze 
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # keep track of the walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else: 
                        row.append(True)    
                except IndexError:
                    row.appemd(False)
            self.walls.append[row]

        self.solution = None
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print(" ", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state

        # all possible actions
        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]

        #ensure actions are valid
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result


    def solve(self):
        """Find a solution to maze, if it exists"""

        # keep the track of number of states explored
        self.num_explored = 0

        # Initialize frontier ot the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # initialize explored set
        self.explored = set()

        # loop
        while True:

            # if nothing is left in the frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Chose a node from the frontier
            node = frontier.remove()
            self.num_explored +=1

            # do we have a solution
            if node.state == self.goal:
                actions = []
                cells = []

                # Follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
        
            # if it is not solution, just mark it as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    

             

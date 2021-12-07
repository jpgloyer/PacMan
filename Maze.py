
import EMV

#Creates and Stores list of wall and dot coordinates
class Maze:
    #Height and width in blocks
    def __init__(self, height_input: int, width_input: int):
        #Maze will have (height_input) lists of (width_input) characters
        #Maze will also have one more list appended to the end with height and width values
        self.Maze = [[]]
        self.height = height_input
        self.width = width_input
        self.dots_in_maze: int = 0
        self.dots_eaten: int = 0
        self.pickup_trigger: int = 000

        #Reads Maze text file and converts information to a list of lists (rows of columns)
        
        with open("PacManMazeV2.txt", "r") as Maze_Text:
            line_counter: int = -1
            for line in Maze_Text:
                line_counter += 1
                for i in range(self.width):
                    #print(line_counter, i)
                    self.Maze[line_counter].append(line[i])
                self.Maze.append([])
        self.Maze[-1] = ([len(self.Maze), len(self.Maze[0]), EMV.Square_height, EMV.Square_width])
    
    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.Maze[i][j], end="")
            print()
        print(self.Maze[-1])
        # for i in range(len(self.Maze)):
        #     for j in range(len(self.Maze[i])):
        #         print(self.Maze[i][j], end="")
        #     print()

    def is_clear(self, x, y, direction):
        #print(x, y)
        # x=x
        # y=y
        #print(x, y)

        if x < EMV.Grid_x - 1 and y < EMV.Grid_y - 1:
            if self.Maze[y+1][x] != '-' and direction == 'D' and self.Maze[y+1][x] != '^':
                return True
            elif self.Maze[y][x+1] != '-' and direction == 'R':
                return True

        if self.Maze[y-1][x] != '-' and direction == 'U':
            return True
        elif self.Maze[y][x-1] != '-' and direction == 'L':
            return True
        return False



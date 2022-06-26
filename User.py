import EMV
from Ghost import Ghost

class User:
    def __init__(self):
        self.x_grid = EMV.PacMan_x
        self.y_grid = EMV.PacMan_y
        self.color = EMV.PacMan
        self.current_direction = ' '
        self.direction_queue = ' '
        self.Points = 0
        self.lives = 2
        self.Points_per_ghost = 100
        self.quitting: bool = False
        self.pickup_name: str = ""
        self.Deathless = False
    

    def Move(self, direction_queue, maze):
        #Teleport function
        if (abs(self.y_grid - EMV.Teleport_y) < .5):
            if (abs(self.x_grid - EMV.Grid_x) < 2) and self.current_direction == 'R': 
                self.x_grid = 0
            if (abs(self.x_grid) < 1) and self.current_direction == 'L':
                self.x_grid = EMV.Grid_x - 1

        #Change direction to most recent input
        if maze.is_clear(round(self.x_grid),round(self.y_grid),direction_queue) and self.at_center_of_block():
            self.current_direction = direction_queue

        #180 on whim
        if direction_queue == 'U' and self.current_direction == 'D':
            self.current_direction = direction_queue
        elif direction_queue == 'D' and self.current_direction == 'U':
            self.current_direction = direction_queue
        elif direction_queue == 'L' and self.current_direction == 'R':
            self.current_direction = direction_queue
        elif direction_queue == 'R' and self.current_direction == 'L':
            self.current_direction = direction_queue

        #Move if possible
        if self.current_direction == 'U':
            if self.at_center_of_block() and not maze.is_clear(round(self.x_grid),round(self.y_grid),self.current_direction):
                self.current_direction = ' '
            else:
                self.y_grid -= .1
        elif self.current_direction == 'D':
            if self.at_center_of_block() and not maze.is_clear(round(self.x_grid),round(self.y_grid),self.current_direction):
                self.current_direction = ' '
            else:
                self.y_grid += .1
        elif self.current_direction == 'L':
            if self.at_center_of_block() and not maze.is_clear(round(self.x_grid),round(self.y_grid),self.current_direction):
                self.current_direction = ' '
            else:
                self.x_grid -= .1
        elif self.current_direction == 'R':
            if self.at_center_of_block() and not maze.is_clear(round(self.x_grid),round(self.y_grid),self.current_direction):
                self.current_direction = ' '
            else:
                self.x_grid += .1

        
    def at_center_of_block(self):
        if self.x_grid%1 <.1 and self.y_grid%1 <.1:
            return True
        else:
            return False
        

    #Only controls behaviors initiated by item pickup; stored/user-activated functions are activated on space-bar input 
    def pickup_behaviors(self, Ghost_List):
        if self.pickup_name == "Extra_Life":
            print("Extra_Life")
            self.lives += 1
            self.pickup_name = ""
        elif self.pickup_name == "Fruit":
            self.Points += 500
            print(self.Points)
            self.pickup_name = ""
        elif self.pickup_name == "Big_Dot":
            for i in range(len(Ghost_List)):
                if Ghost_List[i].status == "Corners" or Ghost_List[i].status == "Pursuit":
                    Ghost_List[i].status = "Frightened"
                    Ghost_List[i].color = EMV.Frightened_Color
                    Ghost_List[i].speed = Ghost_List[i].speed/2
                    Ghost_List[i].turn_around_when_frightened()
            self.pickup_name = ""
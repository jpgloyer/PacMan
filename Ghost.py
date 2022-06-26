import EMV
from Maze import Maze
from random import *
import pygame

class Ghost:
    def __init__(self, color):
        self.corner_target_x = 0
        self.corner_target_y = 0
        self.current_direction = ' '
        self.last_direction = ' '
        self.color = color
        self.last_x:int = 0
        self.last_y:int = 0
        self.status = "Center"
        #Status can be "Corners", "Pursuit", "Center", "Frightened", "Activating"
        self.activating_timer:int = 0
        self.center_timer: int = 0
        self.hide_in_center_duration: int = 0
        self.ghost_corral_coord_mod: int = 0
        self.frightened_timer: int = 50
        self.speed = EMV.Ghost_default_speed

        

        #Set corner targets and timers by color
        #Red
        if self.color == EMV.Red:
            self.corner_target_x = -3
            self.corner_target_y = -3
            self.x_grid = EMV.Red_x
            self.y_grid = EMV.Red_y
            self.hide_in_center_duration = 10
            self.name = "Blinky"
            #self.dots_to_increase_speed: int = 100
        #Blue
        elif self.color == EMV.Blue:
            self.corner_target_x = EMV.Grid_x - 1
            self.corner_target_y = -3
            self.x_grid = EMV.Blue_x
            self.y_grid = EMV.Blue_y
            self.hide_in_center_duration = 20
            self.name = "Inky"
        #Pink
        elif self.color == EMV.Pink:
            self.corner_target_x = -3
            self.corner_target_y = EMV.Grid_y - 1
            self.x_grid = EMV.Pink_x
            self.y_grid = EMV.Pink_y
            self.hide_in_center_duration = 30
            self.name = "Pinky"
        #Orange
        elif self.color == EMV.Orange:
            self.corner_target_x = EMV.Grid_x + 5
            self.corner_target_y = EMV.Grid_y + 5
            self.x_grid = EMV.Orange_x
            self.y_grid = EMV.Orange_y
            self.current_direction = 'L'
            self.hide_in_center_duration = 40
            self.ghost_corral_coord_mod = 1
            self.name = "Clyde"

        pass

        

    def get_direction_toward_target(self, target_x, target_y, maze):
        Choice = ' '
        least_distance = 9999999999999
        up_distance = 111111111
        down_distance = 111111111
        left_distance = 111111111
        right_distance = 111111111
        if maze.is_clear(round(self.x_grid),round(self.y_grid),'U'):
            up_distance = self.get_squared_distance_toward_target(target_x, target_y, 'U')
        if maze.is_clear(round(self.x_grid),round(self.y_grid),'D'):
            down_distance = self.get_squared_distance_toward_target(target_x, target_y, 'D')
        if maze.is_clear(round(self.x_grid),round(self.y_grid),'L'):
            left_distance = self.get_squared_distance_toward_target(target_x, target_y, 'L')
        if maze.is_clear(round(self.x_grid),round(self.y_grid),'R'):
            right_distance = self.get_squared_distance_toward_target(target_x, target_y, 'R')

        if up_distance < least_distance and self.last_direction != 'D':
            least_distance = up_distance
            Choice = 'U'
        if down_distance < least_distance and self.last_direction != 'U':
            least_distance = down_distance
            Choice = 'D'
        if left_distance < least_distance and self.last_direction != 'R':
            least_distance = left_distance
            Choice = 'L'
        if right_distance < least_distance and self.last_direction != 'L':
            least_distance = right_distance
            Choice = 'R'
        return Choice


    def move(self, PacMan, maze, Ghost_list, screen):
        if (abs(self.y_grid - EMV.Teleport_y) < .5):
            if (abs(self.x_grid - EMV.Grid_x) < 2) and self.current_direction == 'R': 
                self.x_grid = 0
            if (abs(self.x_grid) < 1) and self.current_direction == 'L':
                self.x_grid = EMV.Grid_x - 1

        if self.at_center_of_block():
            if self.status == "Center":
                self.center_timer += 1
                self.current_direction = self.get_direction_toward_target(int(EMV.Grid_x/2)+2, int(EMV.Grid_y/2), maze)

                if maze.dots_eaten >= EMV.Dots_orange and self.color == EMV.Orange and self.center_timer >= self.hide_in_center_duration:
                    self.status = "Activating"
                    self.center_timer = 0
                elif maze.dots_eaten >= EMV.Dots_blue and self.color == EMV.Blue and self.center_timer >= self.hide_in_center_duration:
                    self.status = "Activating"
                    self.center_timer = 0
                elif maze.dots_eaten >= EMV.Dots_pink and self.color == EMV.Pink and self.center_timer >= self.hide_in_center_duration:
                    self.status = "Activating"
                    self.center_timer = 0
                elif maze.dots_eaten >= EMV.Dots_red and self.color == EMV.Red and self.center_timer >= self.hide_in_center_duration:
                    self.status = "Activating"
                    self.center_timer = 0

            elif self.status == "Corners":
                self.current_direction = self.get_direction_toward_target(self.corner_target_x, self.corner_target_y, maze)
                if maze.dots_eaten >= EMV.Dots_to_Switch_to_Pursuit:
                    self.status = "Pursuit"
            
            
            elif self.status == "Activating":
                self.current_direction = self.get_direction_toward_target(EMV.ghost_corral_entry_x, EMV.ghost_corral_entry_y, maze)
                if (self.x_grid - (EMV.ghost_corral_entry_x)) < .1 and (self.y_grid - (EMV.ghost_corral_entry_y)) < .1:
                    self.status = "Corners"
            
            
            elif self.status == "Pursuit":
                #Red pursuit strategy
                if self.color == EMV.Red:
                    self.current_direction = self.get_direction_toward_target(PacMan.x_grid, PacMan.y_grid, maze)

                #Blue pursuit strategy
                elif self.color == EMV.Blue:
                    self.current_direction = self.blue_targeting(PacMan, Ghost_list[0], maze, screen)
                
                #Pink pursuit strategy
                elif self.color == EMV.Pink:
                    if PacMan.current_direction == 'L':
                        self.current_direction = self.get_direction_toward_target(PacMan.x_grid-2, PacMan.y_grid, maze)
                    elif PacMan.current_direction == 'R':
                        self.current_direction = self.get_direction_toward_target(PacMan.x_grid+2, PacMan.y_grid, maze)
                    elif PacMan.current_direction == 'U':
                        self.current_direction = self.get_direction_toward_target(PacMan.x_grid, PacMan.y_grid-2, maze)
                    elif PacMan.current_direction == 'D':
                        self.current_direction = self.get_direction_toward_target(PacMan.x_grid, PacMan.y_grid+2, maze)
                    elif PacMan.current_direction == ' ':
                        self.current_direction = self.get_direction_toward_target(PacMan.x_grid, PacMan.y_grid, maze)

                #Orange pursuit strategy
                elif self.color == EMV.Orange:
                    if self.get_squared_distance_toward_target(PacMan.x_grid, PacMan.y_grid, ' ') > 20:
                        self.current_direction = self.get_direction_toward_target(PacMan.x_grid, PacMan.y_grid, maze)
                    else:
                        self.randomize_direction(maze)  

            elif self.status == "Frightened":
                self.randomize_direction(maze)  
                self.frightened_timer -= 1
                if self.frightened_timer <= 0:
                    PacMan.Points_per_ghost = 100
                    self.reset_ghost()
                    self.status = "Pursuit"
                    self.speed = EMV.Ghost_default_speed

            self.last_direction = self.current_direction


        if self.current_direction == 'U':
            self.y_grid -= self.speed
        elif self.current_direction == 'D':
            self.y_grid += self.speed
        elif self.current_direction == 'R':
            self.x_grid += self.speed
        elif self.current_direction == 'L':
            self.x_grid -= self.speed


    def get_squared_distance_toward_target(self, target_x, target_y, direction):
        if direction == 'U':
            distance = (target_x - self.x_grid)**2 + (target_y - (self.y_grid-1))**2
        elif direction == 'D':
            distance = (target_x - self.x_grid)**2 + (target_y - (self.y_grid+1))**2
        elif direction == 'L':
            distance = (target_x - (self.x_grid-1))**2 + (target_y - (self.y_grid))**2
        elif direction == 'R':
            distance = (target_x - (self.x_grid+1))**2 + (target_y - (self.y_grid))**2
        elif direction == ' ':
            distance = ((target_x - (self.x_grid))**2 + (target_y - self.y_grid)**2)
        return distance
        


    def at_center_of_block(self):
        if self.x_grid%1 <.1 and self.y_grid%1 <.1:
            return True
        else:
            return False

    def randomize_direction(self, maze):
        direction_choice = []
        if self.current_direction == 'U':
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'U'):
                direction_choice.append('U')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'L'):
                direction_choice.append('L')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'R'):
                direction_choice.append('R')

        elif self.current_direction == 'D':
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'D'):
                direction_choice.append('D')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'L'):
                direction_choice.append('L')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'R'):
                direction_choice.append('R')

        elif self.current_direction == 'L':
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'U'):
                direction_choice.append('U')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'D'):
                direction_choice.append('D')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'L'):
                direction_choice.append('L')

        elif self.current_direction == 'R':
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'U'):
                direction_choice.append('U')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'D'):
                direction_choice.append('D')
            if maze.is_clear(round(self.x_grid),round(self.y_grid),'R'):
                direction_choice.append('R')

        self.current_direction = sample(direction_choice, 1)[0]
    
    def blue_targeting(self, PacMan, Red, maze, screen):
        #Returns direction
        #Replaces (and calls) get_direction_toward_target for Blue
        target_x: int = 0
        target_y: int = 0
        if PacMan.current_direction == 'U':
            target_x = (PacMan.x_grid - Red.x_grid) + PacMan.x_grid
            target_y = (PacMan.y_grid - 1 - Red.y_grid) + PacMan.y_grid - 1

        elif PacMan.current_direction == 'D':
            target_x = (PacMan.x_grid - Red.x_grid) + PacMan.x_grid
            target_y = (PacMan.y_grid + 1 - Red.y_grid) + PacMan.y_grid + 1

        elif PacMan.current_direction == 'R':
            target_x = (PacMan.x_grid + 1 - Red.x_grid) + PacMan.x_grid + 1
            target_y = (PacMan.y_grid - Red.y_grid) + PacMan.y_grid

        elif PacMan.current_direction == 'L':
            target_x = (PacMan.x_grid - 1 - Red.x_grid) + PacMan.x_grid - 1
            target_y = (PacMan.y_grid - Red.y_grid) + PacMan.y_grid

        return (self.get_direction_toward_target(round(target_x-1), round(target_y-2), maze))


    #Resets ghost to roam in center, have default speed, and regain their default color
    def reset_ghost(self):
        self.status = "Center"
        self.speed = EMV.Ghost_default_speed
        if self.name == "Blinky":
            self.color = EMV.Red
        elif self.name == "Inky":
            self.color = EMV.Blue
        elif self.name == "Pinky":
            self.color = EMV.Pink
        elif self.name == "Clyde":
            self.color = EMV.Orange

    def turn_around_when_frightened(self):
        if self.current_direction == 'U':
            self.current_direction = 'D'
        elif self.current_direction == 'D':
            self.current_direction = 'U'
        elif self.current_direction == 'L':
            self.current_direction = 'R'
        elif self.current_direction == 'R':
            self.current_direction = 'L'
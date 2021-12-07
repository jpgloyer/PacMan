#Easy Modification Variables

#Ratio of Grid_X:screen_bounds_x must equal Grid_Y:screen_bounds_y
#Grid_x and Grid_y must correspond to characters and rows in PacManMazeV2.txt
Grid_x: int = 27
Grid_y: int = 36
screen_bounds_x: int = 600
screen_bounds_y: int = 800
Square_height: int = int(screen_bounds_y/Grid_y)
Square_width: int = int(screen_bounds_x/Grid_x)


#Map Specific Coordinates
ghost_corral_entry_x: int = 13
ghost_corral_entry_y: int = 12
Teleport_y: int = 14

#Dots to activate ghosts
Dots_red = 10
Dots_pink = 20
Dots_blue = 30
Dots_orange = 40
Dots_to_Switch_to_Pursuit = 70

#Ghost Spawn Coordinates
Red_x: int = int((Grid_x/2)+1)
Red_y: int = int((Grid_y/2)-5)
Blue_x: int = int((Grid_x/2)-1)
Blue_y: int = int((Grid_y/2)-5)
Pink_x: int = int((Grid_x/2)+1)
Pink_y: int = int((Grid_y/2)-3)
Orange_x: int = int((Grid_x/2)-1)
Orange_y: int = int((Grid_y/2)-3)
Ghost_x_coord_list = [Red_x, Blue_x, Pink_x, Orange_x]
Ghost_y_coord_list = [Red_y, Blue_y, Pink_y, Orange_y]

Ghost_default_speed = .09

#PacMan Spawn Coords
PacMan_x: int = int((Grid_x/2))
PacMan_y: int = int((Grid_y/2)-1)


#colors
maze_color = (0, 50, 128)
PacMan = (255,255,77)
Red = (255, 0, 0)
Blue = (102, 255, 255)
Pink = (255, 128, 255)
Orange = (255, 128, 0)
Ghost_colors = [Red, Blue, Pink, Orange]
Frightened_Color = (0,0,255)

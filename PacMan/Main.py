#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame import key
from typing import List
from Maze import Maze
import ScoreSort
import Dot
from Ghost import Ghost
from User import User
import User_Interface_Functions
import EMV
from contextlib import redirect_stdout
from Pickup import Pickup
import random


def main():

    #ENABLE THIS LOOP if running without a command line
    #with open('terminal_log.txt', 'w') as f:
        #with redirect_stdout(f):

    #Object creation
    #All but maze, dot_list, and screen can be used on any round/input maze
    maze = Maze(EMV.Grid_y, EMV.Grid_x)
    dot_list = Dot.dot_generationv2(maze.Maze)
    PacMan = User()
    Pickup1 = Pickup(random.randrange(0, 3))
    Red = Ghost(EMV.Red)
    Pink = Ghost(EMV.Pink)
    Orange = Ghost(EMV.Orange)
    Blue = Ghost(EMV.Blue)
    Ghost_List = [Red, Blue, Pink, Orange]
    Round_num = 1
        #Subtracting from screen bounds reduces black space at edges
    screen = User_Interface_Functions.start_game(EMV.screen_bounds_x-5, EMV.screen_bounds_y-5, maze.Maze)

    maze.print()    

    while PacMan.lives >= 0 and not PacMan.quitting:
        User_Interface_Functions.refresh_loop(screen, dot_list, PacMan, maze, Ghost_List, Round_num, Pickup1)
        Round_num += 1
        if PacMan.lives >= 0 and not PacMan.quitting:
            User_Interface_Functions.reset_after_round(PacMan, Ghost_List, dot_list, maze)



    pygame.display.quit()
    User_Interface_Functions.end_game(screen, PacMan)





if __name__ == "__main__":
    main()
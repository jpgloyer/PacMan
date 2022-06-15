#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pygame
from pygame import key
from Dot import dot
from Ghost import Ghost
from Projectile import Projectile
from User import User
import EMV
import ScoreSort
from Pickup import Pickup

#Pygame Section

#Initialize Pygame Window
def start_game(screen_bounds_x, screen_bounds_y, maze):
    pygame.init()
    screen = pygame.display.set_mode((screen_bounds_x, screen_bounds_y))
    draw_background(screen, screen_bounds_x, screen_bounds_y, maze)
    return screen

#Main gameplay function
def refresh_loop(screen, dot_list, PacMan, maze, Ghost_List, Round_num, Pickup1):
    clock = pygame.time.Clock()
    input_character: str = ' '
    direction_queue: str = ' '
    dead: bool = False
    Points_per_ghost: int = 100
    #shot = Projectile('L', PacMan.x_grid, PacMan.y_grid)

    #Round beginning Pygame window settings
    Round_string = "Round " + str(Round_num)
    pygame.display.set_caption(Round_string)
    Icon = pygame.image.load('PacMan.png')
    pygame.display.set_icon(Icon)


    #Make dots eaten and dots in maze variables in maze object
    for i in range(len(dot_list)):
        for j in range(len(dot_list[i])):
            if dot_list[i][j].Active == True:
                maze.dots_in_maze += 1

    #Loop runs 50x/second while player doesn't quit and hasn't eaten all the dots            
    while input_character != 'q' and maze.dots_eaten < maze.dots_in_maze and PacMan.lives >= 0:
        clock.tick(50)
        input_character = get_inputted_key_char()



        if input_character == 'q':
            PacMan.quitting = True

    #Refreshes black space (clears previous character locations)
        draw_black_space(screen, maze.Maze)


        #shot.move()
        #shot.draw(screen)

    #----------------------PICKUP SYSTEM----------------------
        if PacMan.Points > maze.pickup_trigger:
            Pickup1.active = True
            maze.pickup_trigger += 1000
        if Pickup1.active:
            Pickup1.draw(screen)
            if(abs(PacMan.x_grid - Pickup1.location[0]) < .5 and abs(PacMan.y_grid - Pickup1.location[1]) < 5):
                PacMan.pickup_name = Pickup1.type
                PacMan.pickup_behaviors(Ghost_List)
                Pickup1.active = False
                Pickup1 = Pickup(random.randrange(0, 3))

    #Draws Active Dots
        for i in range(len(dot_list)):
            for j in range(len(dot_list[i])):
                if dot_list[i][j].Active:
                    pygame.draw.circle(screen, (255,255,255), (dot_list[i][j].x_coord, dot_list[i][j].y_coord), dot_list[i][j].size)


    #Collision Detection (also sets ghosts to frightened when big dot is eaten)
    #Dots
        if(dot_list[round(PacMan.y_grid)][round(PacMan.x_grid)].Active):
            PacMan.Points += 10
            maze.dots_eaten += 1
            #Big dot ghost frightening
            if dot_list[round(PacMan.y_grid)][round(PacMan.x_grid)].size == EMV.Square_width/3:
                PacMan.Points += 90
                for i in range(len(Ghost_List)):
                    Ghost_List[i].frightened_timer = 50
                    if Ghost_List[i].status == "Corners" or Ghost_List[i].status == "Pursuit":
                        Ghost_List[i].status = "Frightened"
                        Ghost_List[i].speed = Ghost_List[i].speed / 2
                        #180 when becomming frightened
                        Ghost_List[i].turn_around_when_frightened()
                        Ghost_List[i].frightened_timer = 50
                        Ghost_List[i].color = EMV.Frightened_Color

            print(PacMan.Points)
            #Turns off dot at current pacman location
            dot_list[round(PacMan.y_grid)][round(PacMan.x_grid)].Active = False



    #Ghosts
        for i in range(len(Ghost_List)):
            if (abs(Ghost_List[i].x_grid - PacMan.x_grid) < .5) and (abs(Ghost_List[i].y_grid - PacMan.y_grid) < .5) and Ghost_List[i].status != "Frightened":
                PacMan.lives -= 1
                dead = True
                PacMan.Points_per_ghost = 100
            elif (abs(Ghost_List[i].x_grid - PacMan.x_grid) < .5) and (abs(Ghost_List[i].y_grid - PacMan.y_grid) < .5) and Ghost_List[i].status == "Frightened":
                PacMan.Points += Points_per_ghost
                PacMan.Points_per_ghost += 100
                print(PacMan.Points)
                Ghost_List[i].x_grid = EMV.Ghost_x_coord_list[i]
                Ghost_List[i].y_grid = EMV.Ghost_y_coord_list[i]
                Ghost_List[i].status = "Center"
                Ghost_List[i].speed = Ghost_List[i].speed * 2
                Ghost_List[i].color = EMV.Ghost_colors[i]

    #Moves and Draws Characters
        #PacMan
        if input_character == 'U' or input_character == 'D' or input_character == 'R' or input_character == 'L':
            direction_queue = input_character
        PacMan.Move(direction_queue, maze)
        pygame.draw.circle(screen, PacMan.color, ((PacMan.x_grid+.5)*EMV.Square_width,(PacMan.y_grid+.5)*EMV.Square_height), EMV.Square_height/3)

        #Ghosts
        for i in range(len(Ghost_List)):
            Ghost_List[i].move(PacMan, maze, Ghost_List, screen)
            pygame.draw.circle(screen, Ghost_List[i].color, ((Ghost_List[i].x_grid+.5)*EMV.Square_width,(Ghost_List[i].y_grid+.5)*EMV.Square_height), EMV.Square_height/3)

    #Loop requires 'enter' input to reset positions after death
        if dead == True:
            while input_character != "Return" and input_character != 'q':
                input_character = get_inputted_key_char()
            reset_after_death(PacMan, Ghost_List)
            dead = False

        pygame.display.flip()


def end_game(screen, PacMan):
    user_name = input("Please enter your name without spaces:")
    #Run code to remove spaces from user_name
    print("\n\n\n\nGAME OVER\n" + user_name + ": " + str(PacMan.Points) + "\n\n\n" + "High Scores:")

    with open("PacManHighScores.txt", "a") as HighScores:
        HighScores.write("1. " + str(user_name) + ": " + str(PacMan.Points) + "\n")
        HighScores.close()

    ScoreSort.sort()

    with open("PacManHighScores.txt", "r") as HighScores:
        FiveHighScores = HighScores.readlines()
        if len(FiveHighScores) >= 5:
            for i in range(0, 5):
                print(FiveHighScores[i])


def draw_background(screen, screen_bounds_x, screen_bounds_y, maze):
    pygame.draw.rect(screen, (0, 0, 0, 255), (0, 0, screen_bounds_x, screen_bounds_y))
    for i in range(maze[-1][0]-1):
        for j in range(maze[-1][1]):
            if maze[i][j] == "-":
                pygame.draw.rect(screen, EMV.maze_color, (j*maze[-1][3], i*maze[-1][2], maze[-1][3], maze[-1][2]))
            

def draw_black_space(screen, maze):
    for i in range(maze[-1][0]-1):
        for j in range(maze[-1][1]):
            if maze[i][j] != "-" and maze[i][j] != "+":
                pygame.draw.rect(screen, (0, 0, 0, 255), (j*maze[-1][3], i*maze[-1][2], maze[-1][3], maze[-1][2]))

def reset_after_death(PacMan, Ghost_List):
    for i in range(len(Ghost_List)):
        Ghost_List[i].x_grid = EMV.Ghost_x_coord_list[i]
        Ghost_List[i].y_grid = EMV.Ghost_y_coord_list[i]
        Ghost_List[i].center_timer = 0
        Ghost_List[i].reset_ghost()
    PacMan.x_grid = EMV.PacMan_x
    PacMan.y_grid = EMV.PacMan_y

        


#Only works if resetting for the same maze
def reset_after_round(PacMan, Ghost_List, Dot_List, maze):
    maze.dots_eaten = 0
    maze.dots_in_maze = 0
    #Play PacMan sound of some kind
    for i in range(len(Ghost_List)):
        Ghost_List[i].x_grid = EMV.Ghost_x_coord_list[i]
        Ghost_List[i].y_grid = EMV.Ghost_y_coord_list[i]
        Ghost_List[i].reset_ghost()
        Ghost_List[i].center_timer = 0
    PacMan.x_grid = EMV.PacMan_x
    PacMan.y_grid = EMV.PacMan_y
    maze.dots_eaten = 0
    clock = pygame.time.Clock()
    
    for i in range(len(Dot_List)):
        for j in range(len(Dot_List[i])):
            if maze.Maze[i][j] == "*" or maze.Maze[i][j] == "%":
                Dot_List[i][j].Active = True

    for i in range(250):
        #print("here")
        clock.tick(50)


#Input Section

#returns character
def get_inputted_key_char():
    keys = key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'q'
            if event.key == pygame.K_LEFT:
                return 'L'
            if event.key == pygame.K_RIGHT:
                return 'R'
            if event.key == pygame.K_UP:
                return 'U'
            if event.key == pygame.K_DOWN:
                return 'D'
            if event.key == pygame.K_RETURN:
                return 'Return'
    return ' '

def text_box(screen, clock):
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(EMV.screen_bounds_x/2, EMV.screen_bounds_y/2, 140, 30)
    color_active = EMV.Red
    color_passive = EMV.Blue
    color = color_passive
    active = False
    input_character = ''

    while input_character != "Return":
        input_character = get_inputted_key_char()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

        input_rect.w = max(100, text_surface.get_width()+10)
        print("Here")
        clock.tick(50)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import EMV



# def dot_generation(maze):
#     dot_list = []
#     for i in range(maze[-1][0]-1):
#         for j in range(maze[-1][1]):
#             dot_list.append(dot((j+.5)*maze[-1][3], (i+.5)*maze[-1][2], 0))
#             if maze[i][j] == "*":
#                     dot_list[-1].size = EMV.Square_width/6
#                     dot_list[-1].Active = True
#             if maze[i][j] == "%":
#                     dot_list[-1].size = EMV.Square_width/3
#                     dot_list[-1].Active = True
#     return dot_list

def dot_generationv2(maze):
    dot_list = [[]]
    for i in range(maze[-1][0]-1):
        dot_list.append([])
        for j in range(maze[-1][1]):
            dot_list[i].append(dot((j+.5)*maze[-1][3], (i+.5)*maze[-1][2], 0))
            if maze[i][j] == "*":
                    dot_list[i][j].size = EMV.Square_width/6
                    dot_list[i][j].Active = True
            if maze[i][j] == "%":
                    dot_list[i][j].size = EMV.Square_width/3
                    dot_list[i][j].Active = True
    return dot_list

class dot:
    def __init__(self, x_coord: int, y_coord: int, size: int):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.size = size
        self.Active: bool = False

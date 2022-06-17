#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def sort():
    """Sorts PacMan high score document"""
    document_info_strings = []

    #Creates list[list][parts of each line (type string)]
    with open("PacManHighScores.txt") as HighScoreList:
        for line in HighScoreList:
            document_info_strings.append(line.split(" "))

    
    #Clears endline characters after each line
    #Converts score from string to int to allow sorting by score
    for i in range(len(document_info_strings)):
        document_info_strings[i][2] = int(document_info_strings[i][2][:-1])

    #Sorts By Score
    #Lambda key should be the position of the score in the score document
    sorted_score_strings = sorted(document_info_strings, key=lambda x: x[2], reverse=True)


    #Writes over HighScores list with sorted information
    with open("PacManHighScores.txt", "w") as HighScoreList:
        for i in range(len(sorted_score_strings)):
            HighScoreList.write(str(i + 1) + ". " + str(sorted_score_strings[i][1]) + " " + str(sorted_score_strings[i][2]) + "\n")

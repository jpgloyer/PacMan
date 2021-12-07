import EMV
import pygame

class Pickup:
    def __init__(self, type_number):
        #Type can be: extra life(0), fruit(1), bomb(2), laser(3), invisibility(4), big dot(5)
        self.type: str
        self.active: bool = False
        self.location = (EMV.PacMan_x, EMV.PacMan_y)
        self.fruit_surface = pygame.image.load("PacManCherryImage.png")
        self.fruit_image = pygame.transform.scale(self.fruit_surface, (20, 20))
        if type_number == 0:
            self.type = "Extra_Life"
        elif type_number == 1:
            self.type = "Fruit"
        elif type_number == 2:
            self.type = "Big_Dot"
        elif type_number == 3:
            self.type = "Laser"
        elif type_number == 4:
            self.type = "Invisibility"
        elif type_number == 5:
            self.type = "Bomb"

    #MAKE A DRAW FUNCTION
    def draw(self, screen):
        if self.type == "Extra_Life":
            pygame.draw.circle(screen, (EMV.PacMan), ((self.location[0]+.5)*EMV.Square_width, (self.location[1]+.5)*EMV.Square_height), EMV.Square_width/3)
            #pygame.draw.rect(screen, (0,255,0), (self.location[0]*EMV.Square_width, self.location[1]*EMV.Square_height, EMV.Square_width, EMV.Square_height))
        elif self.type == "Fruit":
            #----------------------------BREAKS SCREEN SIZE CHANGING MECHANICS-------------------------
            #----------------------------Implement size altering mechanic to constructor---------------------------
            screen.blit(self.fruit_image, ((self.location[0])*EMV.Square_width, (self.location[1])*EMV.Square_height))
        elif self.type == "Big_Dot":
            pygame.draw.circle(screen, (255,255,255), ((EMV.PacMan_x+.5)*EMV.Square_width, (EMV.PacMan_y+.5)*EMV.Square_height), EMV.Square_width/3)
        
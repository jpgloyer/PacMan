import EMV
import pygame

class Projectile:
    def __init__(self, direction, x_coord, y_coord):
        self.direction = direction
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_speed = .2
        self.y_speed = .2
        if self.direction == 'R':
            self.x_coord+=.5
        if self.direction == 'D':
            self.y_coord+=.5

    def move(self):
        if self.direction == 'U':
            self.y_coord -= self.y_speed
        elif self.direction == 'D':
            self.y_coord += self.y_speed
        elif self.direction == 'R':
            self.x_coord += self.x_speed
        elif self.direction == 'L':
            self.x_coord -= self.x_speed

    def draw(self, screen):
        if self.direction == 'U':
            pygame.draw.rect(screen, (255,255,255), ((self.x_coord+.25)*EMV.Square_width, self.y_coord*EMV.Square_height, EMV.Square_width/2, EMV.Square_height/2))
        elif self.direction == 'D':
            pygame.draw.rect(screen, (255,255,255), ((self.x_coord+.25)*EMV.Square_width, self.y_coord*EMV.Square_height, EMV.Square_width/2, EMV.Square_height/2))

        elif self.direction == 'L':
            pygame.draw.rect(screen, (255,255,255), (self.x_coord*EMV.Square_width, (self.y_coord+.25)*EMV.Square_height, EMV.Square_width/2, EMV.Square_height/2))
            
        elif self.direction == 'R':
            pygame.draw.rect(screen, (255,255,255), (self.x_coord*EMV.Square_width, (self.y_coord+.25)*EMV.Square_height, EMV.Square_width/2, EMV.Square_height/2))

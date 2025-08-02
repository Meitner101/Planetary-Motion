
import pygame
import sys
import math
pygame.init() 

moon_distance = 100  # Distance from Earth (pixels)
moon_angle = 0       # Initial angle in radians
moon_speed = 0.02  
WIDTH , HEIGHT = 800,800
WIN = pygame.display.set_mode((HEIGHT,WIDTH))

pygame.display.set_caption("Satellite")
black = (0,0,0)
white = (255,255,255)
blue = (100,149,137)
clock = pygame.time.Clock()

earth_x,earth_y = WIDTH//2,HEIGHT//2
earth_radius = 30

running = True 
while running:
    WIN.fill(black)
    pygame.draw.circle(WIN,blue,(earth_x,earth_y),earth_radius)
    moon_x = earth_x + moon_distance*math.cos(moon_angle)
    moon_y = earth_y + moon_distance*math.sin(moon_angle)
    moon_angle+=moon_speed
    pygame.draw.circle(WIN,white,(int(moon_x),int(moon_y)),10)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()      
sys.exit()
      
            
import pygame 
import math

pygame.init()#Initialize all the built-in modules like sound, graphics, input, timing, etc.

WIDTH, HEIGHT = 800, 800 # size of the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))# Creates the game window using the width and height above.
# Stored in WIN so we can draw stuff on it.
pygame.display.set_caption("PlanetarySimulation")#Sets the window title

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)#color of sun 
BLACK = (0,0,0)#background color
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY = (80,78,81)

FONT = pygame.font.SysFont("comicsans",16)
class Planet:
    AU = 149.6e6 * 1000# Astronomical Unit in meters
    G = 6.67428e-11 # Gravitational Constant
    SCALE = 200/ AU# 1 AU = 200 pixels
    TimeStep = 3600 * 24# One "tick" = 1 day

    def __init__(self, x, y, radius, color, mass):# Called when a new Planet is created.
        self.x = x #Assigns values (position, size, color, mass) to the planet
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
# Initial velocity of the planet (used for orbiting later)
        self.x_vel = 0
        self.y_vel = 0
        self.orbit = []#Stores past positions for drawing orbit line
        self.distance_to_sun = 0
        self.sun = False
#Drawing the Planet
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 #🔹 Convert physics coords (in meters) to pixel coords on screen
# Adding WIDTH/2 and HEIGHT/2 centers the orbit.
        y = self.y * self.SCALE + HEIGHT / 2
# Actually draws the planet as a circle on the screen.
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1,WHITE)
            win.blit(distance_text,(x - distance_text.get_width()/2,y-distance_text.get_height()/2))

    def attraction(self,other):#calculating the force of attraction between planets
        other_x,other_y = other.x,other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.distance_to_sun=distance

        force = self.G * self.mass*other.mass /distance**2
        theta = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x,force_y
    
    def update_position(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TimeStep
        self.y_vel += total_fy / self.mass * self.TimeStep

        self.x += self.x_vel * self.TimeStep
        self.y += self.y_vel * self.TimeStep
        self.orbit.append((self.x, self.y))

#☀️ Main Game Loop
def main():#The main game function — everything runs from here.
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1*Planet.AU,0,16,BLUE,5.9742*10**24)
    earth.y_vel = 29.783*1000

    mars = Planet(-1.524*Planet.AU,0,12,RED,6.39*10**23)
    mars.y_vel = 24.077*1000

    mercury = Planet(0.387*Planet.AU,0,8,DARK_GREY,3.30*10**23)
    mercury.y_vel = 47.4*1000

    venus = Planet(0.723*Planet.AU,0,14,WHITE,4.8685*10**24)
    venus.y_vel = -35.02*1000

    
    planets = [sun,earth,mars,mercury,venus]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))  # Clear screen every frame

        for event in pygame.event.get():#continuous loop until user press "x" 
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:#to actually draw the planet
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()#to update the page

    pygame.quit()

main()





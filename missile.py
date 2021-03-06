# Missile Command Clone by /u/wynand1004 AKA @TokyoEdTech
# Requires SPGL Version 0.8 or Above

# Explodey Shooty Kablooey Turbo 3 by Alex Helton and Cole Snodgrass
# This code is property of (and a joint venture between) Opossum Systems and Koala Industries
# Import SPGL

# Dear programmer:
# When I wrote this code, only god and
# I knew how it worked.
# Now, only god knows it!
#
# Therefore, if you are trying to optimize
# this routine and it fails (most surely),
# please increase this counter as a
# warning for the next person:
#
# total hours wasted here = 12

import spgl
import math
import random
from turtle import *
from random import choice, randint
import turtle as T
FPS = 60
# Create Classes

class MissileCommand(spgl.Game):
    def __init__(self, screen_width, screen_height, background_coor, title, splash_time):
       spgl.Game.__init__(self, screen_width, screen_height, background_coor, title, splash_time)
       self.level = 1

    def click(self, x, y):
        # Find the closest missile
        closest_missile = None
        closest_missile_distance = 10000
        for player_missile in player_missiles:
            if player_missile.state == "ready":               
                a=player_missile.xcor()-x
                b=player_missile.ycor()-y
                distance = math.sqrt((a**2) + (b**2))
                if distance < closest_missile_distance:
                    closest_missile = player_missile
                    closest_missile_distance = distance
        if closest_missile:
            closest_missile.set_target(x, y)

class Terrain(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
    def drawTerrain(self):
        # this is really ugly but I don't know a better way at the moment.
        # just smear a line at the bottom so it looks sorta good, fuck it
        T.pencolor("dark green")
        T.goto(-500,-200)
        T.width(20)
        T.pendown()
        for i in range(200):
            T.forward(10)
        T.penup()
        T.hideturtle()

class City(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def destroy(self):
        self.clear()
        self.penup()
        self.goto(0, 2000)
        self.state = None 

    def tick(self):
        pass

class Silo(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def destroy(self):
        self.clear()
        self.penup()
        self.goto(0, 2000)
        self.state = None 
        silos.remove(self)

    def tick(self):
        pass

class PlayerMissile(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.speed = 5
        self.state = "ready"
        self.target_x = 0
        self.target_y = 0
        self.size = 0.2
        self.shapesize(self.size, self.size, 0)
        self.frame = 0.0
        

    def set_target(self, target_x, target_y):
        if self.state == "ready":
            game.play_sound("shoot.wav")
            self.target_x = target_x
            self.target_y = target_y
            
            self.dx = self.xcor() - self.target_x
            # Avoid divide by 0 error
            if self.dx == 0:  
                self.dx = 0.01
            self.dy = self.ycor() - self.target_y
            self.m = self.dy/self.dx     
            
            self.state = "launched"

    def explode(self):
        self.frame += 1.0
        if self.frame < 30.0:
            self.size = self.frame / 10
            self.shapesize(self.size, self.size, 0)
        elif self.frame < 55.0:
            self.size = (60 - self.frame)/10
            self.shapesize(self.size, self.size, 0)
        else:
            self.destroy()

    def tick(self):
        if self.state == "launched":
            self.pendown()
            self.setx(self.xcor() + (1 / self.m) * self.speed)
            self.sety(self.ycor() + self.speed)

            # Check for reaching target
            a=self.xcor()-self.target_x
            b=self.ycor()-self.target_y
            distance = math.sqrt((a**2) + (b**2))

            if distance < 10:
                self.state = "explode"

            # Border Checking
            if (self.xcor()< -420) or (self.xcor() > 420):
                self.state = "explode"

        if self.state == "explode":
            self.explode()

    def destroy(self):
        self.clear()
        self.penup()
        self.goto(0, 2000)
        self.state = "ready" 
        player_missiles.remove(self)  
        self.frame = 2

class Starfield(spgl.Sprite):
    # create random dots with pretty colors, the kids like to see colors in their vidjagames
    def __init__(self, shape, color, x=0, y=0, width=20, height=20):
        spgl.Sprite.__init__(shape, color, x=x, y=y, width=width, height=height)

    def drawStarfield(self):
        
        
        screen = Screen()
        width, height = screen.window_width(), screen.window_height()
        starfieldColors = ['red', 'green', 'blue', 'magenta', 'yellow', 'cyan']
        
        for _ in range(randint(50,70)):
            
            radius = 1
            circleX = randint(radius - width//2, width//2 - radius)
            circleY = randint(radius - height//4, height//2 - radius)
            self.setposition(circleX, circleY)
            self.pendown()
            self.dot(radius * 2, choice(starfieldColors))
            self.penup()


class EnemyMissile(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.dx = 0
        self.dy = 0
        self.speed = 2
        self.size = 0.2
        self.shapesize(self.size, self.size, 0)
        self.pendown()
        self.state = "ready"
        self.target_x = 0
        self.target_y = 0
        self.frame = 2

    def set_target(self, target):
        # Move to a random spot outside the screen area
        self.goto(random.randint(-450, 450), random.randint(400, 800))
        self.size = 0.2
        self.shapesize(self.size, self.size, 0)
        self.pendown()

        self.target_x = target.xcor()
        self.target_y = target.ycor()

        self.dx = self.xcor() - target.xcor()
        # Avoid divide by 0 error
        # better not blow up the universe this way
        if self.dx == 0:  
            self.dx = 0.01
        self.dy = self.ycor() - target.ycor()
        self.m = self.dy/self.dx

        self.state = "launched"

    def explode(self):
        self.frame += 1.0
        if self.frame < 30.0:
            self.size = self.frame / 10
            self.shapesize(self.size, self.size, 0)
        elif self.frame < 55.0:
            self.size = (60 - self.frame)/10
            self.shapesize(self.size, self.size, 0)
        else:
            self.destroy()

    def destroy(self):
        
        self.clear()
        self.penup()
        self.goto(2000, 2000)
        self.state = None  
        self.frame = 2
        self.size = 0.2
        self.shapesize(self.size, self.size, 0) 
        self.state = "ready"
        
        enemy_missiles.remove(self)    

    def tick(self):
        if self.state == "launched":
            self.setx(self.xcor() - (1 / self.m) * self.speed)
            self.sety(self.ycor() - self.speed)

            # Check for reaching target
            a=self.xcor()-self.target_x
            b=self.ycor()-self.target_y
            distance = math.sqrt((a**2) + (b**2))

            if distance < 10:
                self.state = "explode"

        if self.state == "explode":
            self.explode()
            # The Explodey has been Kablooeyed by the Shooty

# Create Functions

# Initial Game setup
game = MissileCommand(800, 600, "black", "Explodey Shooty Kablooey Turbo 3", 5)
game.score = 0

# The thing about these arrays is that they're stored as these funky objects and not necessarily a number.
# When looking up the number of "Funky Objects" in this array, use len()!

# Create sprites
cities = []
silos = []
# Hold all player missiles
player_missiles_storage = []
# Hold all active player missiles
player_missiles = []
# Hold all enemy missiles
enemy_missiles_storage = []
# Hold active enemy missiles this level
enemy_missiles = []

for i in range(6):
    cities.append(City("square", "deep sky blue", -250 + (i * 100), -250))

for i in range(3):
    silos.append(Silo("square", "dark green", -350 + (i * 350), -225))

for i in range(30):
    if i <10:
        x = -350
    elif i < 20:
        x = 0
    else:
        x = 350
    playerColors = ['red', 'green', 'blue', 'magenta', 'yellow', 'cyan']

    player_missiles_storage.append(PlayerMissile("circle", random.choices(playerColors), x, -225))

for player_missile in player_missiles_storage:
    player_missiles.append(player_missile)

for i in range(30):
    enemyColors = ['red', 'green', 'blue', 'magenta', 'yellow', 'cyan']
    enemy_missiles_storage.append(EnemyMissile("circle", random.choices(enemyColors), random.randint(-450, 450), random.randint(400, 800)))

for enemy_missile in enemy_missiles_storage:
    if len(enemy_missiles) < game.level:
        enemy_missile.set_target(random.choice(cities + silos))
        enemy_missiles.append(enemy_missile)


# This creates a label to be later formatted "properly" below. :(

status_label = spgl.Label("Explodey Shooty Kablooey Turbo 3  \nLevel: {}  \nScore: {}  \nCities: {}  \nSilos: {}  \nPlayer Missiles: {}  \nEnemy Missiles: {}", "lime", -390, 130, font_name="OCR A Extended")

Terrain.drawTerrain(T) # draws the green smear
Starfield.drawStarfield(T) # draws that fancy starfield
# ^^ You know how long that took me to figure out?
# Turtles, man...

while True:
    status_label.update("Explodey Shooty Kablooey Turbo 3\nCopyright 1981 Opossum Systems\nLevel: {}  \nScore: {}  \nCities: {}  \nSilos: {}  \nPlayer Missiles: {}  \nEnemy Missiles: {}".format(game.level, game.score, len(cities), len(silos), len(player_missiles), len(enemy_missiles)))     

    # Call the game tick method
    game.tick()
    # Check to see if the player missile collides with the enemy missiles
    for player_missile in player_missiles:
        for enemy_missile in enemy_missiles:
            # Check if the player missile is exploding
            if player_missile.state == "explode":
                radius = (player_missile.size * 20) / 2
                a=player_missile.xcor()-enemy_missile.xcor()
                b=player_missile.ycor()-enemy_missile.ycor()
                distance = math.sqrt((a**2) + (b**2))
                if distance < radius:
                    enemy_missile.destroy()  
                    game.score += 10         
                    game.play_sound("explosion.wav")
    # Check to see if the enemy missile collides with the player cities or silos (destroy the missiles there as well)
    for enemy_missile in enemy_missiles:
        for city in cities:
            if enemy_missile.state == "explode":
                radius = (enemy_missile.size * 20) / 2
                a=enemy_missile.xcor()-city.xcor()
                b=enemy_missile.ycor()-city.ycor()
                distance = math.sqrt((a**2) + (b**2))
                if distance < radius:
                    game.play_sound("silo_boom.wav")
                    city.destroy()    
                    cities.remove(city)   

        for silo in silos:
            if enemy_missile.state == "explode":
                radius = (enemy_missile.size * 20) / 2
                a=enemy_missile.xcor()-silo.xcor()
                b=enemy_missile.ycor()-silo.ycor()
                distance = math.sqrt((a**2) + (b**2))
                if distance < radius:
                    game.play_sound("silo_boom.wav")
                    silo.destroy()

                for player_missile in player_missiles:
                    a=enemy_missile.xcor()-player_missile.xcor()
                    b=enemy_missile.ycor()-player_missile.ycor()
                    distance = math.sqrt((a**2) + (b**2))
                    if distance < radius:
                        player_missile.destroy()
                        game.play_sound("explosion.wav")
    # Check to see how many enemy missiles remain in this level
    if len(enemy_missiles) < 1:

        # Add up score
        city_bonus = 100 * len(cities)
        silo_bonus = 50 * len(silos)
        missile_bonus = 10 * len(player_missiles)      

        game.score += (city_bonus + silo_bonus + missile_bonus)
        # these two print statements are just debug information.
        # If you can even call it that
        print("Level {} Complete".format(game.level))
        print("City Bonus: {}  Silo Bonus: {}  Missile Bonus: {}  Cities Left: {}".format(city_bonus, silo_bonus, missile_bonus, len(cities)))
        
        game.level += 1

        # Reset enemy missiles

        # I'm the smartest programmer that's ever lived
        for enemy_missile in enemy_missiles_storage:
            if len(enemy_missiles) < game.level:
                if len(cities) != 0:
                    enemy_missile.set_target(random.choice(cities + silos))
                    enemy_missiles.append(enemy_missile) 
                else:
                    # Now watch this, this'll blow your fuckin mind
                    game.play_sound("sad.wav")
                    game.show_warning("Explodey Shooty Kablooey Turbo 3", "Game over man!")        
                    game.exit()
        # Reset player missiles
        for player_missile in player_missiles:
            player_missile.destroy()
            
        player_missiles = []

        for player_missile in player_missiles_storage:
            player_missiles.append(player_missile)

        for i in range(30):
            if i <10:
                x = -350
            elif i < 20:
                x = 0
            else:
                x = 350

            player_missiles[i].clear()
            player_missiles[i].goto(x, -225)
            player_missiles[i].state = "ready"
            player_missiles[i].shapesize(0.2, 0.2, 0)
            player_missiles[i].clear()

# That's all she wrote
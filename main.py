"""
Runs main Pygame loop

Author: Ellie Newman
Assignment: Final

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given fully documented references to the work of others.  I understand the definition and consequences of plagiarism and acknowledge that the assessor of this assignment may, for the purpose of assessing this assignment, reproduce this assignment and provide a copy to another member of academic staff and/or communicate a copy of this assignment to a plagiarism checking service (which may then retain a copy of this assignment on its database for the purpose of future plagiarism checking).
"""

#https://realpython.com/pygame-a-primer/
#https://docs.replit.com/tutorials/python/building-a-game-with-pygame
import pygame
from spacesprites import Player, CelestBody, Planet, BlackHole, StartButton
from screen_text import Text, WIDTH, HEIGHT


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.transform.scale(pygame.image.load("SpaceScreen.png"), (WIDTH, HEIGHT))

clock = pygame.time.Clock()
pygame.display.set_caption('Beware of black holes! Do you copy?')

#Creates player and celestial bodies
player = Player()

blue_p = Planet((55,70,255),((11/16)*WIDTH,(3/16)*HEIGHT), 30, "Electric Blue", "blue_planet.png")
red_p =Planet((250,70,70),((2/16)*WIDTH,(5/16)*HEIGHT),35, "Red", "red_planet.png")
orange_p = Planet((255,130,40),((14/16)*WIDTH,(11/16)*HEIGHT),40, "Orange", "orange_planet.png")
green_p = Planet((60,150,90),((4/16)*WIDTH,(14/16)*HEIGHT),20, "Green", "green_planet.png")
blackhole = BlackHole("InitBlackHole.png", "PenroseFinal.png")

Planet.correct_seq = [red_p, orange_p, green_p, blue_p, red_p]

#List Comprehension
Text.correct_seq = [Text(Planet.correct_seq[x].first_let, position=((29/64)*WIDTH+(x*20),(13/16)*HEIGHT)) for x in range(len(Planet.correct_seq))]

win_text=Text("Penrose!")
group = pygame.sprite.Group(CelestBody.all_bodies, Text.all_text)

#start button
puzzle_button = StartButton((175,100,175), ((3/8)*WIDTH, (6/8)*HEIGHT), 40, "Puzzle")
art_button = StartButton((75,175,175), ((5/8)*WIDTH, (6/8)*HEIGHT), 40, "Art")

instruct1 = Text("Guide your astronaut through space with your mouse", position=(WIDTH/2, (5/16)*HEIGHT), visible=True)
instruct2 = Text("Click on celestial bodies to interact with them", position=(WIDTH/2, (6/16)*HEIGHT), visible=True)
instruct3 = Text("Select 'Puzzle' mode to try and reveal a secret message,", position=(WIDTH/2, HEIGHT/2), visible=True)
instruct4 = Text("or 'Art' mode to explore without distractions.", position=(WIDTH/2, (9/16)*HEIGHT), visible=True)

start_group = pygame.sprite.Group(puzzle_button, art_button, puzzle_button.message, art_button.message, instruct1, instruct2, instruct3, instruct4)

running = True
while running:
    clock.tick(15)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    
    start_group.update(event_list)
    start_group.draw(screen)

    #https://www.tutorialspoint.com/pygame/pygame_moving_mouse.htm
    x,y = pygame.mouse.get_pos() 
    screen.blit(player.astro, (x,y))
    
    if puzzle_button.start == True or art_button.start == True:
        if art_button.start == True:
            #disables puzzle game
            Planet.winner = True
        for item in start_group:
            item.kill()
        group.update(event_list)
        #draws celestial bodies
        group.draw(screen)
        #puts astronaut on top of planets
        screen.blit(player.astro, (x,y))
            
    pygame.display.flip()
pygame.quit()
exit()

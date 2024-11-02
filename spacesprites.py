"""
Contains sprite classes (Player, CelestialBody, Planet, Black Hole)

Author: Ellie Newman
Assignment: Final

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given fully documented references to the work of others.  I understand the definition and consequences of plagiarism and acknowledge that the assessor of this assignment may, for the purpose of assessing this assignment, reproduce this assignment and provide a copy to another member of academic staff and/or communicate a copy of this assignment to a plagiarism checking service (which may then retain a copy of this assignment on its database for the purpose of future plagiarism checking).
"""

import pygame
from abc import ABC, abstractmethod
from screen_text import Text, WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    """Player sprite. Rectangular region with image of astronaut. Controlled by player's mouse.
    """
    def __init__(self):
        """Initializes instance of Player.
        
        Arguments: none
        Attributes:
            self.astro: image of astronaut
            self.rect: rectangular area of self.astro image
        """
        super(Player, self).__init__()
        self.astro = pygame.image.load("PixelAstronaut.png")
        self.rect = self.astro.get_rect()


class CelestBody(pygame.sprite.Sprite, ABC):
    """Celestial Body sprite.
    
    Attributes:
        all_bodies: list of all Celestial Body objects
    """
    all_bodies= []
    
    def __init__(self, color, position, radius):
        """Initializes instance of planet object with specified color, position, and radius.
        
        Arguments:
            color: (list) RGB color values (3 ints with values 0-255)
            position: (list of 2 numbers) location in respect to top left corner of screen. First value determines horizontal distance, second gives vertical distance.
            radius: (float) radius of object's circle
        """
        super().__init__()
        self.radius = radius
        self.position = position
        
        ##https://replit.com/@Rabbid76/PyGame-MouseClick#main.py
        #Draws simple object (circle with color):
        self.simple_image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.simple_image, color, (radius, radius), radius)
        
        self.image = self.simple_image 
        self.rect = self.image.get_rect(center = position)
        self.clicked = False
        
        CelestBody.all_bodies.append(self)
        
    @abstractmethod
    def update(self, event_list):
        """Determines object's behavior when clicked.
        """
        pass


#Inheritance
class Planet(CelestBody):
    """Planet is a type of celestial body with specified appearance, position, and radius.

    Attributes: 
        _answer: (list) sequence of planets used in name game
        my_seq: (list) list of planets affected by what the user clicks on; used in name game
        winner: (bool) determines whether or not name game should continue to be played
    """
    #name game components:
    _answer = []
    my_seq = []
    winner = False
    
    def __init__(self, color, position, radius, name, detailedIm):
        """Initiates instance of Planet.

        Arguments:
            color: (tuple) RGB color values (3 ints with values 0-255)
            position: (tuple of 2 numbers) location in respect to top left corner of screen. First value determines horizontal distance, second gives vertical distance.
            radius: (float) radius of planet's circle
            name: (str) color name, used in name game
            detailedIm: (image) detailed image of planet
        """
        super().__init__(color, position, radius)
        #Draws detailed object
        self.detail_image = pygame.image.load(detailedIm)
        #Scaled by diameter (slightly adjusted)
        self.detail_image = pygame.transform.scale(self.detail_image, (2.08*radius, 2.08*radius))
        
        self.name = name
        self.first_let = self.name[0]
        self.text = Text(name)

    #Property
    @property
    def correct_seq(cls):
        """Sequence of Planets (list). Used in name game as the solution to the puzzle

        Returns:
            cls._answer
        """
        return cls._answer
    
    @correct_seq.setter
    def correct_seq(cls, fir, sec, thi, fou, fif):
        """Sets sequence of Planets (list). Used in name game as the solution to the puzzle. Planets may appear more than once.

        Arguments:
            fir: (Planet) first planet in sequence
            sec: (Planet) second planet in sequence
            thi: (Planet) third planet in sequence
            fou: (Planet) fourth planet in sequence
            fif: (Planet) fifth planet in sequence
        """
        cls._answer = [fir, sec, thi, fou, fif]
    
    def update(self, event_list):
        """Switches between simple shape and detailed image when user clicks planet

        Arguments:
            event_list: (list) list of events (mouse clicks), gotten by pygame.event.get()
        """
        for event in event_list:
            #Left click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
                    if not Planet.winner:
                        Planet.name_game(self)
                    
        self.image = self.detail_image if self.clicked else self.simple_image

    #Class Method
    @classmethod
    def name_game(cls, my_planet):
        """Puzzle involving sequence of clicking on planets. User's sequence is compared to correct sequence and game is played until the two match.
        
        Arguments: 
            my_planet: (Planet) planet that user clicks on
        """
        if not cls.winner:
            #prints planet's color
            for text in Text.all_text:
                text.visible = False
            my_planet.text.visible = True
            
            cls.my_seq.append(my_planet)
            #Checks if user's sequence matches correct sequence
            if cls.my_seq[0:len(cls.my_seq)] == cls.correct_seq[0:len(cls.my_seq)]:
                for letter in Text.correct_seq:
                    letter.visible = False
                for letter in Text.correct_seq[0:len(cls.my_seq)]:
                    letter.visible = True
                    
                if cls.my_seq == cls.correct_seq:
                    for text in Text.all_text:
                        if len(text.message) > 1 and text.message !="Penrose!":
                            text.visible = False
                        else:
                            text.visible = True
                    cls.winner = True
            else:
                cls.my_seq = []

#Inheritance
class BlackHole(CelestBody):
    """BlackHole is a type of celestial body with specified radius and appearance.
    """
    def __init__(self, initial_im, final_im, radius=12):
        """Initializes instance of Black Hole. Black in color, centered on the screen, starting radius defaults to 12.

        Arguments:
            initial_im: (image) initial detailed image
            final_im: (image) final detailed image
        """
        super().__init__((0,0,0), (WIDTH/2,HEIGHT/2), radius)
        self.penrose = False
        self.initial_im = pygame.image.load(initial_im)
        self.final_im = pygame.image.load(final_im)
        self.angle = 18

    def update(self, event_list):
        """Updates the Blackhole when user clicks on it. If the current blackhole doesn't fill up the screen, it grows when clicked. Else if the blackhole is the size of the screen, it calls Penrose.

        Arguments:
            event_list: (list) list of events (mouse clicks), gotten by pygame.event.get()
        """
        for event in event_list:
            #Left click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.radius*1.5 < WIDTH/2:
                        self.Grow()
                        
                    else:
                        self.Penrose()
                        

    def Grow(self):
        """Increases radius of blackhole

        Arguments: self
        Returns: None
        """
        self.radius = self.radius*1.5
        self.image = pygame.transform.scale(self.initial_im, (2.08*self.radius, 2.08*self.radius))
                
        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))
    
    def Penrose(self):
        """Removes all other celestial bodies. Changes image of blackhole to penrose tile image which rotates when clicked.

        Arguments: self
        Returns: None
        """
        #first time method is called:
        if not self.penrose:
            #Deletes all other celestial bodies
            for body in CelestBody.all_bodies:
                if not isinstance(body, BlackHole):
                    body.kill()
            for text in Text.all_text:
                text.kill()
            #Sets new Penrose tile image
            self.radius = (WIDTH/2)
            self.image = pygame.transform.scale(self.final_im, (2.08*self.radius, 2.08*self.radius))         
            self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))
            self.penrose = True
        else:   
            self.image = pygame.transform.rotate(pygame.transform.scale(self.final_im, (2.08*self.radius, 2.08*self.radius)), self.angle)
            self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))
            self.angle += 18

#Inheritance
class StartButton(CelestBody):
    """Buttons in the form of a celestial body. Used to start the game.
    """
    def __init__(self, color, position, radius, gamemode):
        """Initializes instance of button.

        Arguments:
            color: (tuple) RGB color values (3 ints with values 0-255)
            position: (tuple of 2 numbers) location in respect to top left corner of screen. First value determines horizontal distance, second gives vertical distance.
            radius: (float) radius of button
            gamemode: (str) gamemode that button initiates, displayed in text
        """
        super().__init__(color, position, radius)
        self.position = position
        self.gamemode = gamemode
        self.start = False
        self.message = Text(gamemode, position = self.position, visible=True)
        
    def update(self, event_list):
        """Responds to click on button

        Arguments:
            event_list: (list) list of events (mouse clicks), gotten by pygame.event.get()
        """
        for event in event_list:
            #Left click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.start = True
                    

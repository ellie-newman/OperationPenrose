"""
Contains Text class and screen dimensions

Author: Ellie Newman
Assignment: Final

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given fully documented references to the work of others.  I understand the definition and consequences of plagiarism and acknowledge that the assessor of this assignment may, for the purpose of assessing this assignment, reproduce this assignment and provide a copy to another member of academic staff and/or communicate a copy of this assignment to a plagiarism checking service (which may then retain a copy of this assignment on its database for the purpose of future plagiarism checking).
"""

import pygame

#Display screen width and height, used accross modules and classes
WIDTH = 1040
HEIGHT = 585

#https://codereview.stackexchange.com/questions/31642/text-class-for-pygame
class Text(pygame.sprite.Sprite):
    """Text in the form of a sprite

    Attributes:
        all_text: list of all Text objects
        _correct_text: (list) used in Planet name game
    """
    all_text = []
    _correct_text = []
    
    def __init__(self, text, size=30, color=(255,255,255), font=None, position=(WIDTH/2, (7/8)*HEIGHT), visible=False):
        """Initializes instance of text to display on screen.

        Arguments:
            text: (str) message to display
            size: size of text, defaults to 30
            color: (tuple of RGB values) color of text, defaults to white
            font: font (defaults to none)
            postition: (tuple) postition of text on screen
        """
        super(Text, self).__init__()
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.position = position
        self.message = text

        self.visible = visible
        self.image = self.font.render("", 1, self.color)
        self.rect = self.image.get_rect(center = self.position)
        
        Text.all_text.append(self)
    
    def update(self, *args):
        """Displays text

        Arguments:
            args: catches extra argument so text and other sprites can be grouped and updated together in main loop
        """
        if self.visible == True:
            self.image = self.font.render(self.message, 1, self.color)
        else:
            self.image = self.font.render("", 1, self.color)
        self.rect = self.image.get_rect(center = self.position)
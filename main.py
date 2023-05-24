# Si vous n'avez pas le module pygame d'installé, il suffit d'ouvrir le windows powershell sur windows et de taper :
# 'Le chemin de votre python.exe' -m pip install pygame
# Si vous êtes sur Linux, ouvrez le terminal et faites la meme commande
# Images : Paul-André
# Code : Paul, Paul-André, Gabriel, Léopold
import random
import pygame
import sys
import os
from tkinter import *
from pygame import mixer


# Léopold
class PictureData:
    def __int__(self, imagetype, image, position, size, currentvisual):
        self.imagetype = imagetype
        self.image = image
        self.position = position
        self.size = size
        self.currentvisual = currentvisual

    def __contains__(self, point):
        size = self.size
        xRange = size[0]
        yRange = size[1]
        picture_position = self.position
        # Verification de la présence du point sur l'image
        return picture_position[0] <= point[0] <= picture_position[0] + xRange and picture_position[1] <= point[1] <= \
               picture_position[1] + yRange

    def __equals__(self, other):
        return other is not None and self.position == other.position


# Léopold, Gabriel
def place_images(pictures, screen):
    # On crée un
    # subScreenSize = (int(monitor_width / 10) * 9,int(monitor_height / 10) * 9)
    number_of_images = len(pictures) * 2
    images_positions, images_size = calculate_images_positions(pictures, number_of_images, subScreenSize, 3, 6)
    pictures_datas = []
    for i in range(len(pictures)):
        index1 = random.randint(0, len(images_positions) - 1)
        pos1 = images_positions[index1]
        images_positions.pop(index1)

        index2 = random.randint(0, len(images_positions) - 1)
        pos2 = images_positions[index2]
        images_positions.pop(index2)

        pygamepicture = pictures[i]

        place_new_picture(flipped_card_picture, pos1, i, pygamepicture, pictures_datas, images_size)
        place_new_picture(flipped_card_picture, pos2, i, pygamepicture, pictures_datas, images_size)
    return pictures_datas


# Paul
def place_new_picture(flipped_card_picture, pos, id, pygamepicture, pictures_datas, image_size):
    pictureData = PictureData()
    pictureData.image = pygamepicture
    pictureData.imagetype = id
    pictureData.position = pos
    pictureData.size = image_size
    pictureData.currentvisual = flipped_card_picture
    pictures_datas.append(pictureData)
    screen.blit(flipped_card_picture, pos)


# Gabriel
def calculate_images_positions(pictures, number_of_images, screenSize, colonnes, lignes):
    positions = []
    img_size = images_size
    ecart = 5
    xn=0
    yn=-ecart
    for x in range(lignes):
        for y in range(colonnes):
            positions.append(((x * img_size[0]) + screenOffsets[0]+xn, (y * img_size[1]) + screenOffsets[1]+yn))
            print(positions)
            yn+=ecart
        xn+=ecart
        yn=-ecart
    return positions, img_size

def setCardVisual(visual, card):
    screen.blit(visual, card.position)
    card.currentvisual = visual


def flipCards(cardsData, visual=None):
    for card in cardsData:
        if visual is None:
            visual = card.image
            setCardVisual(visual, card)
            visual = None
        else: setCardVisual(visual, card)

# Paul
def quitGame():
    pygame.quit()
    sys.exit()

#Variables utilitaires
lignes = 3
colonnes = 6
transparent = (0, 0, 0, 0)
root = Tk()
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()


# On met le jeu en grand écran en l'adaptant en fonction de la taille de l'ecran
pygame.init()
screen = pygame.display.set_mode(
    (monitor_width, monitor_height),
    pygame.FULLSCREEN
)
files = [x for x in os.listdir()]

flipped_card_picture = pygame.image.load(os.path.abspath("Images/back_image.png"))
flipped_card_picture_selected = pygame.image.load(os.path.abspath("Images/back_image_selected.png"))
background = pygame.image.load(os.path.abspath("Images/fond.jpg"))

picture_paths = [os.path.abspath("Images/image" + str(x) + ".png") for x in range(1, 10)]

pictures = [pygame.image.load(picture_path) for picture_path in picture_paths]

screen.fill((10, 100, 10))

subScreenSize = ((monitor_width // 10) * 9, (monitor_height // 10) * 9)
screenOffsets = ((monitor_width - subScreenSize[0]) // 2, (monitor_height - subScreenSize[1]) // 2)

images_size = (subScreenSize[0] // colonnes, subScreenSize[1] // lignes)
pictures = [pygame.transform.scale(picture, images_size) for picture in pictures]
flipped_card_picture = pygame.transform.scale(flipped_card_picture, images_size)
flipped_card_picture_selected = pygame.transform.scale(flipped_card_picture_selected, images_size)
background = pygame.transform.scale(background, (monitor_width,monitor_height))


screen.blit(background, (0,0))
# on place les images
picturesData = place_images(pictures, screen)

pygame.display.flip()

currentImageData = None
while True:
    if len(picturesData) == 0:continue
    screen.blit(background, (0, 0))
    for picture in picturesData:
        setCardVisual(picture.currentvisual, picture)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quitGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1: continue
            mouse_pos = event.pos
            for data in picturesData:
                if data.__contains__(mouse_pos):
                    if data.__equals__(currentImageData):
                        setCardVisual(flipped_card_picture, data)
                        currentImageData = None
                    else:
                        if currentImageData is None:
                            currentImageData = data
                            setCardVisual(flipped_card_picture_selected, data)
                        else:
                            flipCards([data, currentImageData])
                            pygame.display.flip()
                            if data.imagetype == currentImageData.imagetype:
                                picturesData.remove(data)
                                picturesData.remove(currentImageData)
                                mixer.music.load("Music/AsianRiff.mp3")
                                mixer.music.play()
                                pygame.time.wait(2850)
                            else:
                                flipCards([data, currentImageData], flipped_card_picture)
                                pygame.time.wait(1000)
                            currentImageData = None
    pygame.display.flip()
pygame.quit()

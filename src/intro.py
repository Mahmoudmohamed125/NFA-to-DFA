import pygame
import math
import time
import re
import sys
import subprocess
FPS = 40

pygame.init()
icon = pygame.image.load("project_logo.png")  # Make sure the path is correct
pygame.display.set_icon(icon)
pygame.display.set_caption("NFA to DFA simulator")
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.smoothscale(bg, (600, 700))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 700))
exit = True
font_path = "pixel.TTF"
font_size = 21
font_object = pygame.font.Font(font_path, font_size)
font_header = pygame.font.Font(font_path, 50)

project_logo = pygame.image.load('project_logo.png')
project_logo = pygame.transform.scale(project_logo, (230, 220))


# Path to background music
background_music = 'Untitled video - Made with Clipchamp.mp3'

# Play background music in a loop
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loop indefinitely (-1)


def draw_text_with_stroke(text, font, position, stroke_color=(0, 0, 0), text_color=(255, 255, 255)):
	stroke_offset = 2

	global stroke_ctr
	for dx in [-stroke_offset, stroke_offset]:
		for dy in [-stroke_offset, stroke_offset]:

			stroke_surface = font.render(text, True, stroke_color)
			screen.blit(stroke_surface, (position[0] + dx, position[1] + dy))

	text_surface = font.render(text, True, text_color)
	screen.blit(text_surface, position)


decrement = +1
name1y = 1000
name2y = 1050
name3y = 1100
name4y = 1150
headery = 700
logoy = 1300
while exit:
	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			exit = False
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			pygame.quit()
			subprocess.run([sys.executable, "GUI.py"])

			exit = False

	screen.blit(bg, (0, 0))
	draw_text_with_stroke("NFA to DFA", font_header, (70, headery))
	draw_text_with_stroke("Samer ELhossany 221001697",
						  font_object, (70, name1y))
	draw_text_with_stroke("Mahmoud Abdelglil 221001313",
						  font_object, (70, name2y))
	draw_text_with_stroke("Abdelrahman Rahal 221001443",
						  font_object, (70, name3y))
	draw_text_with_stroke("Nour Elsharkawy 221001458",
						  font_object, (70, name4y))
	screen.blit(project_logo, (170, logoy))
	name1y -= decrement
	name2y -= decrement
	name3y -= decrement
	name4y -= decrement
	headery -= decrement
	logoy -= decrement
	if logoy < 100:
		decrement = 0
		draw_text_with_stroke("Press any key to continue",
							  font_object, (70, 500))
	clock.tick(FPS)

	pygame.display.update()

pygame.quit()

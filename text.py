import pygame
from pygame import math

pygame.init()


v1 = math.Vector2(5, 7)
v2 = math.Vector2(5, 17)
print(v1.distance_to(v2))
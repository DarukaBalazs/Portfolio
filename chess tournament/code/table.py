import pygame as pg

pg.init()

class Table:
    def __init__(self,surface):
        self.surface = surface
        self.active = False
        self.free = True
        self.counted = False
        self.currentplayers = []
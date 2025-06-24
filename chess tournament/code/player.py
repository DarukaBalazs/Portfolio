import pygame as pg

class Player:
    def __init__(self,name,id):
        self.name = name
        self.id = int(id)
        self.point = 0
        self.black = 0
        self.played_with = []
        self.currentcolor = 0
        self.free = True
    def __str__(self):
        return f"name: {self.name}, id: {self.id} point :{self.point} played with:{self.played_with}"
import time
from flask import Flask
from flask import request, jsonify
import base64
import io
import torch
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)

class cube:
    def __init__(self):
        self.top = ["y", "y", "y", "y", "y", "y", "y", "y", "y"]
        self.bottom = ["w", "w", "w", "w", "w", "w", "w", "w", "w"]
        self.back = ["b", "b", "b", "b", "b", "b", "b", "b", "b"]
        self.front = ["g", "g", "g", "g", "g", "g", "g", "g", "g"]
        self.left = ["r", "r", "r", "r", "r", "r", "r", "r", "r"]
        self.right = ["o", "o", "o", "o", "o", "o", "o", "o", "o"]
        self.c = [self.top, self.bottom, self.left, self.right, self.front, self.back]
        self.cross=[]
        self.first=[]
        self.ftl=[]
        self.oll=[]
        self.pll=[]
        self.scramble=[]
        self.auf=[]

    def setState(self, top, bottom, back, front, left, right):
        self.top = top
        self.bottom = bottom
        self.back = back
        self.front = front
        self.left = left
        self.right = right
        self.c = [self.top, self.bottom, self.left, self.right, self.front, self.back]
    def gettop(self):
        top=1
        return self.top 
        #returns the arraylist instead of 1 because top is a local variable inside the method whereas self.top returns the global variable inside the class
    
    def u(self, stage):
        top=self.c[0]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_top = [top[6], top[3], top[0], top[7], top[4], top[1], top[8], top[5], top[2]]
        new_front = [right[0], right[1], right[2], front[3], front[4], front[5], front[6], front[7], front[8]]
        new_right = [back[0], back[1], back[2], right[3], right[4], right[5], right[6], right[7], right[8]]
        new_back = [left[0], left[1], left[2], back[3], back[4], back[5], back[6], back[7], back[8]]
        new_left = [front[0], front[1], front[2], left[3], left[4], left[5],left[6], left[7], left[8]]
        self.c[0]=new_top
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("U ")
        elif stage == "first":
            self.first.append("U ")
        elif stage == "ftl":
            self.ftl.append("U ")
        elif stage == "oll":
            self.oll.append("U ")
        elif stage == "pll":
            self.pll.append("U ")
        elif stage == "auf":
            self.auf.append("U ")
        elif stage == "scramble":
            self.scramble.append("U ")
    def ui(self, stage):
        top=self.c[0]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_top = [top[2], top[5], top[8], top[1], top[4], top[7], top[0], top[3], top[6]]
        new_front = [left[0], left[1], left[2], front[3], front[4], front[5], front[6], front[7], front[8]]
        new_right = [front[0], front[1], front[2], right[3], right[4], right[5], right[6], right[7], right[8]]
        new_back = [right[0], right[1], right[2], back[3], back[4], back[5], back[6], back[7], back[8]]
        new_left = [back[0], back[1], back[2], left[3], left[4], left[5],left[6], left[7], left[8]]
        self.c[0]=new_top
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("U' ")
        elif stage == "first":
            self.first.append("U' ")
        elif stage == "ftl":
            self.ftl.append("U' ")
        elif stage == "oll":
            self.oll.append("U' ")
        elif stage == "pll":
            self.pll.append("U' ")
        elif stage == "auf":
            self.auf.append("U' ")
        elif stage == "scramble":
            self.scramble.append("U' ")
    def r(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_top = [top[0], top[1], front[2], top[3], top[4], front[5], top[6], top[7], front[8]]
        new_front = [front[0], front[1], bottom[2], front[3], front[4], bottom[5], front[6], front[7], bottom[8]]
        new_right = [right[6], right[3], right[0], right[7], right[4], right[1], right[8], right[5], right[2]]
        new_back = [top[8], back[1], back[2], top[5], back[4], back[5], top[2], back[7], back[8]]
        new_bottom = [bottom[0], bottom[1], back[6], bottom[3], bottom[4], back[3],bottom[6], bottom[7], back[0]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("R ")
        elif stage == "first":
            self.first.append("R ")
        elif stage == "ftl":
            self.ftl.append("R ")
        elif stage == "oll":
            self.oll.append("R ")
        elif stage == "pll":
            self.pll.append("R ")
        elif stage == "scramble":
            self.scramble.append("R ")
    def ri(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_top = [top[0], top[1], back[6], top[3], top[4], back[3], top[6], top[7], back[0]]
        new_front = [front[0], front[1], top[2], front[3], front[4], top[5], front[6], front[7], top[8]]
        new_right = [right[2], right[5], right[8], right[1], right[4], right[7], right[0], right[3], right[6]]
        new_back = [bottom[8], back[1], back[2], bottom[5], back[4], back[5], bottom[2], back[7], back[8]]
        new_bottom = [bottom[0], bottom[1], front[2], bottom[3], bottom[4], front[5],bottom[6], bottom[7], front[8]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("R' ")
        elif stage == "first":
            self.first.append("R' ")
        elif stage == "ftl":
            self.ftl.append("R' ")
        elif stage == "oll":
            self.oll.append("R' ")
        elif stage == "pll":
            self.pll.append("R' ")
        elif stage == "scramble":
            self.scramble.append("R' ")
    def f(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        new_top = [top[0], top[1], top[2], top[3], top[4], top[5], left[8], left[5], left[2]]
        new_front = [front[6], front[3], front[0], front[7], front[4], front[1], front[8], front[5], front[2]]
        new_right = [top[6], right[1], right[2], top[7], right[4], right[5], top[8], right[7], right[8]]
        new_left = [left[0], left[1], bottom[0], left[3], left[4], bottom[1], left[6], left[7], bottom[2]]
        new_bottom = [right[6], right[3], right[0], bottom[3], bottom[4], bottom[5], bottom[6], bottom[7], bottom[8]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        if stage == "cross":
            self.cross.append("F ")
        elif stage == "first":
            self.first.append("F ")
        elif stage == "ftl":
            self.ftl.append("F ")
        elif stage == "oll":
            self.oll.append("F ")
        elif stage == "pll":
            self.pll.append("F ")
        elif stage == "scramble":
            self.scramble.append("F ") 
    def fi(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        new_top = [top[0], top[1], top[2], top[3], top[4], top[5], right[0], right[3], right[6]]
        new_front = [front[2], front[5], front[8], front[1], front[4], front[7], front[0], front[3], front[6]]
        new_right = [bottom[2], right[1], right[2], bottom[1], right[4], right[5], bottom[0], right[7], right[8]]
        new_left = [left[0], left[1], top[8], left[3], left[4], top[7], left[6], left[7], top[6]]
        new_bottom = [left[2], left[5], left[8], bottom[3], bottom[4], bottom[5], bottom[6], bottom[7], bottom[8]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        if stage == "cross":
            self.cross.append("F' ")
        elif stage == "first":
            self.first.append("F' ")
        elif stage == "ftl":
            self.ftl.append("F' ")
        elif stage == "oll":
            self.oll.append("F' ")
        elif stage == "pll":
            self.pll.append("F' ")
        elif stage == "scramble":
            self.scramble.append("F' ") 
    def d(self, stage):
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_back = [back[0], back[1], back[2], back[3], back[4], back[5], right[6], right[7], right[8]]
        new_front = [front[0], front[1], front[2], front[3], front[4], front[5], left[6], left[7], left[8]]
        new_right = [right[0], right[1], right[2], right[3], right[4], right[5], front[6], front[7], front[8]]
        new_left = [left[0], left[1], left[2], left[3], left[4], left[5], back[6], back[7], back[8]]
        new_bottom = [bottom[6], bottom[3], bottom[0], bottom[7], bottom[4], bottom[1], bottom[8], bottom[5], bottom[2]]
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("D ")
        elif stage == "first":
            self.first.append("D ")
        elif stage == "ftl":
            self.ftl.append("D ")
        elif stage == "oll":
            self.oll.append("D ")
        elif stage == "pll":
            self.pll.append("D ")
        elif stage == "scramble":
            self.scramble.append("D ") 
    def di(self, stage):
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_back = [back[0], back[1], back[2], back[3], back[4], back[5], left[6], left[7], left[8]]
        new_front = [front[0], front[1], front[2], front[3], front[4], front[5], right[6], right[7], right[8]]
        new_right = [right[0], right[1], right[2], right[3], right[4], right[5], back[6], back[7], back[8]]
        new_left = [left[0], left[1], left[2], left[3], left[4], left[5], front[6], front[7], front[8]]
        new_bottom = [bottom[2], bottom[5], bottom[8], bottom[1], bottom[4], bottom[7], bottom[0], bottom[3], bottom[6]]
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("D' ")
        elif stage == "first":
            self.first.append("D' ")
        elif stage == "ftl":
            self.ftl.append("D' ")
        elif stage == "oll":
            self.oll.append("D' ")
        elif stage == "pll":
            self.pll.append("D' ")
        elif stage == "scramble":
            self.scramble.append("D' ") 
    def l(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        front=self.c[4]
        back=self.c[5]
        new_back = [back[0], back[1], bottom[6], back[3], back[4], bottom[3], back[6], back[7], bottom[0]]
        new_front = [top[0], front[1], front[2], top[3], front[4], front[5], top[6], front[7], front[8]]
        new_top = [back[8], top[1], top[2], back[5], top[4], top[5], back[2], top[7], top[8]]
        new_left = [left[6], left[3], left[0], left[7], left[4], left[1], left[8], left[5], left[2]]
        new_bottom = [front[0], bottom[1], bottom[2], front[3], bottom[4], bottom[5], front[6], bottom[7], bottom[8]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("L ")
        elif stage == "first":
            self.first.append("L ")
        elif stage == "ftl":
            self.ftl.append("L ")
        elif stage == "oll":
            self.oll.append("L ")
        elif stage == "pll":
            self.pll.append("L ")
        elif stage == "scramble":
            self.scramble.append("L ") 
    def li(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        front=self.c[4]
        back=self.c[5]
        new_back = [back[0], back[1], top[6], back[3], back[4], top[3], back[6], back[7], top[0]]
        new_front = [bottom[0], front[1], front[2], bottom[3], front[4], front[5], bottom[6], front[7], front[8]]
        new_top = [front[0], top[1], top[2], front[3], top[4], top[5], front[6], top[7], top[8]]
        new_left = [left[2], left[5], left[8], left[1], left[4], left[7], left[0], left[3], left[6]]
        new_bottom = [back[8], bottom[1], bottom[2], back[5], bottom[4], bottom[5], back[2], bottom[7], bottom[8]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[4]=new_front
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("L' ")
        elif stage == "first":
            self.first.append("L' ")
        elif stage == "ftl":
            self.ftl.append("L' ")
        elif stage == "oll":
            self.oll.append("L' ")
        elif stage == "pll":
            self.pll.append("L' ")
        elif stage == "scramble":
            self.scramble.append("L' ") 
    def b(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        back=self.c[5]
        new_back = [back[6], back[3], back[0], back[7], back[4], back[1], back[8], back[5], back[2]]
        new_right = [right[0], right[1], bottom[8], right[3], right[4], bottom[7], right[6], right[7], bottom[6]]
        new_top = [right[2], right[5], right[8], top[3], top[4], top[5], top[6], top[7], top[8]]
        new_left = [top[2], left[1], left[2], top[1], left[4], left[5], top[0], left[7], left[8]]
        new_bottom = [bottom[0], bottom[1], bottom[2], bottom[3], bottom[4], bottom[5], left[0], left[3], left[6]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("B ")
        elif stage == "first":
            self.first.append("B ")
        elif stage == "ftl":
            self.ftl.append("B ")
        elif stage == "oll":
            self.oll.append("B ")
        elif stage == "pll":
            self.pll.append("B ")
        elif stage == "scramble":
            self.scramble.append("B ") 
    def bi(self, stage):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        back=self.c[5]
        new_back = [back[2], back[5], back[8], back[1], back[4], back[7], back[0], back[3], back[6]]
        new_right = [right[0], right[1], top[0], right[3], right[4], top[1], right[6], right[7], top[2]]
        new_top = [left[6], left[3], left[0], top[3], top[4], top[5], top[6], top[7], top[8]]
        new_left = [bottom[6], left[1], left[2], bottom[7], left[4], left[5], bottom[8], left[7], left[8]]
        new_bottom = [bottom[0], bottom[1], bottom[2], bottom[3], bottom[4], bottom[5], right[8], right[5], right[2]]
        self.c[0]=new_top
        self.c[1]=new_bottom
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[5]=new_back
        if stage == "cross":
            self.cross.append("B' ")
        elif stage == "first":
            self.first.append("B' ")
        elif stage == "ftl":
            self.ftl.append("B' ")
        elif stage == "oll":
            self.oll.append("B' ")
        elif stage == "pll":
            self.pll.append("B' ")
        elif stage == "scramble":
            self.scramble.append("B' ")
    def remove(self, l1, l2):
        length = len(l1)
        for i in range(len(l2) - length + 1):
            if l2[i:i+length] == l1:
                l2[i:i+length] = []
        return l2
    def rep(self, l1, l2, l3):
        length = len(l1)
        i = 0
        while i < len(l3):
            if l3[i:i+length] == l1:
                l3[i:i+length] = l2
                i += len(l2)
            else:
                i += 1
    def replace(self, stage):
        if stage == 'cross':
           self.rep(["U ", "U ", "U "], ["U' "], self.cross) 
           self.rep(["U' ", "U' ", "U' "], ["U "], self.cross)
           self.rep(["L' ", "L' ", "L' "], ["L "], self.cross) 
           self.rep(["L ", "L ", "L "], ["L' "], self.cross) 
           self.rep(["R' ", "R' ", "R' "], ["R "], self.cross) 
           self.rep(["R ", "R ", "R "], ["R' "], self.cross) 
           self.rep(["B' ", "B' ", "B' "], ["B "], self.cross) 
           self.rep(["B ", "B ", "B "], ["B' "], self.cross) 
           self.rep(["F' ", "F' ", "F' "], ["F "], self.cross) 
           self.rep(["F ", "F ", "F "], ["F' "], self.cross) 
           self.rep(["D ", "D ", "D "], ["D' "], self.cross) 
           self.rep(["D' ", "D' ", "D' "], ["D "], self.cross) 
           self.rep(["U ", "U "], ["U2 "], self.cross) 
           self.rep(["U' ", "U' "], ["U2 "], self.cross)
           self.rep(["L' ", "L' "], ["L2 "], self.cross) 
           self.rep(["L ", "L "], ["L2 "], self.cross) 
           self.rep(["R' ", "R' "], ["R2 "], self.cross) 
           self.rep(["R ", "R "], ["R2 "], self.cross) 
           self.rep(["B' ", "B' "], ["B2 "], self.cross) 
           self.rep(["B ", "B "], ["B2 "], self.cross) 
           self.rep(["F' ", "F' "], ["F2 "], self.cross) 
           self.rep(["F ", "F "], ["F2 "], self.cross) 
           self.rep(["D ", "D "], ["D2 "], self.cross) 
           self.rep(["D' ", "D' "], ["D2 "], self.cross) 
        elif stage == 'first':
           self.rep(["U ", "U ", "U "], ["U' "], self.first) 
           self.rep(["U' ", "U' ", "U' "], ["U "], self.first)
           self.rep(["L' ", "L' ", "L' "], ["L "], self.first) 
           self.rep(["L ", "L ", "L "], ["L' "], self.first) 
           self.rep(["R' ", "R' ", "R' "], ["R "], self.first) 
           self.rep(["R ", "R ", "R "], ["R' "], self.first) 
           self.rep(["B' ", "B' ", "B' "], ["B "], self.first) 
           self.rep(["B ", "B ", "B "], ["B' "], self.first) 
           self.rep(["F' ", "F' ", "F' "], ["F "], self.first) 
           self.rep(["F ", "F ", "F "], ["F' "], self.first) 
           self.rep(["D ", "D ", "D "], ["D' "], self.first) 
           self.rep(["D' ", "D' ", "D' "], ["D "], self.first) 
           self.rep(["U ", "U "], ["U2 "], self.first) 
           self.rep(["U' ", "U' "], ["U2 "], self.first)
           self.rep(["L' ", "L' "], ["L2 "], self.first) 
           self.rep(["L ", "L "], ["L2 "], self.first) 
           self.rep(["R' ", "R' "], ["R2 "], self.first) 
           self.rep(["R ", "R "], ["R2 "], self.first) 
           self.rep(["B' ", "B' "], ["B2 "], self.first) 
           self.rep(["B ", "B "], ["B2 "], self.first) 
           self.rep(["F' ", "F' "], ["F2 "], self.first) 
           self.rep(["F ", "F "], ["F2 "], self.first) 
           self.rep(["D ", "D "], ["D2 "], self.first) 
           self.rep(["D' ", "D' "], ["D2 "], self.first) 
        elif stage == 'ftl':
           self.rep(["U ", "U ", "U "], ["U' "], self.ftl) 
           self.rep(["U' ", "U' ", "U' "], ["U "], self.ftl)
           self.rep(["L' ", "L' ", "L' "], ["L "], self.ftl) 
           self.rep(["L ", "L ", "L "], ["L' "], self.ftl) 
           self.rep(["R' ", "R' ", "R' "], ["R "], self.ftl) 
           self.rep(["R ", "R ", "R "], ["R' "], self.ftl) 
           self.rep(["B' ", "B' ", "B' "], ["B "], self.ftl) 
           self.rep(["B ", "B ", "B "], ["B' "], self.ftl) 
           self.rep(["F' ", "F' ", "F' "], ["F "], self.ftl) 
           self.rep(["F ", "F ", "F "], ["F' "], self.ftl) 
           self.rep(["D ", "D ", "D "], ["D' "], self.ftl) 
           self.rep(["D' ", "D' ", "D' "], ["D "], self.ftl) 
           self.rep(["U ", "U "], ["U2 "], self.ftl) 
           self.rep(["U' ", "U' "], ["U2 "], self.ftl)
           self.rep(["L' ", "L' "], ["L2 "], self.ftl) 
           self.rep(["L ", "L "], ["L2 "], self.ftl) 
           self.rep(["R' ", "R' "], ["R2 "], self.ftl) 
           self.rep(["R ", "R "], ["R2 "], self.ftl) 
           self.rep(["B' ", "B' "], ["B2 "], self.ftl) 
           self.rep(["B ", "B "], ["B2 "], self.ftl) 
           self.rep(["F' ", "F' "], ["F2 "], self.ftl) 
           self.rep(["F ", "F "], ["F2 "], self.ftl) 
           self.rep(["D ", "D "], ["D2 "], self.ftl) 
           self.rep(["D' ", "D' "], ["D2 "], self.ftl) 
        elif stage == 'oll':
           self.rep(["U ", "U ", "U "], ["U' "], self.oll) 
           self.rep(["U' ", "U' ", "U' "], ["U "], self.oll)
           self.rep(["L' ", "L' ", "L' "], ["L "], self.oll) 
           self.rep(["L ", "L ", "L "], ["L' "], self.oll) 
           self.rep(["R' ", "R' ", "R' "], ["R "], self.oll) 
           self.rep(["R ", "R ", "R "], ["R' "], self.oll) 
           self.rep(["B' ", "B' ", "B' "], ["B "], self.oll) 
           self.rep(["B ", "B ", "B "], ["B' "], self.oll) 
           self.rep(["F' ", "F' ", "F' "], ["F "], self.oll) 
           self.rep(["F ", "F ", "F "], ["F' "], self.oll) 
           self.rep(["D ", "D ", "D "], ["D' "], self.oll) 
           self.rep(["D' ", "D' ", "D' "], ["D "], self.oll) 
           self.rep(["U ", "U "], ["U2 "], self.oll) 
           self.rep(["U' ", "U' "], ["U2 "], self.oll)
           self.rep(["L' ", "L' "], ["L2 "], self.oll) 
           self.rep(["L ", "L "], ["L2 "], self.oll) 
           self.rep(["R' ", "R' "], ["R2 "], self.oll) 
           self.rep(["R ", "R "], ["R2 "], self.oll) 
           self.rep(["B' ", "B' "], ["B2 "], self.oll) 
           self.rep(["B ", "B "], ["B2 "], self.oll) 
           self.rep(["F' ", "F' "], ["F2 "], self.oll) 
           self.rep(["F ", "F "], ["F2 "], self.oll) 
           self.rep(["D ", "D "], ["D2 "], self.oll) 
           self.rep(["D' ", "D' "], ["D2 "], self.oll) 
        elif stage == 'pll':
           self.rep(["U ", "U ", "U "], ["U' "], self.pll) 
           self.rep(["U' ", "U' ", "U' "], ["U "], self.pll)
           self.rep(["L' ", "L' ", "L' "], ["L "], self.pll) 
           self.rep(["L ", "L ", "L "], ["L' "], self.pll) 
           self.rep(["R' ", "R' ", "R' "], ["R "], self.pll) 
           self.rep(["R ", "R ", "R "], ["R' "], self.pll) 
           self.rep(["B' ", "B' ", "B' "], ["B "], self.pll) 
           self.rep(["B ", "B ", "B "], ["B' "], self.pll) 
           self.rep(["F' ", "F' ", "F' "], ["F "], self.pll) 
           self.rep(["F ", "F ", "F "], ["F' "], self.pll) 
           self.rep(["D ", "D ", "D "], ["D' "], self.pll) 
           self.rep(["D' ", "D' ", "D' "], ["D "], self.pll) 
           self.rep(["U ", "U "], ["U2 "], self.pll) 
           self.rep(["U' ", "U' "], ["U2 "], self.pll)
           self.rep(["L' ", "L' "], ["L2 "], self.pll) 
           self.rep(["L ", "L "], ["L2 "], self.pll) 
           self.rep(["R' ", "R' "], ["R2 "], self.pll) 
           self.rep(["R ", "R "], ["R2 "], self.pll) 
           self.rep(["B' ", "B' "], ["B2 "], self.pll) 
           self.rep(["B ", "B "], ["B2 "], self.pll) 
           self.rep(["F' ", "F' "], ["F2 "], self.pll) 
           self.rep(["F ", "F "], ["F2 "], self.pll) 
           self.rep(["D ", "D "], ["D2 "], self.pll) 
           self.rep(["D' ", "D' "], ["D2 "], self.pll) 
    def simplify(self, stage):
        if stage == 'cross':
            self.remove(["U' ", "U "], self.cross)
            self.remove(["U ", "U' "], self.cross)
            self.remove(["L ", "L' "], self.cross)
            self.remove(["L' ", "L "], self.cross)
            self.remove(["R ", "R' "], self.cross)
            self.remove(["R' ", "R "], self.cross)
            self.remove(["B ", "B' "], self.cross)
            self.remove(["B' ", "B "], self.cross)
            self.remove(["F ", "F' "], self.cross)
            self.remove(["F' ", "F "], self.cross)
            self.remove(["D ", "D' "], self.cross)
            self.remove(["D' ", "D "], self.cross)
        elif stage == 'first':
            self.remove(["U' ", "U "], self.first)
            self.remove(["U ", "U' "], self.first)
            self.remove(["L ", "L' "], self.first)
            self.remove(["L' ", "L "], self.first)
            self.remove(["R ", "R' "], self.first)
            self.remove(["R' ", "R "], self.first)
            self.remove(["B ", "B' "], self.first)
            self.remove(["B' ", "B "], self.first)
            self.remove(["F ", "F' "], self.first)
            self.remove(["F' ", "F "], self.first)
            self.remove(["D ", "D' "], self.first)
            self.remove(["D' ", "D "], self.first)
        elif stage == 'ftl':
            self.remove(["U' ", "U "], self.ftl)
            self.remove(["U ", "U' "], self.ftl)
            self.remove(["L ", "L' "], self.ftl)
            self.remove(["L' ", "L "], self.ftl)
            self.remove(["R ", "R' "], self.ftl)
            self.remove(["R' ", "R "], self.ftl)
            self.remove(["B ", "B' "], self.ftl)
            self.remove(["B' ", "B "], self.ftl)
            self.remove(["F ", "F' "], self.ftl)
            self.remove(["F' ", "F "], self.ftl)
            self.remove(["D ", "D' "], self.ftl)
            self.remove(["D' ", "D "], self.ftl)
        elif stage == 'oll':
            self.remove(["U' ", "U "], self.oll)
            self.remove(["U ", "U' "], self.oll)
            self.remove(["L ", "L' "], self.oll)
            self.remove(["L' ", "L "], self.oll)
            self.remove(["R ", "R' "], self.oll)
            self.remove(["R' ", "R "], self.oll)
            self.remove(["B ", "B' "], self.oll)
            self.remove(["B' ", "B "], self.oll)
            self.remove(["F ", "F' "], self.oll)
            self.remove(["F' ", "F "], self.oll)
            self.remove(["D ", "D' "], self.oll)
            self.remove(["D' ", "D "], self.oll)
        elif stage == 'pll':
            self.remove(["U' ", "U "], self.pll)
            self.remove(["U ", "U' "], self.pll)
            self.remove(["L ", "L' "], self.pll)
            self.remove(["L' ", "L "], self.pll)
            self.remove(["R ", "R' "], self.pll)
            self.remove(["R' ", "R "], self.pll)
            self.remove(["B ", "B' "], self.pll)
            self.remove(["B' ", "B "], self.pll)
            self.remove(["F ", "F' "], self.pll)
            self.remove(["F' ", "F "], self.pll)
            self.remove(["D ", "D' "], self.pll)
            self.remove(["D' ", "D "], self.pll)
            

    def sxym(self, stage):
        self.r(stage)
        self.u(stage)
        self.ri(stage)
        self.ui(stage)
    def rsxym(self, stage):
        self.u(stage)
        self.r(stage)
        self.ui(stage)
        self.ri(stage)
    def lsxym(self, stage):
        self.li(stage)
        self.ui(stage)
        self.l(stage)
        self.u(stage)
    def rlsxym(self, stage):
        self.ui(stage)
        self.li(stage)
        self.u(stage)
        self.l(stage)
    def bsxym(self, stage):
        self.l(stage)
        self.u(stage)
        self.li(stage)
        self.ui(stage)
    def rbsxym(self, stage):
        self.u(stage)
        self.l(stage)
        self.ui(stage)
        self.li(stage)
    def blsxym(self, stage):
        self.ri(stage)
        self.ui(stage)
        self.r(stage)
        self.u(stage)
    def rblsxym(self, stage):
        self.ui(stage)
        self.ri(stage)
        self.u(stage)
        self.r(stage)
    def sune(self, stage):
        self.r(stage)
        self.u(stage)
        self.ri(stage)
        self.u(stage)
        self.r(stage)
        self.u(stage)
        self.u(stage)
        self.ri(stage)
    def antisune(self, stage):
        self.r(stage)
        self.u(stage)
        self.u(stage)
        self.ri(stage)
        self.ui(stage)
        self.r(stage)
        self.ui(stage)
        self.ri(stage)
    def tperm(self):
        self.sxym('pll')
        self.ri('pll')
        self.f('pll')
        self.r('pll')
        self.r('pll')
        self.ui('pll')
        self.ri('pll')
        self.ui('pll')
        self.r('pll')
        self.u('pll')
        self.ri('pll')
        self.fi('pll')
    def jperm(self):
        self.r('pll')
        self.u('pll')
        self.ri('pll')
        self.fi('pll')
        self.sxym('pll')
        self.ri('pll')
        self.f('pll')
        self.r('pll')
        self.r('pll')
        self.ui('pll')
        self.ri('pll')
        self.ui('pll')
    def uaperm(self):
        self.r('pll')
        self.ui('pll')
        self.r('pll')
        self.u('pll')
        self.r('pll')
        self.u('pll')
        self.r('pll')
        self.ui('pll')
        self.ri('pll')
        self.ui('pll')
        self.r('pll')
        self.r('pll')
    def ubperm(self):
        self.r('pll')
        self.r('pll')
        self.u('pll')
        self.r('pll')
        self.u('pll')
        self.ri('pll')
        self.ui('pll')
        self.ri('pll')
        self.ui('pll')
        self.ri('pll')
        self.u('pll')
        self.ri('pll')
    def zperm(self):
        self.u('pll')
        self.ri('pll')
        self.ui('pll')
        self.r('pll')
        self.ui('pll')
        self.r('pll')
        self.u('pll')
        self.r('pll')
        self.ui('pll')
        self.ri('pll')
        self.u('pll')
        self.r('pll')
        self.u('pll')
        self.r('pll')
        self.r('pll')
        self.ui('pll')
        self.ri('pll')
        self.u('pll')
    def hperm(self):
        self.r('pll')
        self.r('pll')
        self.u('pll')
        self.u('pll')
        self.r('pll')
        self.r('pll')
        self.u('pll')
        self.u('pll')
        self.r('pll')
        self.r('pll')
        self.u('pll')
        self.r('pll')
        self.r('pll')
        self.u('pll')
        self.u('pll')
        self.r('pll')
        self.r('pll')
        self.u('pll')
        self.u('pll')
        self.r('pll')
        self.r('pll')
        self.ui('pll')
    def yperm(self):
        self.f('pll')
        self.r('pll')
        self.ui('pll')
        self.ri('pll')
        self.ui('pll')
        self.r('pll')
        self.u('pll')
        self.ri('pll')
        self.fi('pll')
        self.sxym('pll')
        self.ri('pll')
        self.f('pll')
        self.r('pll')
        self.fi('pll')
    def nbperm(self):
        self.ri('pll')
        self.u('pll')
        self.li('pll')
        self.u('pll')
        self.u('pll')
        self.r('pll')
        self.ui('pll')
        self.l('pll')
        self.ri('pll')
        self.u('pll')
        self.li('pll')
        self.u('pll')
        self.u('pll')
        self.r('pll')
        self.ui('pll')
        self.l('pll')
        self.ui('pll')
    def findEdges(self, c1, c2):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        if top[1] == c1 and back[1] == c2:
            return [top[4],back[4]]
        elif top[3] == c1 and left[1] == c2:
            return [top[4],left[4]]
        elif top[5] == c1 and right[1] == c2:
            return [top[4],right[4]]
        elif top[7] == c1 and front[1] == c2:
            return [top[4],front[4]]
        elif front[1] == c1 and top[7] == c2:
            return [front[4],top[4]]
        elif front[3] == c1 and left[5] == c2:
            return [front[4],left[4]]
        elif front[5] == c1 and right[3] == c2:
            return [front[4],right[4]]
        elif front[7] == c1 and bottom[1] == c2:
            return [front[4],bottom[4]]
        elif bottom[1] == c1 and front[7] == c2:
            return [bottom[4],front[4]]
        elif bottom[3] == c1 and left[7] == c2:
            return [bottom[4],left[4]]
        elif bottom[5] == c1 and right[7] == c2:
            return [bottom[4],right[4]]
        elif bottom[7] == c1 and back[7] == c2:
            return [bottom[4],back[4]]
        elif left[1] == c1 and top[3] == c2:
            return [left[4],top[4]]
        elif left[3] == c1 and back[5] == c2:
            return [left[4],back[4]]
        elif left[5] == c1 and front[3] == c2:
            return [left[4],front[4]]
        elif left[7] == c1 and bottom[3] == c2:
            return [left[4],bottom[4]]
        elif right[1] == c1 and top[5] == c2:
            return [right[4],top[4]]
        elif right[3] == c1 and front[5] == c2:
            return [right[4], front[4]]
        elif right[5] == c1 and back[3] == c2:
            return [right[4],back[4]]
        elif right[7] == c1 and bottom[5] == c2:
            return [right[4],bottom[4]]
        elif back[1] == c1 and top[1] == c2:
            return [back[4],top[4]]
        elif back[3] == c1 and right[5] == c2:
            return [back[4], right[4]]
        elif back[5] == c1 and left[3] == c2:
            return [back[4],left[4]]
        elif back[7] == c1 and bottom[7] == c2:
            return [back[4],bottom[4]]
    def findCorners(self, c1, c2, c3):
        top=self.c[0]
        bottom=self.c[1]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        if top[0] == c1 and back[2] == c2 and left[0] == c3:
            return [top[4],back[4], left[4]]
        elif top[2] == c1 and right[2] == c2 and back[0] == c3:
            return [top[4], right[4], back[4]]
        elif top[6] == c1 and left[2] == c2 and front[0] == c3:
            return [top[4], left[4], front[4]]
        elif top[8] == c1 and front[2] == c2 and right[0] == c3:
            return [top[4], front[4], right[4]]
        elif front[0] == c1 and top[6] == c2 and left[2] == c3:
            return [front[4],top[4], left[4]]
        elif front[2] == c1 and right[0] == c2 and top[8] == c3:
            return [front[4], right[4], top[4]]
        elif front[6] == c1 and left[8] == c2 and bottom[0] == c3:
            return [front[4], left[4], bottom[4]]
        elif front[8] == c1 and bottom[2] == c2 and right[6] == c3:
            return [front[4], bottom[4], right[4]]
        elif bottom[0] == c1 and front[6] == c2 and left[8] == c3:
            return [bottom[4],front[4], left[4]]
        elif bottom[2] == c1 and right[6] == c2 and front[8] == c3:
            return [bottom[4], right[4], front[4]]
        elif bottom[6] == c1 and left[6] == c2 and back[8] == c3:
            return [bottom[4], left[4], back[4]]
        elif bottom[8] == c1 and back[6] == c2 and right[8] == c3:
            return [bottom[4], back[4], right[4]]
        elif right[0] == c1 and top[8] == c2 and front[2] == c3:
            return [right[4],top[4], front[4]]
        elif right[2] == c1 and back[0] == c2 and top[2] == c3:
            return [right[4], back[4], top[4]]
        elif right[6] == c1 and front[8] == c2 and bottom[2] == c3:
            return [right[4], front[4], bottom[4]]
        elif right[8] == c1 and bottom[8] == c2 and back[6] == c3:
            return [right[4], bottom[4], back[4]]
        elif left[0] == c1 and top[0] == c2 and back[2] == c3:
            return [left[4],top[4], back[4]]
        elif left[2] == c1 and front[0] == c2 and top[6] == c3:
            return [left[4], front[4], top[4]]
        elif left[6] == c1 and back[8] == c2 and bottom[6] == c3:
            return [left[4], back[4], bottom[4]]
        elif left[8] == c1 and bottom[0] == c2 and front[6] == c3:
            return [left[4], bottom[4], front[4]]
        elif back[0] == c1 and top[2] == c2 and right[2] == c3:
            return [back[4],top[4], right[4]]
        elif back[2] == c1 and left[0] == c2 and top[0] == c3:
            return [back[4], left[4], top[4]]
        elif back[6] == c1 and right[8] == c2 and bottom[8] == c3:
            return [back[4], right[4], bottom[4]]
        elif back[8] == c1 and bottom[6] == c2 and left[6] == c3:
            return [back[4], bottom[4], left[4]]
    def wcross(self, c1, c2):
        faces=self.findEdges(c1, c2)
        if c2 == 'g':
            if faces == ['o', 'g']:
                self.f('cross')
            elif faces == ['r', 'g']:
                self.fi('cross')
            elif faces == ['y', 'g']:
                self.f('cross')
                self.f('cross')
            elif faces == ['y', 'r']:
                self.ui('cross')
                self.f('cross')
                self.f('cross')
            elif faces == ['y', 'o']:
                self.u('cross')
                self.f('cross')
                self.f('cross')
            elif faces == ['y', 'b']:
                self.u('cross')
                self.u('cross')
                self.f('cross')
                self.f('cross')
            elif faces == ['w', 'r']:
                self.d('cross')
            elif faces == ['w', 'o']:
                self.di('cross')
            elif faces == ['w', 'b']:
                self.d('cross')
                self.d('cross')
            elif faces == ['g', 'o']:
                self.ri('cross')
                self.di('cross')
            elif faces == ['g', 'r']:
                self.l('cross')
                self.d('cross')
            elif faces == ['g', 'y']:
                self.fi('cross')
                self.l('cross')
                self.d('cross')
            elif faces == ['o', 'y']:
                self.ri('cross')
                self.f('cross')
            elif faces == ['r', 'y']:
                self.l('cross')
                self.fi('cross')
            elif faces == ['b', 'y']:
                self.ui('cross')
                self.l('cross')
                self.fi('cross')
            elif faces == ['r', 'w']:
                self.li('cross')
                self.fi('cross')           
            elif faces == ['b', 'w']:
                self.d('cross')
                self.li('cross')
                self.fi('cross')
            elif faces == ['o', 'w']:
                self.r('cross')
                self.f('cross')
            elif faces == ['b', 'o']:
                self.r('cross')
                self.di('cross')
            elif faces == ['b', 'r']:
                self.li('cross')
                self.d('cross')
            elif faces == ['o', 'b']:
                self.r('cross')
                self.r('cross')
                self.f('cross')
            elif faces == ['r', 'b']:
                self.l('cross')
                self.l('cross')
                self.fi('cross')
            elif faces == ['g', 'w']:
                self.fi('cross')
                self.ri('cross')
                self.di('cross')
        elif c2 == 'r':
            if faces == ['o', 'g']:
                self.d('cross')
                self.f('cross')
                self.di('cross')
            elif faces == ['r', 'g']:
                self.d('cross')
                self.fi('cross')
                self.di('cross')
            elif faces == ['y', 'g']:
                self.u('cross')
                self.l('cross')
                self.l('cross')
            elif faces == ['y', 'r']:
                self.l('cross')
                self.l('cross')
            elif faces == ['y', 'o']:
                self.u('cross')
                self.u('cross')
                self.l('cross')
                self.l('cross')
            elif faces == ['y', 'b']:
                self.ui('cross')
                self.l('cross')
                self.l('cross')
            elif faces == ['w', 'o']:
                self.ri('cross')
                self.d('cross')
                self.d('cross')
                self.r('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['w', 'b']:
                self.bi('cross')
                self.di('cross')
                self.b('cross')
                self.d('cross')
            elif faces == ['g', 'o']:
                self.d('cross')
                self.d('cross')
                self.ri('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['g', 'r']:
                self.l('cross')
            elif faces == ['g', 'y']:
                self.fi('cross')
                self.l('cross')
                self.f('cross')
            elif faces == ['o', 'y']:
                self.u('cross')
                self.fi('cross')
                self.l('cross')
                self.f('cross')
            elif faces == ['r', 'y']:
                self.ui('cross')
                self.fi('cross')
                self.l('cross')
                self.f('cross')
            elif faces == ['b', 'y']:
                self.u('cross')
                self.u('cross')
                self.fi('cross')
                self.l('cross')
                self.f('cross')
            elif faces == ['r', 'w']:
                self.li('cross')
                self.d('cross')
                self.fi('cross') 
                self.di('cross')          
            elif faces == ['b', 'w']:
                self.bi('cross')
                self.li('cross')
            elif faces == ['o', 'w']:
                self.ri('cross')
                self.d('cross')
                self.d('cross')
                self.r('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['b', 'o']:
                self.d('cross')
                self.d('cross')
                self.r('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['b', 'r']:
                self.li('cross')
            elif faces == ['o', 'b']:
                self.di('cross')
                self.bi('cross')
                self.d('cross')
            elif faces == ['r', 'b']:
                self.di('cross')
                self.b('cross')
                self.d('cross')
        elif c2 == 'o':
            if faces == ['o', 'g']:
                self.di('cross')
                self.f('cross')
                self.d('cross')
            elif faces == ['r', 'g']:
                self.di('cross')
                self.fi('cross')
                self.d('cross')
            elif faces == ['y', 'g']:
                self.ui('cross')
                self.r('cross')
                self.r('cross')
            elif faces == ['y', 'r']:
                self.u('cross')
                self.u('cross')
                self.r('cross')
                self.r('cross')
            elif faces == ['y', 'o']:
                self.r('cross')
                self.r('cross')
            elif faces == ['y', 'b']:
                self.u('cross')
                self.r('cross')
                self.r('cross')
            elif faces == ['w', 'b']:
                self.b('cross')
                self.d('cross')
                self.bi('cross')
                self.di('cross')
            elif faces == ['g', 'o']:
                self.ri('cross')
            elif faces == ['g', 'r']:
                self.d('cross')
                self.d('cross')
                self.l('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['g', 'y']:
                self.f('cross')
                self.ri('cross')
                self.fi('cross')
            elif faces == ['o', 'y']:
                self.u('cross')
                self.f('cross')
                self.ri('cross')
                self.fi('cross')
            elif faces == ['r', 'y']:
                self.ui('cross')
                self.f('cross')
                self.ri('cross')
                self.fi('cross')
            elif faces == ['b', 'y']:
                self.bi('cross')
                self.r('cross')         
            elif faces == ['b', 'w']:
                self.b('cross')
                self.r('cross')
            elif faces == ['o', 'w']:
                self.ri('cross')
                self.d('cross')
                self.bi('cross')
                self.di('cross')
            elif faces == ['b', 'o']:
                self.r('cross')
            elif faces == ['b', 'r']:
                self.d('cross')
                self.d('cross')
                self.li('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['o', 'b']:
                self.d('cross')
                self.bi('cross')
                self.di('cross')
            elif faces == ['r', 'b']:
                self.d('cross')
                self.b('cross')
                self.di('cross')
        elif c2 == 'b':
            if faces == ['o', 'g']:
                self.d('cross')
                self.d('cross')
                self.f('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['r', 'g']:
                self.d('cross')
                self.d('cross')
                self.fi('cross')
                self.d('cross')
                self.d('cross')
            elif faces == ['y', 'g']:
                self.u('cross')
                self.u('cross')
                self.bi('cross')
                self.bi('cross')
            elif faces == ['y', 'r']:
                self.u('cross')
                self.bi('cross')
                self.bi('cross')
            elif faces == ['y', 'o']:
                self.ui('cross')
                self.bi('cross')
                self.bi('cross')
            elif faces == ['y', 'b']:
                self.bi('cross')
                self.bi('cross')
            elif faces == ['g', 'o']:
                self.di('cross')
                self.ri('cross')
                self.d('cross')
            elif faces == ['g', 'r']:
                self.d('cross')
                self.l('cross')
                self.di('cross')
            elif faces == ['g', 'y']:
                self.f('cross')
                self.di('cross')
                self.ri('cross')
                self.d('cross')
                self.fi('cross')
            elif faces == ['o', 'y']:
                self.r('cross')
                self.bi('cross')
                self.ri('cross')
            elif faces == ['r', 'y']:
                self.li('cross')
                self.b('cross')
                self.l('cross')
            elif faces == ['b', 'y']:
                self.ui('cross')
                self.li('cross')
                self.b('cross')
                self.l('cross')        
            elif faces == ['b', 'w']:
                self.b('cross')
                self.di('cross')
                self.r('cross')
                self.d('cross')
            elif faces == ['o', 'w']:
                self.r('cross')
                self.bi('cross')
                self.ri('cross')
            elif faces == ['b', 'o']:
                self.di('cross')
                self.r('cross')
                self.d('cross')
            elif faces == ['b', 'r']:
                self.d('cross')
                self.li('cross')
                self.di('cross')
            elif faces == ['o', 'b']: 
                self.bi('cross')
            elif faces == ['r', 'b']:
                self.b('cross')
    def wface(self, c1, c2, c3):
        faces=self.findCorners(c1, c2, c3)
        if c2 == 'g' and c3 == 'r':
            if faces == ['r', 'g', 'y']:
                self.lsxym('first')
            elif faces == ['g', 'y', 'r']:
                self.rlsxym('first')
            elif faces == ['y', 'r', 'g']:
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['r', 'w', 'g']:
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['g', 'r', 'w']:
                self.rlsxym('first')
                self.rlsxym('first')
            elif faces == ['o', 'y', 'g']:
                self.li('first')
                self.u('first')
                self.l('first')
            elif faces == ['g', 'o', 'y']:
                self.u('first')
                self.lsxym('first')
            elif faces == ['b', 'y', 'o']:
                self.u('first')
                self.li('first')
                self.u('first')
                self.l('first')
            elif faces == ['r', 'y', 'b']:
                self.u('first')
                self.u('first')
                self.li('first')
                self.u('first')
                self.l('first')
            elif faces == ['y', 'b', 'r']:
                self.ui('first')
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['y', 'o', 'b']:
                self.u('first')
                self.u('first')
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['y', 'g', 'o']:
                self.u('first')
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['o', 'b', 'y']:
                self.u('first')
                self.u('first')
                self.lsxym('first')
            elif faces == ['b', 'r', 'y']:
                self.ui('first')
                self.lsxym('first')
            elif faces == ['g', 'w', 'o']:
                self.sxym('first')
                self.u('first')
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['o', 'g', 'w']:
                self.sxym('first')
                self.li('first')
                self.u('first')
                self.l('first')
            elif faces == ['w', 'o', 'g']:
                self.sxym('first')
                self.u('first')
                self.li('first')
                self.ui('first')
                self.l('first')
            elif faces == ['o', 'w', 'b']:
                self.blsxym('first')
                self.u('first')
                self.u('first')
                self.lsxym('first')
            elif faces == ['b', 'o', 'w']:
                self.blsxym('first')
                self.u('first')
                self.u('first')
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['w', 'b', 'o']:
                self.blsxym('first')
                self.u('first')
                self.li('first')
                self.u('first')
                self.l('first')
            elif faces == ['b', 'w', 'r']:
                self.bsxym('first')
                self.ui('first')
                self.lsxym('first')
                self.lsxym('first')
                self.lsxym('first')
            elif faces == ['r', 'b', 'w']:
                self.bsxym('first')
                self.u('first')
                self.u('first')
                self.li('first')
                self.u('first')
                self.l('first')
            elif faces == ['w', 'r', 'b']:
                self.bsxym('first')
                self.ui('first')
                self.lsxym('first')
        elif c2 == 'o' and c3 == 'g':
            if faces == ['r', 'g', 'y']:
                self.r('first')
                self.ui('first')
                self.ri('first')
            elif faces == ['g', 'y', 'r']:
                self.ui('first')
                self.sxym('first')
            elif faces == ['y', 'r', 'g']:
                self.ui('first')
                self.sxym('first')
                self.sxym('first')
                self.sxym('first')
            elif faces == ['o', 'y', 'g']:
                self.r('first')
                self.u('first')
                self.ri('first')
            elif faces == ['g', 'o', 'y']:
                self.rsxym('first')
            elif faces == ['b', 'y', 'o']:
                self.u('first')
                self.r('first')
                self.u('first')
                self.ri('first')
            elif faces == ['r', 'y', 'b']:
                self.u('first')
                self.u('first')
                self.r('first')
                self.u('first')
                self.ri('first')
            elif faces == ['y', 'b', 'r']:
                self.u('first')
                self.u('first')
                self.sxym('first')
                self.sxym('first')
                self.sxym('first')
            elif faces == ['y', 'o', 'b']:
                self.u('first')
                self.sxym('first')
                self.sxym('first')
                self.sxym('first')
            elif faces == ['y', 'g', 'o']:
                self.sxym('first')
                self.sxym('first')
                self.sxym('first')
            elif faces == ['o', 'b', 'y']:
                self.u('first')
                self.u('first')
                self.r('first')
                self.ui('first')
                self.ri('first')
            elif faces == ['b', 'r', 'y']:
                self.ui('first')
                self.r('first')
                self.ui('first')
                self.ri('first')
            elif faces == ['g', 'w', 'o']:
                self.rsxym('first')
                self.rsxym('first')
            elif faces == ['o', 'g', 'w']:
                self.sxym('first')
                self.sxym('first')
            elif faces == ['o', 'w', 'b']:
                self.ri('first')
                self.u('first')
                self.u('first')
                self.r('first')
                self.r('first')
                self.ui('first')
                self.ri('first')
            elif faces == ['b', 'o', 'w']:
                self.ri('first')
                self.u('first')
                self.u('first')
                self.r('first')
                self.ui('first')
                self.sxym('first')
                self.sxym('first')
                self.sxym('first')
            elif faces == ['w', 'b', 'o']:
                self.ri('first')
                self.u('first')
                self.u('first')
                self.r('first')
                self.ui('first')
                self.sxym('first')
            elif faces == ['b', 'w', 'r']:
                self.l('first')
                self.u('first')
                self.u('first')
                self.li('first')
                self.sxym('first')
                self.sxym('first')
                self.sxym('first')
            elif faces == ['r', 'b', 'w']:
                self.l('first')
                self.u('first')
                self.u('first')
                self.li('first')
                self.sxym('first')
            elif faces == ['w', 'r', 'b']:
                self.l('first')
                self.u('first')
                self.u('first')
                self.li('first')
                self.rsxym('first')
        elif c2 == 'r' and c3 == 'b':
            if faces == ['r', 'g', 'y']:
                self.u('first')
                self.u('first')
                self.l('first')
                self.ui('first')
                self.li('first')
            elif faces == ['g', 'y', 'r']:
                self.u('first')
                self.l('first')
                self.u('first')
                self.li('first')
            elif faces == ['y', 'r', 'g']:
                self.u('first')
                self.bsxym('first')
                self.bsxym('first')
                self.bsxym('first')
            elif faces == ['o', 'y', 'g']:
                self.u('first')
                self.u('first')
                self.l('first')
                self.u('first')
                self.li('first')
            elif faces == ['g', 'o', 'y']:
                self.ui('first')
                self.l('first')
                self.ui('first')
                self.li('first')
            elif faces == ['b', 'y', 'o']:
                self.ui('first')
                self.l('first')
                self.u('first')
                self.li('first')
            elif faces == ['r', 'y', 'b']:
                self.l('first')
                self.u('first')
                self.li('first')
            elif faces == ['y', 'b', 'r']:
                self.bsxym('first')
                self.bsxym('first')
                self.bsxym('first')
            elif faces == ['y', 'o', 'b']:
                self.ui('first')
                self.bsxym('first')
                self.bsxym('first')
                self.bsxym('first')
            elif faces == ['y', 'g', 'o']:
                self.u('first')
                self.u('first')
                self.bsxym('first')
                self.bsxym('first')
                self.bsxym('first')
            elif faces == ['o', 'b', 'y']:
                self.l('first')
                self.ui('first')
                self.li('first')
            elif faces == ['b', 'r', 'y']:
                self.rbsxym('first')
            elif faces == ['o', 'w', 'b']:
                self.ri('first')
                self.ui('first')
                self.r('first')
                self.rbsxym('first')
            elif faces == ['b', 'o', 'w']:
                self.ri('first')
                self.ui('first')
                self.r('first')
                self.bsxym('first')
                self.bsxym('first')
                self.bsxym('first')
            elif faces == ['w', 'b', 'o']:
                self.ri('first')
                self.ui('first')
                self.r('first')
                self.l('first')
                self.u('first')
                self.li('first')
            elif faces == ['b', 'w', 'r']:
                self.rbsxym('first')
                self.rbsxym('first')
            elif faces == ['r', 'b', 'w']:
                self.bsxym('first')
                self.bsxym('first')
        elif c2 == 'b' and c3 == 'o':
            if faces == ['r', 'g', 'y']:
                self.u('first')
                self.u('first')
                self.ri('first')
                self.ui('first')
                self.r('first')
            elif faces == ['g', 'y', 'r']:
                self.u('first')
                self.ri('first')
                self.u('first')
                self.r('first')
            elif faces == ['y', 'r', 'g']:
                self.u('first')
                self.u('first')
                self.blsxym('first')
                self.blsxym('first')
                self.blsxym('first')
            elif faces == ['o', 'y', 'g']:
                self.u('first')
                self.u('first')
                self.ri('first')
                self.u('first')
                self.r('first')
            elif faces == ['g', 'o', 'y']:
                self.ui('first')
                self.ri('first')
                self.ui('first')
                self.r('first')
            elif faces == ['b', 'y', 'o']:
                self.rblsxym('first')
            elif faces == ['r', 'y', 'b']:
                self.ri('first')
                self.u('first')
                self.r('first')
            elif faces == ['y', 'b', 'r']:
                self.u('first')
                self.blsxym('first')
                self.blsxym('first')
                self.blsxym('first')
            elif faces == ['y', 'o', 'b']:
                self.blsxym('first')
                self.blsxym('first')
                self.blsxym('first')
            elif faces == ['y', 'g', 'o']:
                self.ui('first')
                self.blsxym('first')
                self.blsxym('first')
                self.blsxym('first')
            elif faces == ['o', 'b', 'y']:
                self.ri('first')
                self.ui('first')
                self.r('first')
            elif faces == ['b', 'r', 'y']:
                self.u('first')
                self.ri('first')
                self.ui('first')
                self.r('first')
            elif faces == ['o', 'w', 'b']:
                self.blsxym('first')
                self.blsxym('first')
            elif faces == ['b', 'o', 'w']:
                self.rblsxym('first')
                self.rblsxym('first')
    def tl(self, c1, c2):
        faces=self.findEdges(c1, c2)
        if c1 == 'g' and c2 == 'o':
            if faces==['g', 'y']:
                self.rsxym('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['y', 'g']:
                self.u('ftl')
                self.u('ftl')
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
            elif faces==['r', 'y']:
                self.ui('ftl')
                self.rsxym('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['y', 'r']:
                self.u('ftl')
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
            elif faces==['y', 'b']:
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
            elif faces==['b', 'y']:
                self.u('ftl')
                self.u('ftl')
                self.rsxym('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['o', 'y']:
                self.u('ftl')
                self.rsxym('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['o', 'g']:
                self.rsxym('ftl')
                self.u('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.u('ftl')
                self.f('ftl')
                self.u('ftl')
                self.u('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['r', 'g']:
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.r('ftl')
                self.ui('ftl')
                self.ri('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['g', 'r']:
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
            elif faces==['r', 'b']:
                self.rbsxym('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.rsxym('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['b', 'r']:
                self.rbsxym('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.u('ftl')
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
            elif faces==['b', 'o']:
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.u('ftl')
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
            elif faces==['o', 'b']:
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.rsxym('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.f('ftl')
            elif faces==['y', 'o']:
                self.ui('ftl')
                self.ri('ftl')
                self.f('ftl')
                self.r('ftl')
                self.fi('ftl')
                self.r('ftl')
                self.u('ftl')
                self.ri('ftl')
        if c1 == 'r' and c2 == 'g':
            if faces==['g', 'y']:
                self.u('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
            elif faces==['y', 'g']:
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
            elif faces==['r', 'y']:
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
            elif faces==['y', 'r']:
                self.ui('ftl')
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
            elif faces==['b', 'y']:
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
            elif faces==['y', 'b']:
                self.u('ftl')
                self.u('ftl')
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
            elif faces==['o', 'y']:
                self.ui('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
            elif faces==['y', 'o']:
                self.u('ftl')
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
            elif faces==['b', 'r']:
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
            elif faces==['r', 'b']:
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
            elif faces==['b', 'o']:
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.rlsxym('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
            elif faces==['o', 'b']:
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
            elif faces==['g', 'r']:
                self.li('ftl')
                self.u('ftl')
                self.l('ftl')
                self.ui('ftl')
                self.f('ftl')
                self.u('ftl')
                self.u('ftl')
                self.fi('ftl')
                self.u('ftl')
                self.u('ftl')
                self.f('ftl')
                self.ui('ftl')
                self.fi('ftl')
        if c1 == 'o' and c2 == 'b':
            if faces==['g', 'y']:
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.ui('ftl')
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
            elif faces==['y', 'b']:
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
            elif faces==['r', 'y']:
                self.ui('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.ui('ftl')
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
            elif faces==['y', 'r']:
                self.u('ftl')
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
            elif faces==['b', 'y']:
                self.u('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.ui('ftl')
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
            elif faces==['y', 'g']:
                self.u('ftl')
                self.u('ftl')
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
            elif faces==['o', 'y']:
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.ui('ftl')
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
            elif faces==['y', 'o']:
                self.ui('ftl')
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
            elif faces==['b', 'r']:
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.u('ftl')
                self.rblsxym('ftl')
                self.u('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
            elif faces==['r', 'b']:
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.b('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.ui('ftl')
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
            elif faces==['b', 'o']:
                self.ri('ftl')
                self.u('ftl')
                self.r('ftl')
                self.ui('ftl')
                self.b('ftl')
                self.u('ftl')
                self.u('ftl')
                self.bi('ftl')
                self.ui('ftl')
                self.b('ftl')
                self.u('ftl')
                self.u('ftl')
                self.bi('ftl')
        if c1 == 'b' and c2 == 'r':
            if faces==['g', 'y']:
                self.u('ftl')
                self.u('ftl')
                self.rbsxym('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
            elif faces==['y', 'b']:
                self.u('ftl')
                self.u('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
            elif faces==['r', 'y']:
                self.u('ftl')
                self.rbsxym('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
            elif faces==['y', 'r']:
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
            elif faces==['b', 'y']:
                self.rbsxym('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
            elif faces==['y', 'g']:
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
            elif faces==['o', 'y']:
                self.ui('ftl')
                self.rbsxym('ftl')
                self.ui('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
            elif faces==['y', 'o']:
                self.u('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
            elif faces==['r', 'b']:
                self.l('ftl')
                self.ui('ftl')
                self.li('ftl')
                self.u('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.u('ftl')
                self.b('ftl')
                self.u('ftl')
                self.u('ftl')
                self.bi('ftl')
                self.u('ftl')
                self.b('ftl')
    def olastlayer(self):
        if self.c[0][1]=='y' and self.c[0][3]=='y' and self.c[0][5]=='y' and self.c[0][7]=='y':
            if self.c[0][0]=='y' and self.c[0][2]!='y' and self.c[0][6]!='y' and self.c[0][8]!='y':
                if self.c[2][2]=='y':
                    self.ui('oll')
                    self.sune('oll')
                else:
                    self.u('oll')
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]=='y' and self.c[0][6]!='y' and self.c[0][8]!='y':
                if self.c[5][2]=='y':
                    self.u('oll')
                    self.u('oll')
                    self.sune('oll')
                else:
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]!='y' and self.c[0][6]=='y' and self.c[0][8]!='y':
                if self.c[4][2]=='y':
                    self.sune('oll')
                else:
                    self.u('oll')
                    self.u('oll')
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]!='y' and self.c[0][6]!='y' and self.c[0][8]=='y':
                if self.c[3][2]=='y':
                    self.u('oll')
                    self.sune('oll')
                else:
                    self.ui('oll')
                    self.antisune('oll')
            elif self.c[0][0]=='y' and self.c[0][2]!='y' and self.c[0][6]!='y' and self.c[0][8]=='y':
                if self.c[2][2]=='y':
                    self.ui('oll')
                    self.sune('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
                else:
                    self.u('oll')
                    self.sune('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]=='y' and self.c[0][6]=='y' and self.c[0][8]!='y':
                if self.c[5][2]=='y':
                    self.u('oll')
                    self.u('oll')
                    self.sune('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
                else:
                    self.sune('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
            elif self.c[0][0]=='y' and self.c[0][2]=='y' and self.c[0][6]!='y' and self.c[0][8]!='y':
                if self.c[4][2]=='y' and self.c[4][0]=='y':
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
                else:
                    self.u('oll')
                    self.sune('oll')
                    self.ui('oll')
                    self.antisune('oll')
            elif self.c[0][0]=='y' and self.c[0][2]!='y' and self.c[0][6]=='y' and self.c[0][8]!='y':
                if self.c[3][2]=='y' and self.c[3][0]=='y':
                    self.u('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
                else:
                    self.u('oll')
                    self.u('oll')
                    self.sune('oll')
                    self.ui('oll')
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]=='y' and self.c[0][6]!='y' and self.c[0][8]=='y':
                if self.c[2][2]=='y' and self.c[2][0]=='y':
                    self.ui('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
                else:
                    self.sune('oll')
                    self.ui('oll')
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]!='y' and self.c[0][6]=='y' and self.c[0][8]=='y':
                if self.c[5][2]=='y' and self.c[5][0]=='y':
                    self.u('oll')
                    self.u('oll')
                    self.sune('oll')
                    self.u('oll')
                    self.antisune('oll')
                else:
                    self.ui('oll')
                    self.sune('oll')
                    self.ui('oll')
                    self.antisune('oll')
            elif self.c[0][0]!='y' and self.c[0][2]!='y' and self.c[0][6]!='y' and self.c[0][8]!='y':
                if self.c[4][2]=='y' and self.c[4][0]=='y' and self.c[5][2]=='y' and self.c[5][0]=='y':
                    self.f('oll')
                    self.sxym('oll')
                    self.sxym('oll')
                    self.sxym('oll')
                    self.fi('oll')
                elif self.c[3][2]=='y' and self.c[3][0]=='y' and self.c[2][2]=='y' and self.c[2][0]=='y':
                    self.ui('oll')
                    self.f('oll')
                    self.sxym('oll')
                    self.sxym('oll')
                    self.sxym('oll')
                    self.fi('oll')
                elif self.c[4][2]=='y' and self.c[4][0]=='y' and self.c[2][0]=='y' and self.c[3][2]=='y':
                    self.u('oll')
                    self.sune('oll')
                    self.ui('oll')
                    self.sune('oll')
                elif self.c[3][2]=='y' and self.c[3][0]=='y' and self.c[4][0]=='y' and self.c[5][2]=='y':
                    self.u('oll')
                    self.u('oll')
                    self.sune('oll')
                    self.ui('oll')
                    self.sune('oll')
                elif self.c[2][0]=='y' and self.c[2][2]=='y' and self.c[4][2]=='y' and self.c[5][0]=='y':
                    self.sune('oll')
                    self.ui('oll')
                    self.sune('oll')
                elif self.c[5][2]=='y' and self.c[5][0]=='y' and self.c[2][2]=='y' and self.c[3][0]=='y':
                    self.ui('oll')
                    self.sune('oll')
                    self.ui('oll')
                    self.sune('oll')      
        elif self.c[0][4]=='y':  
            if self.c[0][1]=='y' and self.c[0][7]=='y':
                self.u('oll')
                self.f('oll')
                self.sxym('oll')
                self.fi('oll')
            elif self.c[0][3]=='y' and self.c[0][5]=='y':
                self.f('oll')
                self.sxym('oll')
                self.fi('oll')
            elif self.c[0][1]=='y' and self.c[0][3]=='y':
                self.f('oll')
                self.rsxym('oll')
                self.fi('oll')
            elif self.c[0][1]=='y' and self.c[0][5]=='y':
                self.ui('oll')
                self.f('oll')
                self.rsxym('oll')
                self.fi('oll')
            elif self.c[0][3]=='y' and self.c[0][7]=='y':
                self.u('oll')
                self.f('oll')
                self.rsxym('oll')
                self.fi('oll')
            elif self.c[0][7]=='y' and self.c[0][5]=='y':
                self.u('oll')
                self.u('oll')
                self.f('oll')
                self.rsxym('oll')
                self.fi('oll')
            elif self.c[0][4]=='y':
                self.f('oll')
                self.rsxym('oll')
                self.fi('oll')
    def isOp(self, c1, c2):
        if c1 == 'g' and c2 == 'b':
            return True
        elif c1 == 'b' and c2 == 'g':
            return True
        elif c1 == 'r' and c2 == 'o':
            return True
        elif c1 == 'o' and c2 == 'r':
            return True
        else: 
            return False
    def isEq(self, c1, c2):
        if c1 == c2:
            return True
        else:
            return False
    def isEqt(self, c1, c2, c3):
        if c1 == c2 and c2 == c3:
            return True
        else:
            return False

    def plastlayer(self):
        if not self.isEqt(self.c[2][0],self.c[2][1], self.c[2][2]) or not self.isEqt(self.c[3][0],self.c[3][1], self.c[3][2]):
            if self.isEq(self.c[2][0], self.c[2][2]) and self.isEq(self.c[3][0], self.c[3][2]) and self.isEq(self.c[4][0], self.c[4][2]):
                if self.isOp(self.c[5][1], self.c[4][0]) and self.isEq(self.c[2][1], self.c[4][2]):
                    self.uaperm()
                elif self.isOp(self.c[5][1], self.c[4][0]):
                    self.ubperm()
                elif self.isOp(self.c[5][1], self.c[4][1]) and self.isOp(self.c[5][1], self.c[5][0]):
                    self.hperm()
                elif self.isOp(self.c[5][1], self.c[4][1]) and self.isEq(self.c[3][1], self.c[4][0]):
                    self.zperm()
                else:
                    self.u('pll')
            elif self.isEqt(self.c[2][0], self.c[2][1], self.c[2][2]) and self.isEq(self.c[5][1], self.c[5][2]):
                self.jperm()
            elif self.isEq(self.c[2][0], self.c[2][2]) and self.isOp(self.c[5][2], self.c[4][0]):
                self.tperm()
            elif self.isEq(self.c[4][0], self.c[4][1]) and self.isEq(self.c[5][1], self.c[4][2]) and self.isOp(self.c[2][2], self.c[3][2]):
                self.nbperm()
            elif self.isOp(self.c[4][1], self.c[5][1]) and self.isOp(self.c[2][1], self.c[3][1]) and self.isEq(self.c[4][0], self.c[5][2]) and self.isEq(self.c[4][2], self.c[5][0]):
                self.tperm()
            elif self.isEq(self.c[4][0], self.c[4][1]) and self.isEq(self.c[3][1], self.c[3][2]) and self.isOp(self.c[5][0], self.c[4][1]):
                self.yperm()
            elif self.isEq(self.c[4][1], self.c[4][2]) and self.isEq(self.c[5][1], self.c[5][2]) and self.isOp(self.c[2][0], self.c[3][0]):
                self.r('pll')
                self.u('pll')
                self.ri('pll')
                self.u('pll')
                self.jperm()
                self.u('pll')
                self.u('pll')
                self.r('pll')
                self.ui('pll')
                self.ri('pll')
            elif self.isEq(self.c[2][0], self.c[2][1]) and self.isEq(self.c[5][1], self.c[5][2]) and self.isOp(self.c[4][1], self.c[3][2]):
                self.sune('pll')
                self.sune('pll')
                self.f('pll')
                self.sxym('pll')
                self.sxym('pll')
                self.sxym('pll')
                self.fi('pll')
                self.ui('pll')
            else:
                self.u('pll')
    def adjuf(self):
        if self.c[4][1]=='r':
            self.u('auf')
        elif self.c[4][1]=='b':
            self.u('auf')
            self.u('auf')
            self.auf=["U2 "]
        elif self.c[4][1]=='o':
            self.ui('auf')
    def isSolved(self):
        top = ["y", "y", "y", "y", "y", "y", "y", "y", "y"]
        bottom = ["w", "w", "w", "w", "w", "w", "w", "w", "w"]
        back = ["b", "b", "b", "b", "b", "b", "b", "b", "b"]
        front = ["g", "g", "g", "g", "g", "g", "g", "g", "g"]
        left = ["r", "r", "r", "r", "r", "r", "r", "r", "r"]
        right = ["o", "o", "o", "o", "o", "o", "o", "o", "o"]
        c = [top, bottom, left, right, front, back]
        if self.c==c:
                    return "Complete!"
        else:
            self.cross=[]
            self.first=[]
            self.ftl=[]
            self.oll=[]
            self.pll=[]
            self.scramble=[]
            self.auf=[]
            return "Your cube is either unsolvable or there was an input mistake. Please try entering the colours again."

        

        
# solves cube via WCA input
@app.route('/strsolver', methods=["POST"])
def main2():
    body = request.json['body']
    body = body.replace(" ", "").replace(",", "").lower()
    print(body)
    moves = set(['r', 'u', 'l', 'b', 'f', 'd'])
    validInput, error = True, None
    cube1 = cube()
    i = 0
    while i < len(body):
        prime, count = False, 1
        if body[i] not in moves:
            validInput, error = False, 'Invalid input, please input scrambles based off of WCA format'
            break
        move = body[i]
        while i + 1 < len(body) and body[i + 1] not in moves:
            i += 1
            if body[i] == "'":
                prime = not prime
            elif ord('0') <= ord(body[i]) <= ord('9'):
                count = int(body[i])
            else:
                validInput, error = False, 'Invalid input, please input scrambles based off of WCA format'
                break
        for j in range(count):
            if not prime:
                if move == "r":
                    cube1.l('scramble')
                elif move == "u":
                    cube1.d('scramble')
                elif move == "d":
                    cube1.u('scramble')
                elif move == "b":
                    cube1.b('scramble')
                elif move == "l":
                    cube1.r('scramble')
                elif move == "f":
                    cube1.f('scramble')
            else:
                if move == "r":
                    cube1.li('scramble')
                elif move == "u":
                    cube1.di('scramble')
                elif move == "d":
                    cube1.ui('scramble')
                elif move == "b":
                    cube1.bi('scramble')
                elif move == "l":
                    cube1.ri('scramble')
                elif move == "f":
                    cube1.fi('scramble')
        i += 1
    cube2D = []
    cube2D.append(tuple(cube1.c[0]))
    cube2D.append(tuple(cube1.c[2]))
    cube2D.append(tuple(cube1.c[4]))
    cube2D.append(tuple(cube1.c[3]))
    cube2D.append(tuple(cube1.c[5]))
    cube2D.append(tuple(cube1.c[1]))
    cube1.wcross('w', 'g')
    cube1.wcross('w', 'r')
    cube1.wcross('w', 'o')
    cube1.wcross('w', 'b')
    cube1.wface('w', 'g', 'r')
    cube1.wface('w', 'o', 'g')
    cube1.wface('w', 'r', 'b')
    cube1.wface('w', 'b', 'o')
    cube1.tl('g', 'o')
    cube1.tl('r', 'g')
    cube1.tl('o', 'b')
    cube1.tl('b', 'r')
    cube1.olastlayer()
    cube1.olastlayer()
    cube1.olastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.adjuf()
    cube1.simplify('cross')
    cube1.simplify('first')
    cube1.simplify('ftl')
    cube1.simplify('oll')
    cube1.simplify('pll')
    cube1.replace('cross')
    cube1.replace('first')
    cube1.replace('ftl')
    cube1.replace('oll')
    cube1.replace('pll')
    return {'cross': cube1.cross,
            'first': cube1.first,
            'ftl': cube1.ftl,
            'oll': cube1.oll,
            'pll': cube1.pll,
            'auf': cube1.auf,
            'scramble': cube1.scramble,
            'cubestate': cube1.isSolved(),
            'valid': validInput,
            'error': error,
            'state': cube2D}

# endpoint that is a "sandbox" to test full stack and cube class functionality
@app.route('/solver', methods=["POST"])
def main():
    body = request.json['body']
    cube1 = cube()
    cube2 = cube()
    cube1.u('scramble')
    # cube1.r('scramble')
    # cube1.fi('scramble')
    # cube1.di('scramble')
    # cube1.r('scramble')
    # cube1.r('scramble')
    # cube1.di('scramble')
    # cube1.r('scramble')
    # cube1.r('scramble')
    # cube1.b('scramble')
    # cube1.b('scramble')
    # cube1.l('scramble')
    # cube1.l('scramble')
    # cube1.d('scramble')
    # cube1.d('scramble')
    # cube1.r('scramble')
    # cube1.r('scramble')
    # cube1.d('scramble')
    # cube1.f('scramble')
    # cube1.f('scramble')
    # cube1.d('scramble')
    # cube1.f('scramble')
    # cube1.f('scramble')
    # cube1.d('scramble')
    # cube1.ri('scramble')
    # cube1.fi('scramble')
    # cube1.l('scramble')
    # cube1.f('scramble')
    # cube1.u('scramble')
    # cube1.u('scramble')
    # cube1.r('scramble')
    # cube1.r('scramble')
    # cube1.u('scramble')
    # cube1.ri('scramble')
    # cube1.bi('scramble')
    # cube1.ui('scramble')
    # cube1.fi('scramble')
    # cube1.r('scramble')
    # cube1.r('scramble')
    # cube1.d('scramble')
    # cube1.ui('scramble')
    # cube1.b('scramble')
    # cube1.fi('scramble')
    # cube1.tperm()
    # cube1.u('pll')
    # cube1.u('pll')
    # cube1.tperm()
    cube1.wcross('w', 'g')
    cube1.wcross('w', 'r')
    cube1.wcross('w', 'o')
    cube1.wcross('w', 'b')
    cube1.wface('w', 'g', 'r')
    cube1.wface('w', 'o', 'g')
    cube1.wface('w', 'r', 'b')
    cube1.wface('w', 'b', 'o')
    cube1.tl('g', 'o')
    cube1.tl('r', 'g')
    cube1.tl('o', 'b')
    cube1.tl('b', 'r')
    cube1.olastlayer()
    cube1.olastlayer()
    cube1.olastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.adjuf()
    cube1.simplify('cross')
    cube1.simplify('first')
    cube1.simplify('ftl')
    cube1.simplify('oll')
    cube1.simplify('pll')
    cube1.replace('cross')
    cube1.replace('first')
    cube1.replace('ftl')
    cube1.replace('oll')
    cube1.replace('pll')
    #cube1.li('scramble')
    #cube1.ui('scramble')
    #cube1.l('scramble')
    #cube1.u('scramble')
    if body != "brawlstars":
        with open("imageToSave.png", "wb") as fh:
            print(body)
            fh.write(base64.decodebytes(str.encode(body.split(',')[-1])))
    return {'cross': cube1.cross,
            'first': cube1.first,
            'ftl': cube1.ftl,
            'oll': cube1.oll,
            'pll': cube1.pll,
            'auf': cube1.auf,
            'scramble': cube1.scramble,
            'cubestate': body}

model = torch.hub.load(
    'ultralytics/yolov5',          # Official GitHub repo
    'custom', 
    path=r'./models/best.pt',
    force_reload=True              # optional, but ensures up-to-date
)
model.iou = 0.45
model.conf = 0.5

############################
# 3) Helper functions
############################
def decode_base64_image(image_b64):
    """
    Convert a base64-encoded string to an OpenCV BGR image.
    """
    image_data = base64.b64decode(image_b64.split(',')[-1])  # remove "data:image/..."
    pil_image  = Image.open(io.BytesIO(image_data)).convert('RGB')
    np_image   = np.array(pil_image)
    cv_image   = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    return cv_image

def approximate_color(bgr_patch):
    """
    Placeholder color approximation. 
    Real approach might use YOLO's 'class' ID or average BGR→HSV→closest color.
    For demo, let's pretend it returns a single color name.
    """
    # e.g. always 'white' for demonstration
    return "white"

def map_color_name_to_letter(name):
    """
    Map full color names from the frontend/ML to the single-letter codes 
    used by your 'cube' class.
    Adjust as needed.
    """
    name_lower = name.lower()
    mapping = {
        "white":  "w",
        "yellow": "y",
        "blue":   "b",
        "green":  "g",
        "red":    "r",
        "orange": "o",
        "grey":   "x",  # If you want a placeholder
    }
    return mapping.get(name_lower, "x")  # default to 'x' if unknown

def determine_face_from_center_color(color_name):
    """
    Given the center color name (e.g. "green"), return
    which face it corresponds to (e.g. "front").
    """
    color_name = color_name.lower()
    if color_name in ["green", "g"]:
        return "front"
    elif color_name in ["blue", "b"]:
        return "back"
    elif color_name in ["white", "w"]:
        return "down"
    elif color_name in ["yellow", "y"]:
        return "up"
    elif color_name in ["orange", "o"]:
        return "right"
    elif color_name in ["red", "r"]:
        return "left"
    else:
        # If it's something unknown, default to "front" or handle differently
        return "front"
# previous color detecting method without ML
# def approximate_color(bgr_patch):
#     """
#     Given an image patch in BGR, return a string color name like
#     "white", "yellow", "green", "blue", "red", "orange".
#     """

#     # 1) Compute the average B, G, R values
#     avg_bgr = bgr_patch.mean(axis=(0,1))  # shape: (3,)

#     # 2) Convert that average color to a 1x1 HSV image
#     color_bgr_1x1 = np.uint8([[avg_bgr]])  # shape: (1,1,3)
#     color_hsv_1x1 = cv2.cvtColor(color_bgr_1x1, cv2.COLOR_BGR2HSV)
#     h, s, v = color_hsv_1x1[0][0]  # Just get the single HSV pixel

#     # 3) Compare h,s,v against thresholds
#     #    NOTE: Hue is [0..179] in OpenCV, Saturation/Value are [0..255]
#     #    You can refine these thresholds as needed.

#     if s < 30 and v > 200:
#         # low saturation, high brightness → likely "white"
#         return "white"

#     # Rough hue ranges for typical Rubik’s colors (very approximate!):
#     #   red:     h < 10 or h > 160
#     #   orange:  10 < h < 25
#     #   yellow:  25 < h < 35
#     #   green:   40 < h < 85
#     #   blue:    90 < h < 130
#     #   etc.
#     # Tweak these to match your lighting conditions.

#     if ((h < 5) or (h > 175)) and s > 60:
#         return "red"
#     elif 5 <= h < 25 and s > 60:
#         return "orange"
#     elif 25 <= h < 35 and s > 60:
#         return "yellow"
#     elif 40 <= h < 85 and s > 60:
#         return "green"
#     elif 90 <= h < 130 and s > 60:
#         return "blue"

#     # If none of the above matched well, guess "white" or "unknown"
#     return "white"

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    """
    1) Receives { "image": "data:image/jpeg;base64,..." } from the frontend.
    2) Decodes the image, runs YOLO detection.
    3) If exactly 9 squares are found, derive color codes and return them.
       Otherwise, return an error.
    """
    data = request.get_json()
    image_b64 = data.get('image')
    if not image_b64:
        return jsonify({"error": "No image data provided"}), 400

    # Decode the base64 image
    frame = decode_base64_image(image_b64)

    # YOLO detection
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb, size=640)  
    # results = model(frame_rgb)
    detections = results.xyxy[0].cpu().numpy()

    centered = []
    for d in detections:
        x1, y1, x2, y2, conf, cls_id = d[:6]
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        centered.append((cy, cx, d))
    if len(centered) != 9:
        return jsonify({
            "error": f"Expected 9 squares, but detected {len(boxes)}. Please re-capture the photo."
        }), 400
    # Sort by cy ascending, so top squares come first
    centered.sort(key=lambda x: x[0])  # x[0] = cy

    # Slice into top/middle/bottom rows
    # (assuming we have exactly 9 squares)
    top_row    = centered[0:3]
    middle_row = centered[3:6]
    bottom_row = centered[6:9]

    # Within each row, sort by cx ascending (left to right)
    top_row.sort(key=lambda x: x[1])    
    middle_row.sort(key=lambda x: x[1]) 
    bottom_row.sort(key=lambda x: x[1]) 

    # Re-combine into final row-major list of boxes
    final_order = top_row + middle_row + bottom_row

    # Extract the actual detection from each tuple
    final_boxes = [t[2] for t in final_order]  

    # Now final_boxes[0..2] = top row (L→R),
    #    final_boxes[3..5] = middle row (L→R),
    #    final_boxes[6..8] = bottom row (L→R).
    color_map = {
        0: "blue",
        1: "green",
        2: "orange",
        3: "red",
        4: "white",
        5: "yellow"
    }
    raw_colors = []
    for box in final_boxes:
        x1, y1, x2, y2, conf, cls_id = box[:6]
        color_str = color_map[int(cls_id)]
        raw_colors.append(color_str)
    center_color_name = raw_colors[4]
    faceName = determine_face_from_center_color(center_color_name)
    # Map color names (e.g. "white") to single-letter codes (e.g. "w")
    mapped_colors = [map_color_name_to_letter(c) for c in raw_colors]

    response = {
        "faceName": faceName,
        "colors": raw_colors
    }
    return jsonify(response), 200


# solving cube by state
@app.route('/solve-cube', methods=['POST'])
def solve_cube():
    """
    1) Receives the entire cube state in JSON, e.g.:
       {
         "up":    ["white","white","blue", ... 9 total ],
         "left":  [...],
         "front": [...],
         "right": [...],
         "back":  [...],
         "down":  [...]
       }
    2) Map each color name to single-letter code, store in 'cube'.
    3) Solve and return the solution moves in JSON.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No cube data provided"}), 400

    # Create a new 'cube'
    cube1 = cube()

    # For each face: convert color words to single-letter codes and call set_face
    face_map = {
      "up":    "up",
      "down":  "down",
      "front": "front",
      "back":  "back",
      "left":  "left",
      "right": "right"
    }
    tempTop, top = data["up"], []
    tempBottom, bottom = data["down"], []
    tempRight, right = data["right"], []
    tempLeft, left = data["left"], []
    tempFront, front = data["front"], []
    tempBack, back = data["back"], []
    for i in tempTop:
        top.append(i[0])
    for i in tempBottom:
        bottom.append(i[0])
    for i in tempRight:
        right.append(i[0])
    for i in tempLeft:
        left.append(i[0])
    for i in tempFront:
        front.append(i[0])
    for i in tempBack:
        back.append(i[0])
    cube1.setState(top, bottom, back, front, left, right)

    cube1.wcross('w', 'g')
    cube1.wcross('w', 'r')
    cube1.wcross('w', 'o')
    cube1.wcross('w', 'b')
    cube1.wface('w', 'g', 'r')
    cube1.wface('w', 'o', 'g')
    cube1.wface('w', 'r', 'b')
    cube1.wface('w', 'b', 'o')
    cube1.tl('g', 'o')
    cube1.tl('r', 'g')
    cube1.tl('o', 'b')
    cube1.tl('b', 'r')
    cube1.olastlayer()
    cube1.olastlayer()
    cube1.olastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.plastlayer()
    cube1.adjuf()
    cube1.simplify('cross')
    cube1.simplify('first')
    cube1.simplify('ftl')
    cube1.simplify('oll')
    cube1.simplify('pll')
    cube1.replace('cross')
    cube1.replace('first')
    cube1.replace('ftl')
    cube1.replace('oll')
    cube1.replace('pll')
    # print({'cross': cube1.cross,
    #         'first': cube1.first,
    #         'ftl': cube1.ftl,
    #         'oll': cube1.oll,
    #         'pll': cube1.pll,
    #         'auf': cube1.auf,
    #         'cubestate': cube1.isSolved()})
    return {'cross': cube1.cross,
            'first': cube1.first,
            'ftl': cube1.ftl,
            'oll': cube1.oll,
            'pll': cube1.pll,
            'auf': cube1.auf,
            'scramble': cube1.scramble,
            'cubestate': cube1.isSolved(),
            'valid': True}


if __name__ == '__main__':
    app.run(debug=True)

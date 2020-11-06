"""---------------------------------------------------------------------------------------------"""
"""----------------------------------Conway's game of life--------------------------------------"""
"""---------------------------------------------------------------------------------------------"""


import numpy as np
import matplotlib.pyplot as plt
import random

"""A grid class that contains the actual grid with 0 and 1 values along with
   a neighbor grid with values for the number of neighboring grid cells with value of 1. 
   Also contains methods for filling the grid with initial values, updating the neighbor grid
   and updating the actual grid"""
   
class Grid:
    
    #Initalize actual grid object with empty grid attribute with size = inputted dimension x dimension
    #Neighbor grid attribute also created with same size 
    def __init__(self, dimension):
        
        self.grid = np.zeros((dimension,dimension))
        self.neighbors = np.zeros((dimension, dimension))
        self.dim = dimension
     
    #Method for randomly filling the actual grid with value of 1 for n_fill number of cells   
    def filler(self, n_fill):
        
        for i in range(0,n_fill):
            index = random.randint(1,self.dim-1)
            index2 = random.randint(1,self.dim-1)
            
            self.grid[index,index2] = 1
                    
     
    """Two methods are defined for distance, Moore's and Neumann's, for the sake
       of making it possible to use both"""     
     
    #Method that calculates the number of neighbors for every cell according to Neumann distance,
    #which takes the cells directly to the left, right, up and down directions of the specified cell
    def neighbor_update_neumann(self):
    
        
        for i in range(1,np.size(self.grid, axis=0)-1):
            for j in range(1,np.size(self.grid, axis=1)-1):
                
                count = 0
                
                if self.grid[i,j-1] == 1:
                    count += 1
                if self.grid[i,j+1] == 1:
                    count += 1
                if self.grid[i-1,j] == 1:
                    count += 1
                if self.grid[i+1,j] == 1:
                    count += 1
                
                self.neighbors[i,j] = count
    
    #Method that calculates the number of neighbors for every cell according to Moore's distance,
    #which takes the cells directly to the N,S,W,E,NW,NE,SW,SE directions of the specified cell            
    def neighbor_update_moore(self):
    
        for i in range(1,np.size(self.grid, axis=0)-1):
            for j in range(1,np.size(self.grid, axis=1)-1):
                
                count = 0
                
                if self.grid[i,j-1] == 1:
                    count += 1
                if self.grid[i,j+1] == 1:
                    count += 1
                if self.grid[i-1,j] == 1:
                    count += 1
                if self.grid[i+1,j] == 1:
                    count += 1
                if self.grid[i+1,j+1] == 1:
                    count += 1
                if self.grid[i+1,j-1] == 1:
                    count += 1
                if self.grid[i-1,j+1] == 1:
                    count += 1
                if self.grid[i-1,j-1] == 1:
                    count += 1
                
                self.neighbors[i,j] = count
    
    #Method that updates the original actual grid attribute with a new inputted value produced by conways rules
    def cell_update(self, new_value):
        self.grid = new_value
            
    #String method in case you want to print stuff
    def __str__(self):
        return '{} \n'.format(self.grid) + '{}'.format(self.neighbors)       

"""------------------------------------End of grid class---------------------------------"""

#Method for assigning the rules of conways's game of life. Uses the neighborgrid to create
    #a new output grid which can later be set equal to the actual grid with cell_update method
    #rules are: lower than 2 n_bors = death (0), 2 or 3 neighbors = stay alive(1). 3 neighbors
    #and the value of the actual grid is zero, a cell is "born" (1). However when a cell has 
    #3 neighbors whether it's dead or alive it's value is 1 so no rule is coded for the "born" rule.
    #4 neighbors kills that cell by overpopulation (0).
    
def cell_evolve_conway(n_grid, old_grid):
    
    dim = np.size(n_grid, axis=0)
    for i in range(1, np.size(n_grid, axis=0)-1):
        for j in range(1, np.size(n_grid, axis=1)-1):
            
            if  (n_grid[i,j] == 2 or n_grid[i,j] == 3) and (old_grid[i,j] == 1):
                old_grid[i,j] = 1
            elif (n_grid[i,j] == 3) and (old_grid[i,j] == 0):
                old_grid[i,j] = 1
            else:
                old_grid[i,j] = 0
             
    return old_grid
            

"""---------------------------------------------------------------------------------------------"""
"""--------------------------------------Using the class----------------------------------------"""
"""---------------------------------------------------------------------------------------------"""

#cmap is defined with red and blue for clear viewing
from matplotlib.colors import ListedColormap
cmap = ListedColormap(['b','r'])

#Test grid is initialized with size 200x200
testgrid = Grid(70)

#testgrid is filled randomly with 1000 points, n of points can be changed
testgrid.filler(800)

#Figure is opened for plotting the grid
fig, ax = plt.subplots()

#The grid is plotted for 100 cycles and every figure is saved, number of cycles can be changed by
#changing x in range(x)
for i in range(100):
    
    #neihgbor grid updated
    testgrid.neighbor_update_moore()    

    #actual grid is updated by applying rules of life
    out = cell_evolve_conway(testgrid.neighbors, testgrid.grid)
    testgrid.cell_update(out)
    
    #Matrix outputted as png
    mat = ax.matshow(out, cmap=cmap)
    
    plt.savefig('{}.png'.format(i))


"""---------------------------------------------------------------------------------------------"""
"""--------------------------------------Making an animation------------------------------------"""
"""---------------------------------------------------------------------------------------------"""    

import cv2
import glob
 

"""Set the directory for glob() to the directory where you have saved this script!!!!!"""

img_array = []
for filename in glob.glob(r'C:\Users\HP\Documents\Python Scripts\CellularAutomaton\*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
#Use this to define what the video will be called
outnow = cv2.VideoWriter('conway_new.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
 
for i in range(len(img_array)):
    outnow.write(img_array[i])
outnow.release()
        
    
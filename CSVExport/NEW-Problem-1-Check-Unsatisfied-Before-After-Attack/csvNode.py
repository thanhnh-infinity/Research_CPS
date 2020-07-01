import numpy as np




class csvNode:
    
    def __init__(self):
        
       self.name = None
       self.type = None
       self.parent = []
       self.children = []
       self.lineage = []
       
       self.numVisited = 0 
       
     
       self.level = 0
       self.sum = 0
       
       self.leaf = False
       



import tkinter as tk
from tkinter import *
import numpy as np
import tkinter.font as tkFont
from parse import *
from DCENode import DCENode

spartangreen = "#18453b"
class dependencyCalculatorEntry:
    
    def __init__(self,toBind,owlbase,owlapplication,GUI):
    
    
        self.labelFont = tkFont.Font(family = "Helvetica",size = 30, weight = "bold")
        
        self.boundTo = toBind

        self.owlBase = owlbase
        self.owlApplication = owlapplication
        
        self.GUI = GUI
        
        self.numLHSNodes = 0
        self.numRHSNodes = 0
        
        self.LHSNodes = []
        self.RHSNodes = []
        
        self.showTextLHS = ""
        self.showTextRHS = ""
        
        
        
        self.ifFrame = tk.Frame(self.boundTo,bg = spartangreen)
        self.ifFrame.place(relwidth = .05,relheight = .33, relx = .02,rely = .05)
        
        self.LHSFrame = tk.Frame(self.boundTo, bg = spartangreen)
        self.LHSFrame.place(relwidth = .45, relheight = .90, relx = .08, rely = .05)
        
        self.thenFrame = tk.Frame(self.boundTo, bg = spartangreen)
        self.thenFrame.place(relwidth = .15, relheight = .33, relx = .58, rely = .05)
        
        self.RHSFrame = tk.Frame(self.boundTo, bg = spartangreen)
        self.RHSFrame.place(relwidth = .20, relheight = .90, relx = .75, rely = .05)
        
        self.LHSEntry = Text(self.LHSFrame,width = 50, height = 3)
        self.LHSEntry.pack()
        
        self.RHSEntry = Text(self.RHSFrame, width = 50, height = 3)
        self.RHSEntry.pack()
        
        self.ifButton = Button(self.ifFrame, text = "IF", bg = spartangreen, font = self.labelFont, fg = "white",padx = 20, command = self.onIfClick)
        self.ifButton.pack()
        
        self.thenButton = Button(self.thenFrame, text = "THEN", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onThenClick)
        self.thenButton.pack()
        
        
        self.buttonFrame = tk.Frame(self.boundTo,bg = "grey")
        self.buttonFrame.place(relwidth = .90, relheight = .40, relx = .05, rely = .55)
        
        self.parseLHSB = tk.Button(self.buttonFrame, text = "ParseLHS", padx = 10, height = 1, width = 25, bg = spartangreen, fg = "white",borderwidth = 5, command = self.parseLHS)
        #self.parseLHSB.pack()
        
        self.parseRHSB = tk.Button(self.buttonFrame, text = "ParseRHS", padx = 10, height = 1, width = 25, bg = spartangreen, fg = "white",borderwidth = 5, command = self.parseRHS)
        #self.parseRHSB.pack()
        
        self.createDependencyB = tk.Button(self.buttonFrame, text = "Create Dependency", padx = 10, height = 1, width = 35, bg = spartangreen, fg = "white", borderwidth = 5, command = self.onCreateDependencyB)
        self.createDependencyB.pack()
        
        self.editing = self.LHSEntry
        
    def parseLHS(self):
        
        self.LHSNodes = []
        
        
        LHS_text = self.LHSEntry.get(1.0,END)
        
        LHS_text = LHS_text.replace("\n","")
        
        cleaned_LHS = LHS_text.split(" ")
        
        
        
        cleaned_LHS = list(filter(("and").__ne__, cleaned_LHS))
        cleaned_LHS = list(filter(("").__ne__, cleaned_LHS))
        cleaned_LHS = list(filter((" ").__ne__, cleaned_LHS))
        cleaned_LHS = list(filter(("\n").__ne__, cleaned_LHS))
        
        negated_LHS = []
        
        i = 0
        
        while(i < len(cleaned_LHS)):
            
            negated = False
            
            while(cleaned_LHS[i] == "not"):
                
                if(cleaned_LHS[i] == "not"):
                
                    i = i + 1
                    negated = not negated
                
            new_LHS_node_name = cleaned_LHS[i]
            
            new_node = DCENode()
            
            new_node.name = new_LHS_node_name
            
            new_node.negated = negated
            
            new_node.owlNode = self.findNode(new_node.name)
            
            self.LHSNodes.append(new_node)
            
            i = i + 1
        
            
        
        print("printing")
        
        for node in self.LHSNodes:
            
            print(node.name)
            print(node.negated)
            print()
      
    def parseRHS(self):
         
         self.RHSNodes = []
         
         RHS_text = self.RHSEntry.get(1.0,END)
        
         RHS_text = RHS_text.replace("\n","")
        
         cleaned_RHS = RHS_text.split(" ")
        
        
        
         cleaned_RHS = list(filter(("and").__ne__, cleaned_RHS))
         cleaned_RHS = list(filter(("").__ne__, cleaned_RHS))
         cleaned_RHS = list(filter((" ").__ne__, cleaned_RHS))
         cleaned_RHS = list(filter(("\n").__ne__, cleaned_RHS))
        
         negated_RHS = []
        
         i = 0
        
         while(i < len(cleaned_RHS)):
            
             negated = False
            
             while(cleaned_RHS[i] == "not"):
                
                 if(cleaned_RHS[i] == "not"):
                
                     i = i + 1
                     negated = not negated
                
             new_RHS_node_name = cleaned_RHS[i]
            
             new_node = DCENode()
             
             new_node.name = new_RHS_node_name
            
             new_node.negated = negated
             
             new_node.owlNode = self.findNode(new_node.name)
            
             self.RHSNodes.append(new_node)
            
             i = i + 1
        
            
        
         print("printing")
        
         for node in self.RHSNodes:
            
             print(node.name)
             print(node.negated)
             print()
             
        
    
    def findNode(self,name):

        for node in self.owlBase.allConcerns_owlNode:

            if(node.name == name):

                return node

        for node in self.owlApplication.nodeArray:

            if(node.name == name):

                return node


        print("couldn't find " + str(name))
        return 0
    
    
    def onCreateDependencyB(self):
        
        self.parseLHS()
        
        self.parseRHS()
        
        print("LHSNODES")
        for node in self.LHSNodes:
            print(node.name)
            print(node.owlNode.type)
            print()
        
        print("RHSNODES")
        for node in self.RHSNodes:
            print(node.name)
            print(node.owlNode.type)
            print()
            
        
        self.owlApplication.addNewDependency(self.LHSNodes,self.RHSNodes)
        
        self.GUI.updateTree()
        
    def onIfClick(self):
        self.editing = self.LHSEntry
        
    def onThenClick(self):
        self.editing = self.RHSEntry
        
        
         
         
        

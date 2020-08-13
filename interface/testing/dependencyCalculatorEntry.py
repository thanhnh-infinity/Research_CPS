import tkinter as tk
from tkinter import *
import numpy as np
import tkinter.font as tkFont
from parse import *
from DCENode import DCENode
from parsetest import parseAndCreateRules 
from owlFormula import owlFormula


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
        self.LHSEntry.insert(tk.END,"(")
        
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
        
        print("trying to parse LHS")
        
        
        LHS_text = self.LHSEntry.get(1.0,END)
        
        
        forms = parseAndCreateRules(LHS_text,self.RHSNode.name)
        
        for form in forms:
    
            print(form.name)
            
            for member in form.members:
                print(member)
                
            print(form.operator)
            print()
        self.LHSNodes = forms
      
        
     
        
        
        
        
    def parseRHS(self):
         
         
         
         self.RHS_text = self.RHSEntry.get(1.0,END)
        
         self.RHS_text = self.RHS_text.replace("\n","")
         self.RHS_text = self.RHS_text.replace(" ","")
        
        
         self.RHSNode = self.findNode(self.RHS_text)
         
             
        
    
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
        
        
        
        self.parseRHS()
        
        self.parseLHS()
        
    
    
        
        self.owlApplication.addNewDependency(self.LHSNodes,self.RHSNode)
        
        self.GUI.updateTree()
        
    def onIfClick(self):
        self.editing = self.LHSEntry
        
    def onThenClick(self):
        self.editing = self.RHSEntry
        
        
         
         
        

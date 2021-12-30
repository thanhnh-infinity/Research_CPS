import tkinter as tk
from tkinter import *
import numpy as np
import tkinter.font as tkFont
from parse import *
#from DCENode import DCENode
from parseDependency import parseAndCreateRules
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
        self.ifFrame.place(relwidth = .05,relheight = .20, relx = .02,rely = .09)

        self.LHSFrame = tk.Frame(self.boundTo, bg = spartangreen)
        self.LHSFrame.place(relwidth = .45, relheight = .30, relx = .08, rely = .05)

        self.thenFrame = tk.Frame(self.boundTo, bg = spartangreen)
        self.thenFrame.place(relwidth = .15, relheight = .20, relx = .58, rely = .09)

        self.RHSFrame = tk.Frame(self.boundTo, bg = spartangreen)
        self.RHSFrame.place(relwidth = .20, relheight = .30, relx = .75, rely = .05)

        self.leftPFrame = tk.Frame(self.boundTo, bg = "yellow")
        self.leftPFrame.place(relwidth = .05, relheight = .18, relx = 0.05, rely = .35)

        self.rightPFrame = tk.Frame(self.boundTo, bg = "black")
        self.rightPFrame.place(relwidth = .05, relheight = .18, relx = 0.12, rely = .35)

        self.andFrame = tk.Frame(self.boundTo, bg = "black")
        self.andFrame.place(relwidth = .10, relheight = .18, relx = .22, rely = .35)

        self.orFrame = tk.Frame(self.boundTo, bg = "black")
        self.orFrame.place(relwidth = .10, relheight = .18, relx = .34, rely = .35)


        self.notFrame = tk.Frame(self.boundTo, bg = "black")
        self.notFrame.place(relwidth = .10, relheight = .18, relx = .46, rely = .35)


        self.LHSEntry = Text(self.LHSFrame,width = 50, height = 4)
        self.LHSEntry.pack()
        self.LHSEntry.insert(tk.END,"(")

        self.RHSEntry = Text(self.RHSFrame, width = 50, height = 4)
        self.RHSEntry.pack()

        self.ifButton = Button(self.ifFrame, text = "IF", bg = spartangreen, font = self.labelFont, fg = "white",padx = 20, command = self.onIfClick)
        self.ifButton.pack()

        self.thenButton = Button(self.thenFrame, text = "THEN", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onThenClick)
        self.thenButton.pack()

        self.leftPButton = Button(self.leftPFrame, text = "(", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onLeftPClick)
        self.leftPButton.pack()

        self.rightPButton = Button(self.rightPFrame, text = ")", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onRightPClick)
        self.rightPButton.pack()


        self.andButton = Button(self.andFrame, text = "and", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onAndClick)
        self.andButton.pack()

        self.orButton = Button(self.orFrame, text = "or", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onOrClick)
        self.orButton.pack()

        self.notButton = Button(self.notFrame, text = "not", bg = spartangreen, font = self.labelFont, fg = "white", padx = 20, command = self.onNotClick)
        self.notButton.pack()

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

        #for form in forms:

           # print(form.name)

            #for member in form.members:
                #print(member)

            #print(form.operator)
            #print()
        self.LHSNodes = forms







    def parseRHS(self):



         self.RHS_text = self.RHSEntry.get(1.0,END)

         self.RHS_text = self.RHS_text.replace("\n","")
         self.RHS_text = self.RHS_text.replace(" ","")


         self.RHSNode = self.findNode(self.RHS_text)

    def onAndClick(self):

        lhstext = self.LHSEntry.get(1.0,END)


        if(lhstext[len(lhstext) - 2] == " "):

            self.LHSEntry.insert(INSERT,"and")

        else:

            self.LHSEntry.insert(INSERT," and ")

    def onOrClick(self):

        lhstext = self.LHSEntry.get(1.0,END)

        if(lhstext[len(lhstext) - 2] == " "):

            self.LHSEntry.insert(INSERT,"or")

        else:

            self.LHSEntry.insert(INSERT," or ")

    def onNotClick(self):


        lhstext = self.LHSEntry.get(1.0,END)

        if(lhstext[len(lhstext) - 2] == " "):

            self.LHSEntry.insert(INSERT,"not")

        else:

            self.LHSEntry.insert(INSERT," not ")




    def onLeftPClick(self):


        self.LHSEntry.insert(INSERT,"(")
        #print("(")

    def onRightPClick(self):

        self.LHSEntry.insert(INSERT,")")
        #print(")")

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

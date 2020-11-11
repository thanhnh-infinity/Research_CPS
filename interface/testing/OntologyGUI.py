
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from owlFunctions import is_asp_or_conc
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

from script_networkx import remove_namespace

from dependencyCalculatorEntry import dependencyCalculatorEntry
from owlBase import owlBase
from owlApplication import owlApplication
from owlGraph import owlGraph
import platform

from owlready2 import *
pressed = False
spartangreen = "#18453b"

class OntologyGUI:

    def __init__(self,master):

        
        self.fontStyleTest = tkFont.Font(family="Lucida Grande", size=80, weight = "bold")
        
        self.zoom = 1
        self.zoomIndex = 105
        

        self.lcWindowOpen = False
        self.rcWindowOpen = False
        self.relationWindowOpen = False
        self.dependencyWindowOpen = False
        self.removeConfirmationWindowOpen = False
        self.removeChildrenWindowOpen = False
        self.polarityWindowOpen = False
        self.RLIWindowOpen = False


        self.hoveredNode = None
        self.eventX = None
        self.eventY = None


        self.owlBaseLoaded = False
        self.owlAppLoaded = False
        self.owlApplication = None

        self.allTreeNodes = None


        self.master = master
        self.operatingSystem = platform.system()

        self.buttonWidth = 20
        
        self.outputButtonWidth = 15
        
        if(self.operatingSystem == "Windows"):
            
            print("Dealing with Windows")
            
            self.fontsize = 12
            
            self.fontsize_0_5 = 6
            self.fontsize_1 = 12
            self.fontsize_2 = 22
            self.fontsize_3 = 34
        

            self.buttonFontColor = "white"
            self.buttonBGColor = spartangreen
    
        else:
            
            print("Dealing with Non-Windows OS")
            
            self.fontsize = 8.5
            
            self.fontsize_0_5 = 6
            self.fontsize_1 = 8.5
            self.fontsize_2 = 16
            self.fontsize_3 = 24
        

            self.buttonFontColor = "black"
            self.buttonBGColor = "grey"
            
            
        self.master.bind("<Button-4>", self.handleZoom)
        self.master.bind("<Button-5>", self.handleZoom)
        self.master.bind("<MouseWheel>", self.handleZoom)

        master.title("Ontology GUI")

        #set up main canvas
        self.canvas = Canvas(master, height = 1200, width = 1900, bg = "#18453b")
        self.canvas.pack()

        #set up title text
        self.masterHeaderFrame = Frame(master,bg ="#18453b" )
        self.masterHeaderFrame.place(relwidth = .8, relheight = .06, relx = .1, rely = 0.01)

        self.masterHeaderText = Label(self.masterHeaderFrame, text="CPS Ontology Editor",fg = "white",bg = "#18453b", font = "Helvetica 30 bold italic")
        self.masterHeaderText.pack()

        #set up footer text
        self.footerFrame = Frame(master,bg ="#18453b")
        self.footerFrame.place(relwidth = .4, relheight = .10, relx = .61, rely = 0.98)
        self.footerText = Label(self.footerFrame, text="Matt Bundas, Prof. Son Tran, Thanh Ngyuen, Prof. Marcello Balduccini",fg = "white",bg = "#18453b", font = "Helvetica 8 bold italic", anchor = "e")
        self.footerText.pack()

        #set up frame on left for inputs
        self.leftControlFrame = Frame(master, bg="white")
        self.leftControlFrame.place(relwidth = .2, relheight = .91, relx = .01, rely = 0.07)

        #set up prompt/entry for input ontology
        self.inputBasePrompt = Label(self.leftControlFrame, text = "Input base ontology", font = promptFont,fg= "#747780",bg = "white")
        self.inputBasePrompt.pack()

        self.inputBaseEntry = Entry(self.leftControlFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.inputBaseEntry.pack()
        self.inputBaseEntry.insert(0,"cpsframework-v3-base-development.owl")

        #button to load ontology, calls function which handles loading
        self.loadBaseOntologyB = tk.Button(self.leftControlFrame, text = "Load Base Ontology",padx = 10, pady = 1, width = self.buttonWidth, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5,font = buttonFont,command = self.loadBaseOntology)
        self.loadBaseOntologyB.pack()

        self.addSpace(self.leftControlFrame,"white","tiny")

        self.inputAppPrompt = Label(self.leftControlFrame, text = "Input application ontology", font = promptFont,fg= "#747780",bg = "white")
        self.inputAppPrompt.pack()

        self.inputAppEntry = Entry(self.leftControlFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.inputAppEntry.pack()
        self.inputAppEntry.insert(0,"application_ontologies/cpsframework-v3-sr-LKAS-Configuration-V2-neg.owl")

        #button to load ontology, calls function which handles loading
        self.loadAppOntologyB = tk.Button(self.leftControlFrame, text = "Load Application Ontology",padx = 10, pady = 1, width = self.buttonWidth,bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5,font = buttonFont,command = self.loadAppOntology)
        self.loadAppOntologyB.pack()

        self.unloadAppOntologyB = tk.Button(self.leftControlFrame, text = "Unload Application Ontology")

        self.addSpace(self.leftControlFrame,"white","tiny")


        #sets up prompt/entry for name of output owl file
        self.outputPrompt = Label(self.leftControlFrame, text =  "Output Base Name", font = promptFont,fg= "#747780",bg = "white")
        self.outputPrompt.pack()

        self.outputEntry = Entry(self.leftControlFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.outputEntry.pack()
        self.outputEntry.insert(2, "cpsframework-v3-base-development-xd.owl")

        #sets up button to call function which handles saving ontology
        self.saveOntologyB = tk.Button(self.leftControlFrame, text = "Output Base Ontology",padx = 10, pady = 1, width = self.outputButtonWidth, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5,font = buttonFont, command = self.saveOntology)
        self.saveOntologyB.pack()
        
        
        self.addSpace(self.leftControlFrame,"white","tiny")
        
        #sets up prompt/entry for name of output owl file
        self.outputAppPrompt = Label(self.leftControlFrame, text =  "Output App Name", font = promptFont,fg= "#747780",bg = "white")
        self.outputAppPrompt.pack()
        
        self.outputAppEntry = Entry(self.leftControlFrame, width = 30, borderwidth = 5, highlightbackground = "white", fg = "#18453b", font = entryFont)
        self.outputAppEntry.pack()
        self.outputAppEntry.insert(2, "cpsframework-v3-sr-Elevator-Configuration-dependency-xd.owl")
        
        self.saveAppOntologyB = tk.Button(self.leftControlFrame, text = "Output App Ontology",padx = 10, pady = 1, width = self.outputButtonWidth,bg = "#18453b", fg = self.buttonFontColor, borderwidth = 5, font = buttonFont, command  = self.saveAppOntology)
        self.saveAppOntologyB.pack()
    


        self.addSpace(self.leftControlFrame,"white","tiny")

        self.saveOntologyLaunchASPB = tk.Button(self.leftControlFrame, text = "Output Ontology and Run ASP", padx = 10, pady = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.outputAndLaunchASP)
        #self.saveOntologyLaunchASPB.pack()
        self.addSpace(self.leftControlFrame,"white","tiny")
        #sets up gray box for information window

        self.infoFrame = Frame(self.leftControlFrame, bg = "#747780", bd = 5 )
        self.infoFrame.place(relwidth = .9, relheight = .50, relx = .05, rely = .44)
        
       
        

        self.infoFrameHeaderLabel = Label(self.infoFrame,text = "Ontology Information", font = headerFont, fg = "white", bg = "#747780")
        self.infoFrameHeaderLabel.pack()

        self.owlInfoFrame = Frame(self.infoFrame, bg = spartangreen, bd = 5)
        self.owlInfoFrame.place(relwidth = .94, relheight = .45, relx = .03, rely = .06)

        self.owlInfoFrame.update()
        
       

        self.indInfoHeaderFrame = Frame(self.infoFrame, bg = "#747780",bd = 5)
        self.indInfoHeaderFrame.place(relwidth = .9, relheight = .07, relx  = .05, rely = .525)

        self.indInfoHeaderLabel = Label(self.indInfoHeaderFrame,text = "Hovered Information", font = headerFont, fg = "white", bg = "#747780")
        self.indInfoHeaderLabel.pack()

        self.indInfoFrame = Frame(self.infoFrame,  bg = spartangreen, bd = 5)
        self.indInfoFrame.place(relwidth = .94, relheight = .41, relx = .03, rely = .58)


        self.owlBaseNameText = tk.StringVar()
        self.owlBaseNameText.set("Base")

        self.owlAppNameText = tk.StringVar()
        self.owlAppNameText.set("App")

        self.totalNodeText = tk.StringVar()
        self.totalNodeText.set("Total Nodes")

        self.numAspectsText = tk.StringVar()
        self.numAspectsText.set("Num Aspects")

        self.numConcernsText = tk.StringVar()
        self.numConcernsText.set("Num Concerns")

        self.numPropertiesText = tk.StringVar()
        self.numPropertiesText.set("Num Properties")

        self.numComponentsText = tk.StringVar()
        self.numComponentsText.set("Num Components")


        self.owlBaseNameInfo = Label(self.owlInfoFrame, textvariable =  self.owlBaseNameText, font = "Monaco 12 bold" ,fg= "white",bg = spartangreen)
        self.owlBaseNameInfo.pack()
        

        self.owlAppNameInfo = Label(self.owlInfoFrame, textvariable =  self.owlAppNameText, font = "Monaco 12 bold",fg= "white",bg = spartangreen)
        self.owlAppNameInfo.pack()

        self.numNodesInfo = Label(self.owlInfoFrame, textvariable =  self.totalNodeText, font = infoFont,fg= "white",bg = spartangreen)
        self.numNodesInfo.pack()

        self.numAspectsInfo = Label(self.owlInfoFrame, textvariable =  self.numAspectsText, font = infoFont,fg= "white",bg = spartangreen)
        self.numAspectsInfo.pack()

        self.numConcernsInfo = Label(self.owlInfoFrame, textvariable =  self.numConcernsText, font = infoFont,fg= "white",bg = spartangreen)
        self.numConcernsInfo.pack()

        self.numPropertiesInfo = Label(self.owlInfoFrame, textvariable =  self.numPropertiesText, font = infoFont,fg= "white",bg = spartangreen)
        self.numPropertiesInfo.pack()

        self.numComponentsInfo = Label(self.owlInfoFrame, textvariable =  self.numComponentsText, font = infoFont,fg= "white",bg = spartangreen)
        self.numComponentsInfo.pack()


        self.indNameText = tk.StringVar()
        self.indNameText.set("Name")

        self.indTypeText = tk.StringVar()
        self.indTypeText.set("Type")

        self.indParentText = tk.StringVar()
        self.indParentText.set("Parent Name")

        self.indChildrenText = tk.StringVar()
        self.indChildrenText.set("Children")

        self.indRelPropertiesText = tk.StringVar()
        self.indRelPropertiesText.set("Relevant Properties")

        self.indNameInfo = Label(self.indInfoFrame, textvariable = self.indNameText ,fg= "white",bg = spartangreen,font = infoFont)
        self.indNameInfo.pack()

        self.indTypeInfo = Label(self.indInfoFrame, textvariable = self.indTypeText,fg= "white",bg = spartangreen,font = infoFont)
        self.indTypeInfo.pack()

        self.indParentInfo = Label(self.indInfoFrame, textvariable =  self.indParentText,fg= "white",bg = spartangreen,font = infoFont)
        self.indParentInfo.pack()

        self.indChildInfo = Label(self.indInfoFrame, textvariable =  self.indChildrenText,fg= "white",bg = spartangreen,font = "Monaco 12 bold")
        self.indChildInfo.pack()

        self.indPropertyInfo = Label(self.indInfoFrame, textvariable =  self.indRelPropertiesText,fg= "white",bg = spartangreen,font = infoFont)
        self.indPropertyInfo.pack()


        #sets up gray box to put text to show what is going on
        self.textBoxFrame = Frame(self.leftControlFrame,bg = "#747780", bd = 5)
        self.textBoxFrame.place(relwidth = .9, relheight = .04, relx = .05 ,rely = .95)


        self.summaryText = tk.StringVar()
        self.summaryText.set("")

        self.summaryLabel = Label(self.textBoxFrame, textvariable = self.summaryText, font = summaryFont,fg= "white",bg = "#747780")
        self.summaryLabel.pack()

        #sets up frame for ontology tree to exist
        self.treeFrame = tk.Frame(self.master, bg="white")
        self.treeFrame.place(relwidth = .75, relheight = .91, relx = .22, rely = 0.07)




        self.treeFig, self.treeAxis = plt.subplots(figsize = (15,15))
        self.treeChart = FigureCanvasTkAgg(self.treeFig,self.treeFrame)

        self.treeAxis.clear()
        self.treeAxis.axis('off')
        self.treeChart.get_tk_widget().pack()

        self.treeChart.mpl_connect("button_press_event",self.handleClick)
        self.treeChart.mpl_connect("motion_notify_event",self.handleHover)



        #set up sliders/zoom button in tree frame
        self.xSliderFrame = tk.Frame(self.treeFrame,bg = "white")
        self.xSliderFrame.place(relwidth = .7, relheight = .05, relx = .15, rely = .95)

        self.xSliderScale = Scale(self.xSliderFrame, from_ = 0, to = 100,orient = HORIZONTAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)
        self.xSliderScale.pack()


        self.ySliderFrame = tk.Frame(self.treeFrame,bg = "white")
        self.ySliderFrame.place(relwidth = .03, relheight = .7, relx = .95, rely = .15)

        self.ySliderScale = Scale(self.ySliderFrame, from_ = 80, to = 0,orient = VERTICAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)
        self.ySliderScale.pack()


        self.relationButtonFrame = tk.Frame(self.treeFrame,bg = "white")
        self.relationButtonFrame.place(relwidth = .08, relheight = .05, relx = .01, rely = .01)

        self.relationB = tk.Button(self.relationButtonFrame, text = "Relations",width = 10, padx = 10, pady = 5, bg = spartangreen, fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.onRelationButton)
        self.relationB.pack()
        
        self.dependenciesButtonFrame = tk.Frame(self.treeFrame, bg = "white")
        self.dependenciesButtonFrame.place(relwidth = .08, relheight = .05, relx = .01, rely = .07)

        self.dependenciesB = tk.Button(self.dependenciesButtonFrame, text = "Dependencies", width = 10, padx = 10, pady = 5, bg = spartangreen, fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.onDependencyButton)
        self.dependenciesB.pack()

        self.remremoveChildrenFrame = tk.Frame(self.treeFrame,bg = "white")
        self.remremoveChildrenFrame.place(relwidth = .10, relheight = .05, relx = .89, rely = .01)

        self.removeremoveChildrenB = tk.Button(self.remremoveChildrenFrame, text = "Rem Relationless",padx = 10, pady = 5, bg = spartangreen, fg = self.buttonFontColor,borderwidth = 5, font = buttonFont,  command = self.removeFloaters)
        self.removeremoveChildrenB.pack()


    #loads the specified ontology file in
    def loadBaseOntology(self):

        self.owlBase = owlBase(self.inputBaseEntry.get())

        #self.owlApplication = owlApplication("cpsframework-v3-sr-Elevator-Configuration.owl",self.owlBase)

        #summary = "Loaded base ontology " + "file://./../../src/asklab/querypicker/QUERIES/BASE/" + self.inputBaseEntry.get()
        
        summary = "Loaded base ontology " + "file://./" + self.inputBaseEntry.get()
        self.summaryText.set(summary)


        self.owlBaseLoaded = True
        self.updateTree()


    def loadAppOntology(self):

        self.owlApplication = owlApplication(self.inputAppEntry.get(),self.owlBase)

        summary = "Loaded application ontology " + "file://./application_ontologies" + self.inputAppEntry.get()

        self.summaryText.set(summary)


        self.owlAppLoaded = True
        self.updateTree()
        
     #saves the ontology in rdf format
    def saveOntology(self):

        output_file = self.outputEntry.get()

        self.owlBase.owlReadyOntology.save(file = "./" + output_file, format = "rdfxml")
        #self.owlBase.owlReadyOntology.save(file = output_file, format = "rdfxml")

        #self.processFile(output_file)


        #if(self.owlApplication != None):
          #  self.owlApplication.owlReadyOntology.save(file = "app_" + output_file, format = "rdfxml")
          #  #self.processFile("app_" + output_file)

        summary = "Outputted Base ontology to file: " + output_file
        self.summaryText.set(summary)
        
    def saveAppOntology(self):
        
        if(self.owlApplication == None ):
            return
        
        output_file = self.outputAppEntry.get()
        
        self.owlApplication.owlreadyOntology.save(file = "./" + output_file, format = "rdfxml")
        
        summary = "Outputted Application ontology to file: " + output_file
        self.summaryText.set(summary)
        
    def setAllTreeNodes(self):

        if(self.owlBaseLoaded == True):

            self.allTreeNodes = self.owlBase.allConcerns_owlNode

        if(self.owlAppLoaded == True):



            self.allTreeNodes.extend(self.owlApplication.nodeArray)    
    #checks if an concern with the passed name exists
    def check_existence(self,name):

        for node in self.allTreeNodes:

            if(node.name == name):
                return True

        return False
       
    #clears the tree, re sets up owlBase and graph, draws it
    def updateTree(self):

         self.treeAxis.clear()

         self.treeAxis.axis('off')

         self.owlBase.initializeOwlNodes()
         self.owlBase.setNumbers()

         if(self.owlApplication != None):
             self.owlApplication.initializeOwlNodes()
             self.owlApplication.setNumbers()

         self.owlTree = owlGraph(self.owlBase,self.owlApplication)


         self.scale_tree(3)

         self.owlTree.draw_graph(self.treeAxis,self.fontsize)

         self.treeChart.draw()

         self.updateOwlStats()
         self.setAllTreeNodes()
         
    #changes zoom level, fontsize, then calls updateTree to draw it again
    def handleZoom(self,event):

        print("we be zooming")

        original_zoom = self.zoom

        if event.num == 4 or event.delta < 0:

            if(self.zoomIndex - 1 >= 90):
                self.zoomIndex = self.zoomIndex - 1

        if event.num == 5 or event.delta > 0:

            if(self.zoomIndex + 1 <= 130):
                self.zoomIndex = self.zoomIndex + 1


        if(self.zoomIndex >= 90 and self.zoomIndex < 100):
            self.zoom = .5
            self.fontsize = self.fontsize_0_5 

        elif(self.zoomIndex >= 100 and self.zoomIndex < 110):
            self.zoom = 1
            self.fontsize = self.fontsize_1

        elif(self.zoomIndex >= 110 and self.zoomIndex < 120):
            self.zoom = 2
            self.fontsize = self.fontsize_2

        elif(self.zoomIndex >= 120 and self.zoomIndex < 130):
            self.zoom = 3
            self.fontsize = self.fontsize_3

        if(original_zoom != self.zoom):
            self.updateTree()
   
        
    

    #changes the portion of axis we view according to zoom level, slider position
    def scale_tree(self,var):

         leftmostx = self.owlTree.minX + self.owlTree.totalX*self.xSliderScale.get()/100
         leftmosty = self.owlTree.minY + self.owlTree.totalY*self.ySliderScale.get()/100

         if(self.zoom == .5):

             leftmosty = self.owlTree.minY - .5*self.owlTree.totalY
             rightmosty = self.owlTree.maxY + .5 * self.owlTree.totalY

             rightmostx = leftmostx + .50 * self.owlTree.totalX


         if (self.zoom == 1):
             leftmosty = self.owlTree.minY
             rightmostx = leftmostx + .20*self.owlTree.totalX
             rightmosty = self.owlTree.maxY

         if (self.zoom == 2):

             rightmostx = leftmostx + .10*self.owlTree.totalX
             rightmosty = leftmosty + .60*self.owlTree.totalY

         if (self.zoom == 3):

            
           
             rightmostx = leftmostx + .05*self.owlTree.totalX
             rightmosty = leftmosty + .25*self.owlTree.totalY



         self.treeAxis.set(xlim=(leftmostx, rightmostx), ylim=(leftmosty, rightmosty))

         rmx = rightmostx - leftmostx
         rmy = rightmosty - leftmosty



         self.XYRatio = rmx/rmy
         

         self.treeChart.draw()
         
    def getYLimit(self):

        if(self.zoom == .5):
            return 35
        elif(self.zoom == 1):
            return 20
        elif(self.zoom == 2):
            return 18
        elif(self.zoom == 3):
            return 12


    def getXLimit(self,name):

        base = 4.20*len(name) + 8.6

        if(self.zoom == .5):
            return base*1.95

        elif(self.zoom == 1):

            return base

        elif(self.zoom == 2):

            return base * (.90)

        elif(self.zoom == 3):

            return base * (.75)
        
        #handles the given click event, sends code to either handle relation click, normal left click, or right click event
    
    def getDistance(self,node):
    
         try:
             nodepos = self.owlTree.graphPositions[node.name]

         except:
             return np.inf    
         nodeposx = nodepos[0]
         nodeposy = nodepos[1]*1.0

         distance = np.sqrt((self.eventX - nodeposx)**2 + ((self.eventY - nodeposy)*self.XYRatio)**2)

         return distance


    #takes a mouse event, returns the closest node to the mouse event
    def getNearest(self,event):

        self.eventX = event.xdata
        self.eventY = event.ydata

        self.allTreeNodes.sort(key = self.getDistance)
        
        closest = self.allTreeNodes[0]
        secondclosest = self.allTreeNodes[1]
        thirdclosest = self.allTreeNodes[2]

        closestx = np.abs(self.owlTree.graphPositions[closest.name][0] - self.eventX)
        closesty = np.abs(self.owlTree.graphPositions[closest.name][1] - self.eventY)*self.XYRatio

        secondclosestx = np.abs(self.owlTree.graphPositions[secondclosest.name][0] - self.eventX)
        secondclosesty = np.abs( self.owlTree.graphPositions[secondclosest.name][1] - self.eventY)*self.XYRatio

        thirdclosestx = np.abs(self.owlTree.graphPositions[thirdclosest.name][0] - self.eventX)
        thirdclosesty = np.abs(self.owlTree.graphPositions[thirdclosest.name][1] - self.eventY)*self.XYRatio

        if(closestx < self.getXLimit(closest.name) and closesty < self.getYLimit()):

            #print("returning from first ", closest.name)
            return closest

        elif(secondclosestx < self.getXLimit(secondclosest.name) and secondclosesty < self.getYLimit()):

            #print("returning from second ",secondclosest.name)
            return secondclosest

        elif(thirdclosestx < self.getXLimit(thirdclosest.name) and thirdclosesty < self.getYLimit()):

            #print("returning from third ",thirdclosest.name)
            return thirdcloses

        else:

            #print("returning none")
            return None


    #handles mouse hovering, throws away nonsense events, updates concern info window
    def handleHover(self,event):

        if(self.owlBaseLoaded == False):
            return

        NoneType = type(None)


        if(type(event.xdata) == NoneType or type(event.ydata) == NoneType):
            return

        nearest_node = self.getNearest(event)

        if(nearest_node == None):


            self.indNameText.set("Name")
            self.indTypeText.set("Type")
            self.indParentText.set("Parent Name")
            self.indChildrenText.set("Children")
            self.indRelPropertiesText.set("Relevant Properties")

            self.hoveredNode = None

            return

        if(nearest_node != self.hoveredNode):


            self.hoveredNode = nearest_node
            self.indNameText.set("Name - " + str(self.hoveredNode.name))
            self.indTypeText.set("Type - " + str(self.hoveredNode.type))

            parentString = "Parents -"


            i = 1
            for parent in self.hoveredNode.parents:

                if(i%2 == 0):
                    parentString = parentString + "\n" + parent.name

                else:
                    parentString = parentString + " " + parent.name

                i = i + 1

            self.indParentText.set(parentString)


            childString = "Children -"

            nchildren = len(self.hoveredNode.children)
            
            if(nchildren >= 10):
                divisor = 3
            else:
                divisor = 2

            i = 1
            for child in self.hoveredNode.children:
 
                if(len(child.name) >= 25):
                  
                    childString = childString + "\n" + child.name + "\n"   
                
                elif(i % divisor == 0):
                    childString = childString + "\n" + child.name

                else:
                    childString = childString + " " + child.name

                i = i + 1
                
            self.indChildInfo.configure(font = "Monaco " + str(self.getChildFS(nchildren)) + " bold")
            self.indChildrenText.set(childString)
            self.indRelPropertiesText.set("Relevant Properties - ")
           
    def getChildFS(self,n):
        
        if(n >= 10):
            return 7
        
        elif(n >= 8):
            return 9
        
        elif(n >= 6):
            return 10
        elif(n >= 4):
            return 11
        else:
            return 12

                
            
    def getCorrFS(self,text):
        
     
        n = len(text)
        
        if (n > 43):
            return 7
        elif (n > 37):
            return 9
        elif (n > 33):
            return 10
        elif (n > 30):
            return 11
        else:
            return 12
        


    #updates the global ontology stats according to numbers stored in owlBase
    def updateOwlStats(self):

            self.totalNodes = self.owlBase.numNodes
        
            text = "Base-" + str(self.owlBase.owlName)
            
            basefs = self.getCorrFS(text)
            
            
                
            if(basefs <= 8):
                    
                textlen = int(len(text)/2)
                
                text = text[ : textlen] + "\n" + text[textlen : ]
                    
                    
                    
                basefs = 10
        
            
    
            self.owlBaseNameInfo.configure(font = "Monaco " + str(basefs) + " bold")
            self.owlBaseNameText.set(text)
        
            self.numAspectsText.set("Num Aspects - " + str(self.owlBase.numAspects))
            self.numConcernsText.set("Num Concerns - "  + str(self.owlBase.numConcerns))

            if(self.owlAppLoaded == True):

                textapp = "App-" + str(self.owlApplication.owlName)
                
                appfs = self.getCorrFS(textapp)
                
                if(appfs <= 8):
                    
                    textlen = int(len(textapp)/2)
                    
                    textapp = textapp[ : textlen] + "\n" + textapp[textlen : ]
                    
                    
                    
                    appfs = 10
                
                self.owlAppNameInfo.configure(font = "Monaco " + str(appfs) + " bold")
                
                self.owlAppNameText.set(textapp)
                
                
                self.numPropertiesText.set("Num Properties - " + str(self.owlApplication.numProperties))
                self.numComponentsText.set("Num Components - " + str(self.owlApplication.numComponents))

                self.totalNodes = self.totalNodes + self.owlApplication.numNodes

            self.totalNodeText.set("Num Nodes - " + str(self.totalNodes))


    def handleClick(self,event):

        if(event.button == 1):

            if(self.relationWindowOpen == True):
                self.handleRelationLeftClick(event)
            
            elif(self.dependencyWindowOpen == True):
                self.handleDependencyClick(event)
            else:
                self.onLeftClick(event)

        elif(event.button == 3):
            
            if(self.dependencyWindowOpen == True):
                
                self.handleDependencyClick(event)
            else:
                self.onRightClick(event)
                
    def handleEmptyLeftClick(self):
        
        if(self.RLIWindowOpen == True or self.owlBaseLoaded == False):
            
            print(self.RLIWindowOpen)
            print(self.owlBaseLoaded)
            print("returning")
            return
        
        self.errorDisplayed = False
    
        self.RLIWindow = tk.Toplevel(height = 500, width = 400, bg = spartangreen)
        self.RLIWindow.transient(master = self.master)
        
        self.RLIWindowOpen = True
        self.RLIWindow.title("Add Individual")
        
        self.RLIWindow.protocol("WM_DELETE_WINDOW",self.RLIWindowClose)
        
        self.RLIWindowHeaderFrame = tk.Frame(self.RLIWindow,bg = spartangreen)
        self.RLIWindowHeaderFrame.place(relwidth = .7, relheight = .12, relx = .15, rely = .01)
        
        self.RLIWindowHeaderText = Label(self.RLIWindowHeaderFrame, text = "Add New \nIndividual",font = headerFont, fg = "white", bg = spartangreen)
        self.RLIWindowHeaderText.pack()
        
        self.RLIButtonFrame = Frame(self.RLIWindow, bg = "white")
        self.RLIButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)
        
        self.RLIPrompt = Label(self.RLIButtonFrame, text = "Name of New Node", font = promptFont, fg = "#747780", bg = "white")
        self.RLIPrompt.pack()
        
        self.RLIEntry = Entry(self.RLIButtonFrame, width = 30, borderwidth = 5, highlightbackground = "white", fg = spartangreen,font = entryFont)
        self.RLIEntry.pack()
        self.RLIEntry.insert(1,"NewNode")
        
        self.addSpace(self.RLIButtonFrame,"white","tiny")

        addAspectB = tk.Button(self.RLIButtonFrame, text = "Add Aspect",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15 ,font = buttonFont, command = self.addRLAspect)
        addAspectB.pack()
        
        self.addSpace(self.RLIButtonFrame,"white","tiny")
        
        addConcernB = tk.Button(self.RLIButtonFrame, text = "Add Concern", padx = 5, bg = "#18453b", fg = self.buttonFontColor, borderwidth = 5, width = 15, font = buttonFont, command = self.addRLConcern)
        addConcernB.pack()
        
        self.addSpace(self.RLIButtonFrame,"white","tiny")

        addPropertyB = tk.Button(self.RLIButtonFrame, text = "Add Property",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15 ,font = buttonFont, command = self.addRLProperty)
        addPropertyB.pack()

        self.addSpace(self.RLIButtonFrame,"white","tiny")

        addCompB = tk.Button(self.RLIButtonFrame, text = "Add Component",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addRLComponent)
        addCompB.pack()

        
    def addRLAspect(self):
        
        self.owlBase.addNewAspect(self.RLIEntry.get())
        
        self.updateTree()
        
       
        
    def addRLConcern(self):
        
        self.owlBase.addNewRLConcern(self.RLIEntry.get())
        
        self.updateTree()
        
      
        
    def addRLProperty(self):
        
       
        
        self.owlApplication.addRLProperty(self.RLIEntry.get())
        
        self.updateTree()
        
      
        
    def addRLIR(self):
        
        self.launchPolarityWindow()
        self.addIRPolarity()
        
        self.addingRelation = "RLIR"
                
        
    def addRLComponent(self):
        
        self.owlApplication.addNewComponent(self.RLIEntry.get())
        
        self.updateTree()
        
       
        
    def RLIWindowClose(self):
        
    
        print("called close")
        
        self.RLIWindow.destroy()    
        self.RLIWindowOpen = False


    #handles opening left click window, where you can edit clicked concerns
    def onLeftClick(self,event):

        print("got left click")
        
        if(self.lcWindowOpen == True or self.owlBaseLoaded == False):
            
            print("not doing anything")
            return

        self.errorDisplayed = False

        #get the node you just clicked on
        closestnode = self.getNearest(event)

        if(closestnode == None):
            
            print("in if ")
            self.handleEmptyLeftClick()
            return

        self.leftClicked = closestnode

        #open up window and frames
        self.lcWindow = tk.Toplevel(height = 500, width = 400,bg = spartangreen )
        self.lcWindow.transient(master = self.master)

        self.lcWindowOpen = True
        self.lcWindow.title("Concern Editor")
        self.lcWindow.protocol("WM_DELETE_WINDOW", self.leftclickWindowClose)

        self.lcWindowHeaderFrame = tk.Frame(self.lcWindow,bg = spartangreen)
        self.lcWindowHeaderFrame.place(relwidth = .7, relheight = .12, relx = .15, rely = .01)

        self.lcButtonFrame = tk.Frame(self.lcWindow, bg = "white")
        self.lcButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)

        type_item = self.leftClicked.type


        self.lcWindowHeaderText = tk.StringVar()
        self.lcWindowHeaderText.set(self.leftClicked.name + "\n" + self.leftClicked.type)


        self.lcWindowHeaderLabel = Label(self.lcWindowHeaderFrame, textvariable = self.lcWindowHeaderText ,fg= "white",bg = spartangreen,font = headerFont)
        self.lcWindowHeaderLabel.pack()
        
        
        self.indivNamePrompt = Label(self.lcButtonFrame, text = "Name of New Node", font = promptFont,fg= "#747780",bg = "white")
        self.indivNamePrompt.pack()

        self.indivNameEntry = Entry(self.lcButtonFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.indivNameEntry.pack()
        self.indivNameEntry.insert(1,"NewNode")

        self.addSpace(self.lcButtonFrame,"white","tiny")

        if(is_asp_or_conc(self.leftClicked.type) == True):

            self.concernLeftClick(event)

        elif(self.leftClicked.type == "Component"):

            self.componentLeftClick(event)

        elif(self.leftClicked.type == "Property"):

            self.propertyLeftClick(event)

        elif(self.leftClicked.type == "Formula"):
            
            self.formulaLeftClick(event)
            
        elif(self.leftClicked.type == "DecompositionFunction"):
            
            self.decompFuncLeftClick(event)

        else:

            print("Not sure what type that was")

            return
        
        
    def concernLeftClick(self,event):


        #set up buttons for operations
        addConcern = tk.Button(self.lcButtonFrame, text = "Add Subconcern",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addConcern)
        addConcern.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        addParent = tk.Button(self.lcButtonFrame, text = "Add Parent Concern",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15 ,font = buttonFont, command = self.addParent)
        addParent.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        addPropertyB = tk.Button(self.lcButtonFrame, text = "Add Property",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addPropertyAsChildofConcern)
        addPropertyB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        editName = tk.Button(self.lcButtonFrame, text = "Edit Name",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.editConcern)
        editName.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        removeConcernB = tk.Button(self.lcButtonFrame, text = "Delete",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.removeConcern)
        removeConcernB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")



    #adds a concern to the ontology, uses gui entries for inputs, updates tree afterwards
    def addConcern(self):


        #grab name of new concern
        new_concern_name = self.indivNameEntry.get()

        #handle error message, if new concern with name already exists, don't add another
        if (self.handleErrorMessage(new_concern_name,"lc") == 0):
            return


        self.owlBase.addNewConcern(new_concern_name,self.leftClicked.name)

        #prints text in textBoxFrame to tell what happend
        summary = "Added concern " + new_concern_name + " to ontology"

        self.summaryText.set(summary)

        #refresh the tree and owlBase
        self.updateTree()

        #reset the error message because we just did a successful operation
        self.handleErrorMessageDeletion("lc")
       
        
    #function to add parent to clicked node
    def addParent(self):

        #get name from Entry
        new_parent_name = self.indivNameEntry.get()

        #handle error message, if new concern with name already exists, don't add another
        if (self.handleErrorMessage(new_parent_name,"lc") == 0):
            return

        self.owlBase.addConcernAsParent(new_parent_name,self.leftClicked.name)

        summary = "Added " + new_parent_name + " as Parent of " + self.leftClicked.name
        self.summaryText.set(summary)

        self.handleErrorMessageDeletion("lc")

        self.updateTree()

    
    def addPropertyAsChildofConcern(self):
        
        new_property_name = self.indivNameEntry.get()
        
        if (self.handleErrorMessage(new_property_name,"lc") == 0):
            return
        
        self.owlApplication.addPropertyAsChildofConcern(self.leftClicked,new_property_name)
        
        self.handleErrorMessageDeletion("lc")
        
        self.updateTree()
    
    #handles editing an concern
    def editConcern(self):

        #adds concern in
        new_name = self.indivNameEntry.get()
        old_name = self.leftClicked.name
        ind_type = self.leftClicked.type

        if (self.handleErrorMessage(new_name,"lc") == 0):
            return

        #change name of olwready object

        self.owlBase.editName(self.leftClicked,new_name)

        summary = "Changed name of " + old_name + " to " + new_name
        self.summaryText.set(summary)

        self.updateTree()
        self.lcWindowHeaderText.set(new_name + "\n" + ind_type)
        self.handleErrorMessageDeletion("lc")
        
    #handles removing concern left clicked on
    def removeConcern(self):


        #check if there will be removeChildren if you delete node
        nodesChildren = self.owlBase.getChildren(self.leftClicked)

        #if it wouldn't create any removeChildren, just delete it
        if(len(nodesChildren) == 0):

            self.owlBase.removeConcern(self.leftClicked)
            self.updateTree()


            summary = "Removed " + self.leftClicked.name
            self.summaryText.set(summary)
            self.leftclickWindowClose()

        #if deletion would create removeChildren, ask if they want to delete all of the removeChildren
        else:

            self.removeChildrenWindow = tk.Toplevel(height = 250, width = 600, bg = spartangreen)
            #self.removeChildrenWindow.transient(master = self.lcWindow)
            self.lcWindow.withdraw()


            self.removeChildrenWindowOpen = True

            self.removeChildrenWindow.title("Remove Children")

            self.removeChildrenWindow.protocol("WM_DELETE_WINDOW",self.removeChildrenWindowClose)

            self.removeChildrenWindowHeaderFrame = tk.Frame(self.removeChildrenWindow,bg = spartangreen)
            self.removeChildrenWindowHeaderFrame.place(relwidth = .7, relheight = .1, relx = .15, rely = .01)

            self.removeChildrenButtonFrame = tk.Frame(self.removeChildrenWindow, bg = "white")
            self.removeChildrenButtonFrame.place(relwidth = .7, relheight = .825, relx = .15, rely = .13)


            self.removeChildrenWindowHeaderText = tk.StringVar()
            self.removeChildrenWindowHeaderText.set("Choose a Deletion Option")


            self.removeChildrenWindowHeaderLabel = Label(self.removeChildrenWindowHeaderFrame, textvariable = self.removeChildrenWindowHeaderText ,fg= "white",bg = spartangreen,font = headerFont)
            self.removeChildrenWindowHeaderLabel.pack()

            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")

            deleteSelectedB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Selected Only", bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, padx = 5, height = 1, width = 40,font = buttonFont, command = self.removeSingleConcern)
            deleteSelectedB.pack()
            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")

            deleteSelectedRelationlessChildrenB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Selected + Resulting Relationless Children",padx = 5, height = 1, width = 40, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.handleRemoveIndAndRelationless)
            deleteSelectedRelationlessChildrenB.pack()

            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")

            deleteSelectedAllChildrenB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Selected + All Children", bg = "#18453b",padx = 5, height = 1, width = 40, fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.handleRemoveAllChildren)
            deleteSelectedAllChildrenB.pack()

            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")

            #deleteIndB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Concern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeSingleConcern)
            #deleteIndB.pack()

            cancelB = tk.Button(self.removeChildrenButtonFrame, text = "Cancel",padx = 5, height = 1, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.cancelDelete)
            cancelB.pack()

            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")

    def propertyLeftClick(self,event):
        
        editName = tk.Button(self.lcButtonFrame, text = "Edit Name",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.editPropertyName)
        editName.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        removeConcernB = tk.Button(self.lcButtonFrame, text = "Delete",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.removeConcern)
        removeConcernB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")
        
    def editPropertyName(self):

        new_name = self.indivNameEntry.get()
        old_name = self.leftClicked.name
        ind_type = self.leftClicked.type

        if (self.handleErrorMessage(new_name,"lc") == 0):
            return

        #change name of olwready object

        self.owlApplication.editPropertyName(self.leftClicked,new_name)

        summary = "Changed name of " + old_name + " to " + new_name
        self.summaryText.set(summary)
        
        self.updateTree()
        self.handleErrorMessageDeletion("lc")
        self.lcWindowHeaderText.set(new_name + "\n" + ind_type)
    def formulaLeftClick(self,event):
        
        self.addSpace(self.lcButtonFrame,"white","tiny")

        #set up buttons for operations
        addChildPropertyB = tk.Button(self.lcButtonFrame, text = "Add Child Property",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addFormulaChildProperty)
        addChildPropertyB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        switchToDecompFuncB = tk.Button(self.lcButtonFrame, text = "Switch to Functional Decomp",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.switchToDecompFunc)
        #switchToDecompFuncB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        editNameB = tk.Button(self.lcButtonFrame, text = "Edit Name",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.editFormulaName)
        editNameB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        removeFormulaB = tk.Button(self.lcButtonFrame, text = "Delete",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.removeConcern)
        removeFormulaB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")
        
        
    def addFormulaChildProperty(self):
        
        newprop_name = self.indivNameEntry.get()
        
        if (self.handleErrorMessage(new_property_name,"lc") == 0):
            return
        
        self.owlApplication.addNewPropertyToFormula(self.leftClicked,newprop_name)
        
        self.handleErrorMessageDeletion("lc")
        self.updateTree()
        
    def switchToDecompFunc(self):
        
    
        formula_owlready = self.leftClicked.owlreadyObj
        formula_owlready.is_a.append(self.owlApplication.owlreadyOntology.DecompositionFunction)
        self.updateTree() 
        
        
    def editFormulaName(self):
        
        new_name = self.indivNameEntry.get()
        old_name = self.leftClicked.name
        ind_type = self.leftClicked.type


        if (self.handleErrorMessage(new_name,"lc") == 0):
            return
        
        
        self.owlApplication.editFormulaName(self.leftClicked,new_name)
        
        summary = "Changed name of " + old_name + " to " + new_name
        self.summaryText.set(summary)

        self.updateTree()
        self.lcWindowHeaderText.set(new_name + "\n" + ind_type)
        self.handleErrorMessageDeletion("lc")
     
        
        
    def decompFuncLeftClick(self,event):
        
        #set up buttons for operations
        addChildPropertyB = tk.Button(self.lcButtonFrame, text = "Add Child Property",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addDecompFuncChildProperty)
        addChildPropertyB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        switchToFormulaB = tk.Button(self.lcButtonFrame, text = "Switch to Formula",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.switchToFormula)
        #switchToFormulaB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        editNameB = tk.Button(self.lcButtonFrame, text = "Edit Name",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.editDecompFuncName)
        editNameB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        removeDecompFuncB = tk.Button(self.lcButtonFrame, text = "Delete",padx = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.removeConcern)
        removeDecompFuncB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")
        
    def addDecompFuncChildProperty(self):
        
        newprop_name = self.indivNameEntry.get()
        
        if (self.handleErrorMessage(newprop_name,"lc") == 0):
            return
        
        self.owlApplication.addNewPropertyToFormula(self.leftClicked,newprop_name)
        
        self.handleErrorMessageDeletion("lc")
        self.updateTree()
    
        
    def switchToFormula(self):
        
        decompfunc_owlready = self.leftClicked.owlreadyObj
        decompfunc_owlready.is_a.remove(self.owlApplication.owlreadyOntology.DecompositionFunction)
        self.updateTree()
        
        
     
    def editDecompFuncName(self):
        
        new_name = self.indivNameEntry.get()
        old_name = self.leftClicked.name
        ind_type = self.leftClicked.type

        if (self.handleErrorMessage(new_name,"lc") == 0):
            return

        self.owlApplication.editFormulaName(self.leftClicked,new_name)
        
        summary = "Changed name of " + old_name + " to " + new_name
        self.summaryText.set(summary)

        self.updateTree()
        self.lcWindowHeaderText.set(new_name + "\n" + ind_type)
        self.handleErrorMessageDeletion("lc")
         
    def componentLeftClick(self,event):

        #set up buttons for operations
        addParentB = tk.Button(self.lcButtonFrame, text = "Add Parent Property",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addParentProperty)
        addParentB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        editNameB = tk.Button(self.lcButtonFrame, text = "Edit Name",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.editComponent)
        editNameB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

        removeComponentB = tk.Button(self.lcButtonFrame, text = "Delete",padx = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.removeConcern)
        removeComponentB.pack()

        self.addSpace(self.lcButtonFrame,"white","tiny")

    def addParentProperty(self):

        new_parent_name = self.indivNameEntry.get()

        #handle error message, if new concern with name already exists, don't add another
        if (self.handleErrorMessage(new_parent_name,"lc") == 0):
            return

        self.owlApplication.addPropertyAsParentofComponent(new_parent_name,self.leftClicked)

        summary = "Added " + new_parent_name + " as Parent of " + self.leftClicked.name
        self.summaryText.set(summary)

        self.handleErrorMessageDeletion("lc")

        self.updateTree()
        

   
    def editComponent(self):

        new_name = self.indivNameEntry.get()
        old_name = self.leftClicked.name
        ind_type = self.leftClicked.type

        if (self.handleErrorMessage(new_name,"lc") == 0):
            return
        
        self.owlApplication.editComponentName(self.leftClicked,new_name)

        summary = "Changed name of " + old_name + " to " + new_name
        self.summaryText.set(summary)
        
        self.updateTree()
        self.lcWindowHeaderText.set(new_name + "\n" + ind_type)
        self.handleErrorMessageDeletion("lc")
      
    def handleErrorMessage(self,new_name,frame):

        if(frame == "lc"):

            if(self.check_existence(new_name) == True):
               print("Individual Already Exists\n in Ontology")
               if(self.errorDisplayed == True):
                   self.error_message.destroy()
               self.error_message = Label(self.lcButtonFrame, text = "Individual Already Exists\n in Ontology", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
               self.error_message.pack()
               self.errorDisplayed = True
               return 0

        if(frame == "rc"):
            if(self.check_existence(new_name) == True):
               print("Individual Already Exists\n in Ontology")
               if(self.rcErrorDisplayed == True):
                   self.rcerror_message.destroy()
               self.rcerror_message = Label(self.rcButtonFrame, text = "Individual Already Exists\n in Ontology", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
               self.rcerror_message.pack()
               self.rcErrorDisplayed = True
               return 0

    
        
        
    def handleErrorMessageDeletion(self,frame):

        if(frame == "lc"):

            if(self.errorDisplayed == True):
                self.error_message.destroy()
                self.errorDisplayed == False

        if(frame == "rc"):
            if(self.rcErrorDisplayed == True):
                self.rcerror_message.destroy()
                self.rcErrorDisplayed == False


   
   
    #handles closing concern editor window
    def leftclickWindowClose(self):

        self.lcWindowOpen = False
        self.leftClicked = None

        if(self.removeChildrenWindowOpen == True):
            self.removeChildrenWindowClose()

        if(self.removeConfirmationWindowOpen == True):
            self.removeConfirmationWindowClose()

        self.lcWindow.destroy()        
     

    def removeChildrenWindowClose(self):


        self.removeChildrenWindowOpen = False

        if(self.lcWindow.state() == "withdrawn"):
            self.lcWindow.deiconify()

        self.removeChildrenWindow.destroy()


    def removeConfirmationWindowClose(self):

        self.removeConfirmationWindowOpen = False

        if(self.removeChildrenWindow.state() == "withdrawn"):
            self.removeChildrenWindow.deiconify()

        self.removeConfirmationWindow.destroy()
        
    def removeSingleConcern(self):

        self.owlBase.removeConcern(self.leftClicked)

        self.removeChildrenWindowClose()
        self.leftclickWindowClose()

        self.updateTree()


    def handleRemoveAllChildren(self):

        if(self.removeConfirmationWindowOpen == True):
            return

        all_node_children = self.owlBase.getChildren(self.leftClicked)

        self.removeConfirmationWindow = tk.Toplevel(height = 700, width = 400, bg = spartangreen)
        #self.removeConfirmationWindow.transient(master = self.removeChildrenWindow)

        self.lcWindow.withdraw()
        self.removeChildrenWindow.withdraw()

        self.removeConfirmationWindowOpen = True

        self.removeConfirmationWindow.title("Remove Confirmation")
        self.removeConfirmationWindow.protocol("WM_DELETE_WINDOW",self.removeConfirmationWindowClose)


        self.removeConfirmationWindowHeaderFrame = tk.Frame(self.removeConfirmationWindow,bg = spartangreen)
        self.removeConfirmationWindowHeaderFrame.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)

        self.removeConfirmationButtonFrame = tk.Frame(self.removeConfirmationWindow, bg = "white")
        self.removeConfirmationButtonFrame.place(relwidth = .7, relheight = .85, relx = .15, rely = .08)


        self.removeConfirmationWindowHeaderText = tk.StringVar()
        self.removeConfirmationWindowHeaderText.set("This operation will delete the following nodes:")

        self.removeConfirmationWindowHeaderLabel = Label(self.removeConfirmationWindowHeaderFrame, textvariable = self.removeConfirmationWindowHeaderText ,fg= "white",bg = spartangreen,font = promptFont)
        self.removeConfirmationWindowHeaderLabel.pack()

        toDeleteLabel = Label(self.removeConfirmationButtonFrame,text = self.leftClicked.name,fg= "gray",bg = "white",font = promptFont)
        toDeleteLabel.pack()

        for node in all_node_children:

            toDeleteLabel = Label(self.removeConfirmationButtonFrame,text = node.name,fg= "gray",bg = "white",font = promptFont)
            toDeleteLabel.pack()


        self.removeConfirmationQuestionLabel = Label(self.removeConfirmationButtonFrame,text = "Would you like to Remove these?")
        self.removeConfirmationQuestionLabel.pack()


        self.addSpace(self.removeConfirmationButtonFrame,"white","tiny")

        yesB = tk.Button(self.removeConfirmationButtonFrame, text = "Yes",padx = 10, pady = 5, width = 10, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.removeAllChildren)
        yesB.pack()

        self.addSpace(self.removeConfirmationButtonFrame,"white","tiny")
        noB = tk.Button(self.removeConfirmationButtonFrame, text = "No",padx = 10, pady = 5, width = 10, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.removeConfirmationWindowClose)
        noB.pack()




    def removeAllChildren(self):

        all_node_children = self.owlBase.getChildren(self.leftClicked)

        for node in all_node_children:
                print("removing " + node.name)
                self.owlBase.removeConcern(node)

        self.owlBase.removeConcern(self.leftClicked)

        self.removeConfirmationWindowClose()
        self.removeChildrenWindowClose()
        self.leftclickWindowClose()
        self.updateTree()



    def removeIndAndRelationless(self):

        soonToBeRelationless = self.owlBase.getRelationless(self.leftClicked)

        for node in soonToBeRelationless:
                print("removing " + node.name)
                self.owlBase.removeConcern(node)

        self.owlBase.removeConcern(self.leftClicked)

        self.removeConfirmationWindowClose()
        self.removeChildrenWindowClose()
        self.leftclickWindowClose()
        self.updateTree()


    def handleRemoveIndAndRelationless(self):

        if(self.removeConfirmationWindowOpen == True):
            return

        all_node_relationless_children = self.owlBase.getRelationless(self.leftClicked)

        self.removeConfirmationWindow = tk.Toplevel(height = 600, width = 400, bg = spartangreen)
        self.removeConfirmationWindow.transient(master = self.removeChildrenWindow)

        self.removeConfirmationWindowOpen = True

        self.removeConfirmationWindow.title("Remove Confirmation")
        self.removeConfirmationWindow.protocol("WM_DELETE_WINDOW",self.removeConfirmationWindowClose)


        self.removeConfirmationWindowHeaderFrame = tk.Frame(self.removeConfirmationWindow,bg = spartangreen)
        self.removeConfirmationWindowHeaderFrame.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)

        self.removeConfirmationButtonFrame = tk.Frame(self.removeConfirmationWindow, bg = "white")
        self.removeConfirmationButtonFrame.place(relwidth = .7, relheight = .85, relx = .15, rely = .08)


        self.removeConfirmationWindowHeaderText = tk.StringVar()
        self.removeConfirmationWindowHeaderText.set("This operation will delete the following nodes:")

        self.removeConfirmationWindowHeaderLabel = Label(self.removeConfirmationWindowHeaderFrame, textvariable = self.removeConfirmationWindowHeaderText ,fg= "white",bg = spartangreen,font = infoFont)
        self.removeConfirmationWindowHeaderLabel.pack()


        toDeleteLabel = Label(self.removeConfirmationButtonFrame,text = self.leftClicked.name,fg= "gray",bg = "white",font = promptFont)
        toDeleteLabel.pack()

        for node in all_node_relationless_children:

            toDeleteLabel = Label(self.removeConfirmationButtonFrame,text = node.name,fg= "gray",bg = "white",font = promptFont)
            toDeleteLabel.pack()


        self.removeConfirmationQuestionLabel = Label(self.removeConfirmationButtonFrame,text = "Would you like to Remove these?")
        self.removeConfirmationQuestionLabel.pack()

        yesB = tk.Button(self.removeConfirmationButtonFrame, text = "Yes",padx = 10, pady = 5, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.removeIndAndRelationless)
        yesB.pack()

        noB = tk.Button(self.removeConfirmationButtonFrame, text = "No",padx = 10, pady = 5, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.removeConfirmationWindowClose)
        noB.pack()


    def cancelDelete(self):

        self.removeChildrenWindowClose()

    #takes care of right clicks, opens up window where you can add a new aspect
    def onRightClick(self,event):


        if(self.owlBaseLoaded == False or self.rcWindowOpen == True):
            return

        #set up windows and frames
        self.rcWindow = tk.Toplevel(height = 500, width = 400, bg = spartangreen)
        self.rcWindow.title("Right Click Window")
        self.rcWindow.protocol("WM_DELETE_WINDOW", self.rcWindowClose)

        self.rcErrorDisplayed = False

        self.rcWindowFrame = tk.Frame(self.rcWindow,bg = spartangreen)
        self.rcWindowFrame.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)

        self.rcButtonFrame = tk.Frame(self.rcWindow, bg = "white")
        self.rcButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)

    #handles closing right click window
    def rcWindowClose(self):

        self.rcWindow.destroy()
        self.rcWindowOpen = False
        self.rightClicked = None
        
        
    #function to handle when you click Relations button, opens up window where you can do relation operations
    def onRelationButton(self):

        if(self.relationWindowOpen == True):
            return

        #set up window and frames
        self.relationWindow = tk.Toplevel(height = 500, width = 400, bg = spartangreen)
        self.relationWindow.transient(master = self.master)
        self.relationWindow.title("Add New Relation")

        self.relationWindowOpen = True
        self.readyForRelationButton = False
        self.relationClickSelecting = "Parent"
        self.relationWindow.protocol("WM_DELETE_WINDOW", self.relationWindowClose)

        self.relationWindowFrame = tk.Frame(self.relationWindow,bg = spartangreen)
        self.relationWindowFrame.place(relwidth = .8, relheight = .20, relx = .10, rely = .01)

        showtext = "Add New Relation \nClick on Desired Parent \nThen Click on Desired Child"

        self.relationWindowHeader = Label(self.relationWindowFrame, text = showtext,fg= "white",bg = spartangreen,font = headerFont)
        self.relationWindowHeader.pack()

        self.relationButtonFrame = tk.Frame(self.relationWindow, bg = "white")
        self.relationButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .20)

        self.addSpace(self.relationButtonFrame,"white","tiny")


        self.relationParentText = tk.StringVar()
        self.relationParentText.set("Relation Parent - ")

        self.relationChildText = tk.StringVar()
        self.relationChildText.set("Relation Child - ")

        self.relationParentLabel = Label(self.relationButtonFrame, textvariable = self.relationParentText, font = promptFont,fg= "#747780",bg = "white")
        self.relationParentLabel.pack()

        self.relationChildLabel = Label(self.relationButtonFrame, textvariable = self.relationChildText, font = promptFont,fg= "#747780",bg = "white")
        self.relationChildLabel.pack()


        self.addSpace(self.relationButtonFrame,"white","tiny")
        #add buttons for adding subconcern, addresses, remove relation
        addRelationB = tk.Button(self.relationButtonFrame, text = "Add Relation",padx = 10, height = 1, width = 25, bg = "#18453b",fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.addRelation)
        addRelationB.pack()

        self.addSpace(self.relationButtonFrame,"white","tiny")

        #addAddressesConcernRelationB = tk.Button(self.relationButtonFrame, text = "Add Property Addresses Relation",padx = 10, height = 1, width = 25, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.addAddressesConcernRelation)
        #addAddressesConcernRelationB.pack()
        #self.addSpace(self.relationButtonFrame,"white","tiny")

        removeRelationB = tk.Button(self.relationButtonFrame, text = "Remove Relation",padx = 10, height = 1, width = 25, bg = "#18453b", fg = self.buttonFontColor,borderwidth = 5, font = buttonFont, command = self.removeRelation)
        removeRelationB.pack()

    #handles clicks to set up relations, sets either parent or child node
    def handleRelationLeftClick(self,event):

        closestnode = self.getNearest(event)

        if(closestnode == None):
            return


        #if we are selecting parent, make click select parent, then have it select child next
        if(self.relationClickSelecting == "Parent"):
          
            self.readyForRelationButton = False
            closestnode = self.getNearest(event)

            self.relationParent = closestnode
            self.relationParentText.set("Relation Parent - " + self.relationParent.name)

            self.relationClickSelecting = "Child"

            return

        #if we are selecting child, make click select child, then have it select parent next
        elif(self.relationClickSelecting == "Child"):
            closestnode = self.getNearest(event)
            self.relationChild = closestnode
            self.relationChildText.set("Relation Child - " + self.relationChild.name)

           
            self.relationClickSelecting = "Parent"

            self.readyForRelationButton = True


    def addRelation(self):

        if(self.readyForRelationButton == False):
            print("not ready for relation yet")
            return
        
        parent_type = self.relationParent.type
        child_type = self.relationChild.type

        if(is_asp_or_conc(parent_type) == True and is_asp_or_conc(child_type) == True):

            self.addSubConcernRelation()

        elif(parent_type == "Concern" and child_type == "Property"):

            self.addAddressesConcernRelation()
            
        elif(parent_type == "Concern" and (child_type == "Formula" or child_type == "DecompositionFunction" )):

            self.addConcernFormulaRelation()
    
        elif((parent_type == "Formula" or parent_type == "DecompositionFunction") and (child_type == "Formula" or child_type == "DecompositionFunction")):

            if(self.relationChild in self.relationParent.negChildren):
                
              
                
                self.owlApplication.switchToRegMemberOf(self.relationChild,self.relationParent)
                
                self.relationWindowClose()
                
                self.onRelationButton()
                
            
            elif(self.relationChild in self.relationParent.children):
                
                self.owlApplication.switchToNegMemberOf(self.relationChild,self.relationParent)
               
                
                self.relationWindowClose()
                
                self.onRelationButton()
                
            else:
            
            
                self.addFormulaFormulaRelations()
        
        elif((parent_type == "Formula" or parent_type == "DecompositionFunction") and (child_type == "Property")):
            
            
            if(self.relationChild in self.relationParent.negChildren):
                
              
                
                self.owlApplication.switchToRegMemberOf(self.relationChild,self.relationParent)
                
                self.relationWindowClose()
                
                self.onRelationButton()
                
            
            elif(self.relationChild in self.relationParent.children):
                
                self.owlApplication.switchToNegMemberOf(self.relationChild,self.relationParent)
               
                
                self.relationWindowClose()
                
                self.onRelationButton()
                
            else:
                
                
                self.addFormulaPropertyRelations()

        elif(parent_type == "Property" and child_type == "Component"):

            self.addRelatedToRelation()
            

        else:

            print("Parent and child don't make sense")
            
            return
        
        self.updateTree()
        
        summary = "Added relation between " + self.relationParent.name + " and " + self.relationChild.name

        self.summaryText.set(summary)
        
    #adds a subconcern relation between selected parent and child
    def addSubConcernRelation(self):
        
        self.owlBase.addNewSubConcernRelation(self.relationParent,self.relationChild)
        

    def addAddressesConcernRelation(self):

        self.owlApplication.addPropertyAddConcernRelation(self.relationParent,self.relationChild)
       
    def addConcernFormulaRelation(self):
        
        
        self.owlApplication.addNewConcernFormulaRelation(self.relationParent,self.relationChild)
       
    def addFormulaFormulaRelations(self):
        
        self.owlApplication.addFormulaFormulaRelations(self.relationParent,self.relationChild)
        
    def addFormulaPropertyRelations(self):
        
        self.owlApplication.addFormulaPropertyRelations(self.relationParent,self.relationChild)
       
    def addRelatedToRelation(self):

        self.owlApplication.addNewRelatedToRelation(self.relationParent,self.relationChild)
       
        
    #removes the selected relation, at the moment just handles subconcern relation
    def removeRelation(self):

        if(self.readyForRelationButton == False):
            print("not ready for button yet")
            return

        parent_type = self.relationParent.type
        child_type = self.relationChild.type

        if(is_asp_or_conc(parent_type) == True and is_asp_or_conc(child_type) == True):

            self.removeSubConcernRelation()

        elif(parent_type == "Concern" and child_type == "Property"):

            self.removePropertyAddressesConcernRelation()
            
        elif(parent_type == "Concern" and (child_type == "Formula" or child_type == "DecompositionFunction" )):

            self.removeConcernFormulaRelation()
    
        elif((parent_type == "Formula" or parent_type == "DecompositionFunction") and (child_type == "Formula" or child_type == "DecompositionFunction")):

            self.removeFormulaFormulaRelations()
        
        elif((parent_type == "Formula" or parent_type == "DecompositionFunction") and (child_type == "Property")):
            

            self.removeFormulaPropertyRelations()
            
            
        elif(parent_type == "Property" and child_type == "Component"):

            self.removeRelatedToRelation()
        
        else:

            print("Parent and child don't make sense")
            return
        
        self.updateTree()

        summary = "Removed relation between " + self.relationParent.name + " and " + self.relationChild.name

        self.summaryText.set(summary)
   

    def removeSubConcernRelation(self):

        self.owlBase.removeSubConcernRelation(self.relationParent,self.relationChild)

    def removePropertyAddressesConcernRelation(self):

        self.owlApplication.removePropertyAddressesConcernRelation(self.relationParent,self.relationChild)
        
    def removeConcernFormulaRelation(self):
        
        self.owlApplication.removeConcernFormulaRelation(self.relationParent,self.relationChild)
        
    def removeFormulaFormulaRelations(self):
        
        self.owlApplication.removeFormulaFormulaRelation(self.relationParent,self.relationChild)
        
    def removeFormulaPropertyRelations(self):
        
        self.owlApplication.removeFormulaPropertyRelations(self.relationParent,self.relationChild)
    

    def removeRelatedToRelation(self):

        self.owlApplication.removeRelatedToRelation(self.relationParent,self.relationChild)        
        
        
    #handles closing relations window
    def relationWindowClose(self):

        self.relationWindow.destroy()
        self.relationWindowOpen = False
    
    
        
    def onDependencyButton(self):
        
        if(self.dependencyWindowOpen == True):
             return
        
        
        self.dependencyWindow = tk.Toplevel(height = 400, width = 1000, bg = spartangreen)
        self.dependencyWindow.transient(master = self.master)
        self.dependencyWindow.title("Add New Relation")
        
        self.dependencyWindowOpen = True 
        self.readyForDependency = False
        self.inserting = "left"
        
        
        self.dependencyWindowHeaderFrame = tk.Frame(self.dependencyWindow,bg = spartangreen)
        self.dependencyWindowHeaderFrame.place(relwidth = .8, relheight = .10, relx = .10, rely = .01)
        
        showtext = "Add New Dependency"
        
        self.dependencyWindowHeader = Label(self.dependencyWindowHeaderFrame, text = showtext, fg = "white",bg = spartangreen, font = headerFont)
        self.dependencyWindowHeader.pack()
        
        self.dependencyWindowButtonFrame = tk.Frame(self.dependencyWindow,bg = "white")
        self.dependencyWindowButtonFrame.place(relwidth = .8, relheight = .80, relx = .10, rely = .11)
        
        
        self.dependencyEntryFrame = tk.Frame(self.dependencyWindowButtonFrame,bg = spartangreen)
        self.dependencyEntryFrame.place(relwidth = .9, relheight = .80, relx = .05, rely = .05)
     
        self.DCE = dependencyCalculatorEntry(self.dependencyEntryFrame, self.owlBase, self.owlApplication,self)
        self.dependencyWindow.protocol("WM_DELETE_WINDOW",self.dependencyWindowClose)
        
    
    def handleDependencyClick(self,event):
        nearest = self.getNearest(event)
        
        if event.button == 3:
            andor = "or"
        else:
            andor = "and"
        
        if(nearest == None):
            return
    
        currentText = self.DCE.editing.get(1.0,END)
        
       # print("before cleaning")
       # print(currentText)
      #  print(len(currentText))
        
        if(currentText[len(currentText) - 2] == " " or currentText[len(currentText) - 2] == "("):
            
            space = ""
            
        else:
            
            space = " "
        
        currentText = currentText.replace("(","")
        currentText = currentText.replace(")","")
    
        currentText = currentText.split(" ")
        
        goodtext = []
        
        for string in currentText:
            
            string = string.rstrip("\n")
            
            goodtext.append(string)
            #print(string)
            
        
        #goodtext = list(filter((" ").__ne__, goodtext))
        goodtext = list(filter(("").__ne__, goodtext))
        goodtext = list(filter(("\n").__ne__, goodtext))
    
      #  print("after cleaning")
      #  print(goodtext)
     
        if(len(goodtext) == 0):
            
            self.DCE.editing.insert(END, nearest.name)
            return
        
        if(goodtext[-1] == "and" or goodtext[-1] == "or" or goodtext[-1] == "not" or goodtext[-1] == ")"):
            
            self.DCE.editing.insert(END, space + nearest.name)
        
        else:
        
            self.DCE.editing.insert(END, space + andor + " " + nearest.name)
            
        

    def dependencyWindowClose(self):
        
        self.dependencyWindow.destroy()
        self.dependencyWindowOpen = False
        
        
    def launchPolarityWindow(self):
        
        if(self.polarityWindowOpen == True):
            return
        
        self.polarityWindow = tk.Toplevel(height = 350, width = 500, bg = spartangreen)
        self.polarityWindow.title("Polarity")
        
        if(self.relationWindowOpen == True):
            self.polarityWindow.transient(master = self.relationWindow)
            
        elif(self.lcWindowOpen == True):
            self.polarityWindow.transient(master = self.lcWindow)
            
        
        self.polarityWindowOpen = True
    
        self.polarityWindow.protocol("WM_DELETE_WINDOW",self.polarityWindowClose)
        
        self.polarityWindowHeaderFrame = tk.Frame(self.polarityWindow, bg = spartangreen)
        self.polarityWindowHeaderFrame.place(relwidth = .7, relheight = .15, relx = .15, rely = .01)
        
         
        self.polarityWindowButtonFrame = tk.Frame(self.polarityWindow, bg = "white")
        self.polarityWindowButtonFrame.place(relwidth = .85, relheight = .8, relx = .075, rely = .16)
        
        self.addPropertyButtonFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.addPropertyButtonFrame.place(relwidth = .70, relheight = .15, relx = .15, rely = .65)
        
        self.cancelButtonFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.cancelButtonFrame.place(relwidth = .70, relheight = .15, relx = .15, rely = .82)
        
        self.polarityWindowHeaderText = tk.Label(self.polarityWindowHeaderFrame, text = "Select polarity \nfor new relation",fg = "white",bg = spartangreen, font = headerFont)
        self.polarityWindowHeaderText.pack()
        
     
        
        self.addRelationButton = tk.Button(self.addPropertyButtonFrame, text = "Add Relation", bg = spartangreen, fg = self.buttonFontColor, borderwidth = 5, font = buttonFont, command = self.handleRelationAfterPolarity)
        self.addRelationButton.place(relx = .50, rely = .50, anchor = "center")
        
        self.cancelButton = tk.Button(self.cancelButtonFrame, text = "Cancel", bg = spartangreen, fg = self.buttonFontColor, borderwidth = 5, font = buttonFont, command = self.cancelAddProperty)
        self.cancelButton.place(relx = .50, rely = .50, anchor = "center")

        self.conditionPolarity = self.owlApplication.owlReadyOntology.positive
        self.IRPolarity = self.owlApplication.owlReadyOntology.positive    
    def handleRelationAfterPolarity(self):
        if(self.addingRelation == "IRProperty"):
            self.myAddProperty()         
        elif(self.addingRelation == "RLIR"):       
            self.owlApplication.addRLIR(self.RLIEntry.get(),self.IRPolarity)      
            self.updateTree()    
    def addConditionPolarity(self):
        
        
        
        self.conditionTextFrame = tk.Frame(self.polarityWindowButtonFrame,bg = "white")
        self.conditionTextFrame.place(relwidth = .3, relheight = .25, relx = .05, rely = .05)
        
      
        self.conditionPolarityFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.conditionPolarityFrame.place(relwidth = .2, relheight = .25, relx = .37, rely = .05)
        
        self.conditionPlusFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.conditionPlusFrame.place(relwidth = .15, relheight = .25, relx = .65, rely = .05)
        
        self.conditionMinusFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.conditionMinusFrame.place(relwidth = .15, relheight = .25, relx = .81, rely = .05)
        
        self.conditionTextLabel = tk.Label(self.conditionTextFrame, text = "Condition\nPolarity", fg = "black", bg = "white", font = headerFont)
        self.conditionTextLabel.place(relx = .50, rely = .50, anchor = "center")
    
        self.conditionPolarityTextVar = tk.StringVar()
        self.conditionPolarityTextVar.set("+")   
        self.conditionPolarityTextLabel = tk.Label(self.conditionPolarityFrame, textvariable = self.conditionPolarityTextVar, fg = "black",bg = "white",font = "Monaco 60 bold")
        self.conditionPolarityTextLabel.place(relx = .50, rely = .50, anchor = "center")   
        self.conditionPlusButton = tk.Button(self.conditionPlusFrame, text = "+", bg = spartangreen, fg = self.buttonFontColor, borderwidth = 5, font = "Monaco 30 bold", command = self.onConditionPlus)
        self.conditionPlusButton.place(relx = .50, rely = .50, anchor = "center")

        self.conditionMinusButton = tk.Button(self.conditionMinusFrame, text = "-", bg = spartangreen, fg = self.buttonFontColor, borderwidth = 5, font =  "Monaco 30 bold", command = self.onConditionMinus)
        self.conditionMinusButton.place(relx = .50, rely = .50, anchor = "center")
    def addIRPolarity(self):
        
        self.IRTextFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.IRTextFrame.place(relwidth = .3, relheight = .25, relx = .05, rely = .35)
    
        
        self.IRPolarityFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.IRPolarityFrame.place(relwidth = .2, relheight = .25, relx = .37, rely = .35)
        
    
        self.IRPlusFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.IRPlusFrame.place(relwidth = .15, relheight = .25, relx = .65, rely = .35)
        
        self.IRMinusFrame = tk.Frame(self.polarityWindowButtonFrame, bg = "white")
        self.IRMinusFrame.place(relwidth = .15, relheight = .25, relx = .81, rely = .35)

    
        self.IRTextLabel = tk.Label(self.IRTextFrame, text = "Impact Rule\nPolarity", fg = "black", bg = "white", font = headerFont)
        self.IRTextLabel.place(relx = .50, rely = .50, anchor = "center")
        
      
        self.IRPolarityTextVar = tk.StringVar()
        self.IRPolarityTextVar.set("+")
    
        self.IRPolarityTextLabel = tk.Label(self.IRPolarityFrame, textvariable = self.IRPolarityTextVar, fg = "black", bg = "white", font = "Monaco 60 bold")
        self.IRPolarityTextLabel.place(relx = .50, rely = .50, anchor = "center")
        
        self.IRPlusButton = tk.Button(self.IRPlusFrame, text = "+", bg = spartangreen ,fg = self.buttonFontColor, borderwidth = 5, font = "Monaco 30 bold", command = self.onIRPlus)
        self.IRPlusButton.place(relx = .50, rely = .50, anchor = "center")
        
        self.IRMinusButton = tk.Button(self.IRMinusFrame, text = "-", bg = spartangreen, fg = self.buttonFontColor, borderwidth = 5, font = "Monaco 30 bold", command = self.onIRMinus)
        self.IRMinusButton.place(relx = .50, rely = .50, anchor = "center")    
    def polarityWindowClose(self):
        
        self.polarityWindow.destroy()
        self.polarityWindowOpen = False
    def addPropertyAsChild(self):

        self.addingRelation = "PropertyAsChild"
        
        self.launchPolarityWindow()
        self.addConditionPolarity()
        self.addIRPolarity()
    def cancelAddProperty(self):
        
        self.polarityWindowClose()
    def onConditionPlus(self):
        
        self.conditionPolarity = self.owlApplication.owlReadyOntology.positive
        self.conditionPolarityTextVar.set("+")
    def onConditionMinus(self):
        
        self.conditionPolarity = self.owlApplication.owlReadyOntology.negative
        self.conditionPolarityTextVar.set("-")
    def onIRPlus(self):
        
        self.IRPolarity = self.owlApplication.owlReadyOntology.negative
        self.IRPolarityTextVar.set("+")
    def onIRMinus(self):
        
        self.IRPolarity = self.owlApplication.owlReadyOntology.negative
        self.IRPolarityTextVar.set("-")
    #updates the dropdowns containing the list of concerns, keeps whatever is currently select3ed
    def updateConcernDropdown(self):

        subcof = self.subconcernOf.get()
        addC = self.addressedConcern.get()


        self.subconcern_of_name_drop.children["menu"].delete(0,"end")
        self.addressedConcern_drop.children["menu"].delete(0,"end")
        i = 0
        j = 0
        k = 0
        for node in self.sorted_concerns:
            if(node == subcof):
                j = i
            if(node == addC):
                k = i
            self.subconcern_of_name_drop.children["menu"].add_command(label = node, command = lambda name = node: self.subconcernOf.set(name))
            self.addressedConcern_drop.children["menu"].add_command(label = node, command = lambda name = node: self.addressedConcern.set(name))

            i = i + 1
        self.subconcernOf.set(self.sorted_concerns[j])
        self.addressedConcern.set(self.sorted_concerns[k])

    

    #function to add space in specified location, with specified color
    def addSpace(self,on,color,size):

        if(size == "tiny"):
            self.emptySpace = Label(on, text = "", font = tiny,bg = color)

        if(size == "small"):
            self.emptySpace = Label(on, text = "", font = small,bg = color)

        if(size == "medium"):
            self.emptySpace = Label(on, text = "", font = med,bg = color)

        if(size == "large"):
            self.emptySpace = Label(on, text = "", font = large,bg = color)

        self.emptySpace.pack()

    def printSummary(self,text):



        self.summaryLabel = Label(self.textBoxFrame, text = text, font = summaryFont,fg= "white",bg = "#747780")
        self.summaryLabel.pack()

    #handles processing the output file after we save it, for now just strips string tag in owl file.
    def processFile(self,output_file):

        #read input file
        fin = open(output_file, "rt")
        #read file contents to string
        data = fin.read()
        #replace all occurrences of the required string
        data = data.replace( " rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\"", '')
        #close the input file
        fin.close()
        #open the input file in write mode
        fin = open(output_file, "wt")
        #overrite the input file with the resulting data
        fin.write(data)
        #close the file
        fin.close()

    def outputAndLaunchASP(self):

        return

        output_file = self.outputEntry.get()

        #self.owlBase.owlReadyOntology.save(file = "./../../src/asklab/querypicker/QUERIES/BASE/" + output_file, format = "rdfxml")
        self.owlBase.owlReadyOntology.save(file = output_file, format = "rdfxml")

        self.processFile(output_file)


        if(self.owlApplication != None):
            self.owlApplication.owlReadyOntology.save(file = "app_" + output_file, format = "rdfxml")
            self.processFile("app_" + output_file)

        summary = "Outputted ontology to file: " + output_file
        self.summaryText.set(summary)



        return
    #gets the accturate OWL Object via searching the ontology for the passed name
    def getOWLObject(self,name):

        obj_list = self.owlBase.owlReadyOntology.ontology.search(iri = "*" + name)
        obj_names = []

        for obj in obj_list:
            obj_names.append(remove_namespace(obj))

        i = 0
        while i < len(obj_names):

            if(obj_names[i] == name):
                obj = obj_list[i]
                break

            i = i + 1


        return obj


    #removes all nodes which dont have any parents nor any children, and are not aspects
    def removeFloaters(self):

        self.owlBase.removeRelationless()
        self.updateTree()

        summary = "Removed all concerns with no relations"


        self.summaryText.set(summary)


    def remove_namespace(in_netx):

        in_str = str(in_netx)

        leng = len(in_str)
        period = leng
        for i in range(leng):
            if(in_str[i] == '.'):
                period = i
                break

        return in_str[(period + 1):]

root = Tk()

root.state("zoomed")

fontStyle = tkFont.Font(family="Lucida Grande", size=8, weight = "bold")

headerFont = tkFont.Font(family = "Helvetica",size = 14, weight = "bold")
promptFont = tkFont.Font(family = "Lucida Grande", size = 10, weight = "bold")
infoFont = tkFont.Font(family = "Monaco", size = 12, weight = "bold")
entryFont = tkFont.Font(family = "Verdana", size = 11, weight = "bold")
buttonFont = tkFont.Font(family = "Helvetica", size = 12, weight = "normal")
summaryFont = tkFont.Font(family = "Lucida Grande", size = 8, weight = "bold")

tiny = tkFont.Font(family="Lucida Grande", size=1, weight = "bold")
small = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
med = tkFont.Font(family="Lucida Grande", size=12, weight = "bold")
big = tkFont.Font(family="Lucida Grande", size=18, weight = "bold")
selectFont = tkFont.Font(family="Lucida Grande", size=11, weight = "bold")
my_gui = OntologyGUI(root)
root.mainloop()

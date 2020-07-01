
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from owlFunctions import is_asp_or_conc
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

from script_networkx import remove_namespace

from owlBase import owlBase
from owlApplication import owlApplication
from owlGraph import owlGraph


from owlready2 import *
pressed = False
spartangreen = "#18453b"

class OntologyGUI:

    def __init__(self,master):

        self.zoom = 1
        self.zoomIndex = 105
        self.fontsize = 8

        self.lcWindowOpen = False
        self.rcWindowOpen = False
        self.relationWindowOpen = False
        self.removeConfirmationWindowOpen = False
        self.removeChildrenWindowOpen = False
        

        self.hoveredNode = None
        self.owlLoaded = False
        

        self.master = master


        self.master.bind("<Button-4>", self.handleZoom)
        self.master.bind("<Button-5>", self.handleZoom)
        self.master.bind("<MouseWheel>", self.handleZoom)

        master.title("Ontology GUI")

        #set up main canvas
        self.canvas = Canvas(master, height = 1200, width = 1900, bg = "#18453b")
        self.canvas.pack()

        #set up title text
        self.masterHeaderFrame = Frame(master,bg ="#18453b" )
        self.masterHeaderFrame.place(relwidth = .8, relheight = .06, relx = .1, rely = 0.02)
        
        self.masterHeaderText = Label(self.masterHeaderFrame, text="CPS Ontology Visualization",fg = "white",bg = "#18453b", font = "Helvetica 30 bold italic")
        self.masterHeaderText.pack()

        #set up footer text
        self.footerFrame = Frame(master,bg ="#18453b")
        self.footerFrame.place(relwidth = .4, relheight = .2, relx = .61, rely = 0.9)
        self.footerText = Label(self.footerFrame, text="Matt Bundas, Prof. Son Tran, Thanh Ngyuen, Prof. Marcello Balduccini",fg = "white",bg = "#18453b", font = "Helvetica 8 bold italic", anchor = "e")
        self.footerText.pack()

        #set up frame on left for inputs
        self.leftControlFrame = Frame(master, bg="white")
        self.leftControlFrame.place(relwidth = .2, relheight = .8, relx = .01, rely = 0.1)

        #set up prompt/entry for input ontology
        self.inputPrompt = Label(self.leftControlFrame, text = "Input ontology", font = promptFont,fg= "#747780",bg = "white")
        self.inputPrompt.pack()

        self.inputEntry = Entry(self.leftControlFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.inputEntry.pack()
        self.inputEntry.insert(0,"cpsframework-v3-base.owl")

        #button to load ontology, calls function which handles loading
        self.loadOntologyB = tk.Button(self.leftControlFrame, text = "Load Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,font = buttonFont,command = self.loadOntology)
        self.loadOntologyB.pack()

        self.addSpace(self.leftControlFrame,"white","medium")


        #sets up prompt/entry for name of output owl file
        self.outputPrompt = Label(self.leftControlFrame, text =  "Output Name", font = promptFont,fg= "#747780",bg = "white")
        self.outputPrompt.pack()

        self.outputEntry = Entry(self.leftControlFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.outputEntry.pack()
        self.outputEntry.insert(2, "cpsframework-v3-base.owl")

        #sets up button to call function which handles saving ontology
        self.saveOntologyB = tk.Button(self.leftControlFrame, text = "Output Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,font = buttonFont, command = self.saveOntology)
        self.saveOntologyB.pack()


        #sets up gray box for information window

        self.infoFrame = Frame(self.leftControlFrame, bg = "#747780", bd = 5 )
        self.infoFrame.place(relwidth = .8, relheight = .58, relx = .1, rely = .25)

        self.infoFrameHeaderLabel = Label(self.infoFrame,text = "Ontology Information", font = headerFont, fg = "white", bg = "#747780")
        self.infoFrameHeaderLabel.pack()

        self.owlInfoFrame = Frame(self.infoFrame, bg = spartangreen, bd = 5)
        self.owlInfoFrame.place(relwidth = .9, relheight = .3, relx = .05, rely = .05)

        self.indInfoHeaderFrame = Frame(self.infoFrame, bg = "#747780",bd = 5)
        self.indInfoHeaderFrame.place(relwidth = .9, relheight = .07, relx  = .05, rely = .355)

        self.indInfoHeaderLabel = Label(self.indInfoHeaderFrame,text = "Concern Information", font = headerFont, fg = "white", bg = "#747780")
        self.indInfoHeaderLabel.pack()

        self.indInfoFrame = Frame(self.infoFrame,  bg = spartangreen, bd = 5)
        self.indInfoFrame.place(relwidth = .9, relheight = .55, relx = .05, rely = .41)


        self.owlNameText = tk.StringVar()
        self.owlNameText.set("Owl Name")

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


        self.owlNameInfo = Label(self.owlInfoFrame, textvariable =  self.owlNameText, font = infoFont,fg= "white",bg = spartangreen)
        self.owlNameInfo.pack()

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

        self.indChildInfo = Label(self.indInfoFrame, textvariable =  self.indChildrenText,fg= "white",bg = spartangreen,font = infoFont)
        self.indChildInfo.pack()

        self.indPropertyInfo = Label(self.indInfoFrame, textvariable =  self.indRelPropertiesText,fg= "white",bg = spartangreen,font = infoFont)
        self.indPropertyInfo.pack()


        #sets up gray box to put text to show what is going on
        self.textBoxFrame = Frame(self.leftControlFrame,bg = "#747780", bd = 5)
        self.textBoxFrame.place(relwidth = .8, relheight = .14, relx = .1, rely = .85)

        #sets up frame for ontology tree to exist
        self.treeFrame = tk.Frame(self.master, bg="white")
        self.treeFrame.place(relwidth = .70, relheight = .8, relx = .25, rely = 0.1)




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
        self.relationButtonFrame.place(relwidth = .10, relheight = .05, relx = .01, rely = .01)
        
        self.relationB = tk.Button(self.relationButtonFrame, text = "Relations",padx = 10, pady = 5, bg = spartangreen, fg = "white",borderwidth = 5, font = buttonFont, command = self.onRelationButton)
        self.relationB.pack()
        
        self.remremoveChildrenFrame = tk.Frame(self.treeFrame,bg = "white")
        self.remremoveChildrenFrame.place(relwidth = .10, relheight = .05, relx = .89, rely = .01)
    
        self.removeremoveChildrenB = tk.Button(self.remremoveChildrenFrame, text = "Remove Floaters",padx = 10, pady = 5, bg = spartangreen, fg = "white",borderwidth = 5, font = buttonFont,  command = self.removeFloaters)
        self.removeremoveChildrenB.pack()
    

    #removes all nodes which dont have any parents nor any children, and are not aspects
    def removeFloaters(self):
        
        self.owlBase.removeRelationless()
        self.updateTree()
        
        summary = "Removed all concerns with no relations"
        
        self.printSummary(summary)
        
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

    #handles mouse hovering, throws away nonsense events, updates concern info window
    def handleHover(self,event):

        if(self.owlLoaded == False):
            return

        NoneType = type(None)


        if(type(event.xdata) == NoneType or type(event.ydata) == NoneType):
            return

        nearest_node = self.getNearest(event)

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
            
            
            i = 1
            for child in self.hoveredNode.children:
                
                if(i%2 == 0):
                    childString = childString + "\n" + child.name
                
                else:
                    childString = childString + " " + child.name
                
                i = i + 1
                
            self.indChildrenText.set(childString)
            self.indRelPropertiesText.set("Relevant Properties - ")


    #updates the global ontology stats according to numbers stored in owlBase
    def updateOwlStats(self):

            self.owlNameText.set("Owl Name - " + str(self.owlBase.owlName))
            self.totalNodeText.set("Num Nodes - " + str(self.owlBase.numNodes))
            self.numAspectsText.set("Num Aspects - " + str(self.owlBase.numAspects))
            self.numConcernsText.set("Num Concerns - "  + str(self.owlBase.numConcerns))
            
            self.numPropertiesText.set("Num Properties - ")
            self.numComponentsText.set("Num Components - ")



    #adds a concern to the ontology, uses gui entries for inputs, updates tree afterwards
    def addConcern(self):


        #grab name of new concern
        new_concern_name = self.indivNameEntry.get()

        #handle error message, if new concern with name already exists, don't add another
        if(self.check_existence(new_concern_name) == True):
           print("concern already exists")
           if(self.errorDisplayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.lcButtonFrame, text = "Concern Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.errorDisplayed = True
           return

      
        self.owlBase.addNewConcern(new_concern_name,self.leftClicked.name)

        #prints text in textBoxFrame to tell what happend
        summary = "Added concern " + new_concern_name + " to ontology"
        
        self.printSummary(summary)
        
        #refresh the tree and owlBase
        self.updateTree()

        #reset the error message because we just did a successful operation
        if(self.errorDisplayed == True):
            self.error_message.destroy()
            self.errorDisplayed == False

        print("added concern")

    #checks if an concern with the passed name exists
    def check_existence(self,concern):

        #print("checking existence")
        ind_search = self.owlBase.owlReadyOntology.search(iri = "*" + concern)

        if(len(ind_search) == 0):
            return False
        else:
            return True


    #takes a mouse event, returns the closest node to the mouse event
    def getNearest(self,event):

        NoneType = type(None)
        (x,y) = (event.xdata, event.ydata)
       
        smallestdistance = np.inf
        closestnode = None
       
        for node in self.owlBase.allConcerns_owlNode:

            nodepos = self.owlTree.graphPositions[node.name]
        
            distance = np.sqrt((x - nodepos[0])**2 + (y - nodepos[1])**2)
            if(distance < smallestdistance):
                closestnode = node
                smallestdistance = distance
       
        return closestnode

    #returns the type of node with passed name, returns string
    def getType(self,name):
        selected_item = self.getOWLObject(name)
        type_item = remove_namespace(selected_item.is_a)

        return type_item


    #handles the given click event, sends code to either handle relation click, normal left click, or right click event
    def handleClick(self,event):

        if(event.button == 1):
            
            if(self.relationWindowOpen == True):
                self.handleRelationLeftClick(event)
            else:
                self.onLeftClick(event)

        if(event.button == 3):
            self.onRightClick(event)

    #takes care of right clicks, opens up window where you can add a new aspect
    def onRightClick(self,event):

    
        if(self.owlLoaded == False or self.rcWindowOpen == True):
            return

        #set up windows and frames
        self.rcWindow = tk.Toplevel(height = 400, width = 300, bg = spartangreen)
        self.rcWindow.title("Add New Aspect")
        self.rcWindow.protocol("WM_DELETE_WINDOW", self.rcWindowClose)
        
        self.rcErrorDisplayed = False

        self.rcWindowFrame = tk.Frame(self.rcWindow,bg = spartangreen)
        self.rcWindowFrame.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)

        self.rcButtonFrame = tk.Frame(self.rcWindow, bg = "white")
        self.rcButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)
        
        self.rcWindowHeaderFrame = tk.Frame(self.rcWindow,bg = spartangreen)
        self.rcWindowHeaderFrame.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)
        
        showtext = "Add New Parent Concern or Aspect"

        self.rclcWindowHeaderLabel = Label(self.rcWindowHeaderFrame, text =  showtext,fg= "white",bg = spartangreen,font = headerFont)
        self.rclcWindowHeaderLabel.pack()
        
        #set up prompt for new aspect name
        self.rcIndivNamePrompt = Label(self.rcButtonFrame, text = "Name of New Aspect", font = promptFont,fg= "#747780",bg = "white")
        self.rcIndivNamePrompt.pack()
        
        self.rcIndivNameEntry = Entry(self.rcButtonFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.rcIndivNameEntry.pack()
        self.rcIndivNameEntry.insert(1,"NewConcern")
        
        #add button to call function to add new aspect
        addAspectB = tk.Button(self.rcButtonFrame, text = "Add Aspect",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.addAspect)
        addAspectB.pack()
       
    #function to handle when you click Relations button, opens up window where you can do relation operations   
    def onRelationButton(self):
        
        if(self.relationWindowOpen == True):
            return
        
        #set up window and frames
        self.relationWindow = tk.Toplevel(height = 400, width = 300, bg = spartangreen)
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
        
        self.relationParentLabel = Label(self.relationButtonFrame, textvariable = self.relationParentText, font = infoFont,fg= "#747780",bg = "white")
        self.relationParentLabel.pack()
        
        self.relationChildLabel = Label(self.relationButtonFrame, textvariable = self.relationChildText, font = infoFont,fg= "#747780",bg = "white")
        self.relationChildLabel.pack()
        
        
        self.addSpace(self.relationButtonFrame,"white","tiny")
        #add buttons for adding subconcern, addresses, remove relation
        addSubConcernRelationB = tk.Button(self.relationButtonFrame, text = "Add Subconcern Relation",padx = 10, height = 1, width = 25, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.addSubConcernRelation)
        addSubConcernRelationB.pack()
        self.addSpace(self.relationButtonFrame,"white","tiny")
        
        addAddressesConcernRelationB = tk.Button(self.relationButtonFrame, text = "Add Property Addresses Relation",padx = 10, height = 1, width = 25, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.addAddressesConcernRelation)
        addAddressesConcernRelationB.pack()
        self.addSpace(self.relationButtonFrame,"white","tiny")
        
        removeRelationB = tk.Button(self.relationButtonFrame, text = "Remove Relation",padx = 10, height = 1, width = 25, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeRelation)
        removeRelationB.pack()
        
        
        
        
    
      
    #handles clicks to set up relations, sets either parent or child node
    def handleRelationLeftClick(self,event):
        
        #if we are selecting parent, make click select parent, then have it select child next
        if(self.relationClickSelecting == "Parent"):
            print("selected parent")
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
            
            print("selected child")
            self.relationClickSelecting = "Parent"
            
            self.readyForRelationButton = True

    
    #adds a property addressesConcern relation, not functional at the moment
    def addAddressesConcernRelation(self):
    
        return
        if(self.readyForRelationButton == False):
            print("not ready for relation yet")
            return 
        
        parent_relation = self.getOWLObject(self.relationParent.name)
        child_relation = self.getOWLObject(self.relationChild.name)
        
        child_type = remove_namespace(child_relation.is_a[0])
        parent_type = remove_namespace(parent_relation.is_a[0])
        
        if(is_asp_or_conc(child_type) == True and is_asp_or_conc(parent_type) == True):
            print("Neither node is a property")
            return
        
        print("trying to add addresses relation")
        
        summary = "Added addressesConcern relation from " + self.relationParent.name + " to " + self.relationChild.name
        
        self.printSummary(summary)
        
        
        
    #adds a subconcern relation between selected parent and child
    def addSubConcernRelation(self):
        
        if(self.readyForRelationButton == False):
            print("not ready for relation yet")
            return 
        
        if(is_asp_or_conc(self.relationParent.type) == False or is_asp_or_conc(self.relationChild.type) == False):
            print("Either parent or child is not a concern")
            return
        
        self.owlBase.addNewSubConcernRelation(self.relationParent,self.relationChild)
        
        self.updateTree() 
        
        summary = "Added subconcern relation from " + self.relationParent.name + " to " + self.relationChild.name
        
        self.printSummary(summary)
        
    #removes the selected relation, at the moment just handles subconcern relation
    def removeRelation(self):
        
        if(self.readyForRelationButton == False):
            print("not ready for button yet")
            return 
        
        if(is_asp_or_conc(self.relationParent.type) == False or is_asp_or_conc(self.relationParent.type) == False):
            print("One node is not a concern")
            return
        
        self.owlBase.removeSubConcernRelation(self.relationParent,self.relationChild)
        self.updateTree() 
        
        summary = "Removed relation between" + self.relationParent.name + " and " + self.relationChild.name
        
        self.printSummary(summary)
        
    #handles closing relations window    
    def relationWindowClose(self):
        
        self.relationWindow.destroy()
        self.relationWindowOpen = False
        
    #function to add parent to clicked node
    def addParent(self):
        
        #get name from Entry
        new_parent_name = self.indivNameEntry.get()
        
        #handle error message, if new concern with name already exists, don't add another
        if(self.check_existence(new_parent_name) == True):
           print("concern already exists")
           if(self.errorDisplayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.lcButtonFrame, text = "Concern Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.errorDisplayed = True
           return
      
        self.owlBase.addConcernAsParent(new_parent_name,self.leftClicked.name)
        
        summary = "Added " + new_parent_name + " as Parent of " + self.leftClicked.name 
        self.printSummary(summary)
        
        self.updateTree()
        
    #function to add aspect to ontology
    def addAspect(self):
        
        #get name of new aspect from entry
        new_aspect_name = self.rcIndivNameEntry.get()

        #handle error message, if new concern with name already exists, don't add another
        if(self.check_existence(new_aspect_name) == True):
           print("concern already exists")
           if(self.rcErrorDisplayed == True):
               self.rcerror_message.destroy()
           self.rcerror_message = Label(self.rcButtonFrame, text = "Concern Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.rcerror_message.pack()
           self.rcErrorDisplayed = True
           return
        
        #instantiate new aspect object
        self.owlBase.addNewAspect(new_aspect_name)

        #prints text in textBoxFrame to tell what happend
        summary = "Added Aspect " + new_aspect_name + " to ontology"

        self.printSummary(summary)

        self.updateTree()

        if(self.rcErrorDisplayed == True):
            self.rcerror_message.destroy()
            self.rcErrorDisplayed == False

        print("added aspect")


    #handles opening left click window, where you can edit clicked concerns
    def onLeftClick(self,event):

        if(self.lcWindowOpen == True or self.owlLoaded == False):
            return

        self.errorDisplayed = False

        #get the node you just clicked on
        closestnode = self.getNearest(event)
        
        #set global "parent" variable which is essentially the selected node which will be used by other functions
        self.leftClicked = closestnode
        
        #open up window and frames
        self.lcWindow = tk.Toplevel(height = 400, width = 300,bg = spartangreen )
        self.lcWindow.transient(master = self.master)

        self.lcWindowOpen = True
        self.lcWindow.title("Concern Editor")

        self.lcWindow.protocol("WM_DELETE_WINDOW", self.leftclickWindowClose)

        self.lcWindowHeaderFrame = tk.Frame(self.lcWindow,bg = spartangreen)
        self.lcWindowHeaderFrame.place(relwidth = .7, relheight = .12, relx = .15, rely = .01)

        self.lcButtonFrame = tk.Frame(self.lcWindow, bg = "white")
        self.lcButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)

        type_item = closestnode.type
    
    
        self.lcWindowHeaderText = tk.StringVar()
        self.lcWindowHeaderText.set(self.leftClicked.name + "\n" + self.leftClicked.type)
        

        self.lcWindowHeaderLabel = Label(self.lcWindowHeaderFrame, textvariable = self.lcWindowHeaderText ,fg= "white",bg = spartangreen,font = headerFont)
        self.lcWindowHeaderLabel.pack()

        self.indivNamePrompt = Label(self.lcButtonFrame, text = "Name of New Concern", font = promptFont,fg= "#747780",bg = "white")
        self.indivNamePrompt.pack()

        self.indivNameEntry = Entry(self.lcButtonFrame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = entryFont)
        self.indivNameEntry.pack()
        self.indivNameEntry.insert(1,"NewConcern")
        
        self.addSpace(self.lcButtonFrame,"white","tiny")

        #set up buttons for operations
        addConcern = tk.Button(self.lcButtonFrame, text = "Add Subconcern",padx = 5, bg = "#18453b", fg = "white",borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addConcern)
        addConcern.pack()
        
        self.addSpace(self.lcButtonFrame,"white","tiny")

        addParent = tk.Button(self.lcButtonFrame, text = "Add Parent Concern",padx = 5, bg = "#18453b", fg = "white",borderwidth = 5, height = 1, width = 15 ,font = buttonFont, command = self.addParent)
        addParent.pack()
        
        self.addSpace(self.lcButtonFrame,"white","tiny")

        addPropertyB = tk.Button(self.lcButtonFrame, text = "Add Property",padx = 5, bg = "#18453b", fg = "white",borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.addProperty)
        addPropertyB.pack()
        
        self.addSpace(self.lcButtonFrame,"white","tiny")
     
        editName = tk.Button(self.lcButtonFrame, text = "Edit Name",padx = 5, bg = "#18453b", fg = "white",borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.editConcern)
        editName.pack()
        
        self.addSpace(self.lcButtonFrame,"white","tiny")
        
        removeConcernB = tk.Button(self.lcButtonFrame, text = "Delete",padx = 5, bg = "#18453b", fg = "white",borderwidth = 5, height = 1, width = 15, font = buttonFont, command = self.removeConcern)
        removeConcernB.pack()
        
        self.addSpace(self.lcButtonFrame,"white","tiny")
        
    #handles editing an concern
    def editConcern(self):
        
        #adds concern in
        new_name = self.indivNameEntry.get()
        old_name = self.leftClicked.name
        ind_type = self.leftClicked.type

        if(self.check_existence(new_name) == True):
           print("concern already exists")
           if(self.errorDisplayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.lcButtonFrame, text = "Concern Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.errorDisplayed = True
           return

        #change name of olwready object
        
        self.owlBase.editName(self.leftClicked,new_name)
  

    
        summary = "Changed name of " + old_name + " to " + new_name
        self.printSummary(summary)
        
        
        self.updateTree()
        
        
        self.lcWindowHeaderText.set(ind_type + " - " + new_name)

    #handles closing concern editor window
    def leftclickWindowClose(self):

        
        self.lcWindowOpen = False
        self.leftClicked = None
        
        if(self.removeChildrenWindowOpen == True):
            self.removeChildrenWindowClose()
            
        if(self.removeConfirmationWindowOpen == True):
            self.removeConfirmationWindowClose()
            
        self.lcWindow.destroy()
        
    #handles closing right click window
    def rcWindowClose(self):
        
        self.rcWindow.destroy()
        self.rcWindowOpen = False
        self.leftClicked = None
        
        
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

    #handles removing concern left clicked on
    def removeConcern(self):

      
        #check if there will be removeChildren if you delete node
        nodesChildren = self.owlBase.getChildren(self.leftClicked)
        
        
        #if it wouldn't create any removeChildren, just delete it
        if(len(nodesChildren) == 0):
        
            self.owlBase.removeConcern(self.leftClicked)
            self.updateTree()
            
            
            summary = "Removed " + self.leftClicked.name
            self.printSummary(summary)
            self.leftclickWindowClose()
         
        #if deletion would create removeChildren, ask if they want to delete all of the removeChildren
        else:
            
            self.removeChildrenWindow = tk.Toplevel(height = 200, width = 600, bg = spartangreen)
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
            
            deleteSelectedB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Selected Only", bg = "#18453b", fg = "white",borderwidth = 5, padx = 5, height = 1, width = 40,font = buttonFont, command = self.removeSingleConcern)
            deleteSelectedB.pack() 
            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")
            
            deleteSelectedRelationlessChildrenB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Selected + Resulting Relationless Children",padx = 5, height = 1, width = 40, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.handleRemoveIndAndRelationless)
            deleteSelectedRelationlessChildrenB.pack()
            
            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")      
            
            deleteSelectedAllChildrenB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Selected + All Children", bg = "#18453b",padx = 5, height = 1, width = 40, fg = "white",borderwidth = 5, font = buttonFont, command = self.handleRemoveAllChildren)
            deleteSelectedAllChildrenB.pack() 
          
            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")  
            
            #deleteIndB = tk.Button(self.removeChildrenButtonFrame, text = "Delete Concern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeSingleConcern)
            #deleteIndB.pack() 
            
            cancelB = tk.Button(self.removeChildrenButtonFrame, text = "Cancel",padx = 5, height = 1, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.cancelDelete)
            cancelB.pack()
            
            self.addSpace(self.removeChildrenButtonFrame,"white","tiny")
            
            
            
            
    
        

     
        
    def cancelDelete(self):
        
        self.removeChildrenWindowClose()
        
        return
        
    def removeSingleConcern(self):
        
        self.owlBase.removeConcern(self.leftClicked)
        
        self.removeChildrenWindowClose()
        self.leftclickWindowClose()
        
        
        self.updateTree()
        
    
    def handleRemoveAllChildren(self):
        
        
        if(self.removeConfirmationWindowOpen == True):
            return
        
        all_node_children = self.owlBase.getChildren(self.leftClicked)
        
        self.removeConfirmationWindow = tk.Toplevel(height = 600, width = 400, bg = spartangreen)
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
        
        self.removeConfirmationWindowHeaderLabel = Label(self.removeConfirmationWindowHeaderFrame, textvariable = self.removeConfirmationWindowHeaderText ,fg= "white",bg = spartangreen,font = infoFont)
        self.removeConfirmationWindowHeaderLabel.pack()
        
        
        toDeleteLabel = Label(self.removeConfirmationButtonFrame,text = self.leftClicked.name,fg= "gray",bg = "white",font = promptFont)
        toDeleteLabel.pack()
        
        for node in all_node_children:
            
            toDeleteLabel = Label(self.removeConfirmationButtonFrame,text = node.name,fg= "gray",bg = "white",font = promptFont)
            toDeleteLabel.pack()
            
            
        self.removeConfirmationQuestionLabel = Label(self.removeConfirmationButtonFrame,text = "Would you like to Remove these?")
        self.removeConfirmationQuestionLabel.pack()
        
        
        self.addSpace(self.removeConfirmationButtonFrame,"white","tiny")
        
        yesB = tk.Button(self.removeConfirmationButtonFrame, text = "Yes",padx = 10, pady = 5, width = 10, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeAllChildren)
        yesB.pack()
        
        self.addSpace(self.removeConfirmationButtonFrame,"white","tiny")
        noB = tk.Button(self.removeConfirmationButtonFrame, text = "No",padx = 10, pady = 5, width = 10, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeConfirmationWindowClose)
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
        
        yesB = tk.Button(self.removeConfirmationButtonFrame, text = "Yes",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeIndAndRelationless)
        yesB.pack()
        
        noB = tk.Button(self.removeConfirmationButtonFrame, text = "No",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5, font = buttonFont, command = self.removeConfirmationWindowClose)
        noB.pack()
        
        
    #adds a property to the ontology, uses gui for inputs, updates tree afterwards
    def addProperty(self):

        #add in the property
        new_property_name = self.indivNameEntry.get()

        #handle error message, if new concern with name already exists, don't add another
        if(self.check_existence(new_property_name) == True):
           print("concern already exists")
           if(self.errorDisplayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.lcButtonFrame, text = "Concern Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.errorDisplayed = True
           return

      
        #instantiate the new property given the new name
        new_property = self.owlBase.owlReadyOntology.Property(new_property_name, ontology = self.owlBase.owlReadyOntology)
       
        #fill in new properties attributes
        new_property.hasType.append(self.owlBase.owlReadyOntology.PropertyType_Assertion)
        new_property.atomicStatement.append("new_atomic_statement")
        new_property.comment.append("new_comment")

        #new property requires new IR and new condition
        new_ir_name = self.getIRName()
        new_cond_name = self.getCondName()

        #add condition with given name
        new_condition = self.owlBase.owlReadyOntology.Condition(new_cond_name, ontology = self.owlBase.owlReadyOntology)
        new_condition.conditionPolarity.append(self.owlBase.owlReadyOntology.positive)
        new_condition.conditionProperty.append(new_property)

        #find concern that is clicked on, new property addresses it
        addressed_concern = self.getOWLObject(self.leftClicked.name)

        #add the impact rule
        new_impact_rule = self.owlBase.owlReadyOntology.ImpactRule(new_ir_name,ontology = self.owlBase.owlReadyOntology)
        new_impact_rule.addressesAtFunc.append(self.owlBase.owlReadyOntology.bc1)
        new_impact_rule.addressesConcern.append(addressed_concern)
        new_impact_rule.addressesPolarity.append(self.owlBase.owlReadyOntology.positive)
        new_impact_rule.hasCondition.append(new_condition)
        new_impact_rule.comment.append("new_comment")


        #prints text in text box
        summary = "Added property " + new_property_name + " to ontology"

        self.printSummary(summary)

        self.updateTree()

        if(self.errorDisplayed == True):
            self.error_message.destroy()
            self.errorDisplayed == False

    #returns the suitable ir name given how many already exist
    def getIRName(self):

        new_ir_num = self.owlBase.numImpactRules + 1

        if(new_ir_num >= 1000):
            return "ir" + str(new_ir_num)
        if(new_ir_num >= 100):
            return "ir0" + str(new_ir_num)
        if(new_ir_num >= 10):
            return "ir00" + str(new_ir_num)
        if(new_ir_num >= 1):
            return "ir000" + str(new_ir_num)

    #returns the suitable condition name given how many already exist
    def getCondName(self):

        new_cond_num = self.owlBase.numConditions + 1

        if(new_cond_num >= 1000):
            return "c" + str(new_cond_num) + "_01"
        if(new_cond_num >= 100):
            return "c0" + str(new_cond_num) + "_01"
        if(new_cond_num >= 10):
            return "c00" + str(new_cond_num) + "_01"
        if(new_cond_num >= 1):
            return "c000" + str(new_cond_num) + "_01"



    #clears the tree, re sets up owlBase and graph, draws it 
    def updateTree(self):

         self.treeAxis.clear()

         self.treeAxis.axis('off')
        
         self.owlBase.initializeOwlNodes()
         self.owlBase.setNumbers()
         
         self.owlApplication.initializeOwlNodes()
         
         self.constructGraph()
        

         self.scale_tree(3)

         self.owlTree.draw_graph(self.treeAxis,self.fontsize)
         
         self.treeChart.draw()

         self.updateOwlStats()


    #loads the specified ontology file in
    def loadOntology(self):

        self.owlBase = owlBase(self.inputEntry.get())
        
        self.owlApplication = owlApplication("cpsframework-v3-sr-Elevator-Configuration.owl",self.owlBase)

        summary = "Loaded ontology " + "file://./" + self.inputEntry.get()
        self.printSummary(summary)

        self.updateTree()

        self.owlLoaded = True


    def constructGraph(self):
        
        self.owlTree = owlGraph(self.owlBase,self.owlApplication)


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

    #changes zoom level, fontsize, then calls updateTree to draw it again
    def handleZoom(self,event):

        print("we be zooming")

        original_zoom = self.zoom

        if event.num == 4 or event.delta == -120:

            if(self.zoomIndex - 1 >= 90):
                self.zoomIndex = self.zoomIndex - 1

        if event.num == 5 or event.delta == 120:

            if(self.zoomIndex + 1 <= 130):
                self.zoomIndex = self.zoomIndex + 1


        if(self.zoomIndex >= 90 and self.zoomIndex < 100):
            self.zoom = .5
            self.fontsize = 6

        elif(self.zoomIndex >= 100 and self.zoomIndex < 110):
            self.zoom = 1
            self.fontsize = 8

        elif(self.zoomIndex >= 110 and self.zoomIndex < 120):
            self.zoom = 2
            self.fontsize = 16

        elif(self.zoomIndex >= 120 and self.zoomIndex < 130):
            self.zoom = 3
            self.fontsize = 24

        if(original_zoom != self.zoom):
            self.updateTree()
    #saves the ontology in rdf format
    def saveOntology(self):

        output_file = self.outputEntry.get()

        #self.owlBase.owlReadyOntology.save(file = "./../../src/asklab/querypicker/QUERIES/BASE/" + output_file, format = "rdfxml")
        self.owlBase.owlReadyOntology.save(file = output_file, format = "rdfxml")

        self.processFile(output_file)

        summary = "Outputted ontology to file: " + output_file
        self.printSummary(summary)

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

             print("in zoom 3")
             #print(self.owlTree.minX)
             #print(self.owlTree.minY)
             rightmostx = leftmostx + .05*self.owlTree.totalX
             rightmosty = leftmosty + .25*self.owlTree.totalY



         self.treeAxis.set(xlim=(leftmostx, rightmostx), ylim=(leftmosty, rightmosty))
         self.treeChart.draw()





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

fontStyle = tkFont.Font(family="Lucida Grande", size=8, weight = "bold")

headerFont = tkFont.Font(family = "Helvetica",size = 12, weight = "bold")
promptFont = tkFont.Font(family = "Lucida Grande", size = 8, weight = "bold")
infoFont = tkFont.Font(family = "lucida Grande", size = 8, weight = "bold")
entryFont = tkFont.Font(family = "Verdana", size = 10, weight = "bold")
buttonFont = tkFont.Font(family = "Helvetica", size = 8, weight = "normal")
summaryFont = tkFont.Font(family = "Lucida Grande", size = 8, weight = "bold")

tiny = tkFont.Font(family="Lucida Grande", size=1, weight = "bold")
small = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
med = tkFont.Font(family="Lucida Grande", size=12, weight = "bold")
big = tkFont.Font(family="Lucida Grande", size=18, weight = "bold")
selectFont = tkFont.Font(family="Lucida Grande", size=11, weight = "bold")
my_gui = OntologyGUI(root)
root.mainloop()

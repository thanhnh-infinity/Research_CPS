
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

from owlOntology import owlOntology
from script_networkx import remove_namespace
from owlOntology import is_asp_or_conc


from owlready2 import *
pressed = False
spartangreen = "#18453b"

class OntologyGUI:

    def __init__(self,master):

        self.zoom = 1
        self.zoom_index = 105
        self.fontsize = 8

        self.leftclickwindowopen = False
        self.rightclickwindowopen = False
        self.edgeWindowOpen = False
        

        self.hovered_node = None
        self.owl_loaded = False
        

        self.master = master




        self.master.bind("<Button-4>", self.do_zoom)
        self.master.bind("<Button-5>", self.do_zoom)
        self.master.bind("<MouseWheel>", self.do_zoom)

        master.title("Ontology GUI")

        #set up main canvas
        self.canvas = Canvas(master, height = 1200, width = 1900, bg = "#18453b")
        self.canvas.pack()

        #set up title text
        self.header_frame = Frame(master,bg ="#18453b" )
        self.header_frame.place(relwidth = .8, relheight = .06, relx = .1, rely = 0.02)
        self.header_text = Label(self.header_frame, text="CPS Ontology Visualization",fg = "white",bg = "#18453b", font = "Helvetica 30 bold italic")
        self.header_text.pack()

        #set up footer text
        self.footer_frame = Frame(master,bg ="#18453b")
        self.footer_frame.place(relwidth = .4, relheight = .2, relx = .61, rely = 0.9)
        self.footer_text = Label(self.footer_frame, text="Matt Bundas, Prof. Son Tran, Thanh Ngyuen, Prof. Marcello Balduccini",fg = "white",bg = "#18453b", font = "Helvetica 8 bold italic", anchor = "e")
        self.footer_text.pack()

        #set up frame on left for inputs
        self.input_frame = Frame(master, bg="white")
        self.input_frame.place(relwidth = .2, relheight = .8, relx = .01, rely = 0.1)

        #set up prompt/entry for input ontology
        self.inputPrompt = Label(self.input_frame, text = "Input ontology", font = fontStyle,fg= "#747780",bg = "white")
        self.inputPrompt.pack()

        self.input_owl_entry = Entry(self.input_frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.input_owl_entry.pack()
        self.input_owl_entry.insert(0,"cpsframework-v3-base.owl")

        #button to load ontology, calls function which handles loading
        self.loadOntology = tk.Button(self.input_frame, text = "Load Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.load_ontology)
        self.loadOntology.pack()

        self.add_space(self.input_frame,"white","medium")


        #sets up prompt/entry for name of output owl file
        self.outputPrompt = Label(self.input_frame, text =  "Output Name", font = fontStyle,fg= "#747780",bg = "white")
        self.outputPrompt.pack()

        self.output_owl_entry = Entry(self.input_frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.output_owl_entry.pack()
        self.output_owl_entry.insert(2, "cpsframework-v3-base.owl")

        #sets up button to call function which handles saving ontology
        self.saveOntology = tk.Button(self.input_frame, text = "Output Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.save_ontology)
        self.saveOntology.pack()


        #sets up gray box for information window

        self.infoWindow = Frame(self.input_frame, bg = "#747780", bd = 5 )
        self.infoWindow.place(relwidth = .8, relheight = .48, relx = .1, rely = .30)

        self.infoWindowHeader = Label(self.infoWindow,text = "Ontology Information", font = "Helvetica 12 bold italic", fg = "white", bg = "#747780")
        self.infoWindowHeader.pack()

        self.owlInfoWindow = Frame(self.infoWindow, bg = spartangreen, bd = 5)
        self.owlInfoWindow.place(relwidth = .9, relheight = .5, relx = .05, rely = .05)

        self.indWindowHeaderFrame = Frame(self.infoWindow, bg = "#747780",bd = 5)
        self.indWindowHeaderFrame.place(relwidth = .9, relheight = .07, relx  = .05, rely = .595)

        self.indWindowHeader = Label(self.indWindowHeaderFrame,text = "Individual Information", font = "Helvetica 12 bold italic", fg = "white", bg = "#747780")
        self.indWindowHeader.pack()

        self.indInfoWindow = Frame(self.infoWindow,  bg = spartangreen, bd = 5)
        self.indInfoWindow.place(relwidth = .9, relheight = .33, relx = .05, rely = .65)



        self.owlNameText = tk.StringVar()
        self.owlNameText.set("Owl Name")

        self.totalIndText = tk.StringVar()
        self.totalIndText.set("Total Nodes")

        self.numAspectsText = tk.StringVar()
        self.numAspectsText.set("Num Aspects")

        self.numConcernsText = tk.StringVar()
        self.numConcernsText.set("Num Concerns")

        self.numPropertiesText = tk.StringVar()
        self.numPropertiesText.set("Num Properties")

        self.numComponentsText = tk.StringVar()
        self.numComponentsText.set("Num Components")


        self.owlNameInfo = Label(self.owlInfoWindow, textvariable =  self.owlNameText, font = fontStyle,fg= "white",bg = spartangreen)
        self.owlNameInfo.pack()

        self.numNodesInfo = Label(self.owlInfoWindow, textvariable =  self.totalIndText, font = fontStyle,fg= "white",bg = spartangreen)
        self.numNodesInfo.pack()

        self.numAspectsInfo = Label(self.owlInfoWindow, textvariable =  self.numAspectsText, font = fontStyle,fg= "white",bg = spartangreen)
        self.numAspectsInfo.pack()

        self.numConcernsInfo = Label(self.owlInfoWindow, textvariable =  self.numConcernsText, font = fontStyle,fg= "white",bg = spartangreen)
        self.numConcernsInfo.pack()

        self.numPropertiesInfo = Label(self.owlInfoWindow, textvariable =  self.numPropertiesText, font = fontStyle,fg= "white",bg = spartangreen)
        self.numPropertiesInfo.pack()

        self.numComponentsInfo = Label(self.owlInfoWindow, textvariable =  self.numComponentsText, font = fontStyle,fg= "white",bg = spartangreen)
        self.numComponentsInfo.pack()


        self.indNameText = tk.StringVar()
        self.indNameText.set("Ind Name")

        self.indTypeText = tk.StringVar()
        self.indTypeText.set("Ind Type")

        self.indParentText = tk.StringVar()
        self.indParentText.set("Parent Name")

        self.indChildrenText = tk.StringVar()
        self.indChildrenText.set("Children")

        self.indRelPropertiesText = tk.StringVar()
        self.indRelPropertiesText.set("Relevant Properties")

        self.indNameInfo = Label(self.indInfoWindow, textvariable = self.indNameText ,fg= "white",bg = spartangreen,font = fontStyle)
        self.indNameInfo.pack()

        self.indTypeInfo = Label(self.indInfoWindow, textvariable = self.indTypeText,fg= "white",bg = spartangreen,font = fontStyle)
        self.indTypeInfo.pack()

        self.indParentInfo = Label(self.indInfoWindow, textvariable =  self.indParentText,fg= "white",bg = spartangreen,font = fontStyle)
        self.indParentInfo.pack()

        self.indChildInfo = Label(self.indInfoWindow, textvariable =  self.indChildrenText,fg= "white",bg = spartangreen,font = fontStyle)
        self.indChildInfo.pack()

        self.indPropertyInfo = Label(self.indInfoWindow, textvariable =  self.indRelPropertiesText,fg= "white",bg = spartangreen,font = fontStyle)
        self.indPropertyInfo.pack()


        #sets up gray box to put text to show what is going on
        self.textBox = Frame(self.input_frame,bg = "#747780", bd = 5)
        self.textBox.place(relwidth = .8, relheight = .15, relx = .1, rely = .80)

        #sets up frame for ontology tree to exist
        self.tree_frame = tk.Frame(self.master, bg="white")
        self.tree_frame.place(relwidth = .70, relheight = .8, relx = .25, rely = 0.1)




        self.fig, self.ax = plt.subplots(figsize = (15,15))
        self.chart = FigureCanvasTkAgg(self.fig,self.tree_frame)

        self.ax.clear()
        self.ax.axis('off')
        self.chart.get_tk_widget().pack()



        #set up sliders/zoom button in tree frame
        self.xslider_frame = tk.Frame(self.tree_frame,bg = "white")
        self.xslider_frame.place(relwidth = .7, relheight = .05, relx = .15, rely = .95)

        self.xslider = Scale(self.xslider_frame, from_ = 0, to = 100,orient = HORIZONTAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)
        self.xslider.pack()


        self.yslider_frame = tk.Frame(self.tree_frame,bg = "white")
        self.yslider_frame.place(relwidth = .03, relheight = .7, relx = .95, rely = .15)

        self.yslider = Scale(self.yslider_frame, from_ = 80, to = 0,orient = VERTICAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)
        self.yslider.pack()


        self.edge_button_frame = tk.Frame(self.tree_frame,bg = "white")
        self.edge_button_frame.place(relwidth = .10, relheight = .05, relx = .01, rely = .01)
        
        self.edge_button = tk.Button(self.edge_button_frame, text = "Relations",padx = 10, pady = 5, bg = spartangreen, fg = "white",borderwidth = 5, command = self.onEdgeButton)
        self.edge_button.pack()
        
        self.remEdgelessFrame = tk.Frame(self.tree_frame,bg = "white")
        self.remEdgelessFrame.place(relwidth = .10, relheight = .05, relx = .89, rely = .01)
    
        self.remove_edgeless_button = tk.Button(self.remEdgelessFrame, text = "Remove Floaters",padx = 10, pady = 5, bg = spartangreen, fg = "white",borderwidth = 5, command = self.removeFloaters)
        self.remove_edgeless_button.pack()
    


        self.chart.mpl_connect("button_press_event",self.handleClick)
        self.chart.mpl_connect("motion_notify_event",self.handleHover)


    #removes all nodes which dont have any parents nor any children, and are not aspects
    def removeFloaters(self):
        
        self.owlOntology.removeEdgeless()
        self.update_tree()
        
    #gets the accturate OWL Object via searching the ontology for the passed name
    def getOWLObject(self,name):
        
        obj_list = self.owlOntology.owlReadyOntology.ontology.search(iri = "*" + name)

        obj_names = []
        
        for obj in obj_list:
            obj_names.append(remove_namespace(obj))

        i = 0
        while i < len(obj_names):
            
            if(obj_names[i] == name):
                break

            i = i + 1
        obj = obj_list[i]
        
        return obj

    #handles mouse hovering, throws away nonsense events, updates individual info window
    def handleHover(self,event):

        if(self.owl_loaded == False):
            return

        NoneType = type(None)


        if(type(event.xdata) == NoneType or type(event.ydata) == NoneType):
            return

        nearest_node = self.get_nearest(event)

        if(nearest_node != self.hovered_node):


            self.hovered_node = nearest_node
            self.indNameText.set("Ind Name - " + str(self.hovered_node.name))
            self.indTypeText.set("Ind Type - " + str(self.hovered_node.type))
            self.indParentText.set("Parent Name - " + str(self.hovered_node.parent))
            self.indChildrenText.set("Children - " + str(self.hovered_node.children))
            self.indRelPropertiesText.set("Relevant Properties - ")


    #updates the global ontology stats according to numbers stored in owlOntology
    def updateOwlStats(self):

            self.owlNameText.set("Owl Name - " + str(self.owlOntology.owlName))
            self.totalIndText.set("Num Nodes - " + str(self.owlOntology.numNodes))
            self.numAspectsText.set("Num Aspects - " + str(self.owlOntology.numAspects))
            self.numConcernsText.set("Num Concerns - "  + str(self.owlOntology.numConcerns))
            self.numPropertiesText.set("Num Properties - " + str(self.owlOntology.numProperties))
            self.numComponentsText.set("Num Components - " + str(self.owlOntology.numComponents))



    #adds a concern to the ontology, uses gui entries for inputs, updates tree afterwards
    def add_concern(self):


        #grab name of new concern
        new_concern_name = self.indivNameEntry.get()

        #handle error message, if new individual with name already exists, don't add another
        if(self.check_existence(new_concern_name) == True):
           print("individual already exists")
           if(self.error_displayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.buttonwindow, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.error_displayed = True
           return

        #instantiate the object with the given new name
        new_concern = self.owlOntology.owlReadyOntology.Concern(new_concern_name,ontology = self.owlOntology.owlReadyOntology)

        #add the new concern as a subconcern of the clicked node
        subconcern_of = self.getOWLObject(self.parent.name)
        subconcern_of.includesConcern.append(new_concern)

        #prints text in textbox to tell what happend
        summary = "Added concern " + new_concern_name + " to ontology"

        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()

        #refresh the tree and owlOntology
        self.update_tree()

        #reset the error message because we just did a successful operation
        if(self.error_displayed == True):
            self.error_message.destroy()
            self.error_displayed == False

        print("added concern")

    #checks if an individual with the passed name exists
    def check_existence(self,individual):

        #print("checking existence")
        xx = self.owlOntology.owlReadyOntology.search(iri = "*" + individual)

        if(len(xx) == 0):
            return False
        else:
            return True


    #takes a mouse event, returns the closest node to the mouse event
    def get_nearest(self,event):

        NoneType = type(None)
        (x,y) = (event.xdata, event.ydata)
       
        smallestdistance = 9999999999
        closestnode = None
       
        for node in self.owlOntology.nodeArray:

            nodepos = self.owlOntology.graphPositions[node.name]
        
            distance = np.sqrt((x - nodepos[0])**2 + (y - nodepos[1])**2)
            if(distance < smallestdistance):
                closestnode = node
                smallestdistance = distance
       
        return closestnode

    #returns the type of node with passed name, returns string
    def get_type(self,name):
        selected_item = self.getOWLObject(name)
        type_item = remove_namespace(selected_item.is_a)

        return type_item


    #handles the given click event, sends code to either handle edge click, normal left click, or right click event
    def handleClick(self,event):

     
        if(event.button == 1):
            
            if(self.edgeWindowOpen == True):
                self.handleEdgeLeftClick(event)
            else:
                self.onLeftClick(event)

        if(event.button == 3):
            self.onRightClick(event)

    #takes care of right clicks, opens up window where you can add a new aspect
    def onRightClick(self,event):

    
        if(self.owl_loaded == False or self.rightclickwindowopen == True):
            return

        #set up windows and frames
        self.rightclickwindow = tk.Toplevel(height = 400, width = 300, bg = spartangreen)
        self.rightclickwindow.title("Add New Aspect")
        self.rightclickwindow.protocol("WM_DELETE_WINDOW", self.rightclickWindowClose)
        
        self.rcerror_displayed = False

        self.rcwtframe = tk.Frame(self.rightclickwindow,bg = spartangreen)
        self.rcwtframe.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)

        self.rcbuttonframe = tk.Frame(self.rightclickwindow, bg = "white")
        self.rcbuttonframe.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)
        
        self.rctitleframe = tk.Frame(self.rightclickwindow,bg = spartangreen)
        self.rctitleframe.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)
        
        showtext = "Add New Parent Concern or Aspect"

        self.rcwindowtitle = Label(self.rctitleframe, text =  showtext,fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.rcwindowtitle.pack()
        
        #set up prompt for new aspect name
        self.rcIndivNamePrompt = Label(self.rcbuttonframe, text = "Name of New Aspect", font = fontStyle,fg= "#747780",bg = "white")
        self.rcIndivNamePrompt.pack()
        
        self.rcIndivNameEntry = Entry(self.rcbuttonframe, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.rcIndivNameEntry.pack()
        self.rcIndivNameEntry.insert(1,"NewIndividual")
        
        #add button to call function to add new aspect
        addAspect = tk.Button(self.rcbuttonframe, text = "Add Aspect",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_aspect)
        addAspect.pack()
       
    #function to handle when you click Relations button, opens up window where you can do relation operations   
    def onEdgeButton(self):
        
        if(self.edgeWindowOpen == True):
            return
        
        #set up window and frames
        self.edgeWindow = tk.Toplevel(height = 400, width = 300, bg = spartangreen)
        self.edgeWindow.transient(master = self.master)
        self.edgeWindow.title("Add New Relation")
        
        self.edgeWindowOpen = True
        self.readyForEdgeButton = False
        self.edgeClickSelecting = "Parent"
        self.edgeWindow.protocol("WM_DELETE_WINDOW", self.edgeWindowClose)
        
        self.edgeTitleFrame = tk.Frame(self.edgeWindow,bg = spartangreen)
        self.edgeTitleFrame.place(relwidth = .8, relheight = .20, relx = .10, rely = .01)
        
        showtext = "Add New Edge \nClick on Desired Parent \nThen Click on Desired Child"

        self.edgeWindowTitle = Label(self.edgeTitleFrame, text = showtext,fg= "white",bg = spartangreen,font = "Helvetica 8 bold italic")
        self.edgeWindowTitle.pack()

        self.edgeButtonFrame = tk.Frame(self.edgeWindow, bg = "white")
        self.edgeButtonFrame.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)
        
        self.edgeParentText = tk.StringVar()
        self.edgeParentText.set("Edge Parent - ")
        
        self.edgeChildText = tk.StringVar()
        self.edgeChildText.set("Edge Child - ")
        
        self.edgeParentLabel = Label(self.edgeButtonFrame, textvariable = self.edgeParentText, font = "Helvetica 8 bold",fg= "#747780",bg = "white")
        self.edgeParentLabel.pack()
        
        self.edgeChildLabel = Label(self.edgeButtonFrame, textvariable = self.edgeChildText, font = "Helvetica 8 bold",fg= "#747780",bg = "white")
        self.edgeChildLabel.pack()
        
        #add buttons for adding subconcern, addresses, remove relation
        addSubConcern = tk.Button(self.edgeButtonFrame, text = "Add Subconcern Relation",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.addSubConcernRelation)
        addSubConcern.pack()
        
        addPropAddresses = tk.Button(self.edgeButtonFrame, text = "Add Property Addresses Relation",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.addAddressesConcernRelation)
        addPropAddresses.pack()
        
        removeRelation = tk.Button(self.edgeButtonFrame, text = "Remove Relation",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.removeRelation)
        removeRelation.pack()
    
      
    #handles clicks to set up edges, sets either parent or child node
    def handleEdgeLeftClick(self,event):
        
        #if we are selecting parent, make click select parent, then have it select child next
        if(self.edgeClickSelecting == "Parent"):
            print("selected parent")
            self.readyForEdgeButton = False
            closestnode = self.get_nearest(event)
            
            self.edgeParent = closestnode 
            self.edgeParentText.set("Edge Parent - " + self.edgeParent.name)
            
            self.edgeClickSelecting = "Child"
            
            return
        
        #if we are selecting child, make click select child, then have it select parent next
        elif(self.edgeClickSelecting == "Child"):
            closestnode = self.get_nearest(event)
            self.edgeChild = closestnode
            self.edgeChildText.set("Edge Child - " + self.edgeChild.name)
            
            print("selected child")
            self.edgeClickSelecting = "Parent"
            
            self.readyForEdgeButton = True

    
    #adds a property addressesConcern relation, not functional at the moment
    def addAddressesConcernRelation(self):
    
        return
        if(self.readyForEdgeButton == False):
            print("not ready for edge yet")
            return 
        
        parent_edge = self.getOWLObject(self.edgeParent.name)
        child_edge = self.getOWLObject(self.edgeChild.name)
        
        child_type = remove_namespace(child_edge.is_a[0])
        parent_type = remove_namespace(parent_edge.is_a[0])
        
        if(is_asp_or_conc(child_type) == True and is_asp_or_conc(parent_type) == True):
            print("Neither node is a property")
            return
        
        print("trying to add addresses relation")
        return
        
    #adds a subconcern relation between selected parent and child
    def addSubConcernRelation(self):
        
        if(self.readyForEdgeButton == False):
            print("not ready for edge yet")
            return 
        
        parent_edge = self.getOWLObject(self.edgeParent.name)
        child_edge = self.getOWLObject(self.edgeChild.name)
     
        child_type = remove_namespace(child_edge.is_a[0])
        parent_type = remove_namespace(parent_edge.is_a[0])
        
        if(is_asp_or_conc(child_type) == False or is_asp_or_conc(parent_type) == False):
            print("Either parent or child is not a concern")
            return
        
        parent_edge.includesConcern.append(child_edge)
        
        self.update_tree() 
        
    #removes the selected relation, at the moment just handles subconcern relation
    def removeRelation(self):
        
        if(self.readyForEdgeButton == False):
            print("not ready for button yet")
            return 
        
        parent_edge = self.getOWLObject(self.edgeParent.name)
        child_edge = self.getOWLObject(self.edgeChild.name)
        
        child_type = remove_namespace(child_edge.is_a[0])
        parent_type = remove_namespace(parent_edge.is_a[0])
        
        if(is_asp_or_conc(child_type) == False or is_asp_or_conc(parent_type) == False):
            print("One node is not a concern")
            return
        
        parent_edge.includesConcern.remove(child_edge)
        self.update_tree() 
        
    #handles closing relations window    
    def edgeWindowClose(self):
        
        self.edgeWindow.destroy()
        self.edgeWindowOpen = False
        
    #function to add parent to clicked node
    def add_parent(self):
        
        #get name from Entry
        new_parent_name = self.indivNameEntry.get()
        
        #handle error message, if new individual with name already exists, don't add another
        if(self.check_existence(new_parent_name) == True):
           print("individual already exists")
           if(self.error_displayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.buttonwindow, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.error_displayed = True
           return
      
        #instantiate new concern
        new_parent_concern = self.owlOntology.owlReadyOntology.Concern(new_parent_name,ontology = self.owlOntology.owlReadyOntology)
    
        #get owlready object of selected node
        parent_of = self.getOWLObject(self.parent.name)
        
        #sets up parent relation
        new_parent_concern.includesConcern.append(parent_of)
        
        self.update_tree()
        
    #function to add aspect to ontology
    def add_aspect(self):
        
        #get name of new aspect from entry
        new_aspect_name = self.rcIndivNameEntry.get()

        #handle error message, if new individual with name already exists, don't add another
        if(self.check_existence(new_aspect_name) == True):
           print("individual already exists")
           if(self.rcerror_displayed == True):
               self.rcerror_message.destroy()
           self.rcerror_message = Label(self.rcbuttonframe, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.rcerror_message.pack()
           self.rcerror_displayed = True
           return
        
        #instantiate new aspect object
        new_aspect = self.owlOntology.owlReadyOntology.Aspect(new_aspect_name,ontology = self.owlOntology.owlReadyOntology)

        #prints text in textbox to tell what happend
        summary = "Added Aspect " + new_aspect_name + " to ontology"

        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()

        self.update_tree()

        if(self.rcerror_displayed == True):
            self.rcerror_message.destroy()
            self.rcerror_displayed == False

        print("added aspect")


    #handles opening left click window, where you can edit clicked individuals
    def onLeftClick(self,event):

        if(self.leftclickwindowopen == True or self.owl_loaded == False):
            return

        self.error_displayed = False

        #get the node you just clicked on
        closestnode = self.get_nearest(event)
        
        #set global "parent" variable which is essentially the selected node which will be used by other functions
        self.parent = closestnode
        
        #open up window and frames
        self.onleftclickwindow = tk.Toplevel(height = 400, width = 300,bg = spartangreen )
        self.onleftclickwindow.transient(master = self.master)

        self.leftclickwindowopen = True
        self.onleftclickwindow.title("Individual Editor")

        self.onleftclickwindow.protocol("WM_DELETE_WINDOW", self.leftclickWindowClose)

        self.wtitleframe = tk.Frame(self.onleftclickwindow,bg = spartangreen)

        self.wtitleframe.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)

        self.buttonwindow = tk.Frame(self.onleftclickwindow, bg = "white")
        self.buttonwindow.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)

        type_item = closestnode.type
    
        showtext = type_item  + " - " + closestnode.name

        self.windowtitle = Label(self.wtitleframe, text =  showtext,fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.windowtitle.pack()

        self.indivNamePrompt = Label(self.buttonwindow, text = "Name of New Individual", font = fontStyle,fg= "#747780",bg = "white")
        self.indivNamePrompt.pack()

        self.indivNameEntry = Entry(self.buttonwindow, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.indivNameEntry.pack()
        self.indivNameEntry.insert(1,"NewIndividual")

        #set up buttons for operations
        addConcern = tk.Button(self.buttonwindow, text = "Add SubConcern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_concern)
        addConcern.pack()

        addProperty = tk.Button(self.buttonwindow, text = "Add Property",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_property)
        addProperty.pack()
        
        addParent = tk.Button(self.buttonwindow, text = "Add Parent Concern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_parent)
        addParent.pack()

        removeIndividualB = tk.Button(self.buttonwindow, text = "Remove Individual",padx = 10, pady = 5,  bg = "#18453b", fg = "white",borderwidth = 5,command = self.removeIndividual)
        removeIndividualB.pack()
        
        editName = tk.Button(self.buttonwindow, text = "Edit Name",padx = 10, pady = 5,  bg = "#18453b", fg = "white",borderwidth = 5,command = self.editIndividual)
        editName.pack()
        
    #handles editing an individual
    def editIndividual(self):
        
        #adds concern in
        new_name = self.indivNameEntry.get()

        if(self.check_existence(new_name) == True):
           print("individual already exists")
           if(self.error_displayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.buttonwindow, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.error_displayed = True
           return

        
        #grab owlready object
        to_edit = self.getOWLObject(self.parent.name)

        #change name of olwready object
        to_edit.name = new_name
        
        print("Changing name of " + self.parent.name + " to " + str(new_name))
        self.update_tree()

    #handles closing individual editor window
    def leftclickWindowClose(self):

        self.onleftclickwindow.destroy()
        self.leftclickwindowopen = False
        self.parent = None
        
    #handles closing right click window
    def rightclickWindowClose(self):
        
        self.rightclickwindow.destroy()
        self.rightclickwindowopen = False
        self.parent = None
        

    #handles removing individual left clicked on
    def removeIndividual(self):

        individual = self.getOWLObject(self.parent.name)
      
        destroy_entity(individual)
        self.leftclickWindowClose()
        self.update_tree()

    #adds a property to the ontology, uses gui for inputs, updates tree afterwards
    def add_property(self):

        #add in the property
        new_property_name = self.indivNameEntry.get()

        #handle error message, if new individual with name already exists, don't add another
        if(self.check_existence(new_property_name) == True):
           print("individual already exists")
           if(self.error_displayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.buttonwindow, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.error_displayed = True
           return

      
        #instantiate the new property given the new name
        new_property = self.owlOntology.owlReadyOntology.Property(new_property_name, ontology = self.owlOntology.owlReadyOntology)
       
        #fill in new properties attributes
        new_property.hasType.append(self.owlOntology.owlReadyOntology.PropertyType_Assertion)
        new_property.atomicStatement.append("new_atomic_statement")
        new_property.comment.append("new_comment")

        #new property requires new IR and new condition
        new_ir_name = self.get_ir_name()
        new_cond_name = self.get_cond_name()

        #add condition with given name
        new_condition = self.owlOntology.owlReadyOntology.Condition(new_cond_name, ontology = self.owlOntology.owlReadyOntology)
        new_condition.conditionPolarity.append(self.owlOntology.owlReadyOntology.positive)
        new_condition.conditionProperty.append(new_property)

        #find concern that is clicked on, new property addresses it
        addressed_concern = self.getOWLObject(self.parent.name)

        #add the impact rule
        new_impact_rule = self.owlOntology.owlReadyOntology.ImpactRule(new_ir_name,ontology = self.owlOntology.owlReadyOntology)
        new_impact_rule.addressesAtFunc.append(self.owlOntology.owlReadyOntology.bc1)
        new_impact_rule.addressesConcern.append(addressed_concern)
        new_impact_rule.addressesPolarity.append(self.owlOntology.owlReadyOntology.positive)
        new_impact_rule.hasCondition.append(new_condition)
        new_impact_rule.comment.append("new_comment")


        #prints text in text box
        summary = "Added property " + new_property_name + " to ontology"

        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()

        self.update_tree()

        if(self.error_displayed == True):
            self.error_message.destroy()
            self.error_displayed == False

    #returns the suitable ir name given how many already exist
    def get_ir_name(self):

        new_ir_num = self.owlOntology.numImpactRules + 1

        if(new_ir_num >= 1000):
            return "ir" + str(new_ir_num)
        if(new_ir_num >= 100):
            return "ir0" + str(new_ir_num)
        if(new_ir_num >= 10):
            return "ir00" + str(new_ir_num)
        if(new_ir_num >= 1):
            return "ir000" + str(new_ir_num)

    #returns the suitable condition name given how many already exist
    def get_cond_name(self):

        new_cond_num = self.owlOntology.numConditions + 1

        if(new_cond_num >= 1000):
            return "c" + str(new_cond_num) + "_01"
        if(new_cond_num >= 100):
            return "c0" + str(new_cond_num) + "_01"
        if(new_cond_num >= 10):
            return "c00" + str(new_cond_num) + "_01"
        if(new_cond_num >= 1):
            return "c000" + str(new_cond_num) + "_01"



    #clears the tree, re sets up owlOntology and graph, draws it 
    def update_tree(self):

         self.ax.clear()

        
         self.owlOntology.constructIndividualArray()
         self.owlOntology.setNumbers()

         self.owlOntology.makeGraph()

         self.scale_tree(3)

         self.owlOntology.draw_graph(self.ax,self.fontsize)


         self.chart.draw()

         self.updateOwlStats()




    #loads the specified ontology file in
    def load_ontology(self):

        self.owlOntology = owlOntology(self.input_owl_entry.get())

        summary = "Loaded ontology " + "file://./" + self.input_owl_entry.get()

        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle, fg= "white",bg = "#747780")
        self.summaryLabel.pack()

        self.update_tree()

        self.owl_loaded = True





    #updates the dropdowns containing the list of concerns, keeps whatever is currently select3ed
    def update_concern_dropdown(self):

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

    #changes zoom level, fontsize, then calls update_tree to draw it again
    def do_zoom(self,event):

        print("we be zooming")

        original_zoom = self.zoom

        if event.num == 4 or event.delta == -120:

            if(self.zoom_index - 1 >= 90):
                self.zoom_index = self.zoom_index - 1

        if event.num == 5 or event.delta == 120:

            if(self.zoom_index + 1 <= 130):
                self.zoom_index = self.zoom_index + 1


        if(self.zoom_index >= 90 and self.zoom_index < 100):
            self.zoom = .5
            self.fontsize = 6

        elif(self.zoom_index >= 100 and self.zoom_index < 110):
            self.zoom = 1
            self.fontsize = 8

        elif(self.zoom_index >= 110 and self.zoom_index < 120):
            self.zoom = 2
            self.fontsize = 16

        elif(self.zoom_index >= 120 and self.zoom_index < 130):
            self.zoom = 3
            self.fontsize = 24

        if(original_zoom != self.zoom):
            self.update_tree()
    #saves the ontology in rdf format
    def save_ontology(self):

        output_file = self.output_owl_entry.get()

        #self.owlOntology.owlReadyOntology.save(file = "./../../src/asklab/querypicker/QUERIES/BASE/" + output_file, format = "rdfxml")
        self.owlOntology.owlReadyOntology.save(file = output_file, format = "rdfxml")

        self.process_file(output_file)

        summary = "Outputted ontology to file: " + output_file
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()


    #changes the portion of axis we view according to zoom level, slider position
    def scale_tree(self,var):

         leftmostx = self.owlOntology.minX + self.owlOntology.totalX*self.xslider.get()/100
         leftmosty = self.owlOntology.minY + self.owlOntology.totalY*self.yslider.get()/100

         if(self.zoom == .5):

             leftmosty = self.owlOntology.minY - .5*self.owlOntology.totalY
             rightmosty = self.owlOntology.maxY + .5 * self.owlOntology.totalY

             rightmostx = leftmostx + .50 * self.owlOntology.totalX


         if (self.zoom == 1):
             leftmosty = self.owlOntology.minY
             rightmostx = leftmostx + .20*self.owlOntology.totalX
             rightmosty = self.owlOntology.maxY

         if (self.zoom == 2):

             rightmostx = leftmostx + .10*self.owlOntology.totalX
             rightmosty = leftmosty + .60*self.owlOntology.totalY

         if (self.zoom == 3):

             print("in zoom 3")
             #print(self.owlOntology.minX)
             #print(self.owlOntology.minY)
             rightmostx = leftmostx + .05*self.owlOntology.totalX
             rightmosty = leftmosty + .25*self.owlOntology.totalY



         self.ax.set(xlim=(leftmostx, rightmostx), ylim=(leftmosty, rightmosty))
         self.chart.draw()



    #function to add space in specified location, with specified color
    def add_space(self,on,color,size):

        if(size == "small"):
            self.emptySpace = Label(on, text = "", font = small,bg = color)

        if(size == "medium"):
            self.emptySpace = Label(on, text = "", font = med,bg = color)

        if(size == "large"):
            self.emptySpace = Label(on, text = "", font = large,bg = color)

        self.emptySpace.pack()


    #handles processing the output file after we save it, for now just strips string tag in owl file.
    def process_file(self,output_file):

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
small = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
med = tkFont.Font(family="Lucida Grande", size=12, weight = "bold")
big = tkFont.Font(family="Lucida Grande", size=18, weight = "bold")
selectFont = tkFont.Font(family="Lucida Grande", size=11, weight = "bold")
my_gui = OntologyGUI(root)
root.mainloop()

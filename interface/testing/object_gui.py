from script_networkx import draw_ontology, remove_namespace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from script_networkx import draw_ontology
import numpy as np

import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

from owlready2 import *
pressed = False
spartangreen = "#18453b"

class OntologyGUI:
    
    def __init__(self,master):
        
        self.zoom = 1
        self.zoom_index = 105
        self.fontsize = 8
        
        self.leftclickwindowopen = False
        
        self.hovered_node = None
        self.owl_loaded = False
        
        self.master = master
        
      
        
        
        self.master.bind("<Button-4>", self.do_zoom)
        self.master.bind("<Button-5>", self.do_zoom)
        self.master.bind("<MouseWheel>", self.do_zoom)
        
        master.title("Ontology GUI")
          
        #set up main canvas
        self.canvas = Canvas(master, height = 1200, width = 2000, bg = "#18453b")
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
        self.output_owl_entry.insert(2, "newConcern.owl")
        
        #sets up button to call function which handles saving ontology
        self.saveOntology = tk.Button(self.input_frame, text = "Output Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.save_ontology)
        self.saveOntology.pack()
        
        
        #sets up gray box for information window
        
        self.infoWindow = Frame(self.input_frame, bg = "#747780", bd = 5 )
        self.infoWindow.place(relwidth = .8, relheight = .48, relx = .1, rely = .30)
        
        
        self.owlInfoWindow = Frame(self.infoWindow, bg = spartangreen, bd = 5)
        self.owlInfoWindow.place(relwidth = .9, relheight = .5, relx = .05, rely = .05)
        
        self.indInfoWindow = Frame(self.infoWindow,  bg = "pink", bd = 5)
        self.indInfoWindow.place(relwidth = .9, relheight = .35, relx = .05, rely = .6)
        
        
        self.owlNameInfo = Label(self.owlInfoWindow, text =  "Owl Name", font = fontStyle,fg= "#747780",bg = "white")
        self.owlNameInfo.pack()
        
        self.numAspectsInfo = Label(self.owlInfoWindow, text =  "Num Aspects", font = fontStyle,fg= "#747780",bg = "white")
        self.numAspectsInfo.pack()
        
        self.numConcernsInfo = Label(self.owlInfoWindow, text =  "Num Concerns", font = fontStyle,fg= "#747780",bg = "white")
        self.numConcernsInfo.pack()
        
        self.numPropertiesInfo = Label(self.owlInfoWindow, text =  "Num Properties", font = fontStyle,fg= "#747780",bg = "white")
        self.numPropertiesInfo.pack()
        
        self.numComponentsInfo = Label(self.owlInfoWindow, text =  "Num Components", font = fontStyle,fg= "#747780",bg = "white")
        self.numComponentsInfo.pack()
        
        
        self.indNameText = tk.StringVar()
        self.indNameText.set("Ind Name")
        
        self.indNameInfo = Label(self.indInfoWindow, textvariable = self.indNameText ,fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.indNameInfo.pack()
        
        self.indTypeInfo = Label(self.indInfoWindow, text =  "Ind Type",fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.indTypeInfo.pack()
        
        self.indParentInfo = Label(self.indInfoWindow, text =  "Parent",fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.indParentInfo.pack()
        
        self.indChildInfo = Label(self.indInfoWindow, text =  "Children",fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.indChildInfo.pack()
        
        self.indPropertyInfo = Label(self.indInfoWindow, text =  "Relevant Properties",fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
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
        
        
        self.zoom_frame = tk.Frame(self.tree_frame,bg = "white")
        self.zoom_frame.place(relwidth = .05, relheight = .05, relx = .94, rely = .01)
        
      
     
        self.chart.mpl_connect("button_press_event",self.handleClick)
        self.chart.mpl_connect("motion_notify_event",self.handleHover)
        
        
        
      
    def handleHover(self,event):
        
        if(self.owl_loaded == False):
            return
        
        NoneType = type(None)
        
        
        if(type(event.xdata) == NoneType or type(event.ydata) == NoneType):
            return
       
        nearest_node = self.get_nearest(event)
        
        if(nearest_node != self.hovered_node):
           
            #self.indNameInfo.destroy()
            self.indNameText.set(str(nearest_node))
            #self.indNameInfo.pack()
            
            self.hovered_node = nearest_node
        
        
        
    #adds a concern to the ontology, uses gui entries for inputs, updates tree afterwards
    def add_concern(self):
    
        
        #adds concern in
        new_concern = self.indivNameEntry.get()
        
        if(self.check_existence(new_concern) == True):
           print("individual already exists")
           if(self.error_displayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.buttonwindow, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.error_displayed = True
           return
       
        test_concern = self.ontology.Concern(new_concern,ontology = self.ontology)
        
        subconcern_of = self.ontology.search(iri = "*" + self.parent)
        subconcern_of = subconcern_of[0]
        
        subconcern_of.includesConcern.append(test_concern)
            
        #prints text in textbox to tell what happend
        summary = "Added concern " + new_concern + " to ontology"
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
             
        self.update_tree()
        
        if(self.error_displayed == True):
            self.error_message.destroy()
            self.error_displayed == False
    
    def check_existence(self,individual):
        
        print("checking existence")
        xx = self.ontology.search(iri = "*" + individual)
        
        
        if(len(xx) == 0):
            return False
        else:
            return True
        
    def get_nearest(self,event):
        
        NoneType = type(None)
        (x,y) = (event.xdata, event.ydata)
        #print("clicked")
        #print(x)
        #print(y)
        
        
        smallestdistance = 9999999999
        closestnode = None
        #print(self.sorted_concerns)
        for node in self.sorted_concerns:
            
            nodepos = self.positions[node]
            
        
            #print(type(x))
            #print(type(y))
            
            #print(type(nodepos[0]))
            #print(type(nodepos[1]))
            distance = np.sqrt((x - nodepos[0])**2 + (y - nodepos[1])**2)
            if(distance < smallestdistance):
                closestnode = node
                smallestdistance = distance
        #print("closest node is ", closestnode)
        return closestnode
    
    def get_type(self,name):
        selected_item = self.ontology.search(iri = "*" + name)
        selected_item = selected_item[0]
        
        print(selected_item)
        type_item = remove_namespace(selected_item.is_a[0])
        
       
        print("is a ", type_item) 
        
        return type_item
        
        
    
    def do_wheel(self,event):
         print("scrolled")
         #if pressed == False:
         #    return
         global count
         # respond to Linux or Windows wheel event
         if event.num == 5 or event.delta == -120:
             print("down")
         if event.num == 4 or event.delta == 120:
             print("up")

    def handleClick(self,event):
        
        print("pressed ",event.button)
        
        print(type(event))
        
        if(event.button == 1):
            self.onLeftClick(event)
        
        if(event.button == 3):
            self.onRightClick(event)

    def onRightClick(self,event):
        
        if(self.owl_loaded == False):
            return
        
        node = self.get_nearest(event)
        
        newrightclickwindow = tk.Toplevel(height = 400, width = 300, bg = spartangreen)
        
        newrightclickwindow.title("Individual Information")
            
        rcwtframe = tk.Frame(newrightclickwindow,bg = spartangreen)
        
        rcwtframe.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)
        
        textframe = tk.Frame(newrightclickwindow, bg = "white")
        textframe.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)
        
        showtext = "INFO WINDOW"
        
        
        name = node
        node_type = self.get_type(name)
    
        rcwtitle = Label(rcwtframe, text =  showtext,fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        rcwtitle.pack()
        
        namelabel = Label(textframe,text = "Name: " + name, fg = "black",bg = "white", font = "Helvetica 6 bold italic")
        namelabel.pack()
        
        typelabel = Label(textframe,text = "Type: " + node_type, fg = "black",bg = "white", font = "Helvetica 6 bold italic")
        typelabel.pack()
        
        parentlabel = Label(textframe,text = "Parent: ", fg = "black",bg = "white", font = "Helvetica 6 bold italic")
        parentlabel.pack()
        
        childlabel = Label(textframe,text = "Children: ", fg = "black",bg = "white", font = "Helvetica 6 bold italic")
        childlabel.pack()

                
        
        
        
        
        

    def onLeftClick(self,event):
       
        if(self.leftclickwindowopen == True or self.owl_loaded == False):
            return
        
        self.error_displayed = False
        

        closestnode = self.get_nearest(event)
        
        self.onleftclickwindow = tk.Toplevel(height = 400, width = 300,bg = spartangreen )
        
        self.leftclickwindowopen = True
        self.onleftclickwindow.title("Individual Editor")
        
        self.onleftclickwindow.protocol("WM_DELETE_WINDOW", self.leftclickWindowClose)
        
        self.wtitleframe = tk.Frame(self.onleftclickwindow,bg = spartangreen)
        
        self.wtitleframe.place(relwidth = .7, relheight = .05, relx = .15, rely = .01)
        
        self.buttonwindow = tk.Frame(self.onleftclickwindow, bg = "white")
        self.buttonwindow.place(relwidth = .7, relheight = .7, relx = .15, rely = .15)
        
    
        type_item = self.get_type(closestnode)
        print("is a ", type_item) 
        
        showtext = type_item  + " - " + closestnode
        
        self.parent = closestnode
        
        self.windowtitle = Label(self.wtitleframe, text =  showtext,fg= "white",bg = spartangreen,font = "Helvetica 12 bold italic")
        self.windowtitle.pack()
        
        
        self.indivNamePrompt = Label(self.buttonwindow, text = "Name of New Individual", font = fontStyle,fg= "#747780",bg = "white")
        self.indivNamePrompt.pack()

        self.indivNameEntry = Entry(self.buttonwindow, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.indivNameEntry.pack()
        self.indivNameEntry.insert(1,"NewIndividual")
        
        addConcern = tk.Button(self.buttonwindow, text = "Add SubConcern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_concern)
        addConcern.pack()
        
        
        addProperty = tk.Button(self.buttonwindow, text = "Add Property",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_property)
        addProperty.pack()
        
    def leftclickWindowClose(self):
        
        
        self.onleftclickwindow.destroy()
        self.leftclickwindowopen = False
        
   
        
        

    #adds a property to the ontology, uses gui for inputs, updates tree afterwards
    def add_property(self):
        
        #add in the property
        new_property_name = self.indivNameEntry.get()
        
        if(self.check_existence(new_property_name) == True):
           print("individual already exists")
           if(self.error_displayed == True):
               self.error_message.destroy()
           self.error_message = Label(self.buttonwindow, text = "Individual Already Exists", font = "Helvetica 8 bold italic",fg= "red",bg = "white")
           self.error_message.pack()
           self.error_displayed = True
           return
        
        new_ir_name = self.get_ir_name()
        new_cond_name = self.get_cond_name()
        
        new_property = self.ontology.Property(new_property_name, ontology = self.ontology)
        new_property.hasType.append(self.ontology.PropertyType_Assertion)
        
        new_property.atomicStatement.append("new_atomic_statement")
        new_property.comment.append("new_comment")
        
        #add teh condition
        new_condition = self.ontology.Condition(new_cond_name, ontology = self.ontology)
        
        new_condition.conditionPolarity.append(self.ontology.positive)
        new_condition.conditionProperty.append(new_property)
        
        addressed_concern = self.ontology.search(iri = "*" + self.parent)
        addressed_concern = addressed_concern[0]
        
        #add the impact rule
        new_impact_rule = self.ontology.ImpactRule(new_ir_name,ontology = self.ontology)
        new_impact_rule.addressesAtFunc.append(self.ontology.bc1)
        new_impact_rule.addressesConcern.append(addressed_concern)
        new_impact_rule.addressesPolarity.append(self.ontology.positive)
        new_impact_rule.hasCondition.append(new_condition)
        new_impact_rule.comment.append("new_comment")
        
        
        self.no_impact_rules += 1
        self.no_conditions += 1
        
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
        
        new_ir_num = self.no_impact_rules + 1
        
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
        
        new_cond_num = self.no_conditions + 1
        
        if(new_cond_num >= 1000):
            return "c" + str(new_cond_num) + "_01"
        if(new_cond_num >= 100):
            return "c0" + str(new_cond_num) + "_01"
        if(new_cond_num >= 10): 
            return "c00" + str(new_cond_num) + "_01"
        if(new_cond_num >= 1): 
            return "c000" + str(new_cond_num) + "_01"       
        
        
        
    #draws the tree and scales it according to zoom level, scroll bar positions
    def update_tree(self):
         
         self.ax.clear()
         

         self.xmin, self.xmax, self.ymin, self.ymax, self.sorted_concerns, self.positions = draw_ontology(self.ax,self.ontology,self.fontsize)
         
         self.totalx = self.xmax - self.xmin
         self.totaly = self.ymax - self.ymin
         
         self.xmin = self.xmin - self.totalx/10
         self.xmax = self.xmax + self.totalx/10
         
         self.ymin = self.ymin - self.totaly/10
         self.ymax = self.ymax + self.totaly/10
         
         self.newtotalx = self.xmax - self.xmin
         self.newtotaly = self.ymax - self.ymin
         
         
         self.ax.clear()
         
         self.scale_tree(3)
         
         self.xmin, self.xmax, self.ymin, self.ymax, self.sorted_concerns, self.positions= draw_ontology(self.ax,self.ontology,self.fontsize)
         
         self.totalx = self.xmax - self.xmin
         self.totaly = self.ymax - self.ymin
         
         self.xmin = self.xmin - self.totalx/10
         self.xmax = self.xmax + self.totalx/10
         
         self.ymin = self.ymin - self.totaly/10
         self.ymax = self.ymax + self.totaly/10
         
         self.newtotalx = self.xmax - self.xmin
         self.newtotaly = self.ymax - self.ymin
         
         print(self.ymin, " self.ymin")
         print(self.ymax, " self.ymax")

         
         #self.scale_tree(3)
       
         self.chart.draw()
         
         #updates the concern dropdowns with whatever was found in draw_ontology
         
        
    #loads the specified ontology file in
    def load_ontology(self):
        
        self.owlOntology = owlOntology(self.input_owl_entry.get())
        
        summary = "Loaded ontology " + "file://./" + self.input_owl_entry.get()
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle, fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        self.update_tree()
        
        self.no_conditions = len(self.ontology.search(type = self.ontology.Condition))
        self.no_impact_rules =  len(self.ontology.search(type = self.ontology.ImpactRule))
        
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
        
        
        print(self.zoom_index)
        print(self.zoom)
        
        if(original_zoom != self.zoom):
            self.update_tree()
    #saves the ontology in rdf format
    def save_ontology(self):
         
        output_file = self.output_owl_entry.get()
        self.ontology.save(file = output_file, format = "rdfxml")
        
        
        self.process_file(output_file)
        
        summary = "Outputted ontology to file: " + output_file
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        
        
    #changes the portion of axis we view according to zoom level, slider position
    def scale_tree(self,var):
        
         leftmostx = self.xmin + self.newtotalx*self.xslider.get()/100
         leftmosty = self.ymin + self.newtotaly*self.yslider.get()/100
         
         print(self.xslider.get()/100)
         print(self.yslider.get()/100)
    
        
         if(self.zoom == .5):
             
             leftmosty = self.ymin - .5*self.newtotaly
             rightmosty = self.ymax + .5 * self.newtotaly
             
             rightmostx = leftmostx + .50 * self.newtotalx
        
        
         if (self.zoom == 1):
             leftmosty = self.ymin
             rightmostx = leftmostx + .20*self.newtotalx
             rightmosty = self.ymax
         
         if (self.zoom == 2):
             #self.ax.set(xlim=(self.xmax*(self.xslider.get()/100 + .0001), self.xmax*(self.xslider.get()/100 + .10)), ylim=(self.ymax*(self.yslider.get()/100 + .001)  , self.ymax*(self.yslider.get()/100 + .5)))
             
             rightmostx = leftmostx + .10*self.newtotalx
             rightmosty = leftmosty + .50*self.newtotaly
            
         if (self.zoom == 3):
            
             print("in zoom 3")
             print(self.xmin)
             print(self.ymin)
             rightmostx = leftmostx + .05*self.newtotalx
             rightmosty = leftmosty + .25*self.newtotaly
            
             

         self.ax.set(xlim=(leftmostx, rightmostx), ylim=(leftmosty, rightmosty))
        # self.xmin, self.xmax, self.ymin, self.ymax, self.sorted_concerns= draw_ontology(self.ax,self.ontology,self.fontsize)
         print(self.ax.get_xlim(), " in scale")
         print(self.ax.get_ylim(), " in scale")
         #print(self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
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
        

        
        
        
         
        

    
root = Tk()




fontStyle = tkFont.Font(family="Lucida Grande", size=8, weight = "bold")
small = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
med = tkFont.Font(family="Lucida Grande", size=12, weight = "bold")
big = tkFont.Font(family="Lucida Grande", size=18, weight = "bold") 
selectFont = tkFont.Font(family="Lucida Grande", size=11, weight = "bold")
my_gui = OntologyGUI(root)
root.mainloop()
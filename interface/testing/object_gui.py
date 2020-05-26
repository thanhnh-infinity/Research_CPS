from script_networkx import draw_ontology
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from script_networkx import draw_ontology
import numpy as np

import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

from owlready2 import *


class OntologyGUI:
    
    def __init__(self,master):
        
        self.zoom = 1
        self.fontsize = 8
        
        self.master = master
        
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

        #set up prompt/Entry for new concern name
        self.concernNamePrompt = Label(self.input_frame, text = "Concern Name", font = fontStyle,fg= "#747780",bg = "white")
        self.concernNamePrompt.pack()

        self.concern_name_entry = Entry(self.input_frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.concern_name_entry.pack()
        self.concern_name_entry.insert(1,"testConcern")
        
        #set up prompt/option menu for which concern new concern will be a subconcern of
        self.subconcernOfNamePrompt = Label(self.input_frame, text = "Subconcern of", font = fontStyle,fg= "#747780",bg = "white")
        self.subconcernOfNamePrompt.pack()
       
        self.subconcernOf = StringVar()
        
        self.subconcern_of_name_drop = OptionMenu(self.input_frame,self.subconcernOf,None)
        self.subconcern_of_name_drop.config(width=30, font = selectFont,fg= "#18453b",bg = "white",borderwidth = 3,highlightbackground="white")
        self.subconcern_of_name_drop.pack()
        
        #button to add concern, calls function which handles it
        self.addConcern = tk.Button(self.input_frame, text = "Add Concern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_concern)
        self.addConcern.pack()
        
        self.add_space(self.input_frame,"white","medium")
        
        #set up prompt/entry for new property's name
        self.propertyNamePrompt = Label(self.input_frame, text = "Property Name", font = fontStyle,fg= "#747780",bg = "white")
        self.propertyNamePrompt.pack()

        self.property_name_entry = Entry(self.input_frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.property_name_entry.pack()
        self.property_name_entry.insert(1,"testProperty")
        
        
        #set up prompt/option menu for which concern the new property will address
        self.concernAddressedNamePrompt = Label(self.input_frame, text = "Addresses Concern", font = fontStyle,fg= "#747780",bg = "white")
        self.concernAddressedNamePrompt.pack()
    
        self.addressedConcern = StringVar()
        
        self.addressedConcern_drop = OptionMenu(self.input_frame,self.addressedConcern,None)
        self.addressedConcern_drop.config(width=30, font = selectFont,fg= "#18453b",bg = "white",borderwidth = 3,highlightbackground="white")
        self.addressedConcern_drop.pack()
        
        #set up button for adding proerty, calls function which handles it
        self.addProperty = tk.Button(self.input_frame, text = "Add Property",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_property)
        self.addProperty.pack()
        
        
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
        
        #sets up gray box to put text to show what is going on
        self.textBox = Frame(self.input_frame,bg = "#747780", bd = 5)
        self.textBox.place(relwidth = .8, relheight = .2, relx = .1, rely = .75)
        
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

        self.xslider = Scale(self.xslider_frame, from_ = 0, to = 80,orient = HORIZONTAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)     
        self.xslider.pack()    


        self.yslider_frame = tk.Frame(self.tree_frame,bg = "white")
        self.yslider_frame.place(relwidth = .03, relheight = .7, relx = .95, rely = .15)

        self.yslider = Scale(self.yslider_frame, from_ = 50, to = 0,orient = VERTICAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)     
        self.yslider.pack()
        
        
        self.zoom_frame = tk.Frame(self.tree_frame,bg = "white")
        self.zoom_frame.place(relwidth = .05, relheight = .05, relx = .94, rely = .01)
        
        self.zoom_button = tk.Button(self.zoom_frame, text = "Zoom",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.do_zoom)
        self.zoom_button.pack()
        
        
      
        
        
    #adds a concern to the ontology, uses gui entries for inputs, updates tree afterwards
    def add_concern(self):
    
        #adds concern in
        new_concern = self.concern_name_entry.get()
       
        test_concern = self.ontology.Concern(new_concern,ontology = self.ontology)
        
        subconcern_of = self.ontology.search(iri = "*" + self.subconcernOf.get())
        subconcern_of = subconcern_of[0]
        
        subconcern_of.includesConcern.append(test_concern)
            
        #prints text in textbox to tell what happend
        summary = "Added concern " + new_concern + " to ontology"
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
             
        self.update_tree()
        
    #adds a property to the ontology, uses gui for inputs, updates tree afterwards
    def add_property(self):
        
        #add in the property
        new_property_name = self.property_name_entry.get()
        
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
        
        addressed_concern = self.ontology.search(iri = "*" + self.addressedConcern.get())
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
         

         self.xmin, self.xmax, self.ymin, self.ymax, self.sorted_concerns= draw_ontology(self.ax,self.ontology,self.fontsize)
         
         self.totalx = self.xmax - self.xmin
         self.totaly = self.ymax - self.ymin
         
         self.xmin = self.xmin - self.totalx/10
         self.xmax = self.xmax + self.totalx/10
         
         self.ymin = self.ymin - self.totaly/10
         self.ymax = self.ymax + self.totaly/10
         
         print(self.ymin, " self.ymin")
         print(self.ymax, " self.ymax")

         
         self.scale_tree(3)
       
         self.chart.draw()
         
         #updates the concern dropdowns with whatever was found in draw_ontology
         self.update_concern_dropdown()
         
     
    #loads the specified ontology file in
    def load_ontology(self):
        
        self.ontology = get_ontology("file://./" + self.input_owl_entry.get()).load() 
        
        summary = "Loaded ontology " + "file://./" + self.input_owl_entry.get()
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle, fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        self.update_tree()
        
        self.no_conditions = len(self.ontology.search(type = self.ontology.Condition))
        self.no_impact_rules =  len(self.ontology.search(type = self.ontology.ImpactRule))
        
    
    
    
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
    def do_zoom(self):
        
        print("we be zooming")
        
        if(self.zoom == 1):
            self.zoom = 2
            self.fontsize = 16
            
        elif(self.zoom == 2):
            self.zoom = 1
            self.fontsize = 8
        
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
        
    
         if (self.zoom == 1):
             self.ax.set(xlim=(self.xmax*(self.xslider.get()/100), self.xmax*(self.xslider.get()/100 + .2)), ylim=(self.ymin, self.ymax))
         
         if (self.zoom == 2):
             self.ax.set(xlim=(self.xmax*(self.xslider.get()/100 + .05), self.xmax*(self.xslider.get()/100 + .15)), ylim=(self.ymax*(self.yslider.get()/100 + .001)  , self.ymax*(self.yslider.get()/100 + .5)))

         #print(self.ax.get_xlim(), " in scale")
         #print(self.ax.get_ylim(), " in scale")
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
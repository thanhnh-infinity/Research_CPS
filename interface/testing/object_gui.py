from script_networkx import draw_ontology
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from script_networkx import draw_ontology


import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

from owlready2 import *


class OntologyGUI:
    
    def __init__(self,master):
        self.master = master
        
    
        
        master.title("Ontology GUI")
          
        self.canvas = Canvas(master, height = 1200, width = 2000, bg = "#18453b")
        self.canvas.pack()
        
        
        self.header_frame = Frame(master,bg ="#18453b" )
        self.header_frame.place(relwidth = .8, relheight = .06, relx = .1, rely = 0.02)
        self.header_text = Label(self.header_frame, text="CPS Ontology Visualization",fg = "white",bg = "#18453b", font = "Helvetica 30 bold italic")
        self.header_text.pack()
        
        self.footer_frame = Frame(master,bg ="#18453b")
        self.footer_frame.place(relwidth = .4, relheight = .2, relx = .61, rely = 0.9)
        self.footer_text = Label(self.footer_frame, text="Matt Bundas, Prof. Son Tran, Thanh Ngyuen, Prof. Marcello Balduccini",fg = "white",bg = "#18453b", font = "Helvetica 8 bold italic", anchor = "e")
        self.footer_text.pack()

        self.frame = Frame(master, bg="white")
        self.frame.place(relwidth = .2, relheight = .8, relx = .01, rely = 0.1)



            
        self.inputPrompt = Label(self.frame, text = "Input ontology", font = fontStyle,fg= "#747780",bg = "white")
        self.inputPrompt.pack()
    
        self.input_owl_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.input_owl_entry.pack()
        self.input_owl_entry.insert(0,"cpsframework-v3-base.owl")

        self.loadOntology = tk.Button(self.frame, text = "Load Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.load_ontology)
        self.loadOntology.pack()
        
        self.add_space(self.frame,"white","medium")


        
        self.concernNamePrompt = Label(self.frame, text = "Concern Name", font = fontStyle,fg= "#747780",bg = "white")
        self.concernNamePrompt.pack()

        self.concern_name_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.concern_name_entry.pack()
        self.concern_name_entry.insert(1,"testConcern")
        
        self.subconcernOfNamePrompt = Label(self.frame, text = "Subconcern of", font = fontStyle,fg= "#747780",bg = "white")
        self.subconcernOfNamePrompt.pack()
        self.subconcern_of_name_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.subconcern_of_name_entry.pack()
        self.subconcern_of_name_entry.insert(1,"Trustworthiness")
        
        self.addConcern = tk.Button(self.frame, text = "Add Concern",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_concern)
        self.addConcern.pack()
        
        
        self.add_space(self.frame,"white","medium")
        
        self.propertyNamePrompt = Label(self.frame, text = "Property Name", font = fontStyle,fg= "#747780",bg = "white")
        self.propertyNamePrompt.pack()

        self.property_name_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.property_name_entry.pack()
        self.property_name_entry.insert(1,"testProperty")
        
        self.concernAddressedNamePrompt = Label(self.frame, text = "Addresses Concern", font = fontStyle,fg= "#747780",bg = "white")
        self.concernAddressedNamePrompt.pack()
        self.concern_addressed_name_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.concern_addressed_name_entry.pack()
        self.concern_addressed_name_entry.insert(1,"Trustworthiness")
        
        self.addProperty = tk.Button(self.frame, text = "Add Property",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.add_property)
        self.addProperty.pack()
        
        
        self.add_space(self.frame,"white","medium")




        self.outputPrompt = Label(self.frame, text =  "Output Name", font = fontStyle,fg= "#747780",bg = "white")
        self.outputPrompt.pack()
        
        self.output_owl_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.output_owl_entry.pack()
        self.output_owl_entry.insert(2, "newConcern.owl")
        
        self.saveOntology = tk.Button(self.frame, text = "Output Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.save_ontology)
        self.saveOntology.pack()
        
        self.textBox = Frame(self.frame,bg = "#747780", bd = 5)
        self.textBox.place(relwidth = .8, relheight = .2, relx = .1, rely = .75)
        

        self.tree_frame = tk.Frame(self.master, bg="white")
        self.tree_frame.place(relwidth = .70, relheight = .8, relx = .25, rely = 0.1)

        self.fig, self.ax = plt.subplots(figsize = (15,15))
        self.chart = FigureCanvasTkAgg(self.fig,self.tree_frame)
        
        self.ax.clear()
        self.ax.axis('off')
        self.chart.get_tk_widget().pack()

        self.slider_frame = tk.Frame(self.tree_frame,bg = "white")
        self.slider_frame.place(relwidth = .7, relheight = .05, relx = .15, rely = .95)

        self.xslider = Scale(self.slider_frame, from_ = 0, to = 80,orient = HORIZONTAL,bg = "gray", fg = "white",length = 900,command = self.scale_tree)     
        self.xslider.pack()
      
        
        

    def add_concern(self):
    
        new_concern = self.concern_name_entry.get()
       
        test_concern = self.ontology.Concern(new_concern,ontology = self.ontology)
        
        subconcern_of = self.ontology.search(iri = "*" + self.subconcern_of_name_entry.get())
        subconcern_of = subconcern_of[0]
        
        subconcern_of.includesConcern.append(test_concern)
            
        summary = "Added concern " + new_concern + " to ontology"
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
            
        self.update_tree()
        
    def add_property(self):
        
        new_property_name = self.property_name_entry.get()
        
        new_ir_name = self.get_ir_name()
        new_cond_name = self.get_cond_name()
        
        new_property = self.ontology.Property(new_property_name, ontology = self.ontology)
        new_property.hasType.append(self.ontology.PropertyType_Assertion)
        
        new_property.atomicStatement.append("new_atomic_statement")
        new_property.comment.append("new_comment")
        
        new_condition = self.ontology.Condition(new_cond_name, ontology = self.ontology)
        
        new_condition.conditionPolarity.append(self.ontology.positive)
        new_condition.conditionProperty.append(new_property)
        
        addressed_concern = self.ontology.search(iri = "*" + self.concern_addressed_name_entry.get())
        addressed_concern = addressed_concern[0]
        
        new_impact_rule = self.ontology.ImpactRule(new_ir_name,ontology = self.ontology)
        new_impact_rule.addressesAtFunc.append(self.ontology.bc1)
        new_impact_rule.addressesConcern.append(addressed_concern)
        new_impact_rule.addressesPolarity.append(self.ontology.positive)
        new_impact_rule.hasCondition.append(new_condition)
        new_impact_rule.comment.append("new_comment")
        
        
        self.no_impact_rules += 1
        self.no_conditions += 1
        
        summary = "Added property " + new_property_name + " to ontology"
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
            
        self.update_tree()
        
    
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
        
        
        
        
        
    def update_tree(self):
         
         self.ax.clear()
         

         self.xmin, self.xmax, self.ymin, self.ymax = draw_ontology(self.ax,self.ontology)
         
         self.totalx = self.xmax - self.xmin
         self.totaly = self.ymax - self.ymin
         
         self.xmin = self.xmin - self.totalx/10
         self.xmax = self.xmax + self.totalx/10
         
         self.ymin = self.ymin - self.totaly/10
         self.ymax = self.ymax + self.totaly/10
         
         
         
         self.ax.set(xlim=(self.xmax*(self.xslider.get()/100), self.xmax*(self.xslider.get()/100 + .2)), ylim=(self.ymin, self.ymax))

         
         print(self.ax.get_xlim())
         print(self.ax.get_ylim())
         self.chart.draw()
         
         
    def load_ontology(self):
        
        self.ontology = get_ontology("file://./" + self.input_owl_entry.get()).load() 
        
        summary = "Loaded ontology " + "file://./" + self.input_owl_entry.get()
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle, fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        self.update_tree()
        
        self.no_conditions = len(self.ontology.search(type = self.ontology.Condition))
        self.no_impact_rules =  len(self.ontology.search(type = self.ontology.ImpactRule))
    
     
    def save_ontology(self):
         
        output_file = self.output_owl_entry.get()
        self.ontology.save(file = output_file, format = "rdfxml")
        
        
        self.process_file(output_file)
        
        summary = "Outputted ontology to file: " + output_file
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        
        
    def scale_tree(self,var):
        
         self.ax.set(xlim=(self.xmax*(self.xslider.get()/100), self.xmax*(self.xslider.get()/100 + .2)), ylim=(self.ymin, self.ymax))
         
         print(self.ax.get_xlim())
         print(self.ax.get_ylim())
         print(self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
         self.chart.draw()
        
        


    def add_space(self,on,color,size):
        
        if(size == "small"):
            self.emptySpace = Label(on, text = "", font = small,bg = color)
            
        if(size == "medium"):
            self.emptySpace = Label(on, text = "", font = med,bg = color) 
        
        if(size == "large"):
            self.emptySpace = Label(on, text = "", font = large,bg = color)
        
        self.emptySpace.pack()
        
        
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
fontStyle = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
small = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
med = tkFont.Font(family="Lucida Grande", size=12, weight = "bold")
big = tkFont.Font(family="Lucida Grande", size=18, weight = "bold") 
my_gui = OntologyGUI(root)
root.mainloop()
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
          
        self.canvas = Canvas(master, height = 900, width = 1500, bg = "#18453b")
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




        self.outputPrompt = Label(self.frame, text =  "Output Name", font = fontStyle,fg= "#747780",bg = "white")
        self.outputPrompt.pack()
        
        self.output_owl_entry = Entry(self.frame, width = 30,borderwidth = 5,highlightbackground="white", fg = "#18453b",font = "Verdana 10 bold")
        self.output_owl_entry.pack()
        self.output_owl_entry.insert(2, "newConcern.owl")
        
        self.saveOntology = tk.Button(self.frame, text = "Output Ontology",padx = 10, pady = 5, bg = "#18453b", fg = "white",borderwidth = 5,command = self.save_ontology)
        self.saveOntology.pack()
        
        self.textBox = Frame(self.frame,bg = "#747780", bd = 5)
        self.textBox.place(relwidth = .8, relheight = .4, relx = .1, rely = .55)
        

        self.tree_frame = tk.Frame(self.master, bg="white")
        self.tree_frame.place(relwidth = .70, relheight = .8, relx = .25, rely = 0.1)

        self.fig, self.ax = plt.subplots(figsize = (25,15))
        self.chart = FigureCanvasTkAgg(self.fig,self.tree_frame)
        
        self.ax.clear()
        self.ax.axis('off')
        self.chart.get_tk_widget().pack()
        
        
      
        
        

    def add_concern(self):
    
        new_concern = self.concern_name_entry.get()
        owlfile_in = self.input_owl_entry.get()
        owlfile_out = self.output_owl_entry.get()
            
      
        test_concern = self.ontology.Concern(new_concern,ontology = self.ontology)
        
        subconcern_of = self.ontology.search(iri = "*" + self.subconcern_of_name_entry.get())
        subconcern_of = subconcern_of[0]
        
        subconcern_of.includesConcern.append(test_concern)
            
        summary = "Added concern " + new_concern + " to ontology"
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
            
        self.update_tree()
        
    def update_tree(self):
         
         self.ax.clear()
         
         draw_ontology(self.ax,self.ontology)
         
         self.chart.draw()
         
         
    def load_ontology(self):
        
        self.ontology = get_ontology("file://./" + self.input_owl_entry.get()).load() 
        
        summary = "Loaded ontology " + "file://./" + self.input_owl_entry.get()
            
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle, fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        self.update_tree()
        
    
    def save_ontology(self):
         
        output_file = self.output_owl_entry.get()
        self.ontology.save(file = output_file, format = "rdfxml")
        
        summary = "Outputted ontology to file: " + output_file
        self.summaryLabel = Label(self.textBox, text = summary, font = fontStyle,fg= "white",bg = "#747780")
        self.summaryLabel.pack()
        
    def add_space(self,on,color,size):
        
        if(size == "small"):
            self.emptySpace = Label(on, text = "", font = small,bg = color)
            
        if(size == "medium"):
            self.emptySpace = Label(on, text = "", font = med,bg = color) 
        
        if(size == "large"):
            self.emptySpace = Label(on, text = "", font = large,bg = color)
        
        self.emptySpace.pack()
        
        
         
        

    
root = Tk()
fontStyle = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
small = tkFont.Font(family="Lucida Grande", size=6, weight = "bold")
med = tkFont.Font(family="Lucida Grande", size=12, weight = "bold")
big = tkFont.Font(family="Lucida Grande", size=18, weight = "bold") 
my_gui = OntologyGUI(root)
root.mainloop()
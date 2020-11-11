from owlBase import owlBase


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from owlNode import owlNode
from script_networkx import remove_namespace
from owlready2 import *
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

from owlFunctions import graphviz_layout_with_rank
class owlGraph:

    def __init__(self,baseOWL,appOWL = None):

        self.graphProperties = True
        self.graphComponents = True
       
        
        
        self.owlBase = baseOWL
        self.owlApplication = appOWL

        self.graphPositions = None

        self.aspectConcernArray = None
        self.aspectNameList = None
        self.formulaArray = None
        self.decompFuncArray = None
        self.componentArray = None
        
        
        self.subconcernEdges = None
        self.concernFormulaEdges = None
        self.formulaDecompFuncEdges = None
        self.formulaPropertyEdges = None
        self.componentEdges = None

        self.concernEdgeLabels = None
        self.concernFormulaEdgeLabels = None
        self.formulaDecompFuncEdgeLabels = None
        self.formulaPropertyEdgeLabels = None
        self.componentEdgeLabels = None

        self.aspectNodeLabels = None
        self.concernNodeLabels = None
        self.propertyNodeLabels = None
        self.formulaNodeLabels = None
        self.decompFuncNodeLabels = None
        self.componentNodeLabels = None

        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None
        self.totalX = None
        self.totalY = None
        self.XYRatio = None

        self.makeGraph()

    def makeGraph(self):

        self.netXGraph = nx.DiGraph()

        self.addGraphNodes()

        self.addGraphEdgesAndLabels()

        self.addNodeLabels()

        self.setPositions()


    def addGraphNodes(self):

        self.aspectConcernArray = np.array(())
        self.aspectNameList = [[]]
        self.propertyArray = np.array(())
        self.formulaArray = np.array(())
        self.decompFuncArray = np.array(())
        self.componentArray = np.array(())

        for node in self.owlBase.allConcerns_owlNode:

            self.netXGraph.add_node(node.name)

            if(str(node.type) == "Concern" or str(node.type) == "Aspect"):
                #print("found concern or aspect")
                #print(node.type)
                self.aspectConcernArray = np.append(self.aspectConcernArray,node)

                if(str(node.type) == "Aspect"):

                    self.aspectNameList[0].append(node.name)

            else:
                print("couldnt find type")
                print(node.type)

        if(self.owlApplication != None):

            for node in self.owlApplication.nodeArray:

               

                if(str(node.type) == "Property" and self.graphProperties == True):
                    #print("found property")
                    #print("found property " + node.name)
                    self.netXGraph.add_node(node.name)
                    self.propertyArray = np.append(self.propertyArray,node)
                
                elif(str(node.type) == "Formula" and self.graphProperties == True):
                    self.netXGraph.add_node(node.name)
                    self.formulaArray = np.append(self.formulaArray,node)
                    continue
                    
                elif(str(node.type) == "DecompositionFunction" and self.graphProperties == True):
                    self.netXGraph.add_node(node.name)
                    self.decompFuncArray = np.append(self.decompFuncArray,node)
                
                elif(str(node.type) == "Component" and self.graphComponents == True):
                    self.netXGraph.add_node(node.name)
                    self.componentArray = np.append(self.componentArray,node)

                else:
                    
                    print("not graphing ", node.name," - ", node.type)
                    continue
                 


    def addGraphEdgesAndLabels(self):

     
        
        self.subconcernEdges = []
        self.concernFormulaEdges = []
        
        
        self.formulaDecompFuncDisEdges = []
        self.formulaDecompFuncConjEdges = []
        
        self.formulaPropertyDisEdges = []
        self.formulaPropertyConjEdges = []
        
        self.negFormulaPropertyDisEdges = []
        self.negFormulaPropertyConjEdges = []
        
        
        self.concernPropertyEdges = []
        
        self.componentEdges = []
        
        
        
        self.concernEdgeLabels = {}
        self.concernFormulaEdgeLabels = {}
        
        self.formulaDecompFuncDisEdgeLabels = {}
        self.formulaDecompFuncConjEdgeLabels = {}
        
        self.formulaPropertyDisEdgeLabels = {}
        self.formulaPropertyConjEdgeLabels = {}
        
        self.negFormulaPropertyDisEdgeLabels = {}
        self.negFormulaPropertyConjEdgeLabels = {}
        
        
        
        
        self.concernPropertyEdgeLabels = {}
        
        self.componentEdgeLabels = {}


        for node in self.owlBase.allConcerns_owlNode:

            if len(node.children) == 0:
                continue


            for child in node.children:

                #print(str(child) + " in edges")

                if(child.type == "Concern"):
                    self.netXGraph.add_edge(node.name,child.name,length = 1)
                    self.subconcernEdges.append((node.name,child.name))
                    
                    self.concernEdgeLabels[(node.name,child.name)] = 'subconcern'
                    
                elif(child.type == "Formula" or child.type == "DecompositionFunction"):
                    self.netXGraph.add_edge(node.name,child.name,length = 1)
                    self.concernFormulaEdges.append((node.name,child.name))
                    
                   
                    
                    self.concernFormulaEdgeLabels[(node.name,child.name)] = "addressesConcern" 
                    
                elif(child.type == "Property" and len(child.parents) == 1):
                    
                    self.netXGraph.add_edge(node.name,child.name, length = 1)
                    
                    self.concernPropertyEdges.append((node.name,child.name))
                    self.concernPropertyEdgeLabels[(node.name,child.name)] = "addressesConcern"


        if(self.owlApplication == None):
             return

        for node in self.owlApplication.nodeArray:

            if (len(node.children) + len(node.negChildren)) == 0:
                continue

          
            for negChild in node.negChildren:
                
                
                #print("in neg child loop in graph", negChild.name)
                
                #WILL NEED TO ADAPT THIS FOR NEGATION
                if( (negChild.type == "DecompositionFunction" or negChild.type == "Formula") and self.graphProperties == True):
                    
                     self.netXGraph.add_edge(node.name,negChild.name,length = 1)
                    
                     if(node.subtype == "Disjunction"):
                        
                        
                      
                            
                        self.negFormulaPropertyDisEdges.append((node.name,negChild.name))
                        self.negFormulaPropertyDisEdgeLabels[(node.name,negChild.name)] = "negMemberOf" 
                            
                    
    
                     else:
            
                            
                        self.negFormulaPropertyConjEdges.append((node.name,negChild.name))
                        self.negFormulaPropertyConjEdgeLabels[(node.name,negChild.name)] = "negMemberOf"
                    
                    
                    
                    

                if(negChild.type == "Property" and self.graphProperties == True):
                    
                    
                    #print("got to property if statement")
                    
                    self.netXGraph.add_edge(node.name,negChild.name,length = 1)
                    
                    
                    if(node.subtype == "Disjunction"):
                        
                        
                      
                            
                        self.negFormulaPropertyDisEdges.append((node.name,negChild.name))
                        self.negFormulaPropertyDisEdgeLabels[(node.name,negChild.name)] = "negMemberOf" 
                            
                    
    
                    else:
            
                            
                        self.negFormulaPropertyConjEdges.append((node.name,negChild.name))
                        self.negFormulaPropertyConjEdgeLabels[(node.name,negChild.name)] = "negMemberOf"
                            
                        
                    
                    



            for child in node.children:

                #print(str(child) + " in edges")

                
                #WILL NEED TO ADAPT THIS FOR NEGATION
                if( (child.type == "DecompositionFunction" or child.type == "Formula") and self.graphProperties == True):
                    self.netXGraph.add_edge(node.name,child.name,length = 1)
                   
                    if(node.subtype == "Disjunction"):
                    
                        self.formulaDecompFuncDisEdges.append((node.name,child.name))
                        self.formulaDecompFuncDisEdgeLabels[(node.name,child.name)] = "memberOf"
                        
                    else:
                        
                        self.formulaDecompFuncConjEdges.append((node.name,child.name))
                        self.formulaDecompFuncConjEdgeLabels[(node.name,child.name)] = "memberOf"
                        
                        
                        
                        
                        
                    
                elif(child.type == "Property" and self.graphProperties == True):
                    
                
                    self.netXGraph.add_edge(node.name,child.name,length = 1)
                    
                    
                    if(node.subtype == "Disjunction"):
                        

                       
                        self.formulaPropertyDisEdges.append((node.name,child.name))
                        self.formulaPropertyDisEdgeLabels[(node.name,child.name)] = "memberOf" 
                    
                    else:
                        
                      
                        self.formulaPropertyConjEdges.append((node.name,child.name))
                        self.formulaPropertyConjEdgeLabels[(node.name,child.name)] = "memberOf" 
                 
                elif(child.type == "Component" and self.graphComponents == True):
                    
                        self.netXGraph.add_edge(node.name,child.name,length = 1)
                        
                        self.componentEdges.append((node.name,child.name))
                        self.componentEdgeLabels[(node.name,child.name)] = "relatedTo" 
                        
                        
                    
                #elif(child.type == "Formula" and self.graphProperties == True):
                    
                    
                    #self.netXGraph.add_edge(node.name,child.name,length = 1)
                    
                  #  if(node.subtype == "Disjunction"):
                        
                   #     x  = 2
                        
                    
                    
                    
                    
    def addNodeLabels(self):

        self.aspectNodeLabels = {}
        self.concernNodeLabels = {}
        self.propertyNodeLabels = {}
        self.formulaNodeLabels = {}
        self.decompFuncNodeLabels = {}
        self.componentNodeLabels = {}


        for node in self.aspectConcernArray:



            if(node.type == "Aspect"):
                self.aspectNodeLabels[node.name] = node.name
            if(node.type == "Concern"):
                self.concernNodeLabels[node.name] = node.name

        if(self.owlApplication == None):
             return

        for node in self.owlApplication.nodeArray:

                if(node.type == "Component" and self.graphComponents == True):

                    
                    #print("Component adding, ", node.name)
                    self.componentNodeLabels[node.name] = node.name


                elif(node.type == "Property" and self.graphProperties == True):

                    #print("Property adding, ", node.name)
                    self.propertyNodeLabels[node.name] = node.name
                    
                elif(node.type == "Formula" and self.graphProperties == True):

                   # print("Formula adding, ", node.name)
                    self.formulaNodeLabels[node.name] = node.name
                    
                elif(node.type == "DecompositionFunction" and self.graphProperties == True):

                   # print("DecompFunc adding, ", node.name)
                    self.decompFuncNodeLabels[node.name] = node.name
                
                
             




    def setPositions(self):


        #print(list(self.netXGraph.nodes))
        #self.graphPositions = graphviz_layout(self.netXGraph, prog='dot')

        self.graphPositions = graphviz_layout_with_rank(self.netXGraph, prog='dot',sameRank=self.aspectNameList)
        #don't want negative position values, so add 500 to all x's, 100 to all y's
        for x in self.graphPositions:

            #print(x)
            lst = list(self.graphPositions[x])
            lst[0] = lst[0] + 500
            lst[1] = lst[1] + 100

            self.graphPositions[x] = tuple(lst)

        #find x,y mins and maxes for gui graphing purposes
        x_pos = np.array(())
        y_pos = np.array(())

        for x in self.graphPositions:

            position = self.graphPositions[x]
            x_pos = np.append(x_pos,position[0])
            y_pos = np.append(y_pos,position[1])


           # print(x)

            mynode = self.findNode(x)

            mynode.xpos = position[0]
            mynode.ypos = position[1]



        xmax = np.max(x_pos)
        ymax = np.max(y_pos)

        xmin = np.min(x_pos)
        ymin = np.min(y_pos)

        totalx_o = xmax - xmin
        totaly_o = ymax - ymin

        self.minX = xmin - totalx_o/10
        self.maxX = xmax + totalx_o/10

        self.minY = ymin - totaly_o/10
        self.maxY = ymax + totaly_o/10

        self.totalX = self.maxX - self.minX
        self.totalY = self.maxY - self.minY


        self.XYRatio = self.totalX/self.totalY
      



    def draw_graph(self, ax,fs):

        #ax.axis('off')
        aspect_color = "#000a7d"
        concern_color = "#800000"
        
       
        property_color = "#595858"
        formula_color = "#3000ab"
        decompfunc_color ="#3000ab"
        #decompfunc_color = "#0eb0a8"
        component_color = "pink"
        edge_color = "black"
        edge_width = 2
        edge_alpha = .8


        fs = fs*.69

        plt.tight_layout()

        nx.draw_networkx_nodes(self.netXGraph, pos = self.graphPositions, with_labels=False, arrows=False, ax = ax, node_size = .1,scale = 1)

        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.subconcernEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color,alpha = edge_alpha)
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.concernFormulaEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color, alpha = edge_alpha)
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.concernPropertyEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color,alpha = edge_alpha)

        
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.formulaDecompFuncDisEdges, arrows=False,style = "dotted",width = edge_width,edge_color = edge_color, alpha = edge_alpha)   
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.formulaDecompFuncConjEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color, alpha = edge_alpha)  
        
        
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.formulaPropertyDisEdges, arrows=False,style = "dotted",width = edge_width,edge_color = edge_color, alpha = edge_alpha)
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.formulaPropertyConjEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color, alpha = edge_alpha)
        
        
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.negFormulaPropertyDisEdges, arrows=False,style = "dotted",width = edge_width,edge_color = "red", alpha = edge_alpha)
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.negFormulaPropertyConjEdges, arrows=False,style = "solid",width = edge_width,edge_color = "red", alpha = edge_alpha)
        
        
        
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.componentEdges, arrows=False,style = "dotted",width = edge_width,edge_color = edge_color, alpha = edge_alpha)


        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.concernEdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.concernFormulaEdgeLabels,font_size = fs)
        
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.concernPropertyEdgeLabels,font_size = fs)

        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.formulaDecompFuncDisEdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.formulaDecompFuncConjEdgeLabels,font_size = fs)
        
        
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.formulaPropertyDisEdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.formulaPropertyConjEdgeLabels,font_size = fs)
        
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.negFormulaPropertyDisEdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.negFormulaPropertyConjEdgeLabels,font_size = fs)
        
        
        
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.componentEdgeLabels,font_size = fs)


        nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.aspectNodeLabels,font_size=fs,bbox=dict(facecolor=aspect_color, boxstyle='square,pad=.3'),font_color = "white")
        nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.concernNodeLabels,font_size= fs,bbox=dict(facecolor=concern_color, boxstyle='square,pad=.3'),font_color = "white")

        if(self.owlApplication != None):
            nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.propertyNodeLabels,font_size=fs*.85,bbox=dict(facecolor=property_color, boxstyle='round4,pad=.3'),font_color = "white")
            nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.formulaNodeLabels,font_size=fs,bbox=dict(facecolor=formula_color, boxstyle='round4,pad=.3'),font_color = "white")
            nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.decompFuncNodeLabels,font_size=fs,bbox=dict(facecolor=decompfunc_color, boxstyle='round4,pad=.3'),font_color = "white")
            nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.componentNodeLabels,font_size=fs,bbox=dict(facecolor=component_color, boxstyle='round,pad=.3'),font_color = "white")


    def findNode(self,name):

        for node in self.owlBase.allConcerns_owlNode:

            if(node.name == name):

                return node

        for node in self.owlApplication.nodeArray:

            if(node.name == name):

                return node


        print("couldn't find " + str(name))
        return 0



#testOwlOntology = owlBase("cpsframework-v3-base.owl")

#testOwlOntology.initializeOwlNodes()

#testOwlGraph = owlGraph(testOwlOntology)

#fig, ax = plt.subplots(figsize = (15,15))

#testOwlGraph.draw_graph(ax,10)

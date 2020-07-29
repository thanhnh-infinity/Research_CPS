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
        self.graphComponents = False
       
        
        
        self.owlBase = baseOWL
        self.owlApplication = appOWL

        self.graphPositions = None

        self.aspectConcernArray = None
        self.aspectNameList = None
        self.propertyArray = None
        self.conditionArray = None
        self.IRArray = None
        self.componentArray = None
        
        
        self.subconcernEdges = None
        self.IRPropertyEdges = None
        self.ConcernIREdges = None
        self.componentEdges = None

        self.concernEdgeLabels = None
        self.IRPropertyEdgeLabels = None
        self.ConcernIREdgeLabels = None
        self.componentEdgeLabels = None

        self.aspectNodeLabels = None
        self.concernNodeLabels = None
        self.propertyNodeLabels = None
        self.conditionNodeLabels = None
        self.IRNodeLabels = None
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
        self.conditionArray = np.array(())
        self.IRArray = np.array(())
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
                
                elif(str(node.type) == "Condition" and self.graphProperties == True):
                    #self.netXGraph.add_node(node.name)
                    #self.componentArray = np.append(self.conditionArray,node)
                    continue
                    
                elif(str(node.type) == "ImpactRule" and self.graphComponents == True):
                    self.netXGraph.add_node(node.name)
                    self.componentArray = np.append(self.IRArray,node)
                
                elif(str(node.type) == "Component" and self.graphComponents == True):
                    self.netXGraph.add_node(node.name)
                    self.componentArray = np.append(self.componentArray,node)

                else:
                    
                    #print("not graphing ", node.name," - ", node.type)
                    continue
                 


    def addGraphEdgesAndLabels(self):


        self.subconcernEdges = []
        self.propertyIREdges = []
        self.concernIREdges = []
        self.IRPropertyEdges = []
        self.componentEdges = []
        
        self.concernEdgeLabels = {}
        self.concernIREdgeLabels = {}
        self.IRPropertyEdgeLabels = {}
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
                    
                elif(child.type == "ImpactRule"):
                    self.netXGraph.add_edge(node.name,child.name,length = 1)
                    self.concernIREdges.append((node.name,child.name))
                    
                    if(child.polarity ) == "positive":
                        
                        pol = "+"
                        
                    elif(child.polarity) == "negative":
                        
                        pol = "-"
                        
                    else:
                        
                        pol = ""
                    
                    self.concernEdgeLabels[(node.name,child.name)] = "addressesConcern " + pol


        if(self.owlApplication == None):
             return

        for node in self.owlApplication.nodeArray:

            if len(node.children) == 0:
                continue


            for child in node.children:

                #print(str(child) + " in edges")

                if(child.type == "Component" and self.graphComponents == True):
                    self.netXGraph.add_edge(node.name,child.name,length = 1)
                    self.componentEdges.append((node.name,child.name))
                    
                    elf.propertyEdgeLabels[(node.name,child.name)] = "related to"
                    
                elif(child.type == "Condition" and self.graphProperties == True):
                    
                    
                    condition_prop = child.children[0]
                    
                    
                    self.netXGraph.add_edge(node.name,condition_prop.name,length = 1)
                    self.IRPropertyEdges.append((node.name,condition_prop.name))
                    
                    if(child.polarity ) == "positive":
                        
                        pol = "+"
                        
                    elif(child.polarity) == "negative":
                        
                        pol = "-"
                        
                    else:
                        
                        pol = ""
                    
                    self.IRPropertyEdgeLabels[(node.name,condition_prop.name)] = "conditionProperty" + pol




    def addEdgeLabels(self):

        self.concernEdgeLabels = {}
        self.concernIREdgeLabels = {}
        self.IRPropertyEdgeLabels = {}
        self.componentEdgeLabels = {}

        for edge in self.subconcernEdges:
            self.concernEdgeLabels[edge] = 'subconcern'

        for edge in self.concernIREdges:
            
            IR = self.findNode(edge[0])
            
            polarity = IR.polarity
            
            if (polarity == "positive"):
                self.concernIREdgeLabels[edge] = 'addressesConcern ' + "+"
           
            elif (polarity == "negative"):
                
                self.concernIREdgeLabels[edge] = 'addressesConcern ' + "-"
                
            else:
                
                self.concernIREdgeLabels[edge] = 'addressesConcern '
            
        for edge in self.IRPropertyEdges:
            
            x = 2
            

        for edge in self.componentEdges:
            
            self.propertyEdgeLabels[edge] = "related to"

    def addNodeLabels(self):

        self.aspectNodeLabels = {}
        self.concernNodeLabels = {}
        self.propertyNodeLabels = {}
        self.IRNodeLabels = {}
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

                    self.componentNodeLabels[node.name] = node.name


                if(node.type == "Property" and self.graphProperties == True):

                    self.propertyNodeLabels[node.name] = node.name
                    
                if(node.type == "ImpactRule" and self.graphProperties == True):

                    self.IRNodeLabels[node.name] = node.name
                    
             

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
        print(self.totalX)
        print(self.totalY)



    def draw_graph(self, ax,fs):

        #ax.axis('off')
        aspect_color = "#000a7d"
        concern_color = "#800000"
        
       
        property_color = "#595858"
        IR_color = "#3000ab"
        component_color = "pink"
        edge_color = "black"
        edge_width = 2
        edge_alpha = .8


        fs = fs*.69

        plt.tight_layout()

        nx.draw_networkx_nodes(self.netXGraph, pos = self.graphPositions, with_labels=False, arrows=False, ax = ax, node_size = .1,scale = 1)

        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.subconcernEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color,alpha = edge_alpha)
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.concernIREdges, arrows=False,style = "dashed",width = edge_width,edge_color = edge_color, alpha = edge_alpha)
        nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.IRPropertyEdges, arrows=False,style = "dotted",width = edge_width,edge_color = edge_color, alpha = edge_alpha)        
        #nx.draw_networkx_edges(self.netXGraph, pos = self.graphPositions, edgelist = self.componentEdges, arrows=False,style = "dotted",width = edge_width,edge_color = edge_color, alpha = edge_alpha)


        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.concernEdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.concernIREdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.IRPropertyEdgeLabels,font_size = fs)
        #nx.draw_networkx_edge_labels(self.netXGraph, pos = self.graphPositions, edge_labels=self.componentEdgeLabels,font_size = fs)


        nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.aspectNodeLabels,font_size=fs,bbox=dict(facecolor=aspect_color, boxstyle='square,pad=.3'),font_color = "white")
        nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.concernNodeLabels,font_size=fs,bbox=dict(facecolor=concern_color, boxstyle='square,pad=.3'),font_color = "white")
        
        if(self.owlApplication != None):
            nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.propertyNodeLabels,font_size=fs*.85,bbox=dict(facecolor=property_color, boxstyle='round4,pad=.3'),font_color = "white")
            nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.IRNodeLabels,font_size=fs,bbox=dict(facecolor=IR_color, boxstyle='round4,pad=.3'),font_color = "white")
        #nx.draw_networkx_labels(self.netXGraph,self.graphPositions,self.componentNodeLabels,font_size=fs,bbox=dict(facecolor=component_color, boxstyle='round,pad=.3'),font_color = "white")


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

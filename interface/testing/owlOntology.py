
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from owlNode import owlNode
from script_networkx import remove_namespace
from owlready2 import *
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


class owlOntology:

    def __init__(self,filename):

        self.owlReadyOntology = None
        self.owlName = None
        self.nodeArray = None
        self.concernArray = None
        self.propertyArray = None
        self.numNodes = None
        self.numAspects = None
        self.numConcerns = None
        self.numProperties = None
        self.numComponents = None
        self.numConditions = None
        self.numImpactRules = None



        self.owlGraph = None
        self.graphPositions = None

        self.aspectConcernArray = None
        self.propertyArray = None
        self.subconcernEdges = None
        self.propertyEdges = None

        self.concernEdgeLabels = None
        self.propertyEdgeLabels = None

        self.aspectNodeLabels = None
        self.concernNodeLabels = None
        self.propertyNodeLabels = None


        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None
        self.totalX = None
        self.totalY = None

        self.initializeOwlOntology(filename)



    def initializeOwlOntology(self,filename):

        self.loadOwlFile(filename)

        self.constructIndividualArray()

        self.setNumbers()


    def makeGraph(self):

        self.owlGraph = nx.DiGraph()

        self.addGraphNodes()

        self.addGraphEdges()

        self.addEdgeLabels()

        self.addNodeLabels()

        self.setPositions()
    
    def checkAddedToArray(self,name):
        
        
        for node in self.nodeArray:
            
            if(node.name == name):
                return True
            
        return False





    def addGraphNodes(self):

        self.aspectConcernArray = np.array(())
        self.propertyArray = np.array(())

        for node in self.nodeArray:
            #print(str(node.name) + " in add_nodes")
            self.owlGraph.add_node(node.name)

            if(str(node.type) == "Concern" or str(node.type) == "Aspect"):
                #print("found concern or aspect")
                #print(node.type)
                self.aspectConcernArray = np.append(self.aspectConcernArray,node.name)
            elif(str(node.type) == "Property"):
                #print("found property")
                self.propertyArray = np.append(self.propertyArray,node.name)
            else:
                print("couldnt find type")
                print(node.type)




    def addGraphEdges(self):


        self.subconcernEdges = []
        self.propertyEdges = []


        for node in self.nodeArray:

            if len(node.children) == 0:
                continue


            for child in node.children:

                #print(str(child) + " in edges")
                child = self.findNode(child)
                if(child.type == "Concern"):
                    self.owlGraph.add_edge(node.name,child.name,length = 1)
                    self.subconcernEdges.append((node.name,child.name))


                if(child.type == "Property"):

                    self.owlGraph.add_edge(node.name,child.name,length = 1)
                    self.propertyEdges.append((node.name,child.name))


    def addEdgeLabels(self):

        self.concernEdgeLabels = {}
        self.propertyEdgeLabels = {}

        for edge in self.subconcernEdges:
            self.concernEdgeLabels[edge] = 'subconcern'

        for edge in self.propertyEdges:
            self.propertyEdgeLabels[edge] = 'addresses concern'

    def addNodeLabels(self):

        self.aspectNodeLabels = {}
        self.concernNodeLabels = {}
        self.propertyNodeLabels = {}


        for aspect_concern in self.aspectConcernArray:
            
            node = self.findNode(aspect_concern)
            
            if(node.type == "Aspect"):
                self.aspectNodeLabels[aspect_concern] = aspect_concern
            else:
                self.concernNodeLabels[aspect_concern] = aspect_concern

        for myproperty in self.propertyArray:
            self.propertyNodeLabels[myproperty] = myproperty

    def setPositions(self):


        #print(list(self.owlGraph.nodes))
        self.graphPositions = graphviz_layout(self.owlGraph, prog='dot')

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





    def draw_graph(self, ax,fs):

        ax.axis('off')
        aspect_color = "#000a7d"
        concern_color = "#800000"
        property_color = "#595858"
        edge_color = "black"
        edge_width = 2
        edge_alpha = .8

        plt.tight_layout()

        nx.draw_networkx_nodes(self.owlGraph, pos = self.graphPositions, with_labels=False, arrows=False, ax = ax, node_size = .1,scale = 1)

        nx.draw_networkx_edges(self.owlGraph, pos = self.graphPositions, edgelist = self.subconcernEdges, arrows=False,style = "solid",width = edge_width,edge_color = edge_color,alpha = edge_alpha)
        nx.draw_networkx_edges(self.owlGraph, pos = self.graphPositions, edgelist = self.propertyEdges, arrows=False,style = "dashed",width = edge_width,edge_color = edge_color, alpha = edge_alpha)


        nx.draw_networkx_edge_labels(self.owlGraph, pos = self.graphPositions, edge_labels=self.concernEdgeLabels,font_size = fs)
        nx.draw_networkx_edge_labels(self.owlGraph, pos = self.graphPositions, edge_labels=self.propertyEdgeLabels,font_size = fs)

        nx.draw_networkx_labels(self.owlGraph,self.graphPositions,self.aspectNodeLabels,font_size=fs,bbox=dict(facecolor=aspect_color, boxstyle='square,pad=.3'),font_color = "white")
        nx.draw_networkx_labels(self.owlGraph,self.graphPositions,self.concernNodeLabels,font_size=fs,bbox=dict(facecolor=concern_color, boxstyle='square,pad=.3'),font_color = "white")
        nx.draw_networkx_labels(self.owlGraph,self.graphPositions,self.propertyNodeLabels,font_size=fs,bbox=dict(facecolor=property_color, boxstyle='round4,pad=.3'),font_color = "white")





    def loadOwlFile(self,filename):

        #self.owlReadyOntology = get_ontology("file://./../../src/asklab/querypicker/QUERIES/BASE/" + filename).load()
        self.owlReadyOntology = get_ontology("file://./" + filename).load()
        self.owlName = str(filename)

    def constructIndividualArray(self):

        self.owlIndividualArray = np.array(())
        self.nodeArray = np.array(())

        all_aspects = np.asarray(self.owlReadyOntology.search(type = self.owlReadyOntology.Aspect))


        #all_aspects = np.asarray(self.owlReadyOntology.search(iri = "*" + "Trustworthiness"))
        #all_aspects = np.array((self.owlReadyOntology.Trustworthiness))

        for aspect in all_aspects:


           self.addAllConcernsFromParent(aspect,"None",0)

        self.addDanglingParentConcerns()
       # self.addAllProperties()



    def addAllConcernsFromParent(self,concern,parent,level):

        #print("called")

        #appends to the total concern list
        self.owlIndividualArray = np.append(self.owlIndividualArray,concern)

        newOwlNode = owlNode()
        newOwlNode.name = remove_namespace(concern)
        newOwlNode.type = remove_namespace(concern.is_a[0])
        newOwlNode.parent = remove_namespace(parent)
        newOwlNode.children = np.array(())
        newOwlNode.level = level

        for child in concern.includesConcern:

            newOwlNode.children = np.append(newOwlNode.children,remove_namespace(child))


        if(newOwlNode.type == "Aspect"):
            newOwlNode.parent = "None"



        self.nodeArray = np.append(self.nodeArray,newOwlNode)

        level = level + 1
        #recursively calls subconcerns
        for subconcern in concern.includesConcern:

            self.addAllConcernsFromParent(subconcern,concern,level)
        
    
    
    def addDanglingParentConcerns(self):
        
        all_concerns = np.asarray(self.owlReadyOntology.search(type = self.owlReadyOntology.Concern))
        
        
        #print("ALL CONCERNS IN DANGLING PARENT")
        #print(all_concerns)
        
        for concern in all_concerns:
            #print("concern in loop is " + remove_namespace(concern))
            
            if(self.checkAddedToArray(remove_namespace(concern)) == False):
                
                #print("adding dangling parent = " + remove_namespace(concern))
                
                self.owlIndividualArray = np.append(self.owlIndividualArray,concern)
                
                newOwlNode = owlNode()
                newOwlNode.name = remove_namespace(concern)
                newOwlNode.type = remove_namespace(concern.is_a[0])
                newOwlNode.children = np.array(())
                newOwlNode.parent = "None"
                
                for child in concern.includesConcern:

                    newOwlNode.children = np.append(newOwlNode.children,remove_namespace(child))
                
                self.nodeArray = np.append(self.nodeArray,newOwlNode)
                
                
                
                
        

    def addAllProperties(self):

        #print("called add all properties/n/n/n/n")
        #print("")
        #print("")

        #print("")
        #print("")
        #print("")
        #print("")
        #print("")



        impact_rules = np.asarray(self.owlReadyOntology.search(type = self.owlReadyOntology.ImpactRule))



        for ir in impact_rules:


            if(len(ir.hasCondition) == 0 or len(ir.hasCondition[0].conditionProperty) == 0):
                print("bad list")
                continue
            prop = ir.hasCondition[0].conditionProperty[0]

            #if(remove_namespace(prop) == "Input1ConsistentReadingFreq" or remove_namespace(prop) == "Input1Modes"):
            #    continue
            self.owlIndividualArray = np.append(self.owlIndividualArray,prop)



            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(prop)
            newOwlNode.type = remove_namespace(prop.is_a[0])

            #becaseu of this probs
            newOwlNode.children = np.array(())


            #need to add property as child of concern
            if(len(ir.addressesConcern) == 0):
                print("IR doesn't address anything")
                continue
            newOwlNode.parent = str(remove_namespace(ir.addressesConcern[0]))

            parentNode = self.findNode(newOwlNode.parent)

            parentNode.children = np.append(parentNode.children, newOwlNode.name)

            print(newOwlNode.name)
            newOwlNode.level = self.findNode(newOwlNode.parent).level + 1

            self.nodeArray = np.append(self.nodeArray,newOwlNode)



    def constructOwlNodes(self):

        #self.nodeArray = np.array(())

        for indiv in self.owlIndividualArray:

            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(indiv)
            newOwlNode.type = remove_namespace(indiv.is_a[0])

            self.nodeArray = np.append(self.nodeArray,newOwlNode)

    def setNumbers(self):

        #print("called set numbers")
        self.numAspects =  len(self.owlReadyOntology.search(type = self.owlReadyOntology.Aspect))
        self.numConcerns =  len(self.owlReadyOntology.search(type = self.owlReadyOntology.Concern))
        self.numProperties =  len(self.owlReadyOntology.search(type = self.owlReadyOntology.Property))
        self.numNodes = self.numAspects + self.numConcerns + self.numProperties

        self.numComponents = 0
        self.numConditions = len(self.owlReadyOntology.search(type = self.owlReadyOntology.Condition))
        self.numImpactRules =  len(self.owlReadyOntology.search(type = self.owlReadyOntology.ImpactRule))

        #self.printNumbers()

    def findNode(self,name):

        for node in self.nodeArray:

            if(node.name == name):

                return node

        print("couldn't find " + str(name))
        return 0

    def removeEdgeless(self):
        
        for node in self.nodeArray:
            
            print(node.name + " in removeEdgeless")
            print(node.parent == "None")
            print(len(node.children) == 0)
            print(node.type != "Aspect")
    
            print()            
            
            if(node.parent == "None" and len(node.children) == 0 and node.type != "Aspect"):
                
                print("trying to remove " + node.name)
                to_remove = self.owlReadyOntology.ontology.search(iri = "*" + node.name)
        
                names = []
        
                for subc in to_remove:
                    names.append(remove_namespace(subc))
        
                i = 0
        
                while i < len(names):
        
                    if(names[i] == node.name):
                        break
        
                    i = i + 1
                to_remove = to_remove[i]
                
                destroy_entity(to_remove)

    def printNumbers(self):



        print("numNodes = " + str(self.numNodes))
        print("numAspects = " + str(self.numAspects))
        print("numConcerns = " + str(self.numConcerns))
        print("numProperties = " + str(self.numProperties))
        print("numComponents = " + str(self.numComponents))
        print("numImpactRules = " + str(self.numImpactRules))
        print("numConditions = " + str(self.numConditions))
        
def is_asp_or_conc(mytype):
    
    if(not (mytype == "Concern" or mytype == "Aspect") ):
        return False
    else:
        return True






#testOwlOntology = owlOntology("cpsframework-v3-base.owl")

#for node in testOwlOntology.nodeArray:
#    print(node.name)

#print("done\n\n")

#    print(node.name + " " + node.type + " parent = " + node.parent + " children = " + str(node.children) + " level = " + str(node.level))




#fig, ax = plt.subplots(figsize = (10,10))
#testOwlOntology.makeGraph()

#testOwlOntology.draw_graph(ax,8)

#print(testOwlOntology.aspectConcernArray)

#print(testOwlOntology.propertyArray)

#print(testOwlOntology.subconcernEdges)
#print(testOwlOntology.propertyEdges)

#print(testOwlOntology.owlIndividualArray)

#testOwlOntology.printNumbers()

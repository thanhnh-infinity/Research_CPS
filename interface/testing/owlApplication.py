from owlready2 import *
import numpy as np
from owlNode import owlNode
from owlFunctions import remove_namespace
from owlFunctions import remove_ir
from owlBase import owlBase

class owlApplication:
    
    def __init__(self,filename,base):
        
        self.owlReadyOntology = None
        self.owlBase = base 
        
        self.owlBase.owlApplication = self
        
        self.owlName = None
        self.nodeArray = None
        
        self.allComponents_owlNode = None
        self.allProperties_owlNode = None
        
        self.numNodes = None
        self.numComponents = None
        self.numProperties = None
        self.numConditions = None
        self.numImpactRules = None
        
        self.owlGraph = None
    
        self.loadOwlFile(filename)
        
        
    def loadOwlFile(self,filename):
        
        self.owlReadyOntology = get_ontology("file://./application_ontologies/" + filename).load()
        self.owlName = str(filename)
        
    def initializeOwlNodes(self):
        
        self.nodeArray = []
        
        self.addComponents()
        self.addProperties()
        self.handleRelateToProperty()
        self.handleAddConcern()
        #self.assignParentsFromChildren()
        
    
    def addComponents(self):
        
        self.allComponents_owlNode = []
        
        all_components = np.asarray(self.owlReadyOntology.search(type = self.owlReadyOntology.Component))
        
        
        for component in all_components:
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(component)
            newOwlNode.type = remove_namespace(component.is_a[0])
            newOwlNode.children = []
            newOwlNode.parents = []
            newOwlNode.owlreadyObj = component
            
            self.allComponents_owlNode.append(newOwlNode)
            self.nodeArray.append(newOwlNode)
            
    def addProperties(self):
        
        self.allProperties_owlNode = []
        
        all_properties = np.asarray(self.owlReadyOntology.search(type = self.owlReadyOntology.Property))
        
        for prop in all_properties:
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(prop)
            newOwlNode.type = remove_namespace(prop.is_a[0])
            newOwlNode.children = []
            newOwlNode.parents = []
            
            newOwlNode.owlreadyObj = prop
            
            self.allProperties_owlNode.append(newOwlNode)
            self.nodeArray.append(newOwlNode)
    
    def handleRelateToProperty(self):
        
        for comp in self.allComponents_owlNode:
            
            all_rel_props = comp.owlreadyObj.relateToProperty
            
            #prop is owlready node
            for prop in all_rel_props:
                
                prop_owlNode = self.getOwlNode(remove_namespace(prop))
                
                
        
                prop_owlNode.children.append(comp)
                comp.parents.append(prop_owlNode)
                
    def handleAddConcern(self):
        
        for prop in self.allProperties_owlNode:
            
            all_add_concern = prop.owlreadyObj.addConcern
            
            for concern in all_add_concern:
                
                baseconcern = self.getOwlNodeFromBase(remove_ir(concern))
                
                
                if(baseconcern == 0):
                    
                    #print("couldn't find concern " + remove_ir(concern) + " addressed by " + prop.name + " - ignoring it")
                    continue
                
                
                
                baseconcern.children.append(prop)
                prop.parents.append(baseconcern)
            
            
                
                
    def assignParentsFromChildren(self):
        
        for node in self.nodeArray:
            
            for child in node.children:
                
                child.parents.append(node)
                
                
    def getOwlNode(self,name):
        
        for node in self.nodeArray:
            
            if(node.name == name):
                
                return node
        
        #print("couldnt find from app " + name)
        return 0
    
    
    def getOwlNodeFromBase(self,name):
       
        #print("searching for " + name)
        
        for node in self.owlBase.allConcerns_owlNode:
            
            if(node.name == name):
                
                return node
        #print("couldnt find from base " + name)
        return 0
        
        
    
        
#testBase = owlBase("cpsframework-v3-base.owl")

#testBase.initializeOwlNodes()    




        
#testApp = owlApplication("cpsframework-v3-sr-Elevator-Configuration.owl",testBase)
    
    
#testApp.initializeOwlNodes()


#print()
#print()

#for node in testApp.nodeArray:

 #   print(node.name)
  #  print(node.type)
    
   # print("children")
    #for child in node.children:
       
     #   print(child.name)
        
        
    #print("parents")
    #for parent in node.parents:
        
    #    print(parent.name)
    
    #print()
    
#for node in testBase.allConcerns_owlNode:
    
 #   print(node.name)
    
  #  for child in node.children:
   #     print(child.name)
        
   # print()




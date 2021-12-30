from owlready2 import *
import numpy as np
from owlNode import owlNode
from owlFunctions import remove_namespace
from owlFunctions import remove_ir
from owlBase import owlBase

class owlApplication:
    
    def __init__(self,filename,base):
        
        
        self.handleProperties = True
        self.handleComponents = True
        
        self.owlreadyOntology = None
        self.owlBase = base 
        
        self.owlBase.owlApplication = self
        
        self.owlName = None
        self.nodeArray = None
        
        self.allComponents_owlNode = None
        self.allProperties_owlNode = None
        self.allFormulas_owlNode = None
        self.allDecompFuncs_owlNode = None
        
        self.numNodes = None
        self.numComponents = None
        self.numProperties = None
     
        
        self.owlGraph = None
    
    
        self.loadOwlFile(filename)
        
        
    def loadOwlFile(self,filename):
        
        self.owlreadyOntology = get_ontology("file://./" + filename).load()
        self.owlName = str(filename)
        print(self.owlName)
        #self.numConditions = len(self.owlreadyOntology.search(type = self.owlreadyOntology.Condition))
        #self.numIRs = len(self.owlreadyOntology.search(type = self.owlreadyOntology.ImpactRule))
        
        
    def initializeOwlNodes(self):
        
        self.nodeArray = []
        
        
        
        if(self.handleComponents == True):
            self.addComponents()
            
        if(self.handleProperties == True):
            
            self.addProperties()
            #try:
            self.addFormulas()
           # except:
                #print("couldn't add formulas")
                
            self.addFuncDecomps()
            
            
        if(self.handleComponents == True):
            
           
            
            self.handleRelateToProperty()
            
        if(self.handleProperties == True):
            
            try:
                self.handleMemberOf()
                
            except:
                print("couldn't ao memberof")
                
            try:
                self.handleNegMemberOf()
                
            except:
                print("couldn't do negmemberof")
                
            try:
                self.handleFormulasAddConcern()
                
            except:
                print("couldn't do handleformulasaddconcern")
                
            self.handleaddConcern()
         
            
        
    def addProperties(self):
        
        self.allProperties_owlNode = []
        
        all_props = np.asarray(self.owlreadyOntology.search(type = self.owlreadyOntology.Property))
       
        
        
        for prop in all_props:
        
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(prop)
            newOwlNode.type = "Property"
            newOwlNode.children = []
            newOwlNode.negChildren = []
            newOwlNode.parents = []
            
            newOwlNode.owlreadyObj = prop
            
            self.allProperties_owlNode.append(newOwlNode)
            self.nodeArray.append(newOwlNode)    
            
            
            
    def addFormulas(self):
        
        self.allFormulas_owlNode = []
        
        props = np.asarray(self.owlreadyOntology.search(type =  self.owlreadyOntology.Property))
        forms = np.asarray(self.owlreadyOntology.search(type =  self.owlreadyOntology.Formulas))
        decomps = np.asarray(self.owlreadyOntology.search(type = self.owlreadyOntology.DecompositionFunction))
        
        
        all_Formulas = list(set(props) ^ set(forms) ^ set(decomps))
        
        for Formulas in all_Formulas:
            
            if(remove_namespace(Formulas)[0] == "g"):
                
                
                continue
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(Formulas)
            newOwlNode.type = "Formulas"
            newOwlNode.subtype = self.getSubType(Formulas)
            newOwlNode.children = []
            newOwlNode.negChildren = []
            newOwlNode.parents = []
            newOwlNode.owlreadyObj = Formulas
            
            
            self.allFormulas_owlNode.append(newOwlNode)
            self.nodeArray.append(newOwlNode)
            
    def addFuncDecomps(self):
        
        self.allDecompFuncs_owlNode = []
        
        all_decomps = np.asarray(self.owlreadyOntology.search(type = self.owlreadyOntology.DecompositionFunction))
        
        for decomp in all_decomps:
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(decomp)
            newOwlNode.type = "DecompositionFunction"
            newOwlNode.subtype = self.getSubType(decomp)
            newOwlNode.children = []
            newOwlNode.negChildren = []
            newOwlNode.parents = []
            newOwlNode.owlreadyObj = decomp
          
            
            self.allDecompFuncs_owlNode.append(newOwlNode)
            self.nodeArray.append(newOwlNode)
                    

    def addComponents(self):
        
        self.allComponents_owlNode = []
        
        all_components = np.asarray(self.owlreadyOntology.search(type = self.owlreadyOntology.Component))
        
        
        for component in all_components:
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(component)
            newOwlNode.type = remove_namespace(component.is_a[0])
            newOwlNode.children = []
            newOwlNode.negChildren = []
            newOwlNode.parents = []
            newOwlNode.owlreadyObj = component
            
            self.allComponents_owlNode.append(newOwlNode)
            self.nodeArray.append(newOwlNode)
            
   
            
   
   
    def handleMemberOf(self):
        
        for child in self.nodeArray :
            
            child_owlr = child.owlreadyObj
            
            member_of = child_owlr.memberOf
        
            
            for memberof in member_of:
                
                parent = self.getOwlNode(remove_namespace(memberof))
                
                child.parents.append(parent)
                parent.children.append(child)
                
         
                
    def handleNegMemberOf(self):
        
        
        for child in self.nodeArray:
            
            child_owlr = child.owlreadyObj
        
            
            neg_member_of = child_owlr.negMemberOf
     
            for negmemberof in neg_member_of:
                
        
                parent = self.getOwlNode(remove_namespace(negmemberof))
                
                child.parents.append(parent)
            
                parent.negChildren.append(child)
        
    def handleFormulasAddConcern(self):
        
    
        for child in self.nodeArray:
            
            child_owlr = child.owlreadyObj
            
            addresses = child_owlr.formulasAddConcern
            
            for addressed in addresses:
                
                parent = self.getOwlNodeFromBase(remove_namespace(addressed))
                
                child.parents.append(parent)
                parent.children.append(child)
                
                
    def handleaddConcern(self):
        
    
        for child in self.nodeArray:
            
            child_owlr = child.owlreadyObj
            addresses = child_owlr.addConcern 
    
            for addressed in addresses:
                
                parent = self.getOwlNodeFromBase(remove_namespace(addressed))
                
                child.parents.append(parent)
                parent.children.append(child)
                
                
    def handleRelateToProperty(self):
        
        for comp in self.allComponents_owlNode:
            
         
            
            
            all_rel_props = comp.owlreadyObj.relateToProperty
            
            #prop is owlready node
            for prop in all_rel_props:
                
                prop_owlNode = self.getOwlNode(remove_namespace(prop))
                
                
        
                prop_owlNode.children.append(comp)
                comp.parents.append(prop_owlNode)
  
     
        
  
    def addPropertyAsChildofConcern(self,parentConcern,new_property_name):
        
        new_property = self.owlreadyOntology.Property(new_property_name, ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formulas)
        
        new_property.addConcern.append(parentConcern.owlreadyObj)
     
        
    def addPropertyAsParentofComponent(self,new_name,parent):
        
        #parent is component
        
        new_property =  self.owlreadyOntology.Property(new_name, ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formulas)
        
        parent.owlreadyObj.relateToProperty.append(new_property)
        
    def addRLProperty(self,new_name):
        
        new_property = self.owlreadyOntology.Property(new_name,ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formulas)

    def addNewComponent(self,new_name):
        
        new_component = self.owlreadyOntology.Component(new_name,ontology = self.owlreadyOntology)        
                
    def addNewComponentAsChild(self,new_name,parent):
        
        new_component = self.owlreadyOntology.Component(new_name,ontology = self.owlreadyOntology)
         
        new_component.relateToProperty.append(parent.owlreadyObj)       


    def addaddConcernRelation(self,parent,child):
        
        child.owlreadyObj.addConcern.append(parent.owlreadyObj)
        
        
    def addNewConcernFormulasRelation(self,parent,child):
        
        #parent is concern
        #child is Formulas
        
        child.owlreadyObj.formulasAddConcern.append(parent.owlreadyObj)
        
    def addFormulasPropertyRelations(self,parent,child):
        
        #parent is Formulas
        #child is property
        
        child.owlreadyObj.memberOf.append(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.append(child.owlreadyObj)
        
        self.findAddressedConcern(parent.owlreadyObj)
        
        
        for addconcern in self.addressed_concerns:
            
         
            child.owlreadyObj.addConcern.append(addconcern)
       
        
    def addFormulasFormulasRelations(self,parent,child):
        
        #parent is Formulas/functionaldecomp
        #child is Formulas/functionaldecomp
        
        child.owlreadyObj.memberOf.append(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.append(child.owlreadyObj)

    def addNewPropertyToFormulas(self,parent,child_name):
    
        new_property = self.owlreadyOntology.Property(child_name, ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formulas)
        
        Formulas_owlready = parent.owlreadyObj
        
        new_property.memberOf.append(Formulas_owlready)
        Formulas_owlready.includesMember.append(new_property)
        
        self.findAddressedConcern(Formulas_owlready)
        
        for addconcern in self.addressed_concerns:
            
         
            new_property.addConcern.append(addconcern)

    def addNewRelatedToRelation(self,parent,child):
        
        child.owlreadyObj.relateToProperty.append(parent.owlreadyObj)
        
  
    def addNewDependency(self,LHSNodes,RHSNode):
        
        last_Formulas = None
        
        formulas_number = 1
       
        for lhsnode in LHSNodes:
        
            formulas_number +=1 
            
            if(lhsnode.operator == "and"):
                
                print(lhsnode.name)
                
                new_Formulas = self.owlreadyOntology.Conjunction(lhsnode.name,ontology = self.owlreadyOntology)
            
            else:
                
                new_Formulas = self.owlreadyOntology.Disjunction(lhsnode.name,ontology = self.owlreadyOntology)
                
            
            last_Formulas = new_Formulas
            for member in lhsnode.members:
                
                if(member == ""):
                    continue
                
                
                
                
                member_owlready = self.getOWLObject(member)
                if(self.isProperty(member_owlready) == True):
                    
                   
                    member_owlready.addConcern.append(RHSNode.owlreadyObj)
               
                
                
                #make Formulas have children, negated children 
                
                if(member[0] == "-"):
                    
                
                    print(member, " is negated")
                    
                    
                    new_Formulas.includesMember.append(member_owlready)
                    member_owlready.negMemberOf.append(new_Formulas)
               
                else:
                    
                    new_Formulas.includesMember.append(member_owlready)
                    member_owlready.memberOf.append(new_Formulas)
                    
                
        
        if last_Formulas != None:
           
            last_Formulas.formulasAddConcern.append(RHSNode.owlreadyObj)
        
                     
        
    def editPropertyName(self,node,new_name):
        
        node.owlreadyObj.name = new_name
        
    def editFormulaName(self,node,new_name):
        
        node.owlreadyObj.name = new_name
    
    def editComponentName(self,node,new_name):
        
        node.owlreadyObj.name = new_name
        
    def switchToRegMemberOf(self,relationChild,relationParent):
        
        print("x")
        relationChild.owlreadyObj.memberOf.append(relationParent.owlreadyObj)
        relationChild.owlreadyObj.negMemberOf.remove(relationParent.owlreadyObj)
        
        
        print("y")
        
    def switchToNegMemberOf(self,relationChild,relationParent):
        
        print("z")
        
        relationChild.owlreadyObj.negMemberOf.append(relationParent.owlreadyObj)
        relationChild.owlreadyObj.memberOf.remove(relationParent.owlreadyObj)
        
        
        print("zz")

    def removePropertyAddressesConcernRelation(self,parent,child):
        
        #parent is Concern
        #child is property
        
        child.owlreadyObj.addConcern.remove(parent.owlreadyObj)

    def removeConcernFormulasRelation(self,parent,child):
        
        child.owlreadyObj.formulasAddConcern.remove(parent.owlreadyObj)
        
        
    def removeFormulasFormulasRelation(self,parent,child):
        
        #parent is Formulas
        #child is Formulas
        
        child.owlreadyObj.memberOf.remove(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.remove(child.owlreadyObj)
        
    def removeFormulasPropertyRelations(self,parent,child):
        
        #parent is Formulas
        #child is property 
        
        child.owlreadyObj.memberOf.remove(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.remove(child.owlreadyObj)
        
        
    def removeRelatedToRelation(self,parent,child):
        
        child.owlreadyObj.relateToProperty.remove(parent.owlreadyObj)
           
   
    def findAddressedConcern(self,owlreadyobj):
        
        addressed_concern = owlreadyobj.formulasAddConcern 
        
        if (len(addressed_concern) > 0):
            
            self.addressed_concerns = addressed_concern
            return addressed_concern
        
        else:
            
            if(len(owlreadyobj.memberOf) == 0):
                return
            
            self.findAddressedConcern(owlreadyobj.memberOf[0])
        
                
    def getOwlNode(self,name):
        
        for node in self.nodeArray:
            
            if(node.name == name):
                
                return node
        
        print("couldnt find from app " + name)
        return 0
    
    def getOWLObject(self,name):

        if name[0] == "-":
            
            name = name[1:]
        
        obj_list = self.owlreadyOntology.search(iri = "*" + name)
        
        if(len(obj_list) == 0):
            print("couldnt find " + name)
        obj_names = []

        for obj in obj_list:
            obj_names.append(remove_namespace(obj))

        i = 0
        while i < len(obj_names):

            if(obj_names[i] == name):
                obj = obj_list[i]
                break

            i = i + 1


        #print("found ", obj)
        return obj
    
    
    def getOwlNodeFromBase(self,name):
       
        #print("searching for " + name)
        
        for node in self.owlBase.allConcerns_owlNode:
            
            if(node.name == name):
                
                return node
        #print("couldnt find from base " + name)
        return 0
    
    def setNumbers(self):
        
        try:
            self.numComponents = len(self.allComponents_owlNode)
        except:
            
            self.numComponents = 0
            
        try:
            self.numProperties = len(self.allProperties_owlNode)
        except:
            self.numProperties = 0
        self.numNodes = self.numComponents + self.numProperties
        
    def isProperty(self,owlreadyobj):
        
        is_a = owlreadyobj.is_a
        
        for istype in is_a:
            
            if(remove_namespace(istype) == "Property"):
                
                return True
            
        return False   


    def getSubType(self,owlreadynode):
        
        types = owlreadynode.is_a
        
        if(self.owlreadyOntology.Conjunction in types ):
            
            return "Conjunction"
            
        elif(self.owlreadyOntology.Disjunction in types):
            
            return "Disjunction"
            
        else:
            
            return "None"
    
        
#testBase = owlBase("cpsframework-v3-base-development.owl")



#testBase.initializeOwlNodes()    




        
#testApp = owlApplication("application_ontologies/cpsframework-v3-sr-LKAS-Configuration-V2" + ".owl",testBase)
    
    
#testApp.initializeOwlNodes()

#testApp.getSubType(testApp.owlreadyOntology.energy_func)

#for node in testApp.nodeArray:

    #print(node.name)
    #print(node.type)
    #print(node.polarity)
    #print(node.subtype)
    #print("children")
    #for child in node.children:
       
       # print(child.name)
        
        
    #print("parents")
    #for parent in node.parents:
        
      #  print(parent.name)
    
    #print()
    
#for node in testBase.allConcerns_owlNode:
    
 #   print(node.name)
    
  #  for child in node.children:
   #     print(child.name)
        
    #print()




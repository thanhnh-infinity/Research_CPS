from owlready2 import *
import numpy as np
from owlNode import owlNode
from owlFunctions import remove_namespace
from owlFunctions import remove_ir
from owlBase import owlBase

class owlApplication:
    
    def __init__(self,filename,base):
        
        
        self.handleProperties = True
        self.handleComponents = False
        
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
        #self.numConditions = len(self.owlreadyOntology.search(type = self.owlreadyOntology.Condition))
        #self.numIRs = len(self.owlreadyOntology.search(type = self.owlreadyOntology.ImpactRule))
        
        
    def initializeOwlNodes(self):
        
        self.nodeArray = []
        
        
        
        if(self.handleComponents == True):
            self.addComponents()
            
        if(self.handleProperties == True):
            
            self.addProperties()
            self.addFormulas()
            self.addFuncDecomps()
            
            
        if(self.handleComponents == True):
            
           
            
            self.handleRelateToProperty()
            
        if(self.handleProperties == True):
            
            self.handleMemberOf()
            self.handleNegMemberOf()
            self.handleFormulaAddConcern()
            self.handlePropertyAddConcern()
         
            
        
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
        forms = np.asarray(self.owlreadyOntology.search(type =  self.owlreadyOntology.Formula))
        decomps = np.asarray(self.owlreadyOntology.search(type = self.owlreadyOntology.DecompositionFunction))
        
        
        all_formulas = list(set(props) ^ set(forms) ^ set(decomps))
        
        for formula in all_formulas:
            
            newOwlNode = owlNode()
            newOwlNode.name = remove_namespace(formula)
            newOwlNode.type = "Formula"
            newOwlNode.subtype = self.getSubType(formula)
            newOwlNode.children = []
            newOwlNode.negChildren = []
            newOwlNode.parents = []
            newOwlNode.owlreadyObj = formula
            
            
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
        
    def handleFormulaAddConcern(self):
        
    
        for child in self.nodeArray:
            
            child_owlr = child.owlreadyObj
            
            addresses = child_owlr.formulaAddConcern
            
            for addressed in addresses:
                
                parent = self.getOwlNodeFromBase(remove_namespace(addressed))
                
                child.parents.append(parent)
                parent.children.append(child)
                
                
    def handlePropertyAddConcern(self):
        
    
        for child in self.nodeArray:
            
            child_owlr = child.owlreadyObj
            addresses = child_owlr.propertyAddConcern 
    
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
        new_property.is_a.append(self.owlreadyOntology.Formula)
        
        new_property.propertyAddConcern.append(parentConcern.owlreadyObj)
     
        
    def addPropertyAsParentofComponent(self,new_name,parent):
        
        #parent is component
        
        new_property =  self.owlreadyOntology.Property(new_name, ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formula)
        
        parent.owlreadyObj.relateToProperty.append(new_property)
        
    def addRLProperty(self,new_name):
        
        new_property = self.owlreadyOntology.Property(new_name,ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formula)

    def addNewComponent(self,new_name):
        
        new_component = self.owlreadyOntology.Component(new_name,ontology = self.owlreadyOntology)        
                
    def addNewComponentAsChild(self,new_name,parent):
        
        new_component = self.owlreadyOntology.Component(new_name,ontology = self.owlreadyOntology)
         
        new_component.relateToProperty.append(parent.owlreadyObj)       


    def addPropertyAddConcernRelation(self,parent,child):
        
        child.owlreadyObj.propertyAddConcern.append(parent.owlreadyObj)
        
        
    def addNewConcernFormulaRelation(self,parent,child):
        
        #parent is concern
        #child is formula
        
        child.owlreadyObj.formulaAddConcern.append(parent.owlreadyObj)
        
    def addFormulaPropertyRelations(self,parent,child):
        
        #parent is formula
        #child is property
        
        child.owlreadyObj.memberOf.append(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.append(child.owlreadyObj)
        
        self.findAddressedConcern(parent.owlreadyObj)
        
        
        for addconcern in self.addressed_concerns:
            
         
            child.owlreadyObj.propertyAddConcern.append(addconcern)
       
        
    def addFormulaFormulaRelations(self,parent,child):
        
        #parent is formula/functionaldecomp
        #child is formula/functionaldecomp
        
        child.owlreadyObj.memberOf.append(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.append(child.owlreadyObj)

    def addNewPropertyToFormula(self,parent,child_name):
    
        new_property = self.owlreadyOntology.Property(child_name, ontology = self.owlreadyOntology)
        new_property.is_a.append(self.owlreadyOntology.Formula)
        
        formula_owlready = parent.owlreadyObj
        
        new_property.memberOf.append(formula_owlready)
        formula_owlready.includesMember.append(new_property)
        
        self.findAddressedConcern(formula_owlready)
        
        for addconcern in self.addressed_concerns:
            
         
            new_property.propertyAddConcern.append(addconcern)

    def addNewRelatedToRelation(self,parent,child):
        
        child.owlreadyObj.relateToProperty.append(parent.owlreadyObj)
        
  
    def addNewDependency(self,LHSNodes,RHSNode):
        
        last_formula = None
        
        formulas_number = 1
       
        for lhsnode in LHSNodes:
        
            formulas_number +=1 
            
            if(lhsnode.operator == "and"):
                
                print(lhsnode.name)
                
                new_formula = self.owlreadyOntology.Conjunction(lhsnode.name,ontology = self.owlreadyOntology)
            
            else:
                
                new_formula = self.owlreadyOntology.Disjunction(lhsnode.name,ontology = self.owlreadyOntology)
                
            
            last_formula = new_formula
            for member in lhsnode.members:
                
                if(member == ""):
                    continue
                
                
                
                
                member_owlready = self.getOWLObject(member)
                if(self.isProperty(member_owlready) == True):
                    
                   
                    member_owlready.propertyAddConcern.append(RHSNode.owlreadyObj)
               
                
                
                #make formulas have children, negated children 
                
                if(member[0] == "-"):
                    
                
                    print(member, " is negated")
                    
                    
                    new_formula.includesMember.append(member_owlready)
                    member_owlready.negMemberOf.append(new_formula)
               
                else:
                    
                    new_formula.includesMember.append(member_owlready)
                    member_owlready.memberOf.append(new_formula)
                    
                
        
        if last_formula != None:
           
            last_formula.formulaAddConcern.append(RHSNode.owlreadyObj)
        
                     
        
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
        
        child.owlreadyObj.propertyAddConcern.remove(parent.owlreadyObj)

    def removeConcernFormulaRelation(self,parent,child):
        
        child.owlreadyObj.formulaAddConcern.remove(parent.owlreadyObj)
        
        
    def removeFormulaFormulaRelation(self,parent,child):
        
        #parent is formula
        #child is formula
        
        child.owlreadyObj.memberOf.remove(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.remove(child.owlreadyObj)
        
    def removeFormulaPropertyRelations(self,parent,child):
        
        #parent is formula
        #child is property 
        
        child.owlreadyObj.memberOf.remove(parent.owlreadyObj)
        parent.owlreadyObj.includesMember.remove(child.owlreadyObj)
        
        
    def removeRelatedToRelation(self,parent,child):
        
        child.owlreadyObj.relateToProperty.remove(parent.owlreadyObj)
           
   
    def findAddressedConcern(self,owlreadyobj):
        
        addressed_concern = owlreadyobj.formulaAddConcern 
        
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




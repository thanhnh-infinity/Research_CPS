from parse import *
import csv  
from csvNode import csvNode 
import os



class ASPExporter:
    
    def __init__(self,filename):
        
        self.file = None
        self.allLines = None
        
        self.encodingLine = None
        
        
        self.allNodes = []
        self.allAspects_Node = []
        self.allConcerns_Node = []
        self.allSubConcernRelations_str_str = []
        self.allLeaves_Node = []
        
        self.outputRows = []
        self.outputFields = None
        
        self.maxLevel = 0
        
        self.loadFile(filename)    
        
        self.addAllNodes()
        
        self.assignDataMembers()
        
        
       
        self.removeRelationless()
         
    
    def loadFile(self,filename):
        
        self.file = open(filename,mode = "r")
        
        self.allLines = self.file.readlines()
        
        self.encodingLine = self.allLines[4]
        
        
    
    def addAllNodes(self):
        
        self.addAllAspects()
        self.addAllConcerns()
        self.addAllSubconcernRelations()
        self.addAllChildrenParents()
        self.setSatisfaction()
        
        
        
    def assignDataMembers(self):
        
        
        
        
        
        
        for node in self.allNodes:
        
            if(node.type == "Aspect"):
                self.assignLevel(node,1)
                self.assignAspectTree(node,node)
            
            self.assignLeaf(node)
            
    
        for node in self.allNodes:
            
            self.assignSum(node,node)
            self.assignLineage(node,node)
            
            if(node.level > self.maxLevel):
                
                self.maxLevel = node.level
                
        self.lineLength = self.maxLevel + 6    
        
        self.masterLine = []
        
        for i in range(self.lineLength):
            
            self.masterLine.append("")
        
        
    def addAllAspects(self):
        
        parsed_aspects = ' '.join(r[0] for r in findall("aspect({})", self.encodingLine))
        
        allAspects_strList = parsed_aspects.split(" ")
        
        
        for aspect in allAspects_strList:
            
            newCSVNode = csvNode()
            
            newCSVNode.name = aspect
            newCSVNode.type = "Aspect"
            
            self.allNodes.append(newCSVNode)
            self.allAspects_Node.append(newCSVNode)
            
    def addAllConcerns(self):
        parsed_concerns = ' '.join(r[0] for r in findall(" concern(\"cpsf:{}\")", self.encodingLine))
        
        allConcerns_strList = parsed_concerns.split(" ")
        
        
        for concern in allConcerns_strList:
            
            if(self.getCSVNode(concern) != 0):
                continue
            
            
            newCSVNode = csvNode()
            
            newCSVNode.name = concern
            newCSVNode.type = "Concern"
            
            self.allNodes.append(newCSVNode)
            self.allConcerns_Node.append(newCSVNode)
            
    def addAllSubconcernRelations(self):
        
        parsed_subconcerns = ' '.join(r[0] for r in findall(" subconcern({})", self.encodingLine))
        
        allSubConcerns_strList = parsed_subconcerns.split(" ")
        
        
        for subconcern in allSubConcerns_strList:
            
            self.allSubConcernRelations_str_str.append(subconcern)
            
    def setSatisfaction(self):
        
        parsed_satisfied =  ' '.join(r[0] for r in findall(" h(sat({}),0)", self.encodingLine))
        parsed_unsatisfied =  ' '.join(r[0] for r in findall(" -h(sat({}),0)", self.encodingLine))
        
        
        allSatisfied_strList = parsed_satisfied.split(" ")
        allUnSatisfied_strList = parsed_unsatisfied.split(" ")
        
        for satisfied in allSatisfied_strList:
            
            #print(satisfied, " satisfied")
            if(satisfied == "all" or satisfied == "roles"):
                continue
            
            satisfied_node = self.getCSVNode(satisfied)
            
            if(satisfied_node == 0):
                print("couldn't find ", satisfied)
                continue
            
            satisfied_node.satisfied = True 
            
        for unsatisfied in allUnSatisfied_strList:
            
            #print(unsatisfied, " unsatisfied")
            if(unsatisfied == "all" or unsatisfied == "roles"):
                continue
            
            unsatisfied_node = self.getCSVNode(unsatisfied)
            
            if(unsatisfied_node == 0):
                print("couldn't find ", unsatisfied)
                continue
            
            unsatisfied_node.satisfied = False
            
        
            
            
    def addAllChildrenParents(self):
        
        
        for relation in self.allSubConcernRelations_str_str:
            
            duo = relation.split(",")
        
            
            parent_name = duo[0]
            parent_node = self.getCSVNode(parent_name)
            
            if(parent_node == 0):
                print("couldn't find ", parent_name)
                continue
            
            child_name = duo[1]
            #print(child_name)
            
           
            child_node = self.getCSVNode(child_name)
            
            if(child_node == 0):
                print("couldn't find ", child_name)
                continue
            
            
            parent_node.children.append(child_node)
            
            child_node.parents.append(parent_node)
            
            

        
        
    def assignLevel(self,node,level):
        
        node.level = level
        
        if(len(node.children) == 0):
            return
        
        else:
        
            for child in node.children:
            
                self.assignLevel(child,level + 1)
            
            
            

    def assignLeaf(self,node):
    
            
        if(len(node.children) == 0):
            node.leaf = True
            self.allLeaves_Node.append(node)
            
        else:
            node.leaf = False
            
                
                
    def assignSums(self):
        
        for node in self.allNodes:
            
            self.assignSum(node,node)
        

    def assignSum(self,ognode,currentnode):
        
        if(currentnode.leaf == True):
            #print(ognode.name)
            ognode.sum = ognode.sum + 1
            return 
        
    
        for child in currentnode.children:
        
            self.assignSum(ognode,child)
            
    def assignLineage(self,ognode,node):
        
        ognode.lineage.insert(0,node)
    
        if(len(node.parents) == 0):
    
            return
    
        self.assignLineage(ognode,node.parents[0])
    
    def assignAspectTree(self,aspect_root,node):
        
        node.aspectTree = aspect_root
        
        if(len(node.children) == 0):
            return
        
        for child in node.children:
            
            self.assignAspectTree(aspect_root,child)
        
        
   
        
    def doOutput(self,output_name):
        
        self.setFields()
        
        self.setOutputRows()
        
        self.writeRows(output_name)
        
        
    def setFields(self):
        
        self.outputFields = self.masterLine.copy()
        
        self.outputFields[0] = "CPS_Aspect"
        
        for i in range(1,self.maxLevel):
            self.outputFields[i] = "CPS_Concern"
            
        
        self.outputFields[self.lineLength - 6] = "Level"
        self.outputFields[self.lineLength - 5] = "Pad"
        self.outputFields[self.lineLength - 4] = "To Pad"
        self.outputFields[self.lineLength - 3] = "Sum"
        self.outputFields[self.lineLength - 2] = "Satisfied"
        self.outputFields[self.lineLength - 1] = "Aspect Tree"
        

        
        
        
    
     
    def setOutputRows(self):
        
     
        
        for node in self.allLeaves_Node:


        
            #loop through lineage
            for i in range(len(node.lineage)):
                
                line = self.masterLine.copy()
                #print(i)
                #loop through current node and its lineage
                for j in range(0,i + 1):
                    
                    #print(node.lineage[j].name,end = " ")
                    
                    line[j] = node.lineage[j].name
                    
                    if(j == i):
                        #print(j)
                        currnode = node.lineage[j]
                       # print(str(currnode.level) + " 1 " + "1 " + str(currnode.sum)) 
                        line[self.lineLength - 6] = str(currnode.level)
                        line[self.lineLength - 5] = "1"
                        line[self.lineLength - 4] = "1"
                        line[self.lineLength - 3] = str(currnode.sum)
                        line[self.lineLength - 2] = str(currnode.satisfied)
                        line[self.lineLength - 1] = str(currnode.aspectTree.name)
                        self.outputRows.append(line)    
                        
        for node in self.allLeaves_Node:


        
            #loop through lineage
            for i in range(len(node.lineage)):
                
                line = self.masterLine.copy()
                #print(i)
                #loop through current node and its lineage
                for j in range(0,i + 1):
                    
                    #print(node.lineage[j].name,end = " ")
                    
                    line[j] = node.lineage[j].name
                    
                    if(j == i):
                       # print(j)
                        currnode = node.lineage[j]
                       # print(str(currnode.level) + " 1 " + "1 " + str(currnode.sum)) 
                        line[self.lineLength - 6] = str(currnode.level)
                        line[self.lineLength - 5] = "203"
                        line[self.lineLength - 4] = "203"
                        line[self.lineLength - 3] = str(currnode.sum)
                        line[self.lineLength - 2] = str(currnode.satisfied)
                        line[self.lineLength - 1] = str(currnode.aspectTree.name)
                        self.outputRows.append(line)                     
            
            

        
        
        
        
        
         
    def writeRows(self,out_name):
        
        with open(out_name, 'w',newline = '') as csvfile:  
            # creating a csv writer object  
            csvwriter = csv.writer(csvfile)  
        
        # writing the fields  
            csvwriter.writerow(self.outputFields)  
        
        # writing the data rows  
            csvwriter.writerows(self.outputRows)       
        
        
        
        
            
    def removeRelationless(self):
        
        numremoved = 0
        
        for node in self.allNodes:
            #print("node in remove relationless ",node.name)
            if(len(node.children) == 0 and len(node.parents) == 0):
                
                print("removing 1 ", node.name)
                self.allNodes.remove(node)
                numremoved+=1
        
        for node in self.allLeaves_Node:
            
             if(len(node.children) == 0 and len(node.parents) == 0):
                
                print("removing 2 ", node.name)
                self.allLeaves_Node.remove(node)
                numremoved+=1
                
        for node in self.allAspects_Node:
            
             if(len(node.children) == 0 and len(node.parents) == 0):
                
                print("removing 3 ", node.name)
                self.allAspects_Node.remove(node)
                numremoved+=1
        for node in self.allConcerns_Node:
            
             if(len(node.children) == 0 and len(node.parents) == 0):
                
                print("removing 4 ", node.name)
                self.allConcerns_Node.remove(node)
                numremoved+=1
        
        if(numremoved != 0):
            
            self.removeRelationless()
            
        
            
    def getCSVNode(self,name):
        
         for node in self.allNodes:
             
             if(node.name == name):
                 return node
             
         #print("Couldnt find " + name)
         return 0
            
            
        
 
       
        
        
def exportCSV(input_file_path,output_file_path):
    
    print("loading from ", input_file_path)
    exporter = ASPExporter(input_file_path)
    print("successfully loaded")
    
    #exporter.removeRelationless()
    #for node in exporter.allNodes:
        #print(node.name)
        #print(len(node.children))
        #print(len(node.parents))
        #print(node.aspectTree.name)
        #print()
    
    
    print("exporting to ", output_file_path)
    exporter.doOutput(output_file_path)
    print("successfully exported")
        
       
exportCSV("./SR-01/use_case_2_LKAS_Case_0_after_cyberattack.txt","./SR-01/LKAStest.csv")
        
            
            
            
    

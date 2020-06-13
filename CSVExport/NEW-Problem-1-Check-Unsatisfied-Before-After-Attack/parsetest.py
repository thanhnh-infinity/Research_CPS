import numpy as np
import csv  
from csvNode import csvNode

file = open("simple_nosat_Elevator_after_cyberattack.txt", mode = 'r')
lines = file.readlines()
maxlevel = 3


sep = lines[0].split(" ")

#for x in sep:
#    print(x)
    
    
nodes = np.array(())
edges = []

def get_type(item):
    
    if(item[0] == "a"):
        return "Aspect"
    
    elif(item[0] == "c"):
        return "Concern"

    elif(item[0] == "s"):
        return "Subconcern"
    
    else:
        print("idk")
    
def get_name(item):
    
    substr = ""
    append = False
    
    for i in range(len(item)):
        
        c = item[i]
        
        if(c == ")"):
            break
        
        if(c == "("):
            append = True
            continue
        
        if(append == True):
            substr = substr + c
        
        
        
    return substr

def get_node(name_node,node_list):
    
    for node in node_list:
        
        if(node.name == name_node):
            
            return node
    
    return 0
    

    
def assign_level(node,level):

    node.level = level
    
    if(len(node.children) == 0):
        return
    
    else:
        
        for child in node.children:
            assign_level(child,level + 1)
            
def assign_leaf(node_list):

    for node in node_list:

        if(len(node.children) == 0):
            node.leaf = True
        else:
            node.leaf = False
  

    
def assign_sum(ognode,currentnode):
    
    
    if(currentnode.leaf == True):
        print(ognode.name)
        ognode.sum = ognode.sum + 1
        return 
    
    for child in currentnode.children:
        
        assign_sum(ognode,child)
   
def assign_lineage(ognode,node):
    
    #print("called lineage on " + node.name)
    
    
    ognode.lineage.insert(0,node)
    
    if(len(node.parent) == 0):
    
        return
    
    assign_lineage(ognode,node.parent[0])
    
    
    
        
    

for item in sep:
    
    
    item_type = get_type(item)
    item_name = get_name(item)
    
    if(item_type == "Aspect" or item_type == "Concern"):
        
        newNode = csvNode()
        
        
        newNode.name = item_name
        newNode.type = item_type
        
        nodes = np.append(nodes,newNode)
    
    if(item_type == "Subconcern"):
        
        edge = item_name.split(",")
        
    
        edges.append((edge[0],edge[1]))
        
        
    

for edge in edges:
    
    parent = get_node(edge[0],nodes)
    child = get_node(edge[1],nodes)
    
    parent.children.append(child)
    child.parent.append(parent)
    


aspects = []
leaves = []
for node in nodes:
    
    if(node.type == "Aspect"):
        aspects.append(node)
    
    
        
        
for asp in aspects:

    print("aspect")
    assign_level(asp,1)     
    

assign_leaf(nodes)




for node in nodes:
    #print("leaf "  + leaf.name)
    assign_sum(node,node)
    if(node.leaf == True):
        leaves.append(node)
    
    #lineage = 


    
rows = []




print(leaves, " LEAVES")

for node in leaves:
    
    assign_lineage(node,node)
    
 
for node in leaves:

    #line = np.zeros(7,dtype=str)
    stack = ""
    
    
    #loop through lineage
    for i in range(len(node.lineage)):
        
        line = ["","","","","","",""]
        #print(i)
        #loop through current node and its lineage
        for j in range(0,i+1):
            
            #print(node.lineage[j].name,end = " ")
            
            line[j] = node.lineage[j].name
            
            if(j == i):
                
                currnode = node.lineage[j]
               # print(str(currnode.level) + " 1 " + "1 " + str(currnode.sum)) 
                line[3] = str(currnode.level)
                line[4] = "1"
                line[5] = "1"
                line[6] = str(currnode.sum)
                rows.append(line)


for node in leaves:

    #line = np.zeros(7,dtype=str)
    stack = ""
    
    
    #loop through lineage
    for i in range(len(node.lineage)):
        
        line = ["","","","","","",""]
        #print(i)
        #loop through current node and its lineage
        for j in range(0,i + 1):
            
            #print(node.lineage[j].name,end = " ")
            
            line[j] = node.lineage[j].name
            
            if(j == i):
                print(j)
                currnode = node.lineage[j]
               # print(str(currnode.level) + " 1 " + "1 " + str(currnode.sum)) 
                line[3] = str(currnode.level)
                line[4] = "203"
                line[5] = "203"
                line[6] = str(currnode.sum)
                rows.append(line)            
 
print("ROWS")
print(rows)         
print(len(rows))            
              
            
        

    
# field names  
fields = ['CPS_Aspect', 'CPS_Concern', 'CPS_Property', 'Level','Pad',"To Pad","Sum"]  
    

    
# name of csv file  
filename = "testcsv.csv"
    
# writing to csv file  
with open(filename, 'w',newline = '') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows)       
         
        
        

        
    
    
for node in nodes:
    
    print(node.name)
    print(node.level)
#    print(node.leaf)
#    if(len(node.parent) != 0):
#        print(node.parent[0].name, " parent")
    print(node.sum)
#    print("lineage")
    #for lin in node.lineage:
        #print(lin.name)
    #print(node.lineage)
    #print()
    
    
    




    
    
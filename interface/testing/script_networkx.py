import networkx as nx
import numpy as np
import pygraphviz
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import numpy
from owlready2 import *
my_onto = get_ontology("file://./cpsframework-v3-base.owl").load()





#removes the namespace from an owlr object, turns it into a string
def remove_namespace(in_netx):
   
    in_str = str(in_netx)
    
    leng = len(in_str)
    period = leng
    for i in range(leng):
        if(in_str[i] == '.'):  
            period = i
            break
 
    return in_str[(period + 1):]
    
#recursive function to retrieve all concerns
def get_all_concerns(T,concern,concern_list):
    
    #appends to the total concern list
    concern_list.append(concern)
    
    #recursively calls subconcerns
    for subconcern in concern.includesConcern:
        get_all_concerns(T,subconcern,concern_list)
        
#creates all edges from passed node to its children
def draw_children(G,node):
    
    children = node.includesConcern
        
    for child in children:
        
        G.add_edge(remove_namespace(node),remove_namespace(child),length = 1)
        

def add_properties(G,ontology,property_list,concerns_list,color_map):
    
    impact_rules = ontology.search(type = ontology.ImpactRule)
    
    for ir in impact_rules:
        
        concerns_list.append(ir.addressesConcern[0])
    
    
    for ir in impact_rules:
        
        property_list.append(ir.hasCondition[0].conditionProperty[0])
        
        
        
    #print(property_list)
    #print(concerns_list)
 
    for i in range(len(property_list)):
        
       # if(remove_namespace(property_list[i]) == "Input1ConsistentReadingFreq" or remove_namespace(property_list[i]) == "Input1Modes"):
       #     continue
        
        G.add_node(remove_namespace(property_list[i]))
        
        
        color_map.append("purple")
        
        G.add_edge(remove_namespace(concerns_list[i]),remove_namespace(property_list[i]))
        
    

    
        
        
def draw_ontology(ax,cps_onto):
    

    T = nx.DiGraph()

    all_nodes = []
    addressed_concerns = []
    myproperty_list = []
    
    color_map = []
    shape_map = []
    bbox_map = []

    all_aspects = cps_onto.search(type = cps_onto.Aspect)
    #all_aspects = [cps_onto.Trustworthiness]

    #adds all concerns/aspects into all_nodes
    for aspect in all_aspects:
    
        get_all_concerns(T, aspect, all_nodes)

    #print(all_nodes)

    #adds all nodes into graph
    for node in all_nodes:
        T.add_node(remove_namespace(node))
        
        node_type = remove_namespace(node.is_a[0])
        
        if(node_type == "Aspect"):
            color_map.append("blue")
            shape_map.append("sq")
            
            
        elif(node_type == "Concern"):
            color_map.append("red")
            
    
        
        
    #draws edges between all nodes
    for node in all_nodes:
        
        draw_children(T,node)
    
    add_properties(T,cps_onto,myproperty_list,addressed_concerns,color_map)
    
    #does positioning stuff
    write_dot(T,'test.dot')    
    pos = graphviz_layout(T, prog='dot')#, args = "-Goverlap=scale -Nfixed=true -Nwidth=5 -Nheight=5" )
    
    
    x_pos = np.array(())
    y_pos = np.array(())
    
    #print(pos.keys())
    #i = 0
    for x in pos:
        
        print (pos[x])
        
        position = pos[x]
        
        x_pos = np.append(x_pos,position[0])
        y_pos = np.append(y_pos,position[1])
        
        
        
    xmax = np.max(x_pos)
    ymax = np.max(y_pos)
    
    xmin = np.min(x_pos)
    ymin = np.min(y_pos)
    
    print("maxes")
    print(xmin, " ", xmax)
    print(ymin, " ", ymax)
        #print (pos[x])
        
    
    
    x_pos = np.array(())
    y_pos = np.array(())
    
    
    print(x_pos)
    for x in pos:
    
            lst = list(pos[x])
            lst[0] = lst[0] + 500
            
            pos[x] = tuple(lst)
            
            
    for x in pos:
        
        print(pos[x])
        position = pos[x]
        x_pos = np.append(x_pos,position[0])
        y_pos = np.append(y_pos,position[1])
    
    
    
    xmax = np.max(x_pos)
    ymax = np.max(y_pos)
    
    xmin = np.min(x_pos)
    ymin = np.min(y_pos)
    
    
    print(x_pos)
    
    print("maxes")
    print(xmin, " ", xmax)
    print(ymin, " ", ymax)
               
    
            
        
   

    
    
    plt.tight_layout()
    nx.draw(T, pos, with_labels=True, arrows=True, ax = ax, node_size = .1, font_size = 8,node_shape = "s", bbox=dict(facecolor="blue", edgecolor='black', boxstyle='round,pad=0.2'),font_color = "white",scale = 1)
    
    return xmin, xmax, ymin, ymax
    
fig, ax = plt.subplots(figsize = (10,10))

draw_ontology(ax,my_onto)



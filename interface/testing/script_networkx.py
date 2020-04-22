import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import numpy
from owlready2 import *
my_onto = get_ontology("file://./cpsframework-v3-base.owl").load()


print(my_onto.search(iri = "*Trustworthiness"))


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
        
        G.add_edge(remove_namespace(node),remove_namespace(child))
        

    
    
    
    
        
        
def draw_ontology(ax,cps_onto):
    

    T = nx.DiGraph()

    all_nodes = []

    #all_aspects = cps_onto.search(type = cps_onto.Aspect)
    all_aspects = [cps_onto.Trustworthiness]

    #adds all concerns/aspects into all_nodes
    for aspect in all_aspects:
    
        get_all_concerns(T, aspect, all_nodes)

    print(all_nodes)

    #adds all nodes into graph
    for node in all_nodes:
        T.add_node(remove_namespace(node))
        
    #draws edges between all nodes
    for node in all_nodes:
        
        draw_children(T,node)
    
    #does positioning stuff
    write_dot(T,'test.dot')    
    pos =graphviz_layout(T, prog='dot') 
    


    nx.draw(T, pos, with_labels=True, arrows=True, ax = ax, node_size = 1, font_size = 14)
    
fig, ax = plt.subplots()

draw_ontology(ax,my_onto)
    





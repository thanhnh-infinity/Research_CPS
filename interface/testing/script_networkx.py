import networkx as nx
import numpy as np
import pygraphviz
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import numpy
from owlready2 import *
#my_onto = get_ontology("file://./cpsframework-v3-base.owl").load()



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
    
#recursive function to retrieve all concerns, puts them in concern_list
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
        

#adds properties to the graph by finding all impact rules, finding the concern they address, then the property they are connected to 
def add_properties(G,ontology,property_list):
    
    concerns_list = []
    
    impact_rules = ontology.search(type = ontology.ImpactRule)
    
    for ir in impact_rules:
        
        concerns_list.append(ir.addressesConcern[0])
    
    
    for ir in impact_rules:
        
        property_list.append(remove_namespace(ir.hasCondition[0].conditionProperty[0]))
        
        
    for i in range(len(property_list)):
           
        G.add_node(property_list[i])
        
        G.add_edge(remove_namespace(concerns_list[i]),property_list[i])
      
         
def draw_ontology(ax,cps_onto,fs):
    
    ax.axis('off')
        
    T = nx.DiGraph()

    all_nodes = []
    all_concerns = []
    myproperty_list = []
    
    


    all_aspects = cps_onto.search(type = cps_onto.Aspect)
    #all_aspects = [cps_onto.Trustworthiness]

    #adds all concerns/aspects into all_nodes
    for aspect in all_aspects:
    
        get_all_concerns(T, aspect, all_nodes)

    #adds all nodes into graph
    for node in all_nodes:
        T.add_node(remove_namespace(node))
        
        node_type = remove_namespace(node.is_a[0])

    #draws edges between all concerns
    for node in all_nodes:
        
        draw_children(T,node)
    
    #adds all properties and their edges to graph
    add_properties(T,cps_onto,myproperty_list)
    
    #let graphviz handle creating tree structure
    pos = graphviz_layout(T, prog='dot')
    
    #don't want negative position values, so add 500 to all x's, 100 to all y's
    for x in pos:
    
            lst = list(pos[x])
            lst[0] = lst[0] + 500
            lst[1] = lst[1] + 100
            
            pos[x] = tuple(lst)
      
    #find x,y mins and maxes for gui graphing purposes
    x_pos = np.array(())
    y_pos = np.array(())
                       
    for x in pos:
        
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
               
    #sort the concerns 
    for node in all_nodes:
        all_concerns.append(remove_namespace(node))
   
    sorted_concerns = sorted(all_concerns, key=lambda x:x.upper())
    
    plt.tight_layout()
    #nx.draw(T, pos, with_labels=True, arrows=True, ax = ax, node_size = .1, font_size = fs,node_shape = "s", bbox=dict(facecolor="#737373", boxstyle='round,pad=0.2'),font_color = "white",scale = 1)
    
    #draw all of the nodes, with no labels
    nx.draw_networkx_nodes(T, pos, with_labels=False, arrows=False, ax = ax, node_size = .1,scale = 1)
    #draw all of the edges
    nx.draw_networkx_edges(T, pos, arrows=False)
    
    #draw all of the concerns with one color, the properties with another
    labels = {}
    
    for concern in sorted_concerns:
        labels[concern] = concern
        
    nx.draw_networkx_labels(T,pos,labels,font_size=fs,bbox=dict(facecolor="#737373", boxstyle='round,pad=0.2'),font_color = "white")   
    

    labels = {}
    
    for myproperty in myproperty_list:
        
        labels[myproperty] = myproperty
        
    nx.draw_networkx_labels(T,pos,labels,font_size=fs,bbox=dict(facecolor="red", boxstyle='round,pad=0.2'),font_color = "white") 
    
    
    
    return xmin, xmax, ymin, ymax, sorted_concerns
    
#fig, ax = plt.subplots(figsize = (10,10))

#draw_ontology(ax,my_onto,8)



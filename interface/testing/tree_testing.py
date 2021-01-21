import networkx as nx
import numpy as np

from owlNode import owlNode

from networkx.drawing.nx_agraph import write_dot, graphviz_layout

G = nx.DiGraph()

nodes = ["1","2","3","4"]#,"5","6","7","8","9","10","11","12"]
owlNodes = []

for node in nodes:
    
    
    newNode = owlNode()
    newNode.name = node
    owlNodes.append(newNode)
    
    G.add_node(node)

G.add_edge("1","2")
G.add_edge("1","3")
G.add_edge("1","4")

#G.add_edge("4","5")
#G.add_edge("4","6")
#G.add_edge("4","7")

#G.add_edge("6","8")
#G.add_edge("6","9")

#G.add_edge("3","10")
#G.add_edge("3","11")
#G.add_edge("11","12")

pos = graphviz_layout(G,prog = "dot")




def graphviz_layout_with_rank(G, prog = "neato", root = None, sameRank = [], args = ""):
    ## See original import of pygraphviz in try-except block
    try:
        import pygraphviz
    except ImportError:
        raise ImportError('requires pygraphviz ',
                          'http://pygraphviz.github.io/')
    ## See original identification of root through command line
        
    if root is not None:
        args += f"-Groot={root}"
        
        
    A = nx.nx_agraph.to_agraph(G)
    for sameNodeHeight in sameRank:
        if type(sameNodeHeight) == str:
            print("node \"%s\" has no peers in its rank group" %sameNodeHeight)
        A.add_subgraph(sameNodeHeight, rank="same")
    A.layout(prog=prog, args=args)
    ## See original saving of each node location to node_pos 
    
    node_pos = {}
    for n in G:
        node = pygraphviz.Node(A, n)
        try:
            xs = node.attr["pos"].split(',')
            node_pos[n] = tuple(float(x) for x in xs)
        except:
            print("no position for node", n)
    return node_pos


pos=graphviz_layout_with_rank(G, prog='dot',sameRank=[["1","3"]])
nx.draw(G,pos = pos,with_labels = True)
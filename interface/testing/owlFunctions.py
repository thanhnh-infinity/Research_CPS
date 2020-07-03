from parse import *
import networkx as nx



def is_asp_or_conc(mytype):
    
    if(not (mytype == "Concern" or mytype == "Aspect") ):
        return False
    else:
        return True
    
def remove_namespace(in_netx):

    in_str = str(in_netx)

    leng = len(in_str)
    period = leng
    for i in range(leng):
        if(in_str[i] == '.'):
            period = i
            break

    return in_str[(period + 1):]


def remove_ir(in_netx):
    
   
    in_str = str(in_netx) + " "
    parsed_name = ''.join(r[0] for r in findall("#{} ", in_str))
        
    if(parsed_name == ""):
        return remove_namespace(in_netx)
    
    
    #print("reduced name from " + str(in_netx) + " to " + parsed_name)
    return parsed_name
    
    
#from https://stackoverflow.com/questions/15353087/programmatically-specifying-nodes-of-the-same-rank-within-networkxs-wrapper-for
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
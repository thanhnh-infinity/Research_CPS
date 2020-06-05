
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt


G = nx.Graph()

G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8)
G.add_node(9)
G.add_node(10)
G.add_node(11)
G.add_node(12)
G.add_node(13)


G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,4)
G.add_edge(2,5)

G.add_edge(4,11)
G.add_edge(4,12)
G.add_edge(4,13)

G.add_edge(6,7)
G.add_edge(6,8)
G.add_edge(8,9)
G.add_edge(8,10)

pos = graphviz_layout(G, prog='dot')

xs = []
ys = []
titles = []
labels = []
nodes = []
vals = []
edges = []

i = 1
for d in pos:
    
    print(pos[d])
    xs.append(pos[d][0])
    ys.append(pos[d][1])
    titles.append("Node " + str(i))
    labels.append(str(i))
    nodes.append(i)
    vals.append(1)
    i +=1


def onClick():
    print("clicked")

fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', onClick)
nx.draw(G,ax = ax, pos = pos, with_labels = True)



import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from owlNode import owlNode
from script_networkx import remove_namespace
from owlready2 import *
from networkx.drawing.nx_agraph import write_dot, graphviz_layout



owl = get_ontology("file://./" + "cpsframework-v3-base.owl").load()

all_concerns = np.asarray(owl.search(type = owl.Concern))

print(all_concerns)
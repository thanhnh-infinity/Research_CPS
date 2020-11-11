
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from owlNode import owlNode
from script_networkx import remove_namespace
from owlready2 import *
from networkx.drawing.nx_agraph import write_dot, graphviz_layout



owl = get_ontology("file://./application_ontologies/cpsframework-v3-sr-LKAS-Configuration-V2" + ".owl").load()


props = np.asarray(owl.search(type =  owl.Property))
forms = np.asarray(owl.search(type =  owl.Formula))
decomps = np.asarray(owl.search(type = owl.DecompositionFunction))


form = owl.Authorization_Condition

print(form)

print(form.is_a)


#print(len(props))
#print(len(forms))

#alpha = owl.Property("alpha",ontology = owl)
#bravo = owl.Property("bravo",ontology = owl)
#charles = owl.Property("charles",ontology = owl)

#alpha.is_a.append(owl.Formula)
#bravo.is_a.append(owl.Formula)
#charles.is_a.append(owl.Formula)

#alpha.propertyAddConcern.append(owl.Concern("Network", ontology = owl))
#bravo.propertyAddConcern.append(owl.Network)
#charles.propertyAddConcern.append(owl.Network)

#new_conj = owl.Conjunction("testConj",ontology = owl)

#new_func = owl.DecompositionFunction("testDecompFunc",ontology = owl)
#new_func.is_a.append(owl.Disjunction)
#new_func.includesMember.append(bravo)
#new_func.includesMember.append(charles)
#new_func.memberOf.append(new_conj)


#new_conj.formulaAddConcern.append(owl.Concern("Network", ontology = owl))
#new_conj.includesMember.append(alpha)
#new_conj.includesMember.append(new_func)

#alpha.memberOf.append(new_conj)
#bravo.memberOf.append(new_func)
#charles.memberOf.append(new_func)
#x = forms[34]

#print(x.memberOf)



owl.save(file = "./condtest.owl",format = "rdfxml")
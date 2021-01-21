from owlFunctions import hierarchy_pos
import owlGraph



testOwlOntology = owlBase("cpsframework-v3-base.owl")

testOwlOntology.initializeOwlNodes()

testOwlGraph = owlGraph(testOwlOntology)

fig, ax = plt.subplots(figsize = (15,15))

testOwlGraph.draw_graph(ax,10)
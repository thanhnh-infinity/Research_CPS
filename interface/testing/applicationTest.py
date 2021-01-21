from owlready2 import *
import numpy as np
from owlFunctions import remove_namespace

filename = "./application_ontologies/cpsframework-v3-sr-Elevator-Configuration.owl"

app = get_ontology("file://./" + filename).load()

base = get_ontology("file://./" + "cpsframework-v3-base.owl").load()

#print(list(app.individuals()))

newcomp = app.Component("newComponent",ontology = app)

newcomp.relateToProperty.append(app.Moving_Down)


maint = app.search_one(iri = "*Maintenance_Regularly")
conc = app.search_one(iri = "*Human_Safety*")

#print("\n\n")
print(list(app.different_individuals()))


print(maint)
print(conc)


maint.addConcern.append(app.Concern("newconcern",ontology = app))

maint.addConcern.remove(app.Concern("Controllability",ontology = app))


app.save(file = "applicationtesting.owl",format = "rdfxml")
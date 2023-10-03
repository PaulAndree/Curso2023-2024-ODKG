# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16oqP_oDEXD5qtMAwl0vRv9X69yTITIjB

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery

# 1) RDFLib
print("---RDFLib---")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
    print(s)


# 2) SPARQL
print("---SPARQL---")

q1 = prepareQuery('''
    SELECT ?subClass
    WHERE {
        ?subClass rdfs:subClassOf ns:LivingThing .
    }
    ''',
    initNs={"rdfs": RDFS, "ns": ns}
)
for r in g.query(q1):
  print(r.subClass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO

# 1) RDFLib
print("---RDFLib---")
ns = Namespace("http://somewhere#")

#Individuals of Person
for s,p,o in g.triples((None,RDF.type,ns.Person)):
  print(s)

print("-------")

#Individuals of Person + individuals of subclassesof Person
for s,p,o in g.triples((None,RDF.type,ns.Person)):
  print(s)
for sub_class, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s, p1, o1 in g.triples((None, RDF.type, sub_class)):
        print(s)


# 2) SPARQL
print("---SPARQL---")
#Individuals of Person
q2a = prepareQuery('''
    SELECT ?i
    WHERE {
        {
          ?i rdf:type ns:Person.
        }
    }
    ''',
    initNs={"rdf": RDF, "rdfs": RDFS, "ns": ns}
)
for r in g.query(q2a):
  print(r.i)

print("-------")

#Individuals of Person + individuals of subclassesof Person
q2b = prepareQuery('''
    SELECT ?i
    WHERE {
        {
          ?i rdf:type ns:Person.
        }
        UNION
        {
          ?i rdf:type ?subClass.
          ?subClass rdfs:subClassOf ns:Person
        }
    }
    ''',
    initNs={"rdf": RDF, "ns": ns}
)
for r in g.query(q2b):
  print(r.i)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
# Visualize the results

# 1) RDFLib
print("---RDFLib---")
ns = Namespace("http://somewhere#")

#Individuals of Person
for s,p,o in g.triples((None,RDF.type,ns.Person)):
  print(s)
for s,p,o in g.triples((None,RDF.type,ns.Animal)):
  print(s)

print("----------")

# 2) SPARQL
print("---SPARQL---")

q3 = prepareQuery('''
    SELECT ?x
    WHERE {
        {
          ?x rdf:type ns:Person .
        }
        UNION
        {
          ?x rdf:type ns:Animal .
        }
    }
    ''',
    initNs={"rdf": RDF, "rdfs": RDFS, "ns": ns}
)
for r in g.query(q3):
  print(r.x)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
from rdflib.namespace import FOAF


# 1) RDFLib
ns = Namespace("http://somewhere#")


print("---RDFLib---")
for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
        print(s)

print("---SPARQL---")

# 2) SPARQL
q4 = prepareQuery('''
    SELECT DISTINCT ?x
    WHERE {
        {
          ?x foaf:knows ns:RockySmith .
        }
    }
    ''',
    initNs={"rdf": RDF, "rdfs": RDFS, "ns": ns, "foaf":FOAF}
)
for r in g.query(q4):
  print(r.x)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
# Visualize the results

# 2) SPARQL
print("---SPARQL---")
q5 = prepareQuery('''
    SELECT ?entity
    WHERE {
      ?entity foaf:knows ?person1 .
      ?entity foaf:knows ?person2 .
      FILTER (?person1 != ?person2)
    }
    GROUP BY ?entity
    HAVING (COUNT(?person1) >= 2)
    ''',
    initNs={"rdf": RDF, "rdfs": RDFS, "ns": ns, "foaf":FOAF}
)
for r in g.query(q5):
  print(r.entity)
# set TEST=True to test rdflib without HEX
TEST=False

if not TEST:
  import dlvhex
import rdflib
import sys

def escape(v):
  # dlvhex does not process UTF8
  #if isinstance(v,unicode):
  #  raise Exception("found unicode "+repr(v))
  s = str(v)
  if '\\' in s or '"' in s:
    raise Exception("escape issue: "+repr(v))
  s = '"'+s+'"'
  #sys.stderr.write(s+'\n')
  return s

def concat(strs):
  needquote = any(['"' in s for s in strs])
  unquoted = [s.strip('"') for s in strs]
  result = ''.join(unquoted)
  if needquote:
    result = '"'+result+'"'
  dlvhex.output((result,))

def rdf(url):
  '''
  input: URL
  outputs: S P O of all RDF triples found at URL
  '''
  g = rdflib.Graph()
  uri = url.value().strip('"')
  sys.stderr.write("retrieving "+uri+"\n")
  g.parse(uri)
  triplecount = 0
  badcount = 0
  for triple in g.triples((None,None,None)):
    #sys.stderr.write(repr(triple)+'\n')
    try:
      dlvhex.output(tuple([ escape(v) for v in triple]))
      triplecount += 1
    except:
      # ignore failures in conversion
      badcount += 1
      pass
  sys.stderr.write('returned {} triples and ignored {} triples\n'.format(triplecount, badcount))

def register():
	prop = dlvhex.ExtSourceProperties()
	prop.addFiniteOutputDomain(0)
	prop.addFiniteOutputDomain(1)
	prop.addFiniteOutputDomain(2)
	dlvhex.addAtom("rdf", (dlvhex.CONSTANT,), 3, prop)
	prop = dlvhex.ExtSourceProperties()
	prop.addFiniteOutputDomain(0)
	dlvhex.addAtom("concat", (dlvhex.TUPLE,), 1, prop)

def testrdflib():
  URL = 'http://njh.me/foaf.rdf'
  #URL = 'file:///home/ps/Downloads/njh.foaf.rdf'

  g = rdflib.Graph()
  g.parse(URL)
  for s, o, p in g.triples((None,None,None)):
    print repr([s, o, p])

if TEST:
  testrdflib()

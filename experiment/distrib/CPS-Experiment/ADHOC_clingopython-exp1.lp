#script (python)
import shlex
import clingo
from subprocess import Popen, PIPE

F = clingo.Function

#Finds answer set from query for subject and object from just predicate	
def qSUBOBJ(data, predicate):

    dataString = data.string
    predicateString = predicate.string
    
    queryString = "SELECT ?x ?y \nWHERE\n { ?x <" + predicateString + "> ?y }\n"
    queryFile = open("querytemp.rq","w+")
    queryFile.write(queryString)
    queryFile.close()
    
    cmd = "sparql --data=" + dataString + " --query=querytemp.rq"
    process = Popen(shlex.split(cmd), stdout=PIPE, shell=True)
    output, err = process.communicate()
    exit_code = process.wait()
	
    list = output.decode('utf8')  #LOOK INTO
    splitList = list.splitlines()  #LOOK INTO
    finalList = []
	 
    for z in splitList:
        if ( len(z) != 0 and z[0] == "|"):
            zsplit = z.split("|")
            xstrip = zsplit[1].strip()
            ystrip = zsplit[2].strip()
            if(xstrip != "x" and ystrip != "y" and xstrip != "" and ystrip != ""):
                finalList.append(F("a",[xstrip,ystrip]))

    return finalList
		
#def g(c, f):
#	n = c.name
#	r = F(n, f.arguments)
#	return r

#end.

% --------------------------------------------
% Input extraction
% --------------------------------------------

xrel1(@qSUBOBJ(R,"http://www.semanticweb.org/hashowl#def3146364d5c003c703a3f479c21fa44c4d59e4dce980409922cff2e41d400fd")) :- ontology(R).
xt(@qSUBOBJ(R,"http://www.w3.org/1999/02/22-rdf-syntax-ns#type")) :- ontology(R).
xs(@qSUBOBJ(R,"http://www.w3.org/2000/01/rdf-schema#subClassOf")) :- ontology(R).

rel1(X,Y) :- xrel1(a(X,Y)).
t(X,Y) :- xt(a(X,Y)).
s(X,Y) :- xs(a(X,Y)).

ontology("part1.owl").
%ontology("part2.owl").
%ontology("part3.owl").
%ontology("part4.owl").	

p(I) :- t(I,_).

-rel2(X,Y2) :-
	rel2(X,Y1),
	rel1(_,Y1),
	rel1(_,Y2),
	Y1 != Y2.

rel2(X,Y) :-
	rel1(X,Y).

rel2(X,Y) :-
	t(X,Y),
	rel2(Y,Y),
	not -rel2(X,Y).

rel2(X,Y) :-
	s(X,Y),
	rel2(Y,Y),
	not -rel2(X,Y).

output_headings("a","b").

output(X,Y) :-
	p(X),
	rel2(X,Y).

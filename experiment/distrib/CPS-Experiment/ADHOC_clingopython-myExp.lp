#script (python)
import shlex
import clingo
import subprocess
from subprocess import Popen, PIPE

F = clingo.Function

#Finds answer set from query for subject and object from just predicate	
def qSUBOBJ(data, predicate):

    dataString = data.string
    predicateString = predicate.string

    if (predicateString == "all"):
        queryString = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
    else:
        queryString = "SELECT ?x ?y \nWHERE\n { ?x <" + predicateString + "> ?y }\n"
    
    queryFile = open("querytemp.rq","w+")
    queryFile.write(queryString)
    queryFile.close()
    
    cmd = "/home/thanhnh/All_Workspace/Java_Workspace/CPS/src/asklab/cpsf/apache-jena-3.0.0/bin/sparql --data=" + dataString + " --query=querytemp.rq"
    
    #process = Popen(shlex.split(cmd), stdout=PIPE, shell=True)

    process = subprocess.Popen(['/home/thanhnh/All_Workspace/Java_Workspace/CPS/src/asklab/cpsf/apache-jena-3.0.0/bin/sparql','--data=' + dataString,'--query=querytemp.rq'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output, err = process.communicate()
    exit_code = process.wait()


    #list = output.decode('utf8')  #LOOK INTO
    list = output
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

# Query whole CPS Ontology to generate input/3
def qRDFTriple(data,kind):
    dataString = data.string
    kindString = kind.string
    
    #queryString = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
    if (kindString == "all"):
        queryString = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
    else:
        queryString = "SELECT ?s ?p ?o WHERE { ?s <" + kindString + "> ?o }"
    
    #print(queryString)

    queryFile = open("querytemp.rq","w+")
    queryFile.write(queryString)
    queryFile.close()

    cmd = "/home/thanhnh/All_Workspace/Java_Workspace/CPS/src/asklab/cpsf/apache-jena-3.0.0/bin/sparql --data=" + dataString + " --query=querytemp.rq"

    process = subprocess.Popen(['/home/thanhnh/All_Workspace/Java_Workspace/CPS/src/asklab/cpsf/apache-jena-3.0.0/bin/sparql','--data=' + dataString,'--query=querytemp.rq'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output, err = process.communicate()
    exit_code = process.wait()

    #list = output.decode('utf8')  #LOOK INTO
    #print(output)
    list = output
    splitList = list.splitlines()  #LOOK INTO
    finalList = []
	
    for z in splitList:
        #print(z)
        if ( len(z) != 0 and z[0] == "|"):
            zsplit = z.split("|")
           
            xstrip = zsplit[1].strip() #subject
            ystrip = zsplit[2].strip() #predicate
            ostrip = zsplit[3].strip() #object

            if (kindString == "all"):
                if(xstrip != "s" and ystrip != "p" and ostrip != "o" and xstrip != "" and ystrip != "" and ostrip != ""):
                    finalList.append(F("triple",[xstrip,ystrip,ostrip]))
            else:
                if(xstrip != "s" and ystrip != "p" and ostrip != "o" and xstrip != "" and ostrip != ""):
                    finalList.append(F("triple",[xstrip,kindString,ostrip]))
                

    return finalList

#end.

% --------------------------------------------
% Input extraction
% --------------------------------------------
% Dr Marcello Ontology
%ontology("part1.owl").
%ontology("part2.owl").
%ontology("part3.owl").
%ontology("part4.owl").	

ontology("./Phylotastic/cdao_phylotastic.owl").
ontology("./Phylotastic/mao.owl").
ontology("./Phylotastic/mygrid-moby-service.owl").
ontology("./Phylotastic/mygrid-ontology.owl").
ontology("./Phylotastic/phylogenetic_methods.owl").


%thanhrel(@qRDFTriple(R,"all")) :- ontology(R).

thanhrel(@qRDFTriple(R,"http://www.semanticweb.org/hashowl#def3146364d5c003c703a3f479c21fa44c4d59e4dce980409922cff2e41d400fd")) :- ontology(R).
thanhrel(@qRDFTriple(R,"http://www.w3.org/1999/02/22-rdf-syntax-ns#type")) :- ontology(R).
thanhrel(@qRDFTriple(R,"http://www.w3.org/2000/01/rdf-schema#subClassOf")) :- ontology(R).


input(X,Y,Z) :- thanhrel(triple(X,Y,Z)).

#show input/3.

%%%%%% Time Report %%%%%%%%%
%%%%% GET ALL %%%%%%%%%%%%%%
% part1.owl                    : 1.370s
% part1 + part2                : 2.435s
% part1 + part2 + part3        : 3.519s
% part1 + part2 + part3 + par4 : 24.654s
% CDAO + phylotastic           : 7.022s

%%%% GET WITH CONDITIONS : Anou + Type + SubClassOf %%%%
% part1.owl                    : 3.389s
% part1 + part2                : 6.561s
% part1 + part2 + part3        : 9.859s
% part1 + part2 + part3 + par4 : 32.290s
% CDAO + phylotastic           : 18.018s
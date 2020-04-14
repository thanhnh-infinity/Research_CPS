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
def qRDFTriple(data):
    dataString = data.string
    queryString = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
    queryFile = open("querytemp.rq","w+")
    queryFile.write(queryString)
    queryFile.close()

    cmd = "/home/thanhnh/All_Workspace/Java_Workspace/CPS/src/asklab/cpsf/apache-jena-3.0.0/bin/sparql --data=" + dataString + " --query=querytemp.rq"

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
           
            xstrip = zsplit[1].strip() #subject
            ystrip = zsplit[2].strip() #predicate
            ostrip = zsplit[3].strip() #object

            if(xstrip != "x" and ystrip != "y" and xstrip != "" and ystrip != ""):
                finalList.append(F("triple",[xstrip,ystrip,ostrip]))

    return finalList

#end.

% --------------------------------------------
% Input extraction
% --------------------------------------------
ontology("cpsframework-v3-base.owl").
thanhrel(@qRDFTriple(R)) :- ontology(R).
input(X,Y,Z) :- thanhrel(triple(X,Y,Z)).

#show input/3.

% Time : 1.939s
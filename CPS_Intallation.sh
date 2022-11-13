#Starting
#!/bin/sh
if type -p java; then
    echo found java executable in PATH
    _java=java
elif [[ -n "$JAVA_HOME" ]] && [[ -x "$JAVA_HOME/bin/java" ]];  then
    echo found java executable in JAVA_HOME     
    _java="$JAVA_HOME/bin/java"
else
    echo "You don't have java in your machine. Please install it. On MacOS: Install from Oracle websiet, On Linux: sudo apt-get install java"
fi

if [[ "$_java" ]]; then
    version=$("$_java" -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo version "$version"
    if [[ "$version" > "1.5" ]]; then
        if type -p git; then
           git --version
           java -version
           javac -version
           javac -d bin/ -cp src src/asklab/querypicker/QueryPicker.java
           javac -d bin/ -cp src src/asklab/cpsf/CPSReasoner.java
           cp ./src/asklab/querypicker/dump.sparql ./bin/asklab/querypicker
           cp -r ./src/asklab/querypicker/QUERIES ./bin/asklab/querypicker/
           cp -r ./src/asklab/cpsf/clingo-4.4.0 ./bin/asklab/cpsf/
           cp -r ./src/asklab/cpsf/dlv ./bin/asklab/cpsf/
           cp -r ./src/asklab/cpsf/mkatoms ./bin/asklab/cpsf/
           cp -r ./src/asklab/cpsf/apache-jena-3.0.0 ./bin/asklab/cpsf/
           cp ./src/asklab/cpsf/runjena.bat ./bin/asklab/cpsf/
           cp ./src/asklab/cpsf/runjena.sh ./bin/asklab/cpsf/
           cp ./src/asklab/cpsf/version.txt ./bin/asklab/cpsf/ 
           echo "----- Done : Install CPS successfully ----- "
           echo "Using command: $ ./runCPS.sh to run the application"
        else
           echo "You don't have GIT in your machine. Please install GIT. On MacOS : brew install git, On Linux: sudo apt-get install git"
        fi
    else         
        echo version is less than 1.5
    fi
else
    echo No java
fi

#How to run

##Step 1 : Build the bin/asklab/querypicker

###Command : javac -d bin/ -cp src src/asklab/querypicker/QueryPicker.java

###Command : javac -d bin/ -cp src src/asklab/cpsf/CPSReasoner.java

##Step 2 : Copy file dump.sparql from <your_root_folder_project>/src/asklab/querypicker/dump.sparql to <your_root_folder_project>/bin/asklab/querypicker/

###Command : cp <your_root_folder_project>/src/asklab/querypicker/dump.sparql <your_root_folder_project>/bin/asklab/querypicker/

Example: cp ./src/asklab/querypicker/dump.sparql ./bin/asklab/querypicker

##Step 3 : Copy folder QUERIES from <your_root_folder_project>/src/asklab/querypicker/ to <your_root_folder_project>/bin/asklab/querypicker/

###Command : cp -r <your_root_folder_project>/src/asklab/querypicker/QUERIES <your_root_folder_project>/bin/asklab/querypicker/

Example: cp -r ./src/asklab/querypicker/QUERIES ./bin/asklab/querypicker/

###( I don't know how the best for this command, but if you have problem, you can copy manually an folder QUERIES to the destination directory)

##Step 4 : Copy some folders for cpsf

###Folder clingo-4.4.0 : cp -r <your_root_folder_project>/src/asklab/cpsf/clingo-4.4.0 <your_root_folder_project>/bin/asklab/cpsf/ 

Example: cp -r ./src/asklab/cpsf/clingo-4.4.0 ./bin/asklab/cpsf/ 

###Folder dlv : cp -r <your_root_folder_project>/src/asklab/cpsf/dlv <your_root_folder_project>/bin/asklab/cpsf/ 

Example: cp -r ./src/asklab/cpsf/dlv ./bin/asklab/cpsf/ 

###Folder mkatoms : cp -r <your_root_folder_project>/src/asklab/cpsf/mkatoms <your_root_folder_project>/bin/asklab/cpsf/ 

Example: cp -r ./src/asklab/cpsf/mkatoms ./bin/asklab/cpsf/ 

###Folder apache-jena-3.0.0 : cp -r <your_root_folder_project>/src/asklab/cpsf/apache-jena-3.0.0 <your_root_folder_project>/bin/asklab/cpsf/

Example: cp -r ./src/asklab/cpsf/apache-jena-3.0.0 ./bin/asklab/cpsf/ 

##Step 5 : Copy some files for cpsf

###runjena.bat : cp <your_root_folder_project>/src/asklab/cpsf/runjena.bat <your_root_folder_project>/bin/asklab/cpsf/ 

Example: cp ./src/asklab/cpsf/runjena.bat ./bin/asklab/cpsf/

###runjena.sh : cp <your_root_folder_project>/src/asklab/cpsf/runjena.sh <your_root_folder_project>/bin/asklab/cpsf/ 

Example: cp ./src/asklab/cpsf/runjena.sh ./bin/asklab/cpsf/

###version.txt : cp <your_root_folder_project>/src/asklab/cpsf/version.txt <your_root_folder_project>/bin/asklab/cpsf/

Example: cp ./src/asklab/cpsf/version.txt ./bin/asklab/cpsf/

##Step 4 : Running

###/Library/Java/JavaVirtualMachines/jdk-11.0.12.jdk/Contents/Home/bin/java -Dfile.encoding=UTF-8 -classpath <your_root_folder_project>/CPS_Project/bin asklab.querypicker.QueryPicker

Example: java -Dfile.encoding=UTF-8 -classpath ./bin asklab.querypicker.QueryPicker

<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.asklab.tk/ontologies/CPS-Framework#"
     xml:base="http://www.asklab.tk/ontologies/CPS-Framework"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:CPS-Framework="http://www.asklab.tk/ontologies/CPS-Framework#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
     <owl:Ontology rdf:about="http://www.asklab.tk/ontologies/CPS-Framework"/>


     <owl:Class rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Concern">

     </owl:Class>

     <owl:Class rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Component">

     </owl:Class>



    <!-- http://www.asklab.tk/ontologies/CPS-Framework#addConcern -->
    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#addConcern">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Concern"/>
    </owl:ObjectProperty>

    <!-- http://www.asklab.tk/ontologies/CPS-Framework#memberOf -->
    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#memberOf">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Formulas"/>
    </owl:ObjectProperty>

    <!-- http://www.asklab.tk/ontologies/CPS-Framework#addressToFunc -->
    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#addressToFunc">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Formulas"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#DecompositionFunction"/>
    </owl:ObjectProperty>

    <!-- http://www.asklab.tk/ontologies/CPS-Framework#confComponent -->
    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#confComponent">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component_Property"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
    </owl:ObjectProperty>

    <!-- http://www.asklab.tk/ontologies/CPS-Framework#confProperty -->
    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#confProperty">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component_Property"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
    </owl:ObjectProperty>


    <!-- http://www.asklab.tk/ontologies/CPS-Framework#positiveImpactTo -->
    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#positiveImpactTo">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component_Property"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Concern"/>
    </owl:ObjectProperty>

    <owl:ObjectProperty rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#relateToProperty">
        <rdfs:domain rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
        <rdfs:range rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
    </owl:ObjectProperty>


    <!-- Design Formulas -->
    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#g1">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Formulas"/>
        <addressToFunc rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Sign_In_Func"/>
    </owl:NamedIndividual>


    <!-- Design Components -->
    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#CP">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Maintenance_Regularly"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Communicate_With_Other_Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Send_Actions"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#ER">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Control_Speed"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Send_Actions"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Communicate_With_Other_Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Maintenance_Regularly"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Detect_Up_11"/>
    </owl:NamedIndividual>


    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#PF">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Maintenance_Regularly"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Control_Speed"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Control_Pulley"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Pulley_Release"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Pulley_Clench"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Communicate_With_Other_Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Send_Actions"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#EC">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Maintenance_Regularly"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Control_Speed"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Halting"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Moving_Up"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Moving_Down"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Communicate_With_Other_Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Control_Moving"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Send_Actions"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#ESCam">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Flash_Warning"/>
	      <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Send_Actions"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Communicate_With_Other_Component"/>
        <relateToProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Detect_Up_11"/>
    </owl:NamedIndividual>


    <!-- Desing Properties and Its actions -->
    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Maintenance_Regularly">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Controllability"/>
	      <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Frequency"/>
        </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Control_Speed">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Controllability"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Human_Safety"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Flash_Warning">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Send_Actions">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Functional_Stability"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Control_Pulley">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Functional_Stability"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Pulley_Release">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Pulley_Clench">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Halting">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Moving_Up">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Moving_Down">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Integrity"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Control_Moving">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Functional_Stability"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Communicate_With_Other_Component">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Availability"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Functional_Stability"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Manageability"/>
    </owl:NamedIndividual>

    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#Detect_Up_11">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Property"/>
        <addConcern rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Manageability"/>
    </owl:NamedIndividual>



    <!-- Design possible impact compoennt-property to a concern -->
    <!-- SAM -->
    <!--
    <owl:NamedIndividual rdf:about="http://www.asklab.tk/ontologies/CPS-Framework#pos_imp_sam_data_encrypted">
        <rdf:type rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Component_Property"/>
        <confComponent rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#SAM"/>
        <confProperty rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Data_Encrypted"/>
        <positiveImpactTo rdf:resource="http://www.asklab.tk/ontologies/CPS-Framework#Encryption"/>
    </owl:NamedIndividual>
    -->



</rdf:RDF>

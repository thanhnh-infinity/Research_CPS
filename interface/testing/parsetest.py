from parse import *
import numpy as np
import re
from owlFormula import owlFormula



#LHS_text = "((willy and timmy) and (jim and (tim and bill)))"

#LHS_text = "(sam and chris and john and (tim and (bill and george)))"



def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])
            



def contains_nested(in_line):
    
    #doesnt have a ( and a )
    if(in_line.find(")") != -1 and in_line.find("(") != -1):
        
        return True
    
    elif(in_line.find(")") != -1 or in_line.find("(") != -1):
        
        
        
        return False
    
    else:
        return False
    
def get_nonnested_members(in_line):
    
    searcher = "(" + in_line + ")"
    
    if(in_line.find("and") != -1):
        
        op = "and"
        
    elif(in_line.find("or") != -1):
        
        op = "or"
        
    else:
        
        op = "unknown"
        
    splitline = in_line.split(" ")
    members = []
    
    negated = False
    for element in splitline:
        
      
        if element == "and" or element == "or":
            
            continue
        
        elif (element == "not"):
            
        
            print("in not")
            negated = True
            
            
        
    
            
        else:
            
            if(negated == True):
            
                members.append("-" + element)
                
                negated = False
            else:
                
                members.append(element)
            
        
    print("members")
    print(members)
    return members, op, searcher
            
        
        
def searchForAndReplaceNested(current_formulas,in_line):

    for formula in current_formulas:
        

        in_line = in_line.replace(formula.searcher,formula.name)
          
    
   
    return in_line
 
    
    

def sortFunc(e):

    return e[0]


def parseAndCreateRules(text,RHS_name):
    
   
    
    formlist = []

    rulenum = 1
    
    forms = list(parenthetic_contents(text))
    
    forms.sort(key = sortFunc,reverse = True)
    
    for form in forms:
    
        line = form[1]
        
        if(contains_nested(line) == False):
            
            
            newformula = owlFormula()
            
            newformula.members, newformula.operator, newformula.searcher = get_nonnested_members(line)
            
            newformula.name = RHS_name + "_Condition_" + str(rulenum)
            
            rulenum += 1
            formlist.append(newformula) 
            
        else:
            
           
            
            x = searchForAndReplaceNested(formlist,line)
            
            newformula = owlFormula()
            
            newformula.members, newformula.operator, newformula.searcher = get_nonnested_members(x)
            
            newformula.name = RHS_name + "_Condition_" + str(rulenum)
            
            rulenum += 1
            formlist.append(newformula) 
            
          
            
    return formlist

#LHS_text = "(p1 and not p2 and not (p3 or not p4))"

#forms = parseAndCreateRules(LHS_text,"c1")
    
 
#print("PRINTING FORMULAS\n")
   
#for form in forms:
    
  #  print(form.name)
   # print(form.operator)
   # for member in form.members:
   #     print(member)
        
 #   
#    print()































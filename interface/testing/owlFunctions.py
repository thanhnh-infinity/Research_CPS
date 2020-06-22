from parse import *



def is_asp_or_conc(mytype):
    
    if(not (mytype == "Concern" or mytype == "Aspect") ):
        return False
    else:
        return True
    
def remove_namespace(in_netx):

    in_str = str(in_netx)

    leng = len(in_str)
    period = leng
    for i in range(leng):
        if(in_str[i] == '.'):
            period = i
            break

    return in_str[(period + 1):]


def remove_ir(in_netx):
    
   
    in_str = str(in_netx) + " "
    parsed_name = ''.join(r[0] for r in findall("#{} ", in_str))
        
    if(parsed_name == ""):
        return remove_namespace(in_netx)
    
    
    print("reduced name from " + str(in_netx) + " to " + parsed_name)
    return parsed_name
    
    

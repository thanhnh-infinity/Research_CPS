from parse import *

file = open("./SR-01/use_case_2_LKAS_Case_0_after_cyberattack.txt", mode = 'r')
lines = file.readlines()

line = lines[4]

#print(line)

x = search("aspect({}) ",line)




aspects_parse = ' '.join(r[0] for r in findall("aspect(\"cpsf:{}\")", line))


concerns_parse = ' '.join(r[0] for r in findall(" concern(\"cpsf:{}\")", line))
                                                     #subconcern("cpsf:Human","cpsf:HumanFactors")
#subconcerns_parse = ' '.join(r[0] for r in findall(" subconcern(\"cpsf:{}\",\"cpsf:{}\"", line))
#subconcerns_parse2 = ' '.join(r[1] for r in findall(" subconcern(\"cpsf:{}\",\"cpsf:{}\"", line))

#pairs = []



satisfied_parse =  ' '.join(r[0] for r in findall(" h(sat(\"cpsf:{}\"),0)", line))
unsatisfied_parse = ' '.join(r[0] for r in findall(" -h(sat(\"cpsf:{}\"),0)", line))

aspects_list = aspects_parse.split(" ")
concerns_list = concerns_parse.split(" ")
#subconcerns_list = subconcerns_parse.split(" ")
#subconcerns_list2 = subconcerns_parse2.split(" ")
satisfied_list = satisfied_parse.split(" ")

print()
print()
unsatisfied_list = unsatisfied_parse.split(" ")


print(satisfied_list)
print()
print()
print(unsatisfied_list)
#for i in range( len(subconcerns_list)):
    
  #  parent = subconcerns_list[i]
  #  child = subconcerns_list2[i]
    
   # pairs.append([parent,child])


#print(subconcerns_parse)

print()
print()
#print(subconcerns_parse2)

print()
print()
#print(pairs)
print(len(aspects_list))
print(len(concerns_list))



#print(satisfied_list)
#print()
#print(unsatisfied_list)

#print(len(satisfied_list) + len(unsatisfied_list))
#print(len(concerns_list) + len(aspects_list))

#print(concerns_list)
#print(aspects_list)
#print(subconcerns_list)
from parse import *
import csv  
import argparse

import os

outputfilename = "./maintest.csv"

filename = "./SR01_inputs/use_case_2_LKAS_Case_3_after_cyberattack.txt"   
file = open(filename,mode = "r")   
allLines = file.readlines()
input_str = ''.join(allLines)


cmd = "python3 exportASP.py " + input_str + " " + outputfilename
      

os.system(cmd)


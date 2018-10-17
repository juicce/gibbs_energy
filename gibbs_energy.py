#! /usr/bin/python3

"""The script requires Python3, numpy library and Unix OS, 
run the script from a folder with your .log files """

""" First, the script creates a list of files and a list of file names."""

files = []
names = []

while True: # Asks for next file until you type 'end'.
    entry = input("Please, type a name of .log file or confirm input with blank line: \n")
    if '' != entry:
        files.append(entry)
        if '.log' in entry:
            name = entry.replace('.log','')
            names.append(name)
        elif '.out' in entry:
            name = entry.replace('.out','')
            names.append(name)
        else:
            print('Files should be in .out or .log format')
            break
    if entry == '':
        break
print('\033[31m Working... \033[0m'+'\n')

""""Second, script open each file, find the line with 'Sum of electronic and thermal Free Energies' 
and save energy in Hartree to energies_au list."""

import re

energies_au = []
NumRegex = re.compile(r'-\d+\.\d+') #Regex for negative float

for file in files:
    temp_file = open(file,'r')
    for line in temp_file:
        if 'Sum of electronic and thermal Free' in line:
            gibbs_energy = line
        else:
            pass
    temp_file.close()
    mo = NumRegex.search(gibbs_energy)
    num = float(mo.group())
    energies_au.append(num)

"""Now the script converts energies in Hartree to a new list of energies in eV and kJ/mol. 
It also creates a list of variances between an energy of fist file and energies of the others."""

import numpy as np
Hartree_eV = 27.211385

def eV_convert(eng):
    
    """Converts energies in given list (eng) from Hartree to eV, return a numpy.array"""
    
    loc1 = np.array(eng)
    loc2 = loc1 * Hartree_eV
    return loc2

def variance(eng):
    
    """Takes a list of energies and counts a variance between first energy in the list, 
    returns a list"""
    
    loc1 = []
    for i in eng:
        loc2 = eng[0] - i
        loc1.append(loc2)
    return loc1

energies_eV = eV_convert(energies_au)
variances = variance(energies_eV)

"""At last, the script writes all the data to a new file named gibbs_energy.txt"""

file = open('gibbs_energy.txt','w')
content = "Name,Energy [eV],Eng. Var. [eV]\n"

for i in range(len(names)):
    line = str(names[i]) + ',' + str(energies_eV[i]) + ',' + str(variances[i]) + '\n'
    content += line

file.write(content)
file.close()
print('Done!')
    
    
    



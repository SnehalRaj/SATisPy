import sys
import subprocess32 as sb
inpName=sys.argv[1]
outName=sys.argv[2]
print('Select from the following heuristics:')
print('1.Unit Propogation')
print('')
print('2.Propogations using deterministically assigned interpretations')
print('')
print('3.Propogation using Pure Literal Elimination')
print('')
choice=eval(raw_input('Enter your choice:'))
if choice==1:
    sb.call(['python','heuristic1.py',inpName,outName])
if choice==2:
    sb.call(['python','heuristic2.py',inpName,outName])    
if choice==3:
    sb.call(['python','heuristic3.py',inpName,outName])

import re
import sys
import hashlib
import argparse

def shortenName(name):
	hashObject = hashlib.md5(name.encode())
	return name[0:min(len(name),8)] + '_' + hashObject.hexdigest()[0:3]

def replaceName(name, replacement, string):
	return re.sub(r'(?<![A-Za-z0-9_])(' + name + r')(?![A-Za-z0-9_])', replacement, string)



parser = argparse.ArgumentParser(description='''
	## Small converter, to bypass KAREL's limitation of variable name length to 12 characters
	''')


parser.add_argument('--input', '-i', dest='inputPath', default=None, required=True,
	                 help='Input file path')
parser.add_argument('--output', '-o', dest='outputPath', default=None,
	                 help='Output file path. Defaults to printing to the result')

args = parser.parse_args()

try:
	file = open(args.inputPath, 'rt')
except ValueError : 
	print('Error opening input file')
	sys.exit(0)
inputString = file.read()
constLocation = re.search(r'^[\t ]*CONST[\t ]*(--.*)?', inputString, re.M)
varLocation = re.search(r'^[\t ]*VAR[\t ]*(--.*)?', inputString, re.M)
lineNumberOfConst = inputString.count('\n', 0, constLocation.end() )
lineNumberOfVar = inputString.count('\n', 0, varLocation.end() )

lineNumberOfVarEnd = 0

lines = inputString.split('\n')

for i in range(lineNumberOfVar+1, len(lines)):
	line = lines[i]
	if re.search(r'^[\t ]*(ROUTINE|BEGIN)', line):
		lineNumberOfVarEnd = i
		break

if lineNumberOfVarEnd==0:
	print("Could not find end of VAR statement, aborting")
	sys.exit(0)


lines = inputString.split('\n')
# Changing CONSTs
for lineIndex in range(lineNumberOfConst, lineNumberOfVar):
	line = lines[lineIndex]
	constCandidate = re.search(r'^[\t ]*([A-Za-z0-9_]+)[\t ]', line)
	if constCandidate:
		constName = constCandidate.group(1)
		newConstName = shortenName(constName)
		inputString = replaceName(constName, newConstName, inputString)

# Changing VARs
lines = inputString.split('\n')
for lineIndex in range(lineNumberOfVar, lineNumberOfVarEnd):
	line = lines[lineIndex]
	varCandidate = re.search(r'^[\t ]*(?!ROUTINE)([A-Za-z0-9_]+)[\t ]', line)
	if varCandidate:
		varName = varCandidate.group(1)
		newVarName = shortenName(varName)
		inputString = replaceName(varName, newVarName, inputString)

lines = inputString.split('\n')
# Changing ROUTINES
for lineIndex in range(len(lines)):
	line = lines[lineIndex]
	routineCandidate = re.search(r'^[\t ]*ROUTINE[\t ]*([A-Za-z0-9_]+)[\t ]*\(?(?!from)', line)
	if routineCandidate:
		routineName = routineCandidate.group(1)
		newRoutineName = shortenName(routineName)
		lines = [replaceName(routineName, newRoutineName, line3) for line3 in lines]
		for i in range(lineIndex, len(lines)):
			line2 = lines[i]
			if re.search(r'^[\t ]*BEGIN[\t ]*', line2):
				lineNumberOfRoutineBegin = i
				break
		for i in range(lineNumberOfRoutineBegin+1, len(lines)):
			line2 = lines[i]
			if re.search(r'^[\t ]*END[\t ]+' + newRoutineName, line2):
				lineNumberOfRoutineEnd = i
				break
		argumentLines = '\n'.join(lines[lineIndex:lineNumberOfRoutineBegin])
		arguments = re.findall(r'[;\( \t]*([A-Za-z0-9_]+)[ \t]*:',argumentLines, re.M)
		routineLines = lines[lineIndex:lineNumberOfRoutineEnd]
		for argument in arguments:
			if(argument != newRoutineName):
				routineLines = [replaceName(argument, shortenName(argument),line2) for line2 in routineLines]
		lines[lineIndex:lineNumberOfRoutineEnd] = routineLines
output = '\n'.join(lines)
if(args.outputPath):
	with open(args.outputPath, 'wt') as outputFile:
		outputFile.write(output)
else:
	print(output)
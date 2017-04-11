#! /usr/bin/env python
# -*- coding: latin-1 -*-

import sys
import os
import subprocess
import re
import json
import time
import random

# The order that this program expects the input file to be is:  
#
# transformationAgentQty   = 1  100
# transformationAgentGroupPercentage   = 10  100
# individualExploration = 1  500
# groupExploration = 1  1500
# classesAgentesTransformadores = 0  1
#
# Each of this variables maps to a certain variable in settings ini file.
# Their name was kept the same in order to be easier to understand.
# TODO(murl): find what is the name of 'classesAgentesTransformadores' in ini file.
#
# The output file expect at least 2 varibles, the figure of merit and 
# the null model.
#

configJSONFile = None

with open('./mase-driver-config.json', 'r') as configFile:
	configJSONFile = json.load(configFile)

if configJSONFile is None or "lastConfiguration" not in configJSONFile:
	print "Não é possível executar o MASE-Driver sem um arquivo de configuração. Execute o MASE-Driver-GUI.py e tente novamente."
	sys.exit()

if len(sys.argv) < 3:
	print 'This program expects the names of PSUADE\'s input and output files.'
	sys.exit()

print 'Reading', sys.argv[1], 'as PSUADE input file.'

inputVariables = configJSONFile["lastConfiguration"]["input_variables"]
outputVariables = configJSONFile["lastConfiguration"]["output_variables"]

doubledVariables = ['transformationAgentQty', 'transformationAgentGroupPercentage']

maseArgs = []

maseArgs.append("." + os.pathsep + os.path.dirname(configJSONFile["maseLocation"]) + os.path.sep + "*" + os.pathsep + configJSONFile["maseLocation"] + os.pathsep + os.path.dirname(configJSONFile["maseLocation"]) + os.path.sep + "libmy/*")
maseArgs.append("masex.Starter")

with open(sys.argv[1]) as psuadeInputFile:
	numberOfVariables = int(psuadeInputFile.readline())
	if numberOfVariables is not len(inputVariables):
		print "Number of variables in the input file differs from configuration file. Use GUI to configure", "config file", len(inputVariables), "psuade in file", numberOfVariables
		sys.exit()

	for varIndex in range(numberOfVariables):
		variableValue = int(float(psuadeInputFile.readline()))
		variableName = inputVariables[varIndex]["name"].strip()
		if variableName in doubledVariables:
			maseArgs.append("-MASE" + variableName + "=" + str(variableValue) + "," + str(variableValue))
		else:
			maseArgs.append("-MASE" + variableName + "=" + str(variableValue))

print 'Running MASE: '
# with open(os.devnull, 'w') as DEVNULL:
subprocess.call(["java", "-cp"] + maseArgs)
# include this to hide MASE output: stdout=DEVNULL, close_fds=True)

print 'Finished running MASE.'

currentDir = os.path.dirname(os.path.realpath(__file__))

outputFileContents = ''

# search in the current directory
for file in os.listdir(currentDir):
	# find the csv files
	if file.endswith(".csv"):
		# grab the second line in the csv file and use it as output to PSUADE
		with open(file) as csvFile:
			outputFromMaseHeader = [header.strip(' \n\r\t') for header in csvFile.readline().split(';')]
			outputFromMase = csvFile.readline().split(';')
			for outVar in outputVariables:
				# find this var in mase output header
				try:
					indexOfVar = outputFromMaseHeader.index(outVar["name"])
				except ValueError:
					print "Problem reading MASE-BDI output in CSV file.", outVar["name"]
					sys.exit()
				outputFileContents += outputFromMase[indexOfVar] + '\n'

			os.remove(file)
	elif file.endswith ('.bmp') or file.endswith('.zip'):
		os.remove(file)

with open(sys.argv[2], 'w+') as outputFile:
	outputFile.write(outputFileContents)

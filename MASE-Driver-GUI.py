#!/usr/bin/python
# -*- coding: latin-1 -*-

import Tkinter, tkFileDialog, tkMessageBox
from Tkinter import *
import locale
import ttk
import json
import os
import subprocess
import sys
import threading

locale.setlocale(locale.LC_ALL, 'pt_BR')

currentFolder = os.path.dirname(os.path.realpath(__file__))

configFileName = "mase-driver-config.json"
configFilePath = currentFolder + os.path.sep + configFileName

configFileJSON = None
userConfigFile = {}

hasOpenedConfigFile = False

with open(configFilePath, 'r') as configFile:
	configFileJSON = json.load(configFile)

if configFileJSON is None:
	print "Could not open config file"
	sys.exit()

class PsuadeThread(threading.Thread):

	def __init__(self):
		self.stdout = None
		self.stderr = None
		threading.Thread.__init__(self)

	def run(self):
		# print configFileJSON["psuadeLocation"] + " psuade.in"
		# p = subprocess.Popen(configFileJSON["psuadeLocation"] + " psuade.in",
		# 	shell=False,
		# 	stdout=subprocess.PIPE,
		# 	stderr=subprocess.PIPE)

		# self.stdout, self.stderr = p.communicate()
		subprocess.call([configFileJSON["psuadeLocation"], "psuade.in"])

class PsuadeRunWindow(object):
	def __init__(self, master):
		top = self.top = Toplevel(master)
		self.label = Label(top, text = "PSUADE - Executando")
		self.label.grid(row = 0, column = 0)
		self.cancelButton = Button(top, text="Cancelar", command = self.cleanup)
		self.cancelButton.grid(row = 0, column = 1)
		top.grab_set()
		self.psuadeThread = PsuadeThread()
		self.psuadeThread.start()
		self.psuadeThread.join()
		self.cleanup()

	def cleanup(self):
		self.top.destroy()
		self.top.grab_release()

class PsuadeConfigWindow(object):
	def __init__(self, master):
		global userConfigFile
		global hasOpenedConfigFile

		top = self.top = Toplevel(master)
		# top.title = "PSUADE - Config File"
		self.label = Label(top, text = "PSUADE - Configuração")
		self.label.grid(row = 0, column = 0)
		self.okButton = Button(top, text="Aplicar", command = self.saveClean)
		self.okButton.grid(row = 0, column = 3)
		self.cancelButton = Button(top, text="Cancelar", command = self.cleanup)
		self.cancelButton.grid(row = 0, column = 4)

		self.createMethodSection()
		self.addSeparator()

		if hasOpenedConfigFile and "method" in userConfigFile:
			self.inputSampleMethodVar.set(userConfigFile["method"]["sampling"].strip())
			self.numSamplesVar.set(userConfigFile["method"]["num_samples"].strip())
			self.numReplicationsVar.set(userConfigFile["method"]["num_replications"].strip())
			self.sizeRefinementsVar.set(userConfigFile["method"]["refinement_size"].strip())
			self.numRefinementsVar.set(userConfigFile["method"]["num_refinements"].strip())
			self.refRefinementsVar.set(userConfigFile["method"]["reference_num_refinements"].strip())
			self.inputRefinementTypesVar.set(userConfigFile["method"]["refinement_type"].strip())
			self.randomize.set(userConfigFile["method"]["randomize"].strip())
			self.randomizeMore.set(userConfigFile["method"]["randomize_more"].strip())
			self.randomSeedVar.set(userConfigFile["method"]["random_seed"].strip())
		else:
			self.numSamplesVar.set("300")
			self.numReplicationsVar.set("1")
			self.numRefinementsVar.set("0")
			self.sizeRefinementsVar.set("10000000")
			self.refRefinementsVar.set("0")

		top.grab_set()

	def addSeparator(self):
		separator = Frame(self.top, height = 1, bg = "black")
		separator.grid(row = 10, columnspan = 10, sticky = W+E)

	def createMethodSection(self):
		global configFileJSON
		self.inputSampleMethodComboLabel = Label(self.top, text = "Método de Geração*:")
		self.inputSampleMethodComboLabel.grid(row = 1, column = 0, sticky = E)

		self.inputSampleMethodVar = StringVar()

		validateTextEntries = self.top.register(self.validateSamplingComboBox)

		self.inputSampleMethodCombo = ttk.Combobox(self.top, values = configFileJSON["sampling_methods"], validate='all', validatecommand = (validateTextEntries, '%P'), textvariable = self.inputSampleMethodVar)
		self.inputSampleMethodCombo.grid(row = 1, column = 1, sticky = W)

		self.numSamplesVar = StringVar()

		self.numSamplesEntryLabel = Label(self.top, text = "Quantidade de Amostras*:")
		self.numSamplesEntryLabel.grid(row = 2, column = 0, sticky = E)
		self.numSamplesEntry = Entry(self.top, textvariable = self.numSamplesVar)
		self.numSamplesEntry.grid(row = 2, column = 1, sticky = W)

		self.numReplicationsVar = StringVar()

		self.numReplicationsLabel = Label(self.top, text = "Número de Replicações:")
		self.numReplicationsLabel.grid(row = 3, column = 0, sticky = E)
		self.numReplicationsEntry = Entry(self.top, textvariable = self.numReplicationsVar)
		self.numReplicationsEntry.grid(row = 3, column = 1, sticky = W)

		self.numRefinementsVar = StringVar()

		self.numRefinementsLabel = Label(self.top, text = "Número de Refinamentos:")
		self.numRefinementsLabel.grid(row = 4, column = 0, sticky = E)
		self.numRefinementsEntry = Entry(self.top, textvariable = self.numRefinementsVar)
		self.numRefinementsEntry.grid(row = 4, column = 1, sticky = W)

		self.sizeRefinementsVar = StringVar()

		self.sizeRefinementsLabel = Label(self.top, text = "Tamanho do Refinamento:")
		self.sizeRefinementsLabel.grid(row = 5, column = 0, sticky = E)
		self.sizeRefinementsEntry = Entry(self.top, textvariable = self.sizeRefinementsVar)
		self.sizeRefinementsEntry.grid(row = 5, column = 1, sticky = W)

		self.refRefinementsVar = StringVar()

		self.refRefinementsLabel = Label(self.top, text = "Número de Referência de Refinamento:")
		self.refRefinementsLabel.grid(row = 6, column = 0, sticky = E)
		self.refRefinementsEntry = Entry(self.top, textvariable = self.refRefinementsVar)
		self.refRefinementsEntry.grid(row = 6, column = 1, sticky = W)

		self.inputRefinementTypesVar = StringVar()

		self.inputRefinementTypesComboLabel = Label(self.top, text = "Tipo de Refinamento:")
		self.inputRefinementTypesComboLabel.grid(row = 7, column = 0, sticky = E)
		self.inputRefinementTypesCombo = ttk.Combobox(self.top, values = configFileJSON["refinement_types"], textvariable = self.inputRefinementTypesVar)
		self.inputRefinementTypesCombo.grid(row = 7, column = 1, sticky = W)

		self.randomSeedVar = StringVar()

		self.randomSeedLabel = Label(self.top, text = "Semente Aleatória:")
		self.randomSeedLabel.grid(row = 8, column = 0, sticky = E)
		self.randomSeedEntry = Entry(self.top, textvariable = self.randomSeedVar)
		self.randomSeedEntry.grid(row = 8, column = 1, sticky = W)

		self.randomize = IntVar()

		self.randomizeCheck = Checkbutton(self.top, text = "Adicionar Perturbações", variable = self.randomize)
		self.randomizeCheck.grid(row = 9, column = 0, sticky = E)

		self.randomizeMore = IntVar()

		self.randomizeMoreCheck = Checkbutton(self.top, text = "Mais Perturbações", variable = self.randomizeMore)
		self.randomizeMoreCheck.grid(row = 9, column = 1, sticky = E)

	def validateSamplingComboBox(self, value):
		if len(value) is 0:
			return True
		global configFileJSON
		if value in configFileJSON["sampling_methods"]:
			return True
		return False

	def cleanup(self):
		self.top.destroy()
		self.top.grab_release()

	def saveClean(self):
		global userConfigFile
		global hasOpenedConfigFile
		if self.inputSampleMethodVar.get() is None or len(self.inputSampleMethodVar.get().strip()) is 0:
			tkMessageBox.showerror("Campo não preenchido", "É necessário preencher o campo Método de Geração.")
			return False
		if self.numSamplesVar.get() is None or len(self.numSamplesVar.get().strip()) is 0:
			tkMessageBox.showerror("Campo não preenchido", "É necessário preencher o campo Quantidade de Amostras.")
			return False

		methodSection = userConfigFile["method"] = {}

		methodSection["sampling"] = self.inputSampleMethodVar.get().strip()
		methodSection["num_samples"] = self.numSamplesVar.get().strip()
		methodSection["num_replications"] = self.numReplicationsVar.get().strip()
		methodSection["num_refinements"] = self.numRefinementsVar.get().strip()
		methodSection["refinement_size"] = self.sizeRefinementsVar.get().strip()
		methodSection["reference_num_refinements"] = self.refRefinementsVar.get().strip()
		methodSection["refinement_type"] = self.inputRefinementTypesVar.get().strip()
		methodSection["randomize"] = str(self.randomize.get())
		methodSection["randomize_more"] = str(self.randomizeMore.get())
		methodSection["random_seed"] = self.randomSeedVar.get().strip()

		hasOpenedConfigFile = True

		self.cleanup()

class PopupWindow(object):
    def __init__(self, master, windowLabel, okCallback):
        top = self.top = Toplevel(master)
        self.label = Label(top, text = windowLabel)
        self.label.grid(row = 0, column = 0)
        self.variableName = Entry(top)
        self.variableName.grid(row = 0, column = 1)
        self.variableName.focus_set()
        self.okButton = Button(top, text="OK", command = self.cleanup)
        self.okButton.grid(row = 0, column = 3)
        self.okCallback = okCallback
        self.master = master
        top.grab_set()

    def cleanup(self):
        self.value = self.variableName.get()
        self.top.destroy()
        self.top.grab_release()
    	self.okCallback()

class VariableEntry(object):

	def __init__(self, manager, top, variableName, gridRow):
		self.manager = manager
		self.label = Label(top, text = variableName)
		self.label.grid(row = gridRow, column = 0, sticky = W)
		self.lBoundVar = StringVar()
		self.uBoundVar = StringVar()

		validateTextEntries = top.register(self.validateEntry)

		self.lowerBoundEntry = Entry(top, textvariable = self.lBoundVar)
		self.lowerBoundEntry.grid(row = gridRow, column = 1)
		self.upperBoundEntry = Entry(top, textvariable = self.uBoundVar, validate='all',
         validatecommand = (validateTextEntries, '%P'))
		self.upperBoundEntry.grid(row = gridRow, column = 2)
		self.isInputVar = IntVar()
		self.isInput = Radiobutton(top, variable = self.isInputVar, value = 1, command = self.setEntriesVisible)
		self.isInput.grid(row = gridRow, column = 3)
		self.isOutput = Radiobutton(top, variable = self.isInputVar, value = 0, command = self.setEntriesVisible)
		self.isOutput.grid(row = gridRow, column = 4)
		self.removeEntry = Button(top, text = "-", command = self.removeSelf)
		self.removeEntry.grid(row = gridRow, column = 5)

		self.setEntriesVisible()

	def validateEntry(self, text):
		if text is None or len(text) is 0:
			return True
		try:
			int(text)
			return True
		except ValueError:
			return False

	@staticmethod
	def createEntry(manager, top, name, lBound, uBound, isInput, gridRow):
		entry = VariableEntry(manager, top, name, gridRow)
		entry.lBoundVar.set(lBound)
		entry.uBoundVar.set(uBound)
		entry.isInputVar.set(isInput)
		entry.setEntriesVisible()
		return entry

	def removeSelf(self):
		self.label.grid_forget()
		self.upperBoundEntry.grid_forget()
		self.lowerBoundEntry.grid_forget()
		self.removeEntry.grid_forget()
		self.isInput.grid_forget()
		self.isOutput.grid_forget()
		self.manager.removedEntry(self)

	def setEntriesVisible(self):
		if self.isInputVar.get() == 0:
			self.lowerBoundEntry.grid_remove()
			self.upperBoundEntry.grid_remove()
		else:
			self.lowerBoundEntry.grid()
			self.upperBoundEntry.grid()


class VariableEntryManager(object):
	def __init__(self, top):
		self.entryCount = 1
		self.entryList = []
		self.entryFrame = Frame(top)
		self.entryFrame.pack()
		self.variableNameColumn = Label(self.entryFrame, text = "Nome")
		self.variableNameColumn.grid(row = 0, column = 0)
		self.variableLowerBoundColumn = Label(self.entryFrame, text = "Lim. Inferior")
		self.variableLowerBoundColumn.grid(row = 0, column = 1)
		self.variableLowerUpperColumn = Label(self.entryFrame, text = "Lim. Superior")
		self.variableLowerUpperColumn.grid(row = 0, column = 2)
		self.variableIn = Label(self.entryFrame, text = "Entrada")
		self.variableIn.grid(row = 0, column = 3)
		self.variableOut = Label(self.entryFrame, text = "Saída")
		self.variableOut.grid(row = 0, column = 4)

	def addVariableEntry(self, variableName):
		newEntry = VariableEntry(self, self.entryFrame, variableName, self.entryCount)
		self.entryList.append(newEntry)
		self.entryCount += 1

	def removedEntry(self, entry):
		self.entryCount -= 1
		self.entryList.remove(entry)

	def hasEntries(self):
		return True if len(self.entryList) > 0 else False

	def getInputVariables(self):
		variables = []
		for entry in self.entryList:
			if entry.isInputVar.get() == 1:
				data = {}
				data["name"] = entry.label.cget("text")
				data["lowerBound"] = entry.lowerBoundEntry.get()
				data["upperBound"] = entry.upperBoundEntry.get()
				variables.append(data)
		return variables

	def getOutputVariables(self):
		variables = []
		for entry in self.entryList:
			if entry.isInputVar.get() == 0:
				data = {}
				data["name"] = entry.label.cget("text")
				variables.append(data)
		return variables

	def loadJSONFile(self, file):
		global userConfigFile
		jsonFile = json.load(file)

		
		if jsonFile == None:
			return

		userConfigFile = jsonFile

		for entry in self.entryList:
			entry.removeSelf()

		def createEntriesFromJSON(list, isInput):
			for var in list:
				if isInput is 1:
					entry = VariableEntry.createEntry(self, self.entryFrame, var["name"], var["lowerBound"], var["upperBound"], isInput, self.entryCount)
				else:
					entry = VariableEntry.createEntry(self, self.entryFrame, var["name"], "", "", isInput, self.entryCount)
				self.entryList.append(entry)
				self.entryCount += 1	

		createEntriesFromJSON(jsonFile["input_variables"], 1)
		createEntriesFromJSON(jsonFile["output_variables"], 0)

def addVariable(top):
	popUp = PopupWindow(top, "Adicionar Variável", lambda: variableManager.addVariableEntry(popUp.value))

def openConfigurePsuadeWindow(top):
	PsuadeConfigWindow(top)

def savePsuadeInFile():
	global userConfigFile
	global configFileJSON

	currentInputVariables = variableManager.getInputVariables()

	psuadeInFileContents = "PSUADE\nINPUT\n"
	if len(currentInputVariables) > 0:
		psuadeInFileContents += "dimension\t" + str(len(currentInputVariables)) + "\n"
		for index, inputVar in enumerate(currentInputVariables):
			psuadeInFileContents += "variable\t" + str(index + 1) + "\t" + inputVar["name"] + "\t=\t" + inputVar["lowerBound"] + "\t" + inputVar["upperBound"] + "\n"
	else:
		tkMessageBox.showerror("Declarar Variáveis", "É necessário preencher ao menos uma variável de entrada.")
		return False

	psuadeInFileContents += "END\nOUTPUT\n"
	currentOutputVariables = variableManager.getOutputVariables()

	if len(currentOutputVariables) > 0:
		psuadeInFileContents += "dimension\t" + str(len(currentOutputVariables)) + "\n"
		for index, inputVar in enumerate(currentOutputVariables):
			psuadeInFileContents += "variable\t" + str(index + 1) + "\t"	 + inputVar["name"] + "\n"
	else:
		tkMessageBox.showerror("Declarar Variáveis", "É necessário preencher ao menos uma variável de saída.")
		return False

	psuadeInFileContents += "END\nMETHOD\n"

	if "method" in userConfigFile:
		method = userConfigFile["method"]
		psuadeInFileContents += "sampling\t=\t" + method["sampling"] + "\n"
		psuadeInFileContents += "num_samples\t=\t" + method["num_samples"] + "\n"
		psuadeInFileContents += "num_replications\t=\t" + method["num_replications"] + "\n"
		psuadeInFileContents += "num_refinements\t=\t" + method["num_refinements"] + "\n"
		psuadeInFileContents += "refinement_size\t=\t" + method["refinement_size"] + "\n"
		psuadeInFileContents += "reference_num_refinements\t=\t" + method["reference_num_refinements"] + "\n"

		if method["refinement_type"] is not None or len(method["refinement_type"].strip()) is not 0:
			psuadeInFileContents += "refinement_type\t=\t" + method["refinement_type"] + "\n"

		if "1" in method["randomize"]:
			psuadeInFileContents += "randomize\n"

		if "1" in method["randomize_more"]:
			psuadeInFileContents += "randomize_more\n"

		if len(method["random_seed"].strip()) is not 0:
			psuadeInFileContents += "random_seed\t=\t" + method["random_seed"] + "\n"

	else:
		tkMessageBox.showerror("Configurar PSUADE", "É necessário fazer a configuração do PSUADE. Clique em \"Configurar PSUADE\".")
		return False

	psuadeInFileContents += "END\nAPPLICATION\n"
	psuadeInFileContents += "driver\t=\t./MASE-Driver.py\n"
	psuadeInFileContents += "END\nANALYSIS\n"
	psuadeInFileContents += "analyzer output_id\t=\t1\n"
	psuadeInFileContents += "printlevel\t1\n"
	psuadeInFileContents += "END\nEND\n"

	with open(currentFolder + os.path.sep + "psuade.in", "w+") as psuadeInFile:
		psuadeInFile.write(psuadeInFileContents)

	lastConfiguration = configFileJSON["lastConfiguration"] = {}

	lastConfiguration["input_variables"] = currentInputVariables
	lastConfiguration["output_variables"] = currentOutputVariables
	
	with open(configFilePath, 'w+') as configFile:
		configFile.write(json.dumps(configFileJSON))

	return True

def runMasePsuade(top):
	if "maseLocation" not in configFileJSON:
		tkMessageBox.showerror("Configurar MASE", "É necessário indicar o diretório que o MASE-BDI se encontra.")
		return
	if "psuadeLocation" not in configFileJSON:
		tkMessageBox.showerror("Configurar MASE", "É necessário indicar o diretório que o PSUADE se encontra.")
		return

	if savePsuadeInFile():
		PsuadeRunWindow(top)

def saveConfiguration():
	global hasOpenedConfigFile
	global userConfigFile

	configurationFile = tkFileDialog.asksaveasfile(mode = "w", defaultextension=".json")

	if configurationFile is None:
		return

	userConfigFile["input_variables"] = variableManager.getInputVariables()
	userConfigFile["output_variables"] = variableManager.getOutputVariables()

	configurationFile.write(json.dumps(userConfigFile))
	configurationFile.close()
	hasOpenedConfigFile = True

def findPsuadeApp(top):
	filename = tkFileDialog.askopenfilename()

	if filename is not None and len(filename) is not 0:
		configFileJSON["psuadeLocation"] = filename
		with open(configFilePath, 'w+') as configFile:
			configFile.write(json.dumps(configFileJSON))
			fillPSUADELocation(top, filename)

def fillPSUADELocation(top, psuadeLocationText):
	global psuadeFilenameLabel
	if psuadeFilenameLabel is None:
		psuadeFilenameLabelVar = psuadeLocationText
		psuadeFilenameLabel = Label(top, text = psuadeLocationText)
		psuadeFilenameLabel.grid(row = 1, column = 1)
	psuadeFilenameLabel['text'] = psuadeLocationText
	psuadeFilenameLabel.grid()

def findMaseApp(top):
	filename = tkFileDialog.askopenfilename()

	if filename is not None and len(filename) is not 0:
		configFileJSON["maseLocation"] = filename
		with open(configFilePath, 'w+') as configFile:
			configFile.write(json.dumps(configFileJSON))
			fillMaseLocation(top, filename)

def fillMaseLocation(top, maseLocationText):
	global maseFilenameLabel
	if maseFilenameLabel is None:
		maseFilenameLabelVar = maseLocationText
		maseFilenameLabel = Label(top, text = maseLocationText)
		maseFilenameLabel.grid(row = 2, column = 1)
	maseFilenameLabel['text'] = maseLocationText
	maseFilenameLabel.grid()

def openConfiguration():
	global hasOpenedConfigFile
	configurationFile = tkFileDialog.askopenfile(filetypes=[("Arquivo de Configuracao", ".json")], mode = "r")
	if not configurationFile:
		return

	variableManager.loadJSONFile(configurationFile)
	hasOpenedConfigFile = True

root = Tkinter.Tk()

topFrame = Frame(root)
topFrame.pack(side = TOP)
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

variableManager = VariableEntryManager(bottomFrame)

addVariableButton = Tkinter.Button(topFrame, text = "Adicionar Variável", command = lambda: addVariable(root))
saveConfigurationButton = Tkinter.Button(topFrame, text = "Carregar Configuração Driver", command = openConfiguration)
openConfigurationButton = Tkinter.Button(topFrame, text = "Salvar Configuração", command = saveConfiguration)
openPsuadeExecutable = Tkinter.Button(topFrame, text = "Executável PSUADE", command = lambda: findPsuadeApp(topFrame))
openMaseeExecutable = Tkinter.Button(topFrame, text = "MASE-BDI JAR (com lib)", command = lambda: findMaseApp(topFrame))
configurePsuade = Tkinter.Button(topFrame, text = "Configurar PSUADE", command = lambda: openConfigurePsuadeWindow(root))

runButton = Tkinter.Button(bottomFrame, text = "Executar", command = lambda: runMasePsuade(root))

psuadeFilenameLabel = None
maseFilenameLabel = None

if "psuadeLocation" in configFileJSON:
	fillPSUADELocation(topFrame, configFileJSON["psuadeLocation"])
if "maseLocation" in configFileJSON:
	fillMaseLocation(topFrame, configFileJSON["maseLocation"])

addVariableButton.grid(row = 0, column = 0)
openConfigurationButton.grid(row = 0, column = 1)
saveConfigurationButton.grid(row = 0, column = 2)
openPsuadeExecutable.grid(row = 1, column = 0)
openMaseeExecutable.grid(row = 2, column = 0)
configurePsuade.grid(row = 1, column = 2)
runButton.pack()

root.mainloop()
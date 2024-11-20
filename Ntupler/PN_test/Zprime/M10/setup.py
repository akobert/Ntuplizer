#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(47):
    	template = open("DeepNtuplizerAK8.py", "r")
        newFile = open("ntupler" + str(process) + ".py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "options.inputFiles = 'input.root'"
	newline1 = "options.inputFiles = '"+str(readLine[:-1])+"'"
	
	oldline2 = "options.outputFile = 'output.root'"
	newline2 = "options.outputFile = 'file:/cms/akobert/UL/Ntupler/PN_test/Zprime/M10/PN_test_M10_Ntuple_"+str(process)+".root'"

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()

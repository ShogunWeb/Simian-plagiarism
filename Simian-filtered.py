#Copyright © 2017 <University of Liège - Jérémie Fays - j.fays@ulg.ac.be>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Script analysing results from Simian (http://www.harukizaemon.com/simian/) xml file output 
# in order to detect plagiarism between two projects. It will filter Simian results and remove 
# all duplicated blocks that concern only one project.
#
# File structure needs to be the following :
# 
#  simianBaseDir
# 		bin/
#			simianApp
#		CODE/
#			(this script)
#			projectName/
#				project1/ (contains source code of project 1)
#				project2/ (contains source code of project 2)
#				... (could contain other projects)
#
# ----------------------------------------------------------------------
# Result : writes a file named projectName+'-simian-filtered.xml' in the CODE/ directory
# This file contains only duplicated code from one project to another (all duplicated code within a project is removed)
# 

import subprocess


simianBaseDir='/simianDir'
simianApp="simian-2.4.0.jar"
projectName='projectNameDir'
callArgument='java -jar '+simianBaseDir+'/bin/'+simianApp+' -formatter=xml:'+projectName+'-simian.xml "'+simianBaseDir+'/CODE/Predetector/**/*.*"'
#print callArgument

retcode = subprocess.Popen(callArgument, shell=True)


#function that returns the main subdirectory from the 'projectName' directory
def getSubProject(filePath):
	subProjectPath = filePath.split(projectName, 1)
	subProjectName = subProjectPath[1].split('/',2)
	return subProjectName[1]


import xml.etree.ElementTree as ET
tree = ET.parse(simianBaseDir+"/CODE/"+projectName+'-simian.xml')
root = tree.getroot()
for set in root[0].findall('set'):
	duplicateCount=0
	#stores the first subproject name from the set, in order to compare with others
	sourceFile=set[0].get('sourceFile')		
	firstDir=getSubProject(sourceFile)
	
	for block in set.iter('block'):
		if getSubProject(block.get('sourceFile')) != firstDir:
			duplicateCount=duplicateCount+1		
	if not duplicateCount:
		root[0].remove(set)

tree.write(simianBaseDir+"/CODE/"+projectName+'-simian-filtered.xml')









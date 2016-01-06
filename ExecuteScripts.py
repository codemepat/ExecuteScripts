#!/usr/bin/env python

import xml.sax
import sys
import datetime
import shlex
from subprocess import Popen, PIPE

# This class handles managing of log output and
# execution of script. The xml parser reads the block
# of script and uses the RunScript object to execute.
class RunScript():
    
    def __init__(self):
        """
        Initialize the script.
        Create output file to store logs of script progress
        or errors.
        """
        self.outFile = ""
        self.create_output_file()
        
    def create_output_file(self):
        """
        Create a log file with current date and time.
        Any debug or error statements printed by the scripts
        will be captured in the log file.

        The log file resides in the current directory from
        where the program is launched.
        """
        currentTime = datetime.datetime.now()
        dateStr = str(currentTime).replace(" ","_").replace(".", "-").replace(":", "-")
        # Build output file name
        fileName = 'execute_script'+'_'+dateStr+'.log'
        print "\nOpening output log file ",fileName
        try:
            self.outFile = open(fileName, 'w')
        except IOError as e:
            print "Failed to open file: ", fileName, " ,with error code: ", e.errno, ",error: ", e.strerror
            sys.exit(e.errno)
        
    def run(self, scriptElement):
        """
        For every element in the xml file, check if the
        script is enabled to execute. Execute the command
        and capture output in log file.

        The script should be either on the path from where
        the system can execute, or reside in the same directory
        from where this script is run.
        """
        self.element = scriptElement
                    
        # Check if the desired script is enabled to execute        
        if ((self.element['enable']).lower() != 'true'):
            print "Script ", self.element['name'], " disabled. Skipping execution..."
            return
        
        # We are good to execute
        print "Executing script ", self.element['name'], " with args ", (self.element['args'])
        cmdArgs = shlex.split(self.element['args'].encode('ascii','ignore'))
        cmdLine = []
        cmdLine.append(str(self.element['name']))
        cmdLine += cmdArgs

        # Execute command with arguments, for windows shell needs to be true
        p = Popen(cmdLine,stdout=PIPE,stderr=PIPE, shell=True)
        (stdoutdata, stderrdata) = p.communicate()
        #print stdoutdata, stderrdata
        # Capture script output in to log file
        self.outFile.writelines(stdoutdata)
        self.outFile.writelines(stderrdata)

# This class handles XML parsing.
# The information collected from each element is used to
# execute the script. The class reads and executes the block
# of script data serially.
class ScriptHandler(xml.sax.ContentHandler):
    
    tagDict = {}
    runScript = RunScript()
    
    def __init__(self):
        """
        Initialize the class.
        Set the dictionary with recognizable element tags.
        """
        self.name = ""
        self.tagSet = set(['Release', 'script', 'name', 'args', 'desc', 'enable', 'ver'])
        self.content = ""
        self.scriptInfoNode = "script"
        
    def startElement(self, name, attrs):
        """
        This method is called when the parser recognizes the start
        of the element. Verify the expected start element tag,
        and read attributes.
        """
        if name in self.tagSet:
            # Hold tag for each element
            self.name = name
            # Extract any attributes
            if attrs.getLength() is not 0:
                # Read first attribute
                attrName = attrs.getNames()
                if attrName[0] in self.tagSet:
                    self.tagDict[attrName[0]] = attrs.get(attrName[0])
                    #print ("%s has %s attribute value" %(attrName, self.tagDict[attrName[0]]))
        else:
            exitStatus = "Invalid tag " + name
            sys.exit(exitStatus)
            
    def endElement(self, name):
        """
        This method is called when the parser recognizes end of element
        tag. When all the script details are gathered, the end of element
        of script tag triggers the execution of the script.
        """
        self.tagDict[name] = self.content
        # Collect all the script info
        if name == self.scriptInfoNode:
            # Execute the script
            self.runScript.run(self.tagDict)
        
    def characters(self, content):
        """
        This method is called when characters from xml file are read.
        Save the contents to use when executing the script.
        """
        #print "characters: ", content, "for name: ", self.name
        self.content = content

def main():        
    # Print python version information
    print "\nPython version information"
    print ('%s %s' % (sys.executable or sys.platform, sys.version))
    print ""
    
    # Create XMLReader
    parser = xml.sax.make_parser()

    # Turn off namespace
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # Override the default context handler
    handler = ScriptHandler()
    parser.setContentHandler(handler)

    # Parse scripts input XML
    parser.parse("scripts.xml")    

if __name__ == '__main__':
    main()

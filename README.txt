Execute Scripts

Python program to execute scripts and other executables.
This version of the script serially executes all the commands enabled in scripts.xml file and saves standard output from the command in a log file. 

Where can this be useful?

Number of times we run tasks serially to complete project work, such as a Release engineer may want to package files, generate checksum, lay down repository label, generate package release notes, etc. During course of the project, number of engineers contribute in writing automated scripts, as well as find suitable ones from open source. Scripts may be in different language such as Perl, Python, or Shell. An output of one script can be input of another one. To reduce the release time, some automated tasks can also run in parallel.

This Python script binds all the desired scripts to run in a concise way. It allows user to choose to run commands at this point, or later using configurable XML file. 


How to Run

Desired scripts to run needs to be described in scripts.xml file.
<name>ListDocFiles.py</name>
Sample script which gathers all the files with provided extensions.
<args>.doc .pdf</args>
Arguments to the scripts are provided with 'args' tag, in this case find all the files with .doc* and .pdf extension.
<enable>True</enable>
Turn on or off to execute this script.

python ExecuteScripts.py


Vision

Two enhancements are desirable:
a) Allow output of script to be input of another
b) Allow multiple scripts to run in parallel
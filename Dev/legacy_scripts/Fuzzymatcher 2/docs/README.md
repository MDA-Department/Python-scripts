Entity File - Membership File Fuzzymatcher
--------

Description
--------
This program is a fuzzymatching tool meant to link data from a local's membership files to the corresponding data name and ID in the local's entity file. 

Data in the membership files often have mispellings, abbreviations or other minor spelling 
differences that makes it impossible to match membership data to the correct name and 
ID in the entity file with a merge alone. This program creates a spreadsheet of fuzzy match candidates
for the data entries that do not match perfectly. After the fuzzy match spreadsheet is manually reviewed,
it then remerges the correct data name and ID from the entity file into the membership file. This is 
intended to speed up the process of matching membership file data to the entity file name and ID.

Prerequisites
------------
In order to run the program, you must have Python installed on your computer. Python can be installed 
through Anaconda here: https://www.anaconda.com/products/individual.

Entity File - Membership File Fuzzymatcher is dependent on several Python libraries. Jupyter Notebook
users can install them by individually running each of the following commands in your computer's command prompt*:
    
    pip install pandas
    pip install recordlinkage
    pip install regex
    pip install pathlib
    pip install pytest-shutil
    pip install configparser
    pip install numpy

*Unsure for other IDEs
    
Set-Up
----------
The program can be found in FilesinProcess in the AFTDBFileUpload OneDrive folder. In order for the
program to run correctly, the folder containing the membership file - entity file pair you'd like to
match must meet the following requirements:

    1. There must be a folder called Fuzzymatcher. Within Fuzzymatcher, there must be a folder called 
    testing_locals which contains a third folder that contains the the membership file and entity file
    you want to perform the match for. This third folder must be named the five-digit local number 
    underscore the five-digit ticket number. For example, 00777_14166. 
    
    2. The membership file itself must be an Excel file named the five-digit local number underscore the 
    five-digit ticket number underscore the eight-digit date underscore 'Knackbuild'. 
    For example, 00777_14166_20210709_Knackbuild.xlsx. The entity file itself must be an Excel file named
    the five-digit local number underscore 'EntityList'. For example, 0077_EntityList.xlsx.
    
    3. There must be a separate folder within Fuzzymatcher named cleaning_dictionaries. For each membership file - entity file pair 
    you'd like to match, a csv file named the five-digit local number underscore 'cleaning_dict' must exist. 
    For example, 00777_cleaning_dict.csv. This csv file must contain at least a single line with two values. It may
    contain more than one line but should not contain more or less than two values per line.


Contribute
----------
- Source Code: bitbucket.org/aftsoftwareteam/fuzzymatch

Support
-------
If there's an issue with the program, send Ambrose an email at atarrant@aft.org.

License
-------
The project is licensed under the AFT Software Team license.
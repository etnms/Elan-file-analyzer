# Elan file analyzer
This is a simple python project that allows you to read through multiple elan files to look for values in a tier and how frequently they appear. It allows you to look for all values or a specific value if needed. With just a few clicks it can analyze hundreds of files in seconds and give you a summary as a .csv file (that can be open and read like an Excel or Calc spreadsheet). This program can be very helpful if you are looking for a value across multiple files and don't want to open them one by one. Instead you can have a detailed .csv file with a summary of which elan file the value appear in and how frequently it does.

## Purpose of the program
The program aims at creating a list (as a .csv file) of all the values in the tier you are looking for, how frequently they appear, the proportion it takes in the whole file, the total time a value appears in the file/in multiple files. It can be useful to quickly look through which files contains which values without opening 100s of elan files.
It's important to note that such a program works well for looking at how frequent a value appears. If you are not interested in the frequency of values this program is probably not for you. 
You can specify which tier you are interested it and even which value you are interested in as well. You have the choice to look for all the values in a tier or a specific one.

## For non-developpers
You can simply go in the "dist" folder and use the executable file there.

## How it works
Elan files are simply XML files. Based on this information, the program was meant to look for specific values that are created in the file in order to return a summary of them. Python works fairly well with this type of process and the code remains simple and readable.
The GUI is based of PyQT.

## Limits
- This program is meant to analyze multiple files to look for the frequency of values. If you are not looking for frequencies of apparition of values then this might not be the right tool for you.
- The code can be improved when it comes to readibility of a few functions.

## Why this project
I worked on a research program that required analyzing a lot of elan files and I figured I could automate part of the process, especially when looking for specific values. While this only constituted a small part of the research project it still was helpful to save some time and gather important and detailed values in a few seconds.

#!/usr/bin/bash
#Reads filename 
echo "Please enter the file name"
read filename
#Reads old Word to replaced
echo "Please enter old word"
read old
#Reads new word to be replaced by
echo "Please enter new word"
read new
#Makes copies of the old file on which we are going to perform replace
cp "${filename}.txt" "${filename}-formal.txt"
#Uses SED to read and replace words
sed "s|$old|$new|" "${filename}-formal.txt"



#!/usr/bin/bash
#Promts the user for directory name and reads it as input.
echo -n "enter the directory namme: "
read dir
#Declear an funtion.
function filecount(){
     #This returns the count of files of extesions in directory. 
     find $dir/ -type f | sed -E 's/(.+)(\..+)/\2/' | sort | uniq -c -i | sort -n
}
#Calling to end the main function.
filecount

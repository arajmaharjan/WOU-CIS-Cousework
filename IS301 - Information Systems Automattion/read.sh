#!/usr/bin/bash
#This prompts the user to input and reads pathname of a file or directory.
echo -n "Enter your pathname of a file or directory: "
read filepath 

#This checks whether file/directory exists or not, if its present then we will print its permissions.
if [ -f "$filepath" ] || [ -d "$filepath" ]; 
  then
    echo "There exists an file or directory called $filepath."
    
    #This checks for write permission.
  [ -w $filepath ] && Write="Write_Permission = yes" || Write="Write_Permission = No"
  #This checks for execute permission.
  [ -x $filepath ] && Execute="Execute_Permission = yes" || Execute="Execute_Permission = No" 
  #This checks for read permission.
  [ -r $filepath ] && Read="Read_Permission = yes" || Read="Read_Permission = No" 
  #This gives the path and permissions.
echo -e "$filepath permissions are below: \n $Write \n $Read \n $Execute"

#If path is invalid then we will print does not exist.
else 
    echo "$filepath does not exist in the given path."
fi
#!/usr/bin/bash
# prompts user to enter file extension and reads it.
echo -n "Please enter the file extenion: "
read ext
# prompts user to enter desired prefix and reads it.
echo -n "Enter the prefix: "
read prefix
#reads from for loop to add the desired prefix, if no prefix adds old as default prefix.
for f in *.$ext; do
    if [ -z $prefix ];
    then
        mv $f "old_"$f && echo "All filenames $f are changed to old_$f "
    else
        mv $f $prefix"_"$f && echo "All filenames $f are changed to ${prefix}_${f}"
    fi;
done

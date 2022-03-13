i=$(ls -l ./"$@" |wc -l | sort -n)
echo "Number of item is $i and the list of file are :$@"

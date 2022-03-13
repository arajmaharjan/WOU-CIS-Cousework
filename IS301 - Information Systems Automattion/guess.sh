#!/usr/bin/bash
#Welcome prompt.
echo "Welcome to the guessing game"

#Generates random integer in the range [0 - 10]
n1=$(($RANDOM % 10 )) 

#Reads user input.
read -p "Guess the number between (1-10): " n2 

#Calculates if the guessed number is greater than random number.
if  [ $n2 -ge $n1 ]
	then
 echo  " you've guessed too high!!"
#calculates if the guessed number is less than random number.
elif [ $n2 -lt $n1 ]
	then
 echo "you've guessed it too low!!"
#calculates if the guessed number equal to random number.
elif [ $n2 -eq $n1 ]
	then
#Prompts Congratulations if the guessed number and random number match.
 echo "Congratulations you've guessed right!!"
fi

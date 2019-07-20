To install all the dependencies:
	$ ./depend.sh

To run the program you have to run satis.py specifying the input and output files that our sat solver will use.
Command:
		$ python satis.py input.txt output.txt
Next, a menu will pop up which asks which heuristic you want to implement to solve the dimacs encoding.
The first option solves the encoding with an efficient implementation having unit propagation as it's main stand-out feature.
The second option solves the encoding using a self defined heuristic the details about which has been written in the report present in the folder
The third option solves the encoding using both unit literal propagation and pure literal elimination.
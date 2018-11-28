# Evaluator

Python script which compiles and runs .cpp files and compares the output of the program with the desired output. Main purpose of this was to create my own evaluator to check if my solutions to some problems were correct since I could download the datasets. Currently it supports comparing outputs line by line and comparing outputs by an absolute difference of a given epsilon.

## Usage
Run help with
```
python main.py -h
```
Which will display the following
```
  file            name of the cpp file
  task            name of the task
  {byline,byeps}  byeps - compares the outputs by an epsilon
                  byline - compares the outputs line by line
  timelimit       maximum amount of time the program should run.

optional arguments:
  -h, --help      show this help message and exit
  -eps EPS        absolute error between the compared outputs
```
The .cpp file must be in the same folder as the main.py. All datasets should be contained in the folder /tasks/taskname/. All datasets should be of the form ```taskname.in.num``` and ```taskname.out.num``` where ```num``` is the number of the dataset. The program will compare the output of your program, given ```taskname.in.num.txt``` as the input, to the ```taskname.out.num``` .
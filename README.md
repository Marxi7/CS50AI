# CS50AI Projects


## Description

This repository contains my solutions to the projects for the CS50AI course offered by Harvard University on the edX platform. CS50AI is an introductory course on Artificial Intelligence that covers a range of topics such as search, knowledge representation, probabilistic inference, and machine learning.

## Projects
This repository contains the following projects ([Click here](#how-to-run-each-project) to learn how to run each project).
:

### Degrees

The Degrees project finds the shortest path between two actors in a database of movies, using breadth-first search algorithm. The project comes with a database of over 1,000 movies and their casts, and can find the path between any two actors who have worked together in a movie.

To run the program, navigate to the Degrees directory and run the following command:

```bash
python degrees.py <option> <source_actor> <target_actor>
```

- <option>: Choose the dataset to use. Options are small, medium, and large.
- <source_actor>: Name of the starting actor. Use quotes if there are spaces in the name.
- <target_actor>: Name of the target actor. Use quotes if there are spaces in the name.

```bash
# Your Program should look like this in the terminal 
$ python degrees.py large
Loading data...
Data loaded.
Name: Emma Watson
Name: Jennifer Lawrence
3 degrees of separation.
1: Emma Watson and Brendan Gleeson starred in Harry Potter and the Order of the Phoenix
2: Brendan Gleeson and Michael Fassbender starred in Trespass Against Us
3: Michael Fassbender and Jennifer Lawrence starred in X-Men: First Class
```

### Tic-Tac-Toe
    
![TicTacToe](/images_projects/tictactoe.png)

In the Tic-Tac-Toe project, I implemented an AI to play Tic-Tac-Toe optimally using the minimax algorithm. The program allows you to play against the AI or watch the AI play against itself.

In the repository, you will find two folders for Tic-Tac-Toe: 'tictactoe' and 'tictactoe_without_alpha_beta_pruning'. The former implements the Alpha-Beta-Pruning Method for a more efficient and faster solution, while the latter does not use Alpha-Beta-Pruning and is therefore slower and less efficient.

To run the program, navigate to the 'tictactoe' directory and run the following command:

```bash
python runner.py
```


### Knights

In the Knights project, I implemented an AI to solve logic puzzles using propositional logic and inference by enumeration. The program solves a puzzle in which you have to place knights on a chessboard such that no two knights threaten each other. To run the program, navigate to the Knights directory and run the following command:

```bash
python puzzle.py
```

```bash
# Your Program should look like this in the terminal 
$ python puzzle.py
Puzzle 0
    A is a Knave
Puzzle 1
    A is a Knave
    B is a Knight
Puzzle 2
    A is a Knave
    B is a Knight
Puzzle 3
    A is a Knight
    B is a Knave
    C is a Knight
```


### Minesweeper
    
![Minesweeper](/images_projects/minesweeper.png)

In the Minesweeper project, I implemented an AI to play Minesweeper using knowledge representation and inference. The program uses logical inference to deduce which cells are safe to click and which cells contain mines. To run the program, navigate to the Minesweeper directory and run the following command:

```bash
python runner.py
```


### PageRank

In the PageRank project, I implemented the PageRank algorithm to rank web pages by importance. The program reads in a corpus of web pages and computes the PageRank scores for each page using iterative matrix multiplication. To run the program, navigate to the PageRank directory and run the following command:

```bash
python pagerank.py corpus0
```

```bash
# Your Program should look like this in the terminal 
$ python pagerank.py corpus0
PageRank Results from Sampling (n = 10000)
  1.html: 0.2223
  2.html: 0.4303
  3.html: 0.2145
  4.html: 0.1329
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
```


### Heredity

In the Heredity project, I implemented an AI to assess the likelihood that a person has a genetic trait based on their family's medical history. The program uses Bayesian networks to model the probabilities and make inferences about the likelihood of the trait. To run the program, navigate to the Heredity directory and run the following command:

```bash
python heredity.py data/family0.csv
```

```bash
# Your Program should look like this in the terminal 
$ python heredity.py data/family0.csv
Harry:
  Gene:
    2: 0.0092
    1: 0.4557
    0: 0.5351
  Trait:
    True: 0.2665
    False: 0.7335
James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000
    False: 0.0000
Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000
    False: 1.0000
```


### Crossword

In the Crossword project, I implemented an AI to generate crossword puzzles. The program reads in a list of words and their clues, and generates a crossword puzzle with the words intersecting in the correct places. To run the program, navigate to the Crossword directory and run the following command:

```bash
python generate.py data/structure1.txt data/words1.txt output.png
```

```bash
# Your Program should look like this in the terminal
$ python generate.py data/structure1.txt data/words1.txt output.png
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
```
The program should also generate an image :
![Crossword](/images_projects/crossword.png)




### Shopping

In the Shopping project, I implemented an AI to optimize an online shopping list by finding the cheapest combination of items from different online stores. The program uses a graph-based approach to find the optimal solution. To run the program, navigate to the Shopping directory and run the following command:

```bash
python shopping.py shopping.csv
```

```bash
# Your Program should look like this in the terminal 
$ python shopping.py shopping.csv
Correct: 4088
Incorrect: 844
True Positive Rate: 41.02%
True Negative Rate: 90.55%
```


### Nim

In the Nim project, I implemented an AI to play the game of Nim optimally using the minimax algorithm. The program allows you to play against the AI or watch the AI play against itself. To run the program, navigate to the Nim directory and run the following command:

```bash
python play.py
```

```bash
# Your Program should look like this in the terminal 
$ python play.py
Playing training game 1
Playing training game 2
Playing training game 3
...
Playing training game 9999
Playing training game 10000
Done training

Piles:
Pile 0: 1
Pile 1: 3
Pile 2: 5
Pile 3: 7

AI\'s Turn
AI chose to take 1 from pile 2.
```


### Traffic

In the Traffic project, I implemented a convolutional neural network to classify traffic signs. The program trains the network on a dataset of traffic sign images and then uses the trained model to classify new images of traffic signs. To run the program, navigate to the Traffic directory and run the following commands:


Note that you will need to download a dataset of traffic signs to run this program. When in the traffic directory, download the [dataset](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip).


```bash
pip3 install -r requirements.txt
python3 traffic.py gtsrb

```

```bash
# Your Program should look like this in the terminal 
$ python traffic.py gtsrb
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
Epoch 4/10
500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
Epoch 8/10
500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
Epoch 9/10
500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
Epoch 10/10
500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
333/333 - 5s - loss: 0.1616 - accuracy: 0.9535
```
Here is my video submission for the program in which you can see the program running live:
[Click here to watch the demo](https://youtu.be/g12J4hHZP7Q)



### Parser

In the Parser project, I implemented a PCFG parser to parse sentences using context-free grammar rules. The program reads in a grammar file and a sentence, and then generates all possible parses of the sentence according to the grammar rules. To run the program, navigate to the Parser directory and run the following command:

```bash
# Your Program should look like this in the terminal 
$ python parser.py
Sentence: Holmes sat.
        S
   _____|___
  NP        VP
  |         |
  N         V
  |         |
holmes     sat

Noun Phrase Chunks
holmes
```


### Questions

In the Questions project, I implemented a question-answering AI using natural language processing techniques such as named entity recognition and tf-idf search. The program reads in a corpus of text documents and then allows you to ask questions about the documents. To run the program, navigate to the Questions directory and run the following command:

```bash
python questions.py corpus
```

```bash
# Your Program should look like this in the terminal 
$ python questions.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning , classification and regression.

$ python questions.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python questions.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
```


# Conclusion

These projects provided me with a solid foundation in the field of artificial intelligence and its various applications. Each project focuses on a different aspect of AI and builds upon the concepts learned in the previous projects. I hope this repository serves as a useful resource for anyone interested in learning AI or looking for inspiration for their own AI projects.



# How to Run each Project {#how-to-run-each-project}

In order to run each project, you need to install the dependencies found in the requirements.txt file located in the main folder (CS50AI) containing each project folders. 

First you need to install Python if not done already: Click [Here](https://www.python.org/downloads/) to do so.

Then, run the following command to create a Virtual Environment:

```bash
$ python3 -m venv
```

### Activate your environment
You’ll need to use different syntax for activating the virtual environment depending on which operating system and command shell you’re using.

On Unix or MacOS, using the bash shell: source /path/to/venv/bin/activate<br>
On Unix or MacOS, using the csh shell: source /path/to/venv/bin/activate.csh<br>
On Unix or MacOS, using the fish shell: source /path/to/venv/bin/activate.fish<br>
On Windows using the Command Prompt: path\to\venv\Scripts\activate.bat<br>
On Windows using PowerShell: path\to\venv\Scripts\Activate.ps1<br>

```bash
# After your environment has been activated, install the dependencies
$ pip install -r requirements.txt
```

## Comments
A big thanks to the whole Team of CS50 for providing courses with such a high quality.  


## Stay in touch

- Author - [Marcello](https://github.com/Marxi7)

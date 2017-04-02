# Pygame-Conway-Game-of-Life
 The rule of this game is based on [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).


# Rule
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of
which is in one of two possible states, alive or dead, or "populated" or "unpopulated". Every cell interacts
with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.
At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

<p>
  <br/>
  <img src="http://i.imgur.com/zdIQYcI.gif" width="250"/>
  <br/>
</p>
 
## Dependencies
* Python 2
* Pygame
* PyOpenGL
* Pygubu
* Sip (python package)
* py2exe (only requrired for Winodws environment without python)


## Execution

```
python ChsChess.py
```

## Build as exe file

```
python setup.py
```
Note:

(1) 'py2exe' needs to install from http://sourceforge.net/project/showfiles.php?group_id=15583 

	The above link is provided by https://pypi.python.org/pypi/py2exe/
	
(2) Sip in python 2 should compile from source code https://www.riverbankcomputing.com/software/sip/download/ 
	and configure it with some C++ compiler, and apply MAKEFILE command 'make', 'make install' to install package
	your machine. For futher detail, please see http://pyqt.sourceforge.net/Docs/sip4/installation.html

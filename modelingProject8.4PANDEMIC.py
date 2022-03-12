# WRITTEN BY REMINGTON PONCE AS A PROJECT FOR A FALL 2020 COLLEGE COURSE TO VISUALLY SIMULATE A PANDEMIC'S DEVELOPMENT FROM START TO FINISH.

import turtle
import copy
import random
import matplotlib.pyplot as pyplot

SCALE = 6       # scale at which to draw the grid

def drawSquare(pos, color, tortoise):
    """Draws one square in the given color at the
       given position in the grid.
       
    Parameters: 
        pos:      a (row, column) tuple
        color:    a color string
        tortoise: a Turtle object
        
    Return value: None
    """
    
    (row, column) = pos
    screen = tortoise.getscreen()
    rows = int(screen.canvheight / screen.yscale)
    row = rows - row - 1
    tortoise.shape(color)
    tortoise.up()
    tortoise.goto(column, row + 1)
    tortoise.stamp()
    
def drawGrid(rows, columns, tortoise):
    """Draws an empty grid using turtle graphics.
       
    Parameters: 
        rows:     the number of rows in the grid
        columns:  the number of columns in the grid
        tortoise: a Turtle object
        
    Return value: None
    """
    
    tortoise.pencolor('gray')
    for row in range(rows + 1):
        tortoise.up()
        tortoise.goto(0, row)
        tortoise.down()
        tortoise.goto(columns, row)
    for column in range(columns + 1):
        tortoise.up()
        tortoise.goto(column, 0)
        tortoise.down()
        tortoise.goto(column, rows)
        
def createSquares(screen, colors):
    """Creates square shapes in the given colors to be used
       as turtle graphics stamps in a cellular automata.
       
    Parameters: 
        screen: a Screen object
        colors: a list of color strings
        
    Return value: None
    """
    
    square = ((0, 0), (0, SCALE), (SCALE, SCALE), (SCALE, 0))
    for color in colors:
        squareShape = turtle.Shape('compound')
        squareShape.addcomponent(square, color, 'gray')
        screen.register_shape(color, squareShape)




SUSCEPTIBLE = 0  # value of an uninfected cell
INFECTED = 1     # value of an infected cell
RECOVERED = 2    # value of a cell that is done infecting neighbors

def emptyGrid(rows, columns):
    """Create a rows x columns grid of zeros.

    Parameters:
        rows:    the number of rows in the grid
        columns: the number of columns in the grid

    Return value: a list of ROWS lists of COLUMNS zeros
    """
    
    grid = []
    for r in range(rows):
        row = [SUSCEPTIBLE] * columns
        grid.append(row)
    return grid
    
def initialize(grid, coordinates, tortoise):
    """Set a given list of coordinates to 1 in the grid
       and draw them as black squares.

    Parameters:
        grid:        a grid of values for a cellular automaton
        coordinates: a list of coordinates
        tortoise:    a Turtle object

    Return value: None
    """

    for (r, c) in coordinates:
        grid[r][c] = INFECTED
        drawSquare((r, c), 'black', tortoise)




def infectNeighborhood(grid, newGrid, row, column, R, tortoise):
    """Infect neighbors using a given R value.
    
    Parameters:
        grid:     two-dimensional grid from previous generation
        newGrid:  two-dimensional grid to change
        row:      the row index of the infected cell
        column:   the column index of the infected cell
        R:        reproduction number (average number of cells to infect)
        tortoise: Turtle object
        
    Return value: the number of new infections
    """
    
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    rows = len(grid)
    columns = len(grid[0])
    count = 0
    currentProb = 0
    for offset in offsets:       # for each neighbor (r, c)
        r = row + offset[0]
        c = column + offset[1]
        currentProb = random.random() 
        if (r >= 0 and r < rows) and (c >= 0 and c < columns):
            if (newGrid[r][c] == SUSCEPTIBLE) and (currentProb <= (R / 8)):
                newGrid[r][c] = INFECTED
                count = count + 1
                drawSquare((r, c), 'black', tortoise)
                
    return count




import copy
import random
import matplotlib.pyplot as pyplot

def infection(rows, columns, generations, R, initialNumber, tortoise, fractionSheltered):
    """Simulate the spread of an infectious disease.
    
    Parameters:
        rows:          the number of rows in the grid
        columns:       the number of columns in the grid
        generations:   the number of generations to simulate
        R:             average number of cells an infected cell infects
        initialNumber: number of initially infected cells
        tortoise:      a Turtle object
        fractionSheltered: the number of 'quarantining' cells
        
    Return value: the final configuration of cells in a grid
    """
    
    screen = tortoise.getscreen()
    grid = emptyGrid(rows, columns)
    shelteredCoordinates = [ ]
    
    if fractionSheltered == 0:
        pass
    else:
        r1 = 0
        c1 = 0
        for count in range(fractionSheltered):
            r1 = random.choice(range(rows))
            c1 = random.choice(range(columns))
            shelteredCoordinates.append((r1, c1))
        if (rows // 2, columns // 2) in shelteredCoordinates:
            shelteredCoordinates.remove((rows // 2, columns // 2))
        for (r, c) in shelteredCoordinates:
            grid[r][c] = RECOVERED
            drawSquare((r, c), 'blue', tortoise)
    
    drawGrid(rows, columns, tortoise)
    
    countNewInfected = [initialNumber]
    countInfected = [initialNumber]
    totalInfected = initialNumber
    newInfected = 0
    
    # Initialize the grid with infected individuals: either one in the center
    # or a greater number in randomly chosen cells.
    
    if initialNumber == 1:
        initialCells = [(rows // 2, columns // 2)]
    else:
        initialCells = []
        for count in range(initialNumber):
            r = random.randrange(rows)
            c = random.randrange(columns)
            initialCells.append((r, c))
    initialize(grid, initialCells, tortoise)
    
    for g in range(1, generations + 1):
        newGrid = copy.deepcopy(grid)
        for r in range(rows):
            for c in range(columns):
                if grid[r][c] == INFECTED:
                    count = infectNeighborhood(grid, newGrid, r, c, R, tortoise)# infect neighbors of cell (r, c)
                    totalInfected = totalInfected + count
                    newGrid[r][c] = RECOVERED                                     # cell (r, c) is done infecting others
                    drawSquare((r, c), 'lightgray', tortoise)
                    newInfected = newInfected + count

        countInfected.append(totalInfected)
        countNewInfected.append(newInfected)
        newInfected = 0
                    
        grid = newGrid
        
        screen.title('Generation ' + str(g))
        
    screen.update()
    screen.exitonclick()
    
    return countInfected, countNewInfected # REPLACE with the two lists described below

def main():
    columns = 100   # number of columns in the grid
    rows = 100      # number of rows in the grid

    george = turtle.Turtle()
    screen = george.getscreen()
    screen.setup(columns * SCALE + 20, rows * SCALE + 20)
    screen.setworldcoordinates(0, 0, columns, rows)
    screen.tracer(500)
    george.hideturtle()
    createSquares(screen, ['black', 'white', 'lightgray', 'blue'])
    
    generations = 100
    R = 4
    numInfected = 1
    fractionSheltered = 1666
    countInfected, countNewInfected = infection(rows, columns, generations, R, numInfected, george, fractionSheltered)
    

    if countInfected + countNewInfected != []:
        pyplot.figure(1)
        pyplot.subplot(2, 1, 1) # arguments are (rows, columns, subplot #)
        pyplot.plot(range(generations + 1), countNewInfected, color = 'blue')
        pyplot.xlabel('Generation')
        pyplot.ylabel('New Infections')

        pyplot.subplot(2, 1, 2)
        pyplot.plot(range(generations + 1), countInfected, color = 'blue')
        pyplot.xlabel('Generation')
        pyplot.ylabel('Total Infections')
        pyplot.show()
    
main()

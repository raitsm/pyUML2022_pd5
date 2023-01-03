import turtle
import random
import world_history as wh

class World:
    def __init__(self, mX, mY):
        self.__maxX = mX
        self.__maxY = mY
        self.__thingList = []
        self.__grid = []
        # self.__history = [["Time", "Fish", "Bears"]]
        self.__history = wh.WorldHistory(["Fish","Bears"])

        for aRow in range(self.__maxY):
            row = []
            for aCol in range(self.__maxX):
                row.append(None)
            self.__grid.append(row)

        self.__wTurtle = turtle.Turtle()
        self.__wScreen = turtle.Screen()
        self.__wScreen.setworldcoordinates(0, 0, self.__maxX - 1, 
                                           self.__maxY - 1)
        self.__wScreen.addshape("Bear.gif")
        self.__wScreen.addshape("Fish.gif")
        self.__wTurtle.hideturtle()
        self.__timecount = 0
        
    def draw(self):
        self.__wScreen.tracer(0)
        self.__wTurtle.forward(self.__maxX - 1)
        self.__wTurtle.left(90)
        self.__wTurtle.forward(self.__maxY - 1)
        self.__wTurtle.left(90)
        self.__wTurtle.forward(self.__maxX - 1)
        self.__wTurtle.left(90)
        self.__wTurtle.forward(self.__maxY - 1)
        self.__wTurtle.left(90)
        for i in range(self.__maxY - 1):
            self.__wTurtle.forward(self.__maxX - 1)
            self.__wTurtle.backward(self.__maxX - 1)
            self.__wTurtle.left(90)
            self.__wTurtle.forward(1)
            self.__wTurtle.right(90)
        self.__wTurtle.forward(1)
        self.__wTurtle.right(90)
        for i in range(self.__maxX - 2):
            self.__wTurtle.forward(self.__maxY - 1)
            self.__wTurtle.backward(self.__maxY - 1)
            self.__wTurtle.left(90)
            self.__wTurtle.forward(1)
            self.__wTurtle.right(90)
        self.__wScreen.tracer(1)

    def addThing(self, aThing, x, y):
        aThing.setX(x)
        aThing.setY(y)
        self.__grid[y][x] = aThing       #add life-form to grid
        aThing.setWorld(self)
        self.__thingList.append(aThing)  #add to list of life-forms
        aThing.appear()

    def delThing(self, aThing):
        aThing.hide()
        self.__grid[aThing.getY()][aThing.getX()] = None
        self.__thingList.remove(aThing)

    def moveThing(self, oldX, oldY, newX, newY):
        self.__grid[newY][newX] = self.__grid[oldY][oldX]
        self.__grid[oldY][oldX] = None

    def getMaxX(self):
        return self.__maxX

    def getMaxY(self):
        return self.__maxY

    def liveALittle(self):
        if self.__thingList != [ ]:
           aThing = random.randrange(len(self.__thingList))
           randomThing = self.__thingList[aThing]
           randomThing.liveALittle()
        self.__timecount += 1           # time increases with each cycle.
        self.updateHistory()            # update the history with new settings

    def emptyLocation(self, x, y):
        if self.__grid[y][x] == None:
            return True
        else:
            return False

    def lookAtLocation(self, x, y):
        return self.__grid[y][x]

    def freezeWorld(self):
        self.__wScreen.exitonclick()
        
    # counts the things in the world.
    # input: type of the thing to count, e.g., Bear or Fish
    # output: count of the things belonging to the type
    def countThings(self, animal_type) -> int:
        result = 0
        for y in self.__grid:
            for x in y:
                if isinstance(x, animal_type):
                    result += 1
        return result
    
    def updateHistory(self):
        self.__history.addHistoryItem("Fish",self.countThings(Fish))
        self.__history.addHistoryItem("Bears",self.countThings(Bear))
        # self.__history.append([str(self.__timecount),str(self.countThings(Fish)),str(self.countThings(Bear))])
        
    def exportHistory(self, output: str):
        self.__history.exportHistory(file_name=output)

class Fish:
    def __init__(self):
        self.__turtle = turtle.Turtle()
        self.__turtle.up()
        self.__turtle.hideturtle()
        self.__turtle.shape("Fish.gif")

        self.__xPos = 0
        self.__yPos = 0
        self.__world = None

        self.__breedTick = 0

    def setX(self, newX):
        self.__xPos = newX

    def setY(self, newY):
        self.__yPos = newY

    def getX(self):
        return self.__xPos

    def getY(self):
        return self.__yPos

    def setWorld(self, aWorld):
        self.__world = aWorld

    def appear(self):
        self.__turtle.goto(self.__xPos, self.__yPos)
        self.__turtle.showturtle()

    def hide(self):
        self.__turtle.hideturtle()

    def move(self, newX, newY):
        self.__world.moveThing(self.__xPos, self.__yPos, newX, newY)
        self.__xPos = newX
        self.__yPos = newY
        self.__turtle.goto(self.__xPos, self.__yPos)

    def liveALittle(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjFish = 0  #count adjacent Fish
        for offset in offsetList:
            newX = self.__xPos + offset[0]
            newY = self.__yPos + offset[1]
            if 0 <= newX < self.__world.getMaxX()  and \
                  0 <= newY < self.__world.getMaxY():
                if (not self.__world.emptyLocation(newX, newY)) and \
                    isinstance(self.__world.lookAtLocation(newX, newY), Fish):
                    adjFish = adjFish + 1

        if adjFish >= 2:   #if 2 or more adjacent Fish, die
            self.__world.delThing(self)
        else:
            self.__breedTick = self.__breedTick + 1
            if self.__breedTick >= 12:  #if alive 12 or more ticks, breed
                self.tryToBreed()

            self.tryToMove()            #try to move

    def tryToBreed(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not (0 <= nextX < self.__world.getMaxX() and \
                   0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        if self.__world.emptyLocation(nextX, nextY):
           childThing = Fish()
           self.__world.addThing(childThing, nextX, nextY)
           self.__breedTick = 0     #reset breedTick

    def tryToMove(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not(0 <= nextX < self.__world.getMaxX() and \
                  0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        if self.__world.emptyLocation(nextX, nextY):
           self.move(nextX, nextY)

class Bear:
    BEAR_ENDURANCE = 9

    def __init__(self):
        self.__turtle = turtle.Turtle()
        self.__turtle.up()
        self.__turtle.hideturtle()
        self.__turtle.shape("Bear.gif")

        self.__xPos = 0
        self.__yPos = 0
        self.__world = None

        self.__starveTick = 0
        self.__breedTick = 0
        self.__energy = Bear.BEAR_ENDURANCE

    def setX(self, newX):
        self.__xPos = newX

    def setY(self, newY):
        self.__yPos = newY

    def getX(self):
        return self.__xPos

    def getY(self):
        return self.__yPos

    def setWorld(self, aWorld):
        self.__world = aWorld

    def appear(self):
        self.__turtle.goto(self.__xPos, self.__yPos)
        self.__turtle.showturtle()

    def hide(self):
        self.__turtle.hideturtle()

    def move(self, newX, newY):
        self.__world.moveThing(self.__xPos, self.__yPos, newX, newY)
        self.__xPos = newX
        self.__yPos = newY
        self.__turtle.goto(self.__xPos, self.__yPos)

    def tryToBreed(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not (0 <= nextX < self.__world.getMaxX() and \
                   0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        if self.__world.emptyLocation(nextX, nextY):
           childThing = Bear()
           self.__world.addThing(childThing, nextX, nextY)
           self.__breedTick = 0     #reset breedTick
           self.__energy -= 1       # decrease energy due to breeding

    def tryToMove(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not(0 <= nextX < self.__world.getMaxX() and \
                  0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        if self.__world.emptyLocation(nextX, nextY):
           self.move(nextX, nextY)
           self.__energy -= 1           # decrease energy due to moving. 

    def liveALittle(self):
        self.__breedTick = self.__breedTick + 1
        if self.__breedTick >= 8:  #if alive 8 or more ticks, breed
            self.tryToBreed()

        self.tryToEat()

        if self.__starveTick >= 10:  # if not eaten for 10 ticks, die
            self.__world.delThing(self)
        else:
            self.tryToMove()
        if self.__energy < 0:       
            self.__world.delThing(self)

    def tryToEat(self):
        offsetList = [(-1,1), (0,1) ,(1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjPrey = []     #create list of adjacent prey
        for offset in offsetList:
            newX = self.__xPos + offset[0]
            newY = self.__yPos + offset[1]
            if 0 <= newX < self.__world.getMaxX() and \
               0 <= newY < self.__world.getMaxY():
                if (not self.__world.emptyLocation(newX, newY)) and  \
		          isinstance(self.__world.lookAtLocation(newX, newY), Fish):
                    adjPrey.append(self.__world.lookAtLocation(newX, newY))

        if len(adjPrey) > 0:  #if any Fish are adjacent, pick random Fish to eat
            randomPrey = adjPrey[random.randrange(len(adjPrey))]
            preyX = randomPrey.getX()
            preyY = randomPrey.getY()

            self.__world.delThing(randomPrey)  # delete the Fish
            # NB, movement in connection with eating will not decrease the energy
            self.move(preyX, preyY)            # move to the Fish's location

            self.__starveTick = 0           # starvation counter reset
            self.__energy += 1              # energy increase
        else:
            self.__starveTick = self.__starveTick + 1

def mainSimulation():
    numberOfBears = 10
    numberOfFish = 10
    worldLifeTime = 1000
    worldWidth = 50
    worldHeight = 25
 

    myWorld = World(worldWidth, worldHeight)
    myWorld.draw()

    for i in range(numberOfFish):
        newFish = Fish()
        x = random.randrange(myWorld.getMaxX())
        y = random.randrange(myWorld.getMaxY())
        while not myWorld.emptyLocation(x, y):
            x = random.randrange(myWorld.getMaxX())
            y = random.randrange(myWorld.getMaxY())
        myWorld.addThing(newFish, x, y)

    for i in range(numberOfBears):
        newBear = Bear()
        x = random.randrange(myWorld.getMaxX())
        y = random.randrange(myWorld.getMaxY())
        while not myWorld.emptyLocation(x, y):
            x = random.randrange(myWorld.getMaxX())
            y = random.randrange(myWorld.getMaxY())
        myWorld.addThing(newBear, x, y)
        
    # Record the situation at the beginning of the world history. 
    myWorld.updateHistory()

    for i in range(worldLifeTime):
        myWorld.liveALittle()
        # myWorld.updateHistory()

    print("Simulation over, exporting world history...")
    myWorld.exportHistory("WorldHistory.csv")
    print("All done.")
    myWorld.freezeWorld()

import pygame
import copy


# Knowledge Representation of Game State
class Grid:
    def __init__(self, rows, cols, size, main):
        self.GAME = main
        self.y = rows
        self.x = cols
        self.size = size

        self.white = loadScaledImage('photos/white.png', size)
        self.black = loadScaledImage('photos/black.png', size)
        self.whiteToBlack = [loadScaledImage(f'photos/BlackToWhite{i}.png', self.size) for i in range(1, 4)]
        self.blackToWhite = [loadScaledImage(f'photos/WhiteToBlack{i}.png', self.size) for i in range(1, 4)]
        self.bg = self.loadBackgroundImage()

        self.tokens = {}
        self.gridBackground = self.createBackgroundImage()
        self.gridLogic = self.regenGrid(self.y, self.x)

        self.firstPlayerScore = 0
        self.secondPlayerScore = 0

        self.font = pygame.font.SysFont('Arial', 20, True, False)
#set game state to its initial state
    def startNewGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)
#put background image into a dictionary to load it when render the game
    def loadBackgroundImage(self):
        alpha = 'ABCDEFGHI'
        spriteSheet = pygame.image.load('photos/backGround.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict

    def createBackgroundImage(self):
        gridBackground = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image = pygame.Surface((960, 960))
        for j, row in enumerate(gridBackground):
            for i, img in enumerate(row):
                image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
        return image
#set the initial game state by creating an empty grid and adding the four starting tokens.
    def regenGrid(self, rows, cols):
        grid = []
        for y in range(rows):
            line = []
            for x in range(cols):
                line.append(0)
            grid.append(line)
        self.addCurPlayerToken(grid, 1, 3, 3)
        self.addCurPlayerToken(grid, -1, 3, 4)
        self.addCurPlayerToken(grid, 1, 4, 4)
        self.addCurPlayerToken(grid, -1, 4, 3)

        return grid
#the score of the player on a specific state of the board
    def calcPlyerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, curPlayer, playerScore):
        textImage = self.font.render(f'{curPlayer} : {playerScore}', 1, 'white')
        return textImage

    def endGameScreen(self):
        if self.GAME.endGame:
            finishGameScreen = pygame.Surface((320, 320))
            finishMessage = self.font.render(f'{"yabn ella3eba,ent elle ksebt" if self.firstPlayerScore > self.secondPlayerScore else "ent elle 5esert ya zbooon"}', 1, 'White')
            finishGameScreen.blit(finishMessage, (0, 0))
            startNewGame = pygame.draw.rect(finishGameScreen, 'White', (80, 160, 160, 80))
            newRoundMessage = self.font.render('ell3ab game kaman', 1, 'Black')
            finishGameScreen.blit(newRoundMessage, (85, 190))
        return finishGameScreen

#drawing the background, displaying the current score rendering player tokens 
#highlighting available moves and showing the end game screen
    def drawGrid(self, window):
        window.blit(self.gridBackground, (0, 0))
        window.blit(self.font.render(f'CURRENT SCORE', 1, 'red'), (900, 200))
        window.blit(self.drawScore('You', self.firstPlayerScore), (900, 300))
        window.blit(self.drawScore('Computer Player', self.secondPlayerScore), (900, 400))

        for token in self.tokens.values():
            token.renderGameOnScreen(window)

        availableMoves = self.availableMoves(self.gridLogic, self.GAME.currPlayer)
        if self.GAME.currPlayer == 1:
            for move in availableMoves:
                pygame.draw.rect(window, 'White', (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))

        if self.GAME.endGame:
            window.blit(self.endGameScreen(), (240, 240))

    def availableMoves(self, grid, currPlayer):

        availableMOvesCells = self.determineAvailCells(grid, currPlayer)
        availableToChooseCells = []

        for cell in availableMOvesCells:
            x, y = cell
            if cell in availableToChooseCells:
                continue
            changeTiles = self.ChangableTiles(x, y, grid, currPlayer)

            if len(changeTiles) > 0:
                availableToChooseCells.append(cell)

        return availableToChooseCells
    

    def determineAvailCells(self, grid, curPlayer):
        availCellsToMove = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                validDirections = directions(gridX, gridY)

                for direction in validDirections:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in availCellsToMove:
                        continue

                    availCellsToMove.append((gridX, gridY))
        return availCellsToMove
# this function returns the list of swappable tiles, which are the tiles that will be 
#flipped if the current player places their token at position (x, y)
    def ChangableTiles(self, x, y, grid, player):
        availableCells = directions(x, y)
        if len(availableCells) == 0:
            return []

        ChangableTiles = []
        for availablecell in availableCells:
            check_x, check_y = availablecell
            dif_x, dif_y = check_x - x, check_y - y
            current_line = []

            RUN = True
            while RUN:
                if grid[check_x][check_y] == player * -1:
                    current_line.append((check_x, check_y))
                elif grid[check_x][check_y] == player:
                    RUN = False
                    break
                elif grid[check_x][check_y] == 0:
                    current_line.clear()
                    RUN = False
                check_x += dif_x
                check_y += dif_y

                if check_x < 0 or check_x > 7 or check_y < 0 or check_y > 7:
                    current_line.clear()
                    RUN = False

            if len(current_line) > 0:
                ChangableTiles.extend(current_line)

        return ChangableTiles



    def addCurPlayerToken(self, grid, curPlayer, y, x):
        curPlayerTokenImage = self.white if curPlayer == 1 else self.black
        self.tokens[(y, x)] = Token(curPlayer, y, x, curPlayerTokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

    def transition(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.whiteToBlack, self.white)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.blackToWhite, self.black)


class Token:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.pos_x = 80 + (gridY * 80)
        self.pos_y = 80 + (gridX * 80)
        self.GAME = main

        self.image = image

    def transition(self, transitionImages, curPlayerTokenImage):
        for i in range(30):
            self.image =  transitionImages[i // 10]
            self.GAME.renderGameOnScreen()
        self.image = curPlayerTokenImage

    def renderGameOnScreen(self, window):
        window.blit(self.image, (self.pos_x, self.pos_y))

#  utility functions
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Check to determine which directions are valid from current cell"""
    AvailableDirections = []

    # left
    if x != minX:
        AvailableDirections.append((x - 1, y))

    # right
    if x != maxX:
        AvailableDirections.append((x + 1, y))

    # down direction
    if y != minY:
        AvailableDirections.append((x, y - 1))

    # up direction
    if y != maxY:
        AvailableDirections.append((x, y + 1))

    return AvailableDirections

def loadScaledImage(path, size):
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, new_size, size):
    image = pygame.Surface((33, 33)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, new_size)
    image.set_colorkey('Black')
    return image


# Adequate Utility Function : 
# calculates the score of each player based on the current state of the game grid
def calculateScore(grid, player):
    calculatedScore = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            calculatedScore -= col
    return calculatedScore

#Game Controller 
#serves as the game controller. It organizes the game by handling user input, 
# updating the game state, rendering the game on the screen,
# and controlling the flow of the game
class mainGameClass:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('Othello Game')

        self.firstPlayer = 1 # you  
        self.secondPlayer = -1 # the computer 
        self.currPlayer = 1
        self.time = 0
        self.rows = 8
        self.cols = 8
        self.endGame = True
        self.grid = Grid(self.rows, self.cols, (80, 80), self)
        self.AI_Player = ComputerPlayer(self.grid)

        self.Run = True
        self.difficulty = "medium"  # Default difficulty is set to medium 

    def runGame(self):
        while self.Run:
            self.handleUserInput()
            self.updateGameState()
            self.renderGameOnScreen()

    def handleUserInput(self):
        for event in pygame.event.get():
            # Check if the user quits the game
            if event.type == pygame.QUIT:
                self.Run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left mouse button (button 1) is clicked
                if event.button == 1:
                    if self.currPlayer == 1 and not self.endGame:
                        x, y = pygame.mouse.get_pos()
                        x, y = (x - 80) // 80, (y - 80) // 80
                        availableMovesCells = self.grid.availableMoves(self.grid.gridLogic, self.currPlayer)
                        if not availableMovesCells:
                            pass
                        else:
                            if (y, x) in availableMovesCells:
                                self.grid.addCurPlayerToken(self.grid.gridLogic, self.currPlayer, y, x)
                                ChangableTiles = self.grid.ChangableTiles(y, x, self.grid.gridLogic, self.currPlayer)
                                for tile in ChangableTiles:
                                    self.grid.transition(tile, self.currPlayer)
                                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                                self.currPlayer *= -1
                                self.time = pygame.time.get_ticks()
                    if self.endGame:
                        x, y = pygame.mouse.get_pos()
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.startNewGame()
                            self.endGame = False

    def updateGameState(self):
        if self.currPlayer == -1:
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 100:
                if not self.grid.availableMoves(self.grid.gridLogic, self.currPlayer):
                    self.endGame = True
                    return
                # Adjust depth based on difficulty level
                if self.difficulty == "easy":
                    depth = 1
                elif self.difficulty == "medium":
                    depth = 4
                elif self.difficulty == "hard":
                    depth = 7
                cell, score = self.AI_Player.findBestMoveWithAlphaBeta(self.grid.gridLogic, depth, -64, 64, -1)
                self.grid.addCurPlayerToken(self.grid.gridLogic, self.currPlayer, cell[0], cell[1])
                ChangableTiles = self.grid.ChangableTiles(cell[0], cell[1], self.grid.gridLogic, self.currPlayer)
                for tile in ChangableTiles:
                    self.grid.transition(tile, self.currPlayer)
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                self.currPlayer *= -1
        self.grid.firstPlayerScore = self.grid.calcPlyerScore(self.firstPlayer)
        self.grid.secondPlayerScore = self.grid.calcPlyerScore(self.secondPlayer)
        if not self.grid.availableMoves(self.grid.gridLogic, self.currPlayer):
            self.endGame = True
            return

    def renderGameOnScreen(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()



class ComputerPlayer:
    def __init__(self, grid_object):
        self.grid = grid_object

# Alpha-Beta Pruning Algorithm Implementation

# Support for Different Difficulty Levels:
    def findBestMoveWithAlphaBeta(self, grid, depth, alpha, beta, player):
        tempGrid = copy.deepcopy(grid)
        availableMoves = self.grid.availableMoves(tempGrid, player)

        if depth == 0 or len(availableMoves) == 0:
            bestAvailablemove, Score = None, calculateScore(grid, player)
            return bestAvailablemove, Score

        if player < 0:
            highestScore = -64
            bestAvailablemove = None

            for move in availableMoves:
                x, y = move
                ChangableTiles = self.grid.ChangableTiles(x, y, tempGrid, player)
                tempGrid[x][y] = player
                for tile in ChangableTiles:
                    tempGrid[tile[0]][tile[1]] = player

                b_move, value = self.findBestMoveWithAlphaBeta(tempGrid, depth-1, alpha, beta, player *-1)

                if value > highestScore:
                    highestScore = value
                    bestAvailablemove = move
                alpha = max(alpha, highestScore)
                if beta <= alpha:
                    break

                tempGrid = copy.deepcopy(grid)
            return bestAvailablemove, highestScore

        if player > 0:
            highestScore = 64
            bestAvailablemove = None

            for move in availableMoves:
                x, y = move
                ChangableTiles = self.grid.ChangableTiles(x, y, tempGrid, player)
                tempGrid[x][y] = player
                for tile in ChangableTiles:
                    tempGrid[tile[0]][tile[1]] = player

                b_move, value = self.findBestMoveWithAlphaBeta(tempGrid, depth-1, alpha, beta, player)

                if value < highestScore:
                    highestScore = value
                    bestAvailablemove = move
                beta = min(beta, highestScore)
                if beta <= alpha:
                    break

                tempGrid = copy.deepcopy(grid)
            return bestAvailablemove, highestScore

if __name__ == '__main__':
    game = mainGameClass()
    game.runGame()
    pygame.quit()

import pygame as pg
from settings import *


class Tile:
    changing = False
    changingTilesID = []

    def setNum(self, num):
        self.num = num
        self.numColor = NUM_COLORS[num]
        string = str(num)
        font_size = int(350 / (len(string) + 4))
        self.font = pg.font.Font("ClearSans-Bold.ttf", font_size)
        width, height = self.font.size(string)
        self.numSurface = self.font.render(string, True, self.numColor)
        self.numRelX = (TILE_DRAW_SIZE - width) / 2
        self.numRelY = (TILE_DRAW_SIZE - height) / 2

    def updateGrow(self):
        self.width += (self.targetWidth - self.width) * min(TILE_GROW_SPEED * self.game.dt, 1)
        self.numAlpha = int(self.width / self.targetWidth * 255)
        if abs(self.width - self.targetWidth) < STOP_GROW_WIDTH:
            self.width = 0
            self.numAlpha = 255
            Tile.changingTilesRemove(id(self))
            self.updateFunctions.remove(self.updateGrow)
        self.numSurface.set_alpha(self.numAlpha)

    def updateMove(self):
        self.x += (self.targetX - self.x) * min(TILE_MOVE_SPEED * self.game.dt, 1)
        self.y += (self.targetY - self.y) * min(TILE_MOVE_SPEED * self.game.dt, 1)
        if abs(self.x - self.targetX) < STOP_MOVE_DISTANCE and abs(self.y - self.targetY) < STOP_MOVE_DISTANCE:
            self.x = self.targetX
            self.y = self.targetY
            Tile.changingTilesRemove(id(self))
            self.updateFunctions.remove(self.updateMove)
        self.rect.x = self.x + TILE_PADDING
        self.rect.y = self.y + TILE_PADDING

    def drawNormal(self, screen):
        pg.draw.rect(screen, self.tileColor, self.rect, border_radius=TILE_BORDER_RADIUS, width=int(self.width))
        screen.blit(self.numSurface, (self.rect.x + self.numRelX, self.rect.y + self.numRelY))

    def __init__(self, game, i, j, num):
        self.game = game
        self.tileColor = TILE_COLORS[num]
        self.i = i
        self.j = j
        self.x = self.j * TILE_SIZE
        self.y = self.i * TILE_SIZE
        self.rect = pg.Rect(self.x + TILE_PADDING, self.y + TILE_PADDING, TILE_DRAW_SIZE, TILE_DRAW_SIZE)

        pg.font.init()
        self.numAlpha = 255
        self.setNum(num)

        self.width = 1
        self.targetWidth = TILE_DRAW_SIZE / 2
        self.numAlpha = 0
        Tile.changing = True
        Tile.changingTilesAppend(id(self))

        self.updateFunctions = [self.updateGrow]
        self.drawFunctions = [self.drawNormal]

    def update(self):
        for f in self.updateFunctions:
            f()

    def draw(self, screen):
        for f in self.drawFunctions:
            f(screen)

    """
    def destroyFunction(self, attr):
        def inner():
            self.updateFunctions.remove(getattr(self, attr).update)
            self.drawFunctions.remove(getattr(self, attr).draw)
            getattr(self, attr) = None
        return inner
    """

    def destroyMergeTile(self):
        self.updateFunctions.remove(self.mergeTile.update)
        self.drawFunctions.remove(self.mergeTile.draw)
        self.mergeTile = None

    def destroyIndicator(self):
        self.updateFunctions.remove(self.indicator.update)
        self.drawFunctions.remove(self.indicator.draw)
        self.indicator = None

    def move(self, moveI, moveJ):
        self.i = moveI
        self.j = moveJ
        Tile.changing = True
        Tile.changingTilesAppend(id(self))
        self.targetX = self.j * TILE_SIZE
        self.targetY = self.i * TILE_SIZE

        self.updateFunctions.append(self.updateMove)

    def increase(self, newNum, otherI, otherJ):
        self.mergeTile = MergeTile(self.game, otherI, otherJ, self.num, self.i, self.j, self.destroyMergeTile)
        self.indicator = Indicator(self.game, self.tileColor, self.i, self.j, self.destroyIndicator)
        self.tileColor = TILE_COLORS[newNum]
        self.setNum(newNum)

        self.updateFunctions.insert(0, self.mergeTile.update)
        self.updateFunctions.insert(0, self.indicator.update)
        self.drawFunctions.insert(0, self.mergeTile.draw)
        self.drawFunctions.insert(0, self.indicator.draw)

    @classmethod
    def changingTilesAppend(cls, id):
        cls.changingTilesID.append(id)

    @classmethod
    def changingTilesRemove(cls, id):
        cls.changingTilesID.remove(id)
        if len(cls.changingTilesID) == 0:
            cls.changing = False

    @staticmethod
    def drawBlankTile(screen, i, j):
        rect = pg.Rect(j * TILE_SIZE + TILE_PADDING, i * TILE_SIZE + TILE_PADDING, TILE_DRAW_SIZE, TILE_DRAW_SIZE)
        pg.draw.rect(screen, BLANK_TILE_COLOR, rect, border_radius=TILE_BORDER_RADIUS)

    @staticmethod
    def updateWithKey(gridTiles, key):
        if Tile.changing:
            return False
        tilesToIncrease = []
        if key == pg.K_LEFT or key == pg.K_a:
            for row in range(GRID_SIZE):
                moveCol = 0
                for col in range(1, GRID_SIZE):
                    curTile = gridTiles[row][col]
                    moveTile = gridTiles[row][moveCol]
                    if not curTile:
                        continue
                    if moveTile:
                        moveCol += 1
                        if moveTile.num == curTile.num:
                            tilesToIncrease.append((moveTile, row, col))
                            gridTiles[row][col] = None
                            continue
                    if moveCol == col:
                        continue
                    gridTiles[row][moveCol] = curTile
                    gridTiles[row][col] = None
                    curTile.move(row, moveCol)
        if key == pg.K_RIGHT or key == pg.K_d:
            for row in range(GRID_SIZE):
                moveCol = GRID_SIZE - 1
                for col in range(GRID_SIZE - 2, -1, -1):
                    curTile = gridTiles[row][col]
                    moveTile = gridTiles[row][moveCol]
                    if not curTile:
                        continue
                    if moveTile:
                        moveCol -= 1
                        if moveTile.num == curTile.num:
                            tilesToIncrease.append((moveTile, row, col))
                            gridTiles[row][col] = None
                            continue
                    if moveCol == col:
                        continue
                    gridTiles[row][moveCol] = curTile
                    gridTiles[row][col] = None
                    curTile.move(row, moveCol)
        if key == pg.K_UP or key == pg.K_w:
            for col in range(GRID_SIZE):
                moveRow = 0
                for row in range(1, GRID_SIZE):
                    curTile = gridTiles[row][col]
                    moveTile = gridTiles[moveRow][col]
                    if not curTile:
                        continue
                    if moveTile:
                        moveRow += 1
                        if moveTile.num == curTile.num:
                            tilesToIncrease.append((moveTile, row, col))
                            gridTiles[row][col] = None
                            continue
                    if moveRow == row:
                        continue
                    gridTiles[moveRow][col] = curTile
                    gridTiles[row][col] = None
                    curTile.move(moveRow, col)
        if key == pg.K_DOWN or key == pg.K_s:
            for col in range(GRID_SIZE):
                moveRow = GRID_SIZE - 1
                for row in range(GRID_SIZE - 2, -1, -1):
                    curTile = gridTiles[row][col]
                    moveTile = gridTiles[moveRow][col]
                    if not curTile:
                        continue
                    if moveTile:
                        moveRow -= 1
                        if moveTile.num == curTile.num:
                            tilesToIncrease.append((moveTile, row, col))
                            gridTiles[row][col] = None
                            continue
                    if moveRow == row:
                        continue
                    gridTiles[moveRow][col] = curTile
                    gridTiles[row][col] = None
                    curTile.move(moveRow, col)
        for tile, otherRow, otherCol in tilesToIncrease:
            tile.increase(tile.num * 2, otherRow, otherCol)
        if Tile.changing:
            return True
        return False

class MergeTile:
    def __init__(self, game, i, j, num, targetI, targetJ, destroyCallback):
        self.game = game
        self.x = j * TILE_SIZE
        self.y = i * TILE_SIZE
        self.rect = pg.Rect(self.x + TILE_PADDING, self.y + TILE_PADDING, TILE_DRAW_SIZE, TILE_DRAW_SIZE)
        self.tileColor = TILE_COLORS[num]
        Tile.changingTilesAppend(id(self))

        self.numColor = NUM_COLORS[num]
        string = str(num)
        font_size = int(350 / (len(string) + 4))
        font = pg.font.Font("ClearSans-Bold.ttf", font_size)
        width, height = font.size(string)
        self.numSurface = font.render(string, True, self.numColor)
        self.numRelX = (TILE_DRAW_SIZE - width) / 2
        self.numRelY = (TILE_DRAW_SIZE - height) / 2

        self.targetX = targetJ * TILE_SIZE
        self.targetY = targetI * TILE_SIZE
        self.destroyCallback = destroyCallback

    def update(self):
        self.x += (self.targetX - self.x) * min(TILE_MOVE_SPEED * self.game.dt, 1)
        self.y += (self.targetY - self.y) * min(TILE_MOVE_SPEED * self.game.dt, 1)
        if abs(self.x - self.targetX) < STOP_MOVE_DISTANCE and abs(self.y - self.targetY) < STOP_MOVE_DISTANCE:
            Tile.changingTilesRemove(id(self))
            self.destroyCallback()
        self.rect.x = self.x + TILE_PADDING
        self.rect.y = self.y + TILE_PADDING

    def draw(self, screen):
        pg.draw.rect(screen, self.tileColor, self.rect, border_radius=TILE_BORDER_RADIUS)
        screen.blit(self.numSurface, (self.rect.x + self.numRelX, self.rect.y + self.numRelY))


class Indicator:
    def recenter(self):
        self.rect.x = self.x + TILE_PADDING + (TILE_DRAW_SIZE - self.size) / 2
        self.rect.y = self.y + TILE_PADDING + (TILE_DRAW_SIZE - self.size) / 2
        self.rect.width = self.size
        self.rect.height = self.size

    def __init__(self, game, color, i, j, destroyCallback):
        self.game = game
        self.color = color
        self.i = i
        self.j = j
        self.x = self.j * TILE_SIZE
        self.y = self.i * TILE_SIZE
        self.size = TILE_DRAW_SIZE
        self.rect = pg.Rect(self.x + TILE_PADDING, self.y + TILE_PADDING, self.size, self.size)
        self.width = TILE_DRAW_SIZE / 2
        self.targetWidth = 1
        Tile.changing = True
        Tile.changingTilesAppend(id(self))
        self.destroyCallback = destroyCallback

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, border_radius=TILE_BORDER_RADIUS, width=int(self.width))

    def update(self):
        self.width += (self.targetWidth - self.width) * min(TILE_GROW_SPEED * self.game.dt, 1)
        if abs(self.width - self.targetWidth) < STOP_GROW_WIDTH:
            Tile.changingTilesRemove(id(self))
            self.destroyCallback()
        self.size += INDICATOR_SIZE_CHANGE
        self.recenter()

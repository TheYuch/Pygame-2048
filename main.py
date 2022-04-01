import pygame as pg
import sys
from random import randint
from settings import *
from sprites import *

class Game:
    def __init__(self):
        self.gridTiles = [[None for column in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.eventsFunction = self.events
        self.updateFunction = self.update
        self.drawFunction = self.draw

    def gameOver(self):
        self.gameOverSurface = pg.Surface((WIDTH, HEIGHT))
        self.gameOverSurface.set_alpha(GAME_OVER_START_ALPHA)
        self.gameOverSurface.fill(GAME_OVER_COLOR)
        self.gameOverBlitCount = GAME_OVER_BLIT_COUNT
        self.eventsFunction = self.eventsWhileGameOver
        self.updateFunction = self.updateWhileGameOver
        self.drawFunction = self.drawWhileGameOver

    def checkGameOver(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 1):
                cur = self.gridTiles[row][col].num
                next = self.gridTiles[row][col + 1].num
                if cur and next and cur == next:
                    return
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 1):
                cur = self.gridTiles[row][col].num
                next = self.gridTiles[row + 1][col].num
                if cur and next and cur == next:
                    return
        self.gameOver()

    def spawnTiles(self, nums):
        available = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if not self.gridTiles[row][col]:
                    available.append((row, col))

        for num in nums:
            tile = randint(0, len(available) - 1)
            self.gridTiles[available[tile][0]][available[tile][1]] = Tile(self, available[tile][0], available[tile][1], num)
            del available[tile]

        if len(available) == 0:
            self.checkGameOver()

    def spawnRandTiles(self):
        if randint(1, 5) == 1:
            self.spawnTiles([4])
        else:
            self.spawnTiles([2])

    def new(self):
        #self.spawnTiles([pow(2, 10) for _ in range(16)])
        self.spawnTiles([2, 2])

    def run(self):  # end game by setting self.playing = False
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.eventsFunction()
            self.updateFunction()
            self.drawFunction()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        for tiles in self.gridTiles:
            for tile in tiles:
                if tile:
                    tile.update()

    def updateWhileGameOver(self):
        if Tile.changing:
            self.update()
            self.draw()

    def draw(self):
        self.screen.fill(BG_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                Tile.drawBlankTile(self.screen, row, col)
        for tiles in self.gridTiles:
            for tile in tiles:
                if tile:
                    tile.draw(self.screen)
        pg.display.flip()

    def drawWhileGameOver(self):
        if Tile.changing:
            return

        if self.gameOverBlitCount > 0:
            self.gameOverBlitCount -= 1
            self.screen.blit(self.gameOverSurface, (0, 0))
            pg.display.flip()
        elif self.gameOverBlitCount == 0:
            font = pg.font.Font("ClearSans-Bold.ttf", GAME_OVER_FONT_SIZE)
            width, height = font.size(GAME_OVER_TEXT)
            textSurface = font.render(GAME_OVER_TEXT, True, GAME_OVER_TEXT_COLOR)
            self.screen.blit(textSurface, ((WIDTH - width) / 2, (HEIGHT - height) / 2))
            pg.display.flip()
        else:
            self.playing = False

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                else:
                    if Tile.updateWithKey(self.gridTiles, event.key):
                        self.spawnRandTiles()

    def eventsWhileGameOver(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.quit()

g = Game()
g.new()
g.run()
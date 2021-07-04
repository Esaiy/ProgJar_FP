import pygame as p
import GameEngine
    
BOARD_HEIGHT = 512
BOARD_WIDTH = 512
FRAME_HEIGHT = 600
FRAME_WIDTH = 2 * BOARD_WIDTH + 80
MARGIN_LEFT_ATTACK = 40 + BOARD_WIDTH 
MARGIN_TOP = (FRAME_HEIGHT - BOARD_HEIGHT) / 2
MARGIN_LEFT = 20
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

class Game():
    def loadImages(self):
        pieces = ['1v', '1h', '2v', '2h', '3v', '3h', '5v', '5h']
        for piece in pieces:
            h = 1
            w = int(piece[0])
            if piece[1] == 'v':
                h = w
                w = 1
            IMAGES[piece] = (p.transform.scale(p.image.load('images/' + piece + '.png'), (w * SQ_SIZE, h * SQ_SIZE)), w , h)

    def __init__(self):
        p.init()
        self.clock = p.time.Clock()
        self.screen = p.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
        self.screen.fill(p.Color('white'))
        self.gs = GameEngine.GameState()
        self.loadImages()

        self.placeShip()
        # Kirim ke server board nya
        self.attackState()

        self.running = True
        while self.running:
            self.drawAttackState(self.screen)
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.running = False

    def placeShip(self):
        shipSelected = ()
        playerClicks = []
        rotation = False
        start_ticks=p.time.get_ticks()
        placeShipTime = True
        font = p.font.SysFont('Consolas', 30)
        while placeShipTime:
            seconds=(p.time.get_ticks()-start_ticks) // 1000
            if seconds > 10:
                placeShipTime = False
                print("Time Up")
                break
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.placeShipTime = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if self.inBoard(location):
                        col = int((location[0] - MARGIN_LEFT) // SQ_SIZE)
                        row = int((location[1] - MARGIN_TOP) // SQ_SIZE)
                        if shipSelected == ():
                            piece = self.gs.board[row][col]
                            if piece != '--':
                                shipSelected = (row, col)
                                playerClicks.append(shipSelected)
                                print(playerClicks)
                        elif shipSelected == (row, col):
                            shipSelected = ()
                            playerClicks = []
                        elif shipSelected:
                            shipSelected = (row, col)
                            playerClicks.append(shipSelected)
                            print(playerClicks)

                        if len(playerClicks) == 2:
                            print('move')
                            move = GameEngine.Move(playerClicks[0], playerClicks[1], rotation, self.gs.board)
                            print(move.pieceMoved)
                            self.gs.makeMove(move)
                            shipSelected = ()
                            playerClicks = []
                            rotation = False
                            for i in self.gs.board:
                                 print(i)

                elif e.type == p.KEYDOWN:
                    if e.key == p.K_f:
                        print("hello")
                        if shipSelected:
                            rotation = not rotation

            # self.screen.blit(font.render(str(seconds), True, (0,0,0)), (0, 0))
            self.drawPlaceState(self.screen, self.gs)
            self.clock.tick(MAX_FPS)
            p.display.flip()

    def inBoard(self, location):
        if location[0] > MARGIN_LEFT and location[1] > MARGIN_TOP and location[1] < MARGIN_TOP + BOARD_WIDTH and location[1] < MARGIN_TOP + BOARD_HEIGHT:
            return True
    
    def drawAttackState(self, screen):
        colors = [p.Color(51,152,255), p.Color(153,204,255)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[((row + column) % 2)]
                p.draw.rect(screen, color, p.Rect(MARGIN_LEFT_ATTACK + column * SQ_SIZE, MARGIN_TOP + row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


    def drawPlaceState(self, screen, gs):
        self.drawBoard(screen)
        self.drawShip(screen, gs.board)

    def drawBoard(self, screen):
        colors = [p.Color(51,152,255), p.Color(153,204,255)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[((row + column) % 2)]
                p.draw.rect(screen, color, p.Rect(MARGIN_LEFT + column * SQ_SIZE, MARGIN_TOP + row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def drawShip(self, screen, board):
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                piece = board[row][column]
                if piece != '--':
                    screen.blit(IMAGES[piece][0], p.Rect(MARGIN_LEFT + column * SQ_SIZE, MARGIN_TOP + row * SQ_SIZE, IMAGES[piece][1] * SQ_SIZE, IMAGES[piece][2] *SQ_SIZE))


game = Game()
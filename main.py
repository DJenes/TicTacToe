import os
import sys
import numpy as np
import logging
import time
from logging import config


class FileFilter:

    def __call__(self, log):
        if log.levelno == logging.DEBUG:
            return 1
        else:
            return 0


logging_config = {
    'version': 1,
    'formatters': {
        'debug_formatter': {
            'format': '{asctime} - {name} - {message}',
            'style': '{',
            'datefmt': '%d/%m/%y - %H:%M',
        },
    },
    'filters': {
        'file_filter': {
            '()': FileFilter,
        },
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'debug_formatter',
        },

        'debug_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'debug_formatter',
            'filters': ['file_filter'],
            'filename': 'win.log',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console_handler', 'debug_handler'],
    },
}
config.dictConfig(logging_config)

logger = logging.getLogger(__name__)


class TicTacToe:

    def __init__(self):

        self.GameNotWon = True
        self.TurnPl = 1
        self.playerName1 = ''
        self.playerName2 = ''
        self.MultipleGameFlag = False
        self.WinsCount = {}

    def CreateBoard(self, N):
        self.N = int(N)
        self.GameBoard = np.zeros((self.N, self.N))
        return self.GameBoard

    def MakeTurn(self):
        if self.TurnPl == 1:
            logging.info(f"It's {self.playerName1}'s turn. Enter Coordinates of your move :")
        else:
            logging.info(f"It's {self.playerName2}'s turn. Enter Coordinates of your move :")
        print(self.GameBoard)
        if self.TurnPl:
            self.CurrentMv = 1
        else:
            self.CurrentMv = -1

        if self.GameNotWon:
            move = input().split(",")
            move[0], move[1] = int(move[0]), int(move[1])
            try:
                self.GameBoard[move[0], move[1]] = self.CurrentMv
            except ValueError:
                logging.error("Invalid move.")
                raise
            except IndexError:
                logging.error("Invalid Index.")
                raise
            except Exception:
                logging.error("Error occurred.")
                raise
            else:
                self.TurnPl = not self.TurnPl

    def CheckForWin(self):
        self.RowsSum = np.ndarray.sum(self.GameBoard, axis=1)
        self.ColumsSum = np.ndarray.sum(self.GameBoard, axis=0)
        self.MainDiagonal = np.trace(self.GameBoard, offset=0, axis1=0, axis2=1)
        self.AntiDiagonal = np.sum(np.flipud(self.GameBoard).diagonal())

        #Player 1 win
        if (self.RowsSum == self.N).sum() > 0 or \
           (self.ColumsSum == self.N).sum() > 0 or \
           self.MainDiagonal == self.N or \
           self.AntiDiagonal == self.N:

            logging.debug(f"{self.playerName1} won!")
            self.WinsCount[self.playerName1] += 1
            if self.MultipleGameFlag is True:
                logger.info(f"{self.WinsCount}")

            self.GameNotWon = False


        #Player 2 win
        if (self.RowsSum == -self.N).sum() > 0 or \
           (self.ColumsSum == -self.N).sum() > 0 or \
            self.MainDiagonal == - self.N or \
            self.AntiDiagonal == - self.N:

                logging.debug(f"{self.playerName2} won!")
                self.GameNotWon = False
                self.WinsCount[self.playerName2] += 1
                if self.MultipleGameFlag is True:
                    logger.info(f"{self.WinsCount}")

        if (self.GameBoard == 0).sum() == 0 and self.GameNotWon:
            logging.debug("It's a tie")
            self.GameNotWon = False


def StartGame(GameInst):

    while GameInst.GameNotWon is True:
        GameInst.MakeTurn()
        GameInst.CheckForWin()
    if GameInst.GameNotWon is False:

        flagInp = input("Play one more round?(Yes/No) ")
        if flagInp == "Yes":
            GameInst.MultipleGameFlag = True
            GameInst.GameNotWon = True
            GameInst.CreateBoard(int(GameInst.N))
            StartGame(GameInst)

        else:
            time.sleep(1)
            main()


def ShowLog():
    if os.stat("win.log").st_size == 0:
        logger.error("Log is Empty")
        time.sleep(1)
        main()
    else:
        with open('win.log', 'r') as viewFileOpen:
            data = viewFileOpen.read()
        print(data)
        time.sleep(1)
        main()


def DeleteLog():
    with open('win.log', 'w'):
        pass
    time.sleep(1)
    main()


def main():

    flag = input("""
        1. Play
        2. Show log of victories
        3. Delete log of victories
        4. Exit
        
        Enter number of command:
         """)
    if flag == "1":
        Game1 = TicTacToe()
        Game1.playerName1 = input('Enter name of the first player: ')
        Game1.playerName2 = input('Enter name of the second player: ')
        Game1.N = input("Enter size of the board: ")
        Game1.TurnPl = 1
        Game1.WinsCount = {Game1.playerName1: 0,
                              Game1.playerName2: 0}
        Game1.CreateBoard(int(Game1.N))
        StartGame(Game1)
    elif flag == "2":
        ShowLog()
    elif flag == "3":
        DeleteLog()
    elif flag == "4":
        sys.exit()


if __name__ == '__main__':
    main()



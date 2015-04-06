# from os import listdir
# for filename in listdir("."):
#     try:
#         if filename[-9:] == "Player.py":
#             player = "from strategy." + filename[:-3] + " import " + filename[:-3]
#             exec(player)
#     except ImportError:
#         print("Could not execute \"from " + filename[:-3] + " import " + filename[:-3] + "\"")
#         print("The file name and the class must be the same.")
from strategy.BluePlayer import BluePlayer
from strategy.GreenPlayer import GreenPlayer
from strategy.HumanPlayer import HumanPlayer
from strategy.PlayPlayer import PlayPlayer
from strategy.BurnPlayer import BurnPlayer
from strategy.CheapPlayer import CheapPlayer
from strategy.RedPlayer import RedPlayer
from strategy.RandomPlayer import RandomPlayer
from strategy.MaterialPlayer import MaterialPlayer
from strategy.TemplatePlayer import TemplatePlayer
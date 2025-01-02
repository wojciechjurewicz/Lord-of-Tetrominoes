import os
import pickle
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
path = config['GameSettings']['HighscoresPath']

class Leaderboards:
    def __init__(self):
        if not os.path.exists(path):
            self.highestscores = [0, 0, 0]
        else:
            with open(path, 'rb') as file:
                self.highestscores = pickle.load(file)

    def add_score(self, score):
        if score > self.highestscores[-1]:
            self.highestscores[-1] = score
            self.highestscores.sort(reverse=True)

    def save(self):
        with open(path, 'wb') as file:
            pickle.dump(self.highestscores, file)


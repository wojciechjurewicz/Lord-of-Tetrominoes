import os
import pickle
import configparser

# Config loading
config = configparser.ConfigParser()
config.read('config.ini')
path = config['GameSettings']['HighscoresPath']


class Leaderboards:
    def __init__(self):
        # Load the leaderboards, and create a new one if it doesnt exist
        if not os.path.exists(path):
            self.highestscores = [0, 0, 0]
        else:
            with open(path, 'rb') as file:
                self.highestscores = pickle.load(file)

    # Add new score to the leaderboards
    def add_score(self, score):
        if score > self.highestscores[-1]:
            self.highestscores[-1] = score
            self.highestscores.sort(reverse=True)

    # Save the leaderboards to a file
    def save(self):
        with open(path, 'wb') as file:
            pickle.dump(self.highestscores, file)

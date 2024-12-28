import configparser

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    board_width = int(config['BoardSettings']['Width'])
    board_height = int(config['BoardSettings']['Height']) + int(config['BoardSettings']['SafeZoneHeight'])
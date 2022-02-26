from getData import *
from DataTypes import *

if __name__ == "__main__":
    data = load_data_from_pkl("timelines_bronze.pkl")
    all_types = set()
    for game in data:
        team = User(game)
        print("num of types: ", len(all_types))

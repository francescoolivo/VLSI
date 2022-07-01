import argparse
import os
import pandas as pd

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dir",
                        help="The directory storing the results",
                        required=False, type=str, default="out")

    args = parser.parse_args()

    frames = []

    for rotation in os.listdir(args.dir):
        rotation_dir = os.path.join(args.dir, rotation)
        for sorting in os.listdir(rotation_dir):
            sorting_dir = os.path.join(rotation_dir, sorting)
            for search_goal in os.listdir(sorting_dir):
                search_goal_dir = os.path.join(sorting_dir, search_goal)
                for search_type in os.listdir(search_goal_dir):
                    search_type_dir = os.path.join(search_goal_dir, search_type)
                    print(rotation, sorting, search_goal, search_type)

                    temp = pd.read_csv(os.path.join(search_type_dir, "solutions.csv"))
                    temp['rotation'] = rotation
                    temp['sorting'] = sorting
                    temp['search_goal'] = search_goal
                    temp['search_type'] = search_type

                    frames.append(temp)

    df = pd.concat(frames)

    df.to_csv("performances.csv")

if __name__ == '__main__':
    main()
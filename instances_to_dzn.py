import argparse
import os
import re


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_dir", help="Path to the directory containing the txt instances",
                        required=True, type=str)
    parser.add_argument("-o", "--output_dir", help="Path to the new directory containing the dzn instances",
                        required=True, type=str)

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    directory = args.input_dir
    files = os.listdir(directory)

    for file in files:
        file = os.path.join(directory, file)
        if ".dzn" in file:
            continue
        number_re = re.compile(r".*ins-(\d+).txt")
        number = int(number_re.match(file).group(1))
        # file_dest_name = file.replace(".txt", ".dzn")
        file_dest_name = os.path.join(args.output_dir, f"ins-{number:02d}.dzn")

        f = open(file, "r")
        w = f.readline().strip()
        n = f.readline().strip()

        sizes = []
        for line in f.readlines():
            x1 = line.split()[0]
            x2 = line.split()[1]

            sizes.append((x1, x2))

        f.close()

        new = open(file_dest_name, "w")
        new.write(f"w={w};\nn={n};\ncircuits=[|\n")
        for size in sizes:
            new.write(f"{size[0]}, {size[1]}|\n")
        new.write("|];")
        new.close()

if __name__ == "__main__":

    main()




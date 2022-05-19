import os
import re
import sys

if __name__ == "__main__":

    directory = sys.argv[1]

    os.chdir(directory)

    files = os.listdir(directory)

    for file in files:
        if ".dzn" in file:
            continue
        number_re = re.compile(r"ins-(\d+).txt")
        number = int(number_re.match(file).group(1))
        # file_dest_name = file.replace(".txt", ".dzn")
        file_dest_name = f"ins-{number:02d}.dzn"

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


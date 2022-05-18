import os

dir = "/home/francescoolivo/Documents/Unibo/Master/CDMO/instances"

os.chdir(dir)

files = os.listdir(dir)

for file in files:
    file_dest_name = file.replace(".txt", ".dzn")

    f = open(file, "r")
    w = f.readline().strip()
    n = f.readline().strip()

    sizes = []
    for line in f.readlines():
        x1 = line.split()[0]
        x2 = line.split()[1]

        sizes.append((x1, x2))

    new = open(file_dest_name, "w")
    new.write(f"w={w};\nn={n};\nsizes=[|\n")
    for size in sizes:
        new.write(f"{size[0]}, {size[1]}|\n")
    new.write("|];")
    new.close()


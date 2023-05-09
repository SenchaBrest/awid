import glob

files_path = "*.txt"
output_file = "all.txt"
files = glob.glob(files_path)

with open(output_file, "w", encoding="utf-8") as outfile:
    for f in files:
        with open(f, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(f"{f}\t{line}")

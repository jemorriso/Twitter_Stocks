import sys
import os
import pathlib
import subprocess

if len(sys.argv) > 1:
    query = sys.argv[1].split()

    if "-o" in query:
        output_file = query[query.index("-o") + 1]

        print(pathlib.Path(__file__).parent.absolute())
        # call subscripts
        subprocess.call(["python", "./ts.py", sys.argv[1]])
        subprocess.call(["python", "./dataframe.py", output_file])

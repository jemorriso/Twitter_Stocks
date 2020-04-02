import sys
import pathlib
import subprocess

# scrape all the tweets in the query and output to csv
def twitterscraper_to_csv(cmd_args):
    query = cmd_args[1].split()

    if "-o" in query:
        output_file = query[query.index("-o") + 1]

        print(pathlib.Path(__file__).parent.absolute())
        # call subscripts
        subprocess.call(["python", "./ts.py", cmd_args[1]])
        subprocess.call(["python", "./dataframe.py", output_file])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        twitterscraper_to_csv(sys.argv)

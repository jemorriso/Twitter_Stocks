import os
import sys
import json

# sys.argv[1] is the query string
if (len(sys.argv) > 1):
  query = sys.argv[1].split()
  query_string = sys.argv[1]
  output_file = None

  # save output file, rmeove it to overwrite to tweets.json
  if "-o" in query:
    output_file = query[query.index("-o") + 1] 
    query.remove('-o')
    query.remove(output_file)
    # turn it back into a string
    query_string = ' '.join(query)
  # overwrite to default tweets.json
  os.system(query_string + " -ow")

  # load json data
  with open('tweets.json') as tweets_file:
    tweets_dict = json.load(tweets_file)

  # export indented json to named file
  if output_file: 
    with open(output_file, 'w') as outfile:
      json.dump(tweets_dict, outfile, indent=2)


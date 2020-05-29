from elasticsearch import Elasticsearch
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-S", "--server", help="defines ELK server to query", default="localhost")
parser.add_argument("-i", "--index", help="defines index to query")
parser.add_argument("-f", "--field", help="defines the field to print", default="none")
parser.add_argument("-t", "--time", help="defines the amount of time to look back at", default="15m")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--size", help="defines the number of records to pull", default=0)
group.add_argument("-a", "--aggregate", help="defines what aggregation to use")

args = parser.parse_args()

server = args.server
log_index = args.index
field =  args.field
time = args.time
doc_size = int(args.size)

def print_size(data, filter):
  for f in data["hits"]["hits"]:
    if field == "none":
      json_object = f["_source"]
      json_formatted_str = json.dumps(json_object, indent=2)
      print(json_formatted_str)
    else:
      print(f["_source"][filter])


es = Elasticsearch(hosts=[server])

#print(time)

query_body = {
  "query": {
    "bool": {
      "must": {
        "query_string": {
          "query": "*",
          "analyze_wildcard": "true"
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                    "from": f"now-{time}",
                    "to":  "now"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  }
}

response = es.search(index=log_index, body=query_body, size=doc_size)
#print(response)

if doc_size > 0:
  print_size(response, field)
elif doc_size == 0:
  print("Function on the way")
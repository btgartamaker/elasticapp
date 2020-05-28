from elasticsearch import Elasticsearch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-S", "--server", help="defines ELK server to query")
parser.add_argument("-i", "--index", help="defines index to query")
parser.add_argument("-f", "--field", help="defines the field to print")
args = parser.parse_args()

server = args.server
log_index = args.index
field =  args.field


es = Elasticsearch(hosts=[server])

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
                    "from": "now-5m",
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

response = es.search(index=log_index, body=query_body, size="15")


for f in response["hits"]["hits"]:
    print(f["_source"][field])

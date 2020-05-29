from elasticsearch import Elasticsearch
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-S", "--server", help="defines ELK server to query", default="localhost")
parser.add_argument("-i", "--index", help="defines index to query")
parser.add_argument("-f", "--field", help="defines the field to print", default="none")
parser.add_argument("-b", "--begintime", help="defines the amount of time to look back at.", default="15m")
parser.add_argument("-e", "--endtime", help="defines the amount of time to start at.", default="0m")
parser.add_argument("-q", "--query", help="defines the elk query for filtering the data", default="*")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--size", help="defines the number of records to pull", default=0)
group.add_argument("-t", "--aggtype", help="defines what aggregation to use")

args = parser.parse_args()

server = args.server
log_index = args.index
field =  args.field
begintime = args.begintime
endtime = args.endtime
query = args.query
doc_size = int(args.size)

def parse_aggregate_type(aggtype, field):
    if aggtype == "count":
        aggregate_field  = {}
    elif aggtype == "sum":
        aggregate_field = { "2":{ f"{aggtype}": { "field": field } } }
    elif aggtype == "avg":
         aggregate_field = { "2":{ f"{aggtype}": { "field": field } } }
    elif aggtype == "min":
         aggregate_field = { "2":{ f"{aggtype}": { "field": field } } }
    elif aggtype == "max":
         aggregate_field = { "2":{ f"{aggtype}": { "field": field } } }
    elif aggtype == "median":
        aggregate_field = { "2":{ "percentiles": {"field": field,"percents":["50"] } } }
    elif aggtype == "unique":
         aggregate_field = { "2":{ "cardinality": { "field": field } } }
    elif aggtype == "ninety":
        aggregate_field = { "2":{ "percentiles": {"field": field,"percents":["90"] } } }
    elif aggtype == "ninety-five":
        aggregate_field = { "2":{ "percentiles": {"field": field,"percents":["95"] } } }
    elif aggtype == "ninety-nine":
        aggregate_field = { "2":{ "percentiles": {"field": field,"percents":["99"] } } }
    
    return aggregate_field

if args.aggtype:
    agg_type = args.aggtype
    aggregates = parse_aggregate_type(agg_type, field)
else:
    aggregates = {}

def print_aggs(data, aggtype):
    if aggtype == "count":
        print(data["hits"]["total"])
    elif aggtype == "median":
        print(data["aggregations"]["2"]["values"]["50.0"])
    elif aggtype == "ninety":
        print(data["aggregations"]["2"]["values"]["90.0"])
    elif aggtype == "ninety-five":
        print(data["aggregations"]["2"]["values"]["95.0"])
    elif aggtype == "ninety-nine":
        print(data["aggregations"]["2"]["values"]["99.0"])
    else:
        print(data["aggregations"]["2"]["value"])

def print_docs(data, filter):
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
          "query": query,
          "analyze_wildcard": "true"
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                    "from": f"now-{begintime}",
                    "to":  f"now-{endtime}"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  },
  "aggs": aggregates
}

response = es.search(index=log_index, body=query_body, size=doc_size)

if doc_size > 0:
  print_docs(response, field)
elif doc_size == 0:
  print_aggs(response, agg_type)
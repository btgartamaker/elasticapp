# elasticapp
A script for querying elastic search

## Installation

This application requires the ElasticSearch python module. To install, you can run the following.

```bash
pip install -r requirements.txt
```

## Command Usage

```bash
usage: es-query.py [-h] [-S SERVER] [-i INDEX] [-f FIELD] [-b BEGINTIME] [-e ENDTIME] [-q QUERY] (-s SIZE | -t AGGTYPE)

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        defines ELK server to query
  -i INDEX, --index INDEX
                        defines index to query
  -f FIELD, --field FIELD
                        defines the field to print
  -b BEGINTIME, --begintime BEGINTIME
                        defines the amount of time to look back at.
  -e ENDTIME, --endtime ENDTIME
                        defines the amount of time to start at.
  -q QUERY, --query QUERY
                        defines the elk query for filtering the data
  -s SIZE, --size SIZE  defines the number of records to pull
  -t AGGTYPE, --aggtype AGGTYPE
                        defines what aggregation to use
```

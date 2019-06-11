import pandas as pd
import numpy as np
import tarfile
import json
from ast import literal_eval
import re
from pprint import pprint

## Populating table list ##
tar = tarfile.open('./tables.tar.gz', "r:gz")
table_list = tar.getnames()

def table_scrape(q):
    """
    Determine the table dependencies from a FROM query.

    Input: q (str) - snippet of SQL query
    Output: dependencies (list) - list of table dependencies

    utilizes re module
    """
    ## Initialize list of dependencies
    dependencies = []
    words = q.split(' ') # split query on spaces
    for word in words:
        if '.' in word:
            for t in table_list:
                if word in t and word not in dependencies:
                    dependencies.append(word)
    return (dependencies)

def get_config_string(p_file_name):
    """
    Simple function to get .json string with associated configuration file name

    Input: p_file_name (str) - partial file name (table name)
    Output: json_string (str) - file as a json string
    """
    try:
        #file_name = 'tables/' + p_file_name + '.json'
        file_name = p_file_name
        tar = tarfile.open('./tables.tar.gz', "r:gz")
        json_string = tar.extractfile(tar.getmember(file_name))
        json_string = json_string.read()
        json_string = literal_eval(json_string.decode('utf8'))

        return (json_string)
    except:
        return (None)

def populate_first_level(table_list):
    """
    Passes a list of tables (i.e. configuration files) and returns a dictionary with first-level dependencies.

    Input: table_list (list) - list of strings
    Output: first_level_dict - dictionary of key (str) = table name and value (list) = list of dependencies.
    """
    first_level_dict = dict() # initialize dictionary
    for t in table_list:      # loop through each table
        #print(t)
        q = get_config_string(t) # load config file into memory
        #print(q['query'])
        try:
            dep = table_scrape(q['query']['L'][0]['M']['from']['S'])
        except:
            dep = table_scrape(q['query']['M']['from']['S'])
        first_level_dict[t] = dep
    return (first_level_dict)

def print_dep_table(name, filename, n=0):
    """
    name (str) - table name
    n (int) - number of levels
    """
    if n == 0:
        print(name, '\n', file=open(filename, "a"))
    else:
        print('\t'*n, '|\n', '\t'*n, '|+', name, file=open(filename, "a"))

def pretty_print_dep_table(t, dep_table, filename, n=0):
    """
    Writes to file a human readable dependency graph.

    Inputs:
    t (str) - table name corresponding to an index value
    dep_table (dict) - dictionary of table names as keys and lists of dependencies as values
    filename - string file to write output to.
    n - number of levels of dependency 
    """
    if t not in list(dep_table.keys()):
        print('Table not indexed...')
    else:
        print_dep_table(t[7:-5], filename, n)
        if len(dep_table[t]) > 0:
            n += 1
            for dep in dep_table[t]:
                pretty_print_dep_table('tables/' + dep + '.json', dep_table, filename, n)

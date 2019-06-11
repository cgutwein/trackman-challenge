# trackman-challenge
The Data Engineer Trackman challenge (http://codechallenge.trackmandata.com/)

## Instructions to run code  
1. Requires Python 3  
2. In the terminal, you will need to run python, the `d_graph_run.py` script and one argument for a filename to save the output.  

Example:
`python d_graph_run.py 'output.txt'`

## Purpose  
From the provided `.json` documents containing *SQL* queries - write a script that will:
1. Find table relationships from existing Join clauses
2. Generate a diagram in `ASCII` format presenting these relationships

## Data   
The data provided by Trackman consists of multiple `.json` files that are contained in a tarball (http://codechallenge.trackmandata.com/tables.tar.gz).

## Deliverables   
1. Source code  (two files, d_graph_run.py & table_dependency.py)
2. ASCII output with relationship diagram (output.txt)
3. README file

## Solution Workflow  
### Step 1. EDA
First, I utilized a *Jupyter notebook* to do an initial exploratory data analysis. Parts of the notebook were adopted into the code used to achieve the challenge goal statement.  The notebook is included in the repo.

### Step 2. Data Processing   
I converted the binary `.json`. files to a string using the *literal_eval* command. This allowed me to convert the data to a dictionary which plays nicer with Python and its built-in methods.  

Since the challenge is focused on making a link between the original **table** and dependent tables joined using a **FROM** clause, for each config file, it was necessary to isolate the **FROM** statement and then determine what other tables it has relations with. I wrote a function to scrape the table names.  

```
## Initialize list of dependencies
  dependencies = []
  words = q.split(' ') # split query on spaces
  for word in words:
      if '.' in word:
          for t in table_list:
              if word in t and word not in dependencies:
                  dependencies.append(word)
  return (dependencies)
```
The above code snippet is admittedly a shortcut. Utilizing Regex commands and testing to ensure that all tables in the FROM statements were captured would be more appropriate. This code only captures tables that exist as a .json configuration file on its own.  

### Step 3. Recording Dependencies  
First level dependencies for each table were determined and recorded in a list. A dictionary using the table name as a **key** and list of dependent table names as a **value** is generated.

```
{'report.scheduled_no_exceptions_hist': ['report.schedule_new_level'], ...}
```

From the list, a recursive function was written to print an output of the dependency graph.  

## Future Work
For the sake of time, there is a lot of work left to do to test this code and write in error checking and other fault tolerant features to make it more robust and user friendly. Running multiple test cases would be a next step.

Assessing speed and efficiency of the script is also a consideration that was mostly ignored. There are certainly better ways to accomplish some of the processing steps that were taken to process this data.

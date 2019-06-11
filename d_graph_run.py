from table_dependency import populate_first_level, table_list, pretty_print_dep_table
#import tarfile
#from ast import literal_eval
import sys

filename = sys.argv[1]

print('Dependency graphs being generated...')

# Generate first level dependencies
first_level_deps = populate_first_level(table_list[1:])

# loop through keys of dictionary and generate output file
for t in list(first_level_deps.keys()):
    pretty_print_dep_table(t, first_level_deps, filename)


print('All tables have been processed.')

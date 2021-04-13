import re

with open('protocols/labelled/only_lockdown.csv', 'r') as f:
    col_names = ['sentiment', 'refs', 'lockdown', 'effects', 'impl/org', 'opinion']
    opinions = ['+', '-', 'o', '?']
    opinion_counts = {opinion: {col_name: {} for col_name in col_names} for opinion in opinions}
    for opinion in opinions:
        opinion_counts[opinion]['count'] = 0
    f.readline()
    for line in f:
        col_vals = re.split('\\t', line)
        opinion = col_vals[6]
        opinion_counts[opinion]['count'] += 1
        for i in range(len(col_names[:-1])):
            col_val = col_vals[i]
            col_name = col_names[i]
            if not col_val in opinion_counts[opinion][col_name]:
                opinion_counts[opinion][col_name][col_val] = 0
            opinion_counts[opinion][col_name][col_val] += 1
    print(opinion_counts)


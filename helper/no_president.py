"""Filters out sentences from the presidents"""

import re

input_file = '../protocols/secondary_format/all_sentences.csv'
output_file = '../protocols/secondary_format/all_no_president.csv'

with open(input_file, 'r') as fin:
    with open(output_file, 'w') as fout:
        for line in fin:
            cols = re.split('@@', line)
            name = cols[4]
            if not re.search('[Pp]räsident', name):
                fout.write(line)
                fout.flush()


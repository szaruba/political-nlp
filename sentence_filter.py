import re


input_file = 'protocols/secondary_format/all_no_president.csv'
output_file = 'protocols/secondary_format/only_lockdown_no_pres.csv'

def lockdown():
    with open(input_file, 'r') as fin:
        with open('protocols/secondary_format/only_lockdown.csv', 'w') as fout:
            for line in fin:
                if re.search('[lL]ock.?[dD]own', line):
                    fout.write(line)
                    fout.flush()

def corona():
    with open(input_file, 'r') as fin:
        with open('protocols/secondary_format/only_corona.csv', 'w') as fout:
            for line in fin:
                if re.search('corona|covid|pandemie', line, re.I):
                    fout.write(line)
                    fout.flush()

def sperr():
    with open(input_file, 'r') as fin:
        with open('protocols/secondary_format/only_sperr.csv', 'w') as fout:
            for line in fin:
                if re.search('sperr|schlie.?[e|u]', line, re.I):
                    fout.write(line)
                    fout.flush()


if __name__ == '__main__':
    lockdown()
    corona()
    sperr()
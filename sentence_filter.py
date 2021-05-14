import re


input_file = 'protocols/secondary_format/all_no_president.csv'
output_file = 'protocols/secondary_format/only_lockdown_no_pres.csv'

def lockdown():
    with open(input_file, 'r') as fin:
        with open('protocols/secondary_format/only_lockdown2.csv', 'w') as fout:
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

def massnahmen():
    overlaps = 0
    written_id = 0
    with open(input_file, 'r') as fin:
        with open('protocols/secondary_format/massnahmen.csv', 'w') as fout:
            lines = fin.readlines()
            for i in range(1, len(lines)-1):
                line = lines[i]
                line_cols = line.split('@@')
                preline = lines[i-1]
                postline = lines[i+1]
                #reg_pattern = 'maske|ffp2|[lL]ock.?[dD]own|impf|polizei.?kon|tracing|corona.?app|pcr|testet|testung|tests|testen|distanc|abstand|social.d'
                #reg_pattern = 'impf'
                p_masks = 'mask|ffp2'
                p_lockdown = '[lL]ock.?[dD]own'
                p_vaccines = 'impf'
                p_testing = 'testet|testung|tests|testen|pcr'
                p_distancing = 'distanc|abstand|social.d'

                b_masks = False
                b_lockdown = False
                b_vaccines = False
                b_testing = False
                b_distancing = False

                line_speech = line_cols[6]
                if re.search(p_masks, line_speech, re.I):
                    b_masks = True
                if re.search(p_lockdown, line_speech, re.I):
                    b_lockdown = True
                if re.search(p_vaccines, line_speech, re.I):
                    b_vaccines = True
                if re.search(p_testing, line_speech, re.I):
                    b_testing = True
                if re.search(p_distancing, line_speech, re.I):
                    b_distancing = True

                precontext_cols = preline.split('@@')
                postcontext_cols = postline.split('@@')
                precontext = ''
                if precontext_cols[4] == line_cols[4]:
                    precontext = precontext_cols[6].replace('\n', '')
                postcontext = ''
                if postcontext_cols[4] == line_cols[4]:
                    postcontext = postcontext_cols[6].replace('\n', '')


                if b_masks or b_lockdown or b_vaccines or b_testing or b_distancing:
                    line = line.replace('\n', '')
                    line += f'@@{precontext}@@{postcontext}@@{b_masks}@@{b_lockdown}@@{b_vaccines}@@{b_testing}@@{b_distancing}\n'
                    fout.write(line)
                    fout.flush()
                    if precontext_cols[0] == written_id:
                        overlaps = overlaps + 1
                    written_id = line_cols[0]
    print(f'overlaps: {overlaps}')

if __name__ == '__main__':
    # lockdown()
    # corona()
    # sperr()
    massnahmen()
import requests

class ParserTertiary:
    """Parses to CoNLL format"""
    output_file = None
    input_file = None
    SEP = '@@'
    URL = 'http://localhost:5003/parse/'
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def start_processing(self):
        sentence_nr = 1
        with open(self.input_file, 'r') as f, open(self.output_file, 'a') as fout:
            for line in f:
                print(f'parsing sentence #{sentence_nr}')
                line = line.strip()
                if not line:
                    continue
                cols = line.split(self.SEP)
                meta_info = [f'# sent_id = {cols[0]}\n', f'# date = {cols[1]}\n', f'# protocol_id = {cols[2]}\n',
                             f'# party = {cols[3]}\n', f'# speaker = {cols[4]}\n', f'# governing = {cols[5]}\n',
                             f'# text = {cols[6]}\n']
                sentence = cols[6]

                r = requests.post(url=self.URL, json={'text': sentence}, headers=self.HEADERS)
                sentence_hierarchy = r.text

                fout.writelines(meta_info)
                fout.write(sentence_hierarchy)
                fout.flush()
                sentence_nr += 1

if __name__ == '__main__':
    parser = ParserTertiary('../protocols/secondary_format/only_lockdown.csv', 'protocols/tertiary_format/only_lockdown.txt')
    parser.start_processing()
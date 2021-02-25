import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import os
from pathlib import Path
import re


class ParserSecond:
    sentence_id = 1
    date = '_'
    protocol_id = '_'
    output_file = None
    output_dir = 'protocols/secondary_format/'
    input_file = None
    input_dir = None
    DELIMITER = '@@'

    def __init__(self, input_dir, output_dir):
        self.sentence_id = self.determine_last_id() + 1
        self.input_dir = input_dir
        self.output_dir = output_dir

    def start_processing(self):
        # get files in input dir
        files = os.listdir(self.input_dir)
        # files = ['06_2019_12_11.html']
        for file in sorted(files):
            self.process_file(file)


    def process_file(self, file):
        with open(self.input_dir + file, "r", encoding="utf-8") as f:
            stem = Path(file).stem
            split = re.split('_', stem, 1)
            self.protocol_id = split[0]
            self.date = split[1]
            for line in f:
                self.process_primary_format_line(line)

    def process_primary_format_line(self, line):
        line = line.strip()
        if not line:
            return

        split = re.split('@@', line)
        speaker = split[0]
        party = '_'
        governing = '_'
        speech = split[1]

        speech = self.filter_remarks(speech)

        for sentence in sent_tokenize(speech, language='german'):
            self.write_line(party, speaker, governing, sentence)
            self.sentence_id += 1

    def write_line(self, party, speaker, governing, sentence):
        output_file = 'all_sentences.csv'
        with open(self.output_dir + output_file, 'a', encoding="utf-8") as f:
            line = str(self.sentence_id) + self.DELIMITER + self.date + self.DELIMITER + self.protocol_id + self.DELIMITER + party + self.DELIMITER + speaker + self.DELIMITER + governing + self.DELIMITER + sentence + '\n'
            print(line)
            f.write(line)
            f.flush()

    def filter_remarks(self, text):
        return re.sub('\\(.*?\\)', '', text)

    def determine_last_id(self):
        return 1



if __name__ == '__main__':
    parser = ParserSecond('protocols/primary_format/', 'protocols/secondary_format/')
    parser.start_processing()
    # text = "Nächster Redner ist Herr Abgeordneter Christoph Stark. – Bitte."
    # token_text = sent_tokenize(text, language='german')
    # print("\nSentence-tokenized copy in a list:")
    # print(token_text)
    # print("\nRead the list:")
    # for s in token_text:
    #     print(s)
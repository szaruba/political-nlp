import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import os
from pathlib import Path
import re
from collections import OrderedDict
import datetime as dt

class ParserSecond:
    sentence_id = 1
    date = '_'
    protocol_id = '_'
    output_file = None
    output_dir = '../protocols/secondary_format/'
    input_file = None
    input_dir = None
    DELIMITER = '@@'
    parties = ['SPÖ', 'ÖVP', 'FPÖ', 'Grüne', 'NEOS', 'ohne Klubzugehörigkeit']
    speaker_party = {'Präsident': 'x', 'Schriftführ': 'x', 'Fürst': 'FPÖ', 'Schallenberg': 'ÖVP', 'Patek': 'x',
                     'Kassegger': 'FPÖ', 'Heinisch-Hosek': 'SPÖ', 'Bogner-Strauß': 'ÖVP', 'Belakowitsch': 'FPÖ',
                     'Müller': 'x', 'Krisper': 'NEOS', 'Hafenecker': 'FPÖ', 'Stilling': 'x', 'Kickl': 'FPÖ',
                     'Kogler': 'Grüne', 'Meinl-Reisinger': 'NEOS', 'Amesbauer': 'FPÖ', 'Muchitsch': 'SPÖ',
                     'Peschorn': 'x', 'Krainer': 'SPÖ', 'Silvan': 'SPÖ', 'Wöginger': 'ÖVP', 'Gahr': 'ÖVP',
                     'Kurz': 'ÖVP', 'Blümel': 'ÖVP', 'Gewessler': 'Grüne', 'Laimer': 'SPÖ', 'Taschner': 'ÖVP',
                     'Brückl': 'FPÖ', 'Blimlinger': 'Grüne', 'Brandstätter': 'NEOS', 'Lopatka': 'ÖVP',
                     'Schellhorn': 'NEOS', 'Anschober': 'Grüne', 'Hammer': 'ÖVP', 'Raab': 'ÖVP', 'Köstinger': 'ÖVP',
                     'Aschbacher': 'ÖVP', 'Alma': 'Grüne', 'Hauser': 'FPÖ', 'Tanner': 'ÖVP', 'Schramböck': 'ÖVP',
                     'Schallen­berg': 'ÖVP', 'Julia Elisabeth Herr': 'SPÖ', 'Jabloner': 'SPÖ', 'Faßmann': 'ÖVP', 'Vana': 'Grüne',
                     'Stögmüller': 'Grüne', 'Weratschnig': 'Grüne', 'Ottenschläger': 'ÖVP', 'Stöger': 'SPÖ', 'Rössler': 'Grüne',
                     'Michael Bernhard': 'NEOS', 'Julia Elisabeth Herr': 'SPÖ', 'Pfurtscheller': 'ÖVP', 'Nehammer': 'ÖVP',
                     'Ralph Schallmeiner': 'Grüne', 'Erwin Angerer': 'FPÖ', 'Gabriel Obernosterer': 'ÖVP', 'Christoph Matznetter': 'SPÖ',
                     'Margarete Schram-böck': 'ÖVP', 'Schallen-berg': 'ÖVP', 'Jörg Leichtfried': 'SPÖ', 'Nina Tomaselli': 'Grüne',
                     'Klaus Lindinger': 'ÖVP', 'Magnus Brunner': 'ÖVP', 'Karin Doppelbauer': 'NEOS', 'Peter Haubner': 'ÖVP',
                     'Rendi-Wagner': 'SPÖ', 'Rainer Wimmer': 'SPÖ',
                     'Ulrike Lunacek': 'Grüne',
                     'Karoline Edtstadler': 'ÖVP',
                     'Dziedzic': 'Grüne',
                     'Yannick Shetty': 'NEOS',
                     'Philip Kucher': 'SPÖ',
                     'Petra Steger': 'FPÖ',
                     'Werner Amon': 'ÖVP',
                     'Peter Wurm': 'FPÖ',
                     'Hubert Fuchs': 'FPÖ',
                     'Andrea Mayer': 'Grüne',
                     'Martin Litschauer': 'Grüne',
                     'Harald Troch': 'SPÖ',
                     'Andreas Hanger': 'ÖVP',
                     'Karlheinz Kopf': 'ÖVP',
                     'Michel Reimon': 'Grüne',
                     'Philippa Strache': 'ohne Klubzugehörigkeit',
                     'Bernhard Achitz': 'SPÖ',
                     'Walter Rosenkranz': 'FPÖ', 'Johannes Margreiter': 'NEOS',
                     'Petra Oberrauner': 'SPÖ',
                     'Felix Eypeltauer': 'NEOS',
                     'Himmelbauer': 'ÖVP',
                     'Harald Stefan': 'FPÖ',
                     'Karl Mahrer': 'ÖVP',
                     'Nagashi': 'Grüne',
                     'Nico Marchetti': 'ÖVP',
                     'Georg Bürstmayr': 'Grüne',
                     'Philipp Schrangl': 'FPÖ',
                     'Gerhard Kaniak': 'FPÖ',
                     'Kira Grünberg': 'ÖVP',
                     'Petra Bayr': 'SPÖ',
                     'Georg Mayer': 'FPÖ',
                     'Sigrid Maurer': 'Grüne',
                     'Wolfgang Zanger': 'FPÖ',
                     'Gerald Loacker': 'NEOS',
                     'Andreas Kollross': 'SPÖ',
                     'Manfred Hofinger': 'ÖVP',
                     'Dietmar Keck': 'SPÖ',
                     'Christian Ragger': 'FPÖ',
                     'Norbert Sieber': 'ÖVP',
                     'Gertraud Salzmann': 'ÖVP',
                     'Nikolaus Prinz': 'ÖVP',
                     'Gerhard Deimek': 'FPÖ',
                     'Markus Koza': 'Grüne',
                     'Sibylle Hamann': 'Grüne',
                     'Elisabeth Köstin': 'ÖVP',
                     'Martin Kocher': 'ÖVP',
                     'Wolfgang Mückstein': 'Grüne'
                     }
    party_governing = OrderedDict([('2020-01-07', ['ÖVP', 'Grüne']), ('2019-06-03', []), ('2019-05-28', ['ÖVP']),
                                   ('2017-12-18', ['ÖVP', 'FPÖ'])])

    def __init__(self, input_dir, output_dir):
        self.sentence_id = self.determine_last_id() + 1
        self.input_dir = input_dir
        self.output_dir = output_dir

    def start_processing(self):
        # get files in input dir
        files = os.listdir(self.input_dir)
        # files = ['06_2019_12_11.html']
        sorted_files_99 = sorted([f for f in files if re.match('^[0-9]{2}_', f)])
        sorted_files_999 = sorted([f for f in files if re.match('^[0-9]{3}_', f)])

        for file in sorted_files_99:
            self.process_file(file)

        for file in sorted_files_999:
            self.process_file(file)
        print("All files processed.")


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
        speaker = speaker.replace('\xa0', ' ')
        speaker = speaker.replace('\xad', '-')
        party = self.determine_party(speaker)
        if party == '_':
            print('party not found')
        governing = self.determine_governing(self.date, party)
        speech = split[1]

        speech = self.filter_remarks(speech)

        for sentence in sent_tokenize(speech, language='german'):
            self.write_line(party, speaker, governing, sentence)
            self.sentence_id += 1

    def write_line(self, party, speaker, governing, sentence):
        output_file = 'all_sentences.csv'
        with open(self.output_dir + output_file, 'a+', encoding="utf-8") as f:
            line = str(self.sentence_id) + self.DELIMITER + self.date + self.DELIMITER + self.protocol_id + self.DELIMITER + party + self.DELIMITER + speaker + self.DELIMITER + str(governing) + self.DELIMITER + sentence + '\n'
            print(line)
            f.write(line)
            f.flush()

    def filter_remarks(self, text):
        return re.sub('\\(.*?\\)', '', text)

    def determine_last_id(self):
        return 1

    def determine_party(self, speaker):
        matches = re.findall('(?<=\\().+?(?=\\))', speaker)
        matches = [match for match in matches if match in self.parties]
        if matches:
            return matches[0]
        else:
            for k in self.speaker_party.keys():
                if re.search(k, speaker):
                    return self.speaker_party[k]
            self.speaker_party[speaker] = '_'
            return '_'

    def determine_governing(self, date_str, party):
        date = dt.datetime.strptime(date_str, '%Y_%m_%d')
        for k in self.party_governing:
            if dt.datetime.fromisoformat(k) <= date:
                return True if party in self.party_governing[k] else False
        raise Exception('date outside scope')



if __name__ == '__main__':
    parser = ParserSecond('../protocols/primary_format/', 'protocols/secondary_format/')
    parser.start_processing()
    # text = "Nächster Redner ist Herr Abgeordneter Christoph Stark. – Bitte."
    # token_text = sent_tokenize(text, language='german')
    # print("\nSentence-tokenized copy in a list:")
    # print(token_text)
    # print("\nRead the list:")
    # for s in token_text:
    #     print(s)
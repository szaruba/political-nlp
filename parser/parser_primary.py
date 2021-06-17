import re
import html
import os
from pathlib import Path

class Parser:
    paragraph = 1
    speaker = ''
    DEBUG = False
    output_path = 'protocols/parsed_protocols/1_2019_10_23.csv'

    def __init__(self, output_path):
        self.output_path = output_path

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def extract_name(self, text):
        if re.search('<p.*?(?:class=MsoNormal|StandardR[BE]).*?>', text):
            text = re.split('<p.*?(?:class=MsoNormal|StandardR[BE]).*?>', text, 1)[1]
        return self.remove_html_tags(text)

    def truncate_html_tags_from_beginning(self, text):
        """Removes html tags from the beginning of a string"""
        while text.lstrip().startswith('<'):
            split = re.split('>', text, 1)
            text = split[1]

        return text

    def extract_first_paragraph(self, text):
        # split on colon
        split = re.split(":", text, 1)
        x = self.truncate_html_tags_from_beginning(split[1])
        split = re.split("</p>|</span></p>", x, 1)
        return split

    def extract_next_paragraph(self, text):
        pattern = '<p.*?class=(?:MsoNormal|StandardR[BE]).*?>(?:.|\n)*?</p>'
        search = re.search(pattern, text)
        if search:
            arr = [None] * 2
            arr[0] = search.group(0)
            arr[1] = re.sub(pattern, '', text, 1)
            return arr
        else:
            return ['']

    def write_speech_paragraph(self, speaker, speech):
        # debugging breakpoint
        if self.paragraph == 436:
            print("break here")
        speech = self.remove_html_tags(speech)
        speech = html.unescape(speech).replace('\n', ' ').strip()
        speaker = html.unescape(speaker).replace('\n', ' ')
        speech = speech.strip()
        if speech:
            if self.DEBUG:
                speech = f'(#{self.paragraph})' + speech
                if re.search('Nationalrat', name):
                    print('ERRORname')
            if not speech.endswith('-'):
                speech += ' '
            if self.speaker != speaker:
                line = "\n" + speaker + "@@" + speech
            else:
                line = speech
            # line = speaker + "@@" + speech + "\n"

            line = line.replace('  ', ' ')
            print(line, end='')
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(line)
                f.flush()
            self.speaker = speaker
            self.paragraph += 1

    def remove_zwischenmeldungen(self, text):
        new_text = ""
        while re.search('<p class=ZM>', text):
            split = re.split('<p class=ZM>', text, 1)
            new_text += split[0]
            split = re.split('<p class=ZM>.*?</p>', split[1], 1)
            if len(split) < 2:
                print('ERRORzw')
            text = split[1]
        return new_text


if __name__ == '__main__':
    path_unparsed = '../protocols/periode27utf8/'
    path_parsed = '../protocols/primary_format/'

    files = os.listdir(path_unparsed)
    # files = ['06_2019_12_11.html']
    for file in files:
        with open(path_unparsed + file, "r", encoding="utf-8") as f:
            parser = Parser(path_parsed + Path(file).stem + '.csv')
            file_content = f.read()

            split_content = re.split("<!--†-->", file_content, 1)
            remainder = split_content[1]
            end_reached = False
            while not end_reached:
                # extract speaker's title
                split_content = re.split("<!--¦-->", remainder, 1)

                title = split_content[0]
                # extract speaker's name
                name = parser.extract_name(split_content[0])

                # print(name + "; ")
                # extract speech raw
                split2 = re.split("<!--†-->", split_content[1], 1)
                speech_raw = split2[0]
                # print(speech_raw + "\n")

                # extract paragraphs
                split3 = parser.extract_first_paragraph(speech_raw)
                parser.write_speech_paragraph(name, split3[0])

                speech_ended = False
                while not speech_ended:
                    split3 = parser.extract_next_paragraph(split3[1])
                    if re.search('Stenographisches Protokoll', split3[0]):
                        print('', end='')
                    if split3[0]:
                        parser.write_speech_paragraph(name, split3[0])
                    if len(split3) < 2:
                        speech_ended = True

                if len(split2) == 1:
                    end_reached = True
                else:
                    remainder = split2[1]


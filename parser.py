import re
import html

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def truncate_html_tags_from_beginning(text):
    """Removes html tags from the beginning of a string"""
    split = re.split("> *(?=[a-zA-Z])", text, 1)
    if len(split) > 1:
        return split[1]
    else:
        return ""


def extract_first_paragraph(text):
    # split on colon
    split = re.split(":", text, 1)
    x = truncate_html_tags_from_beginning(split[1])
    split = re.split("</p>|</span></p>", x, 1)
    return split

def extract_next_paragraph(text):
    if re.search('<p class="MsoNormal".*?>', text):
        split = re.split('<p class="MsoNormal".*?>', text, 1)
        text = truncate_html_tags_from_beginning(split[1])
        return re.split("</span></p>", text, 1)
    else:
        return [""]


def write_speech_paragraph(name, speech):
    line = name + ";" + speech
    line = html.unescape(line)
    line = line.replace("\n", " ")
    print(line)
    with open("parsed_protocols/27_016.csv", "a", encoding="iso-8859-15", errors="ignore") as f:
        f.write(line + "\n")
        f.flush()


if __name__ == '__main__':
    with open("protocols/27_016.html", "r") as f:
        file_content = f.read()

        # print(file_content)

        split_content = re.split("<!--†-->", file_content, 1)
        remainder = split_content[1]
        end_reached = False
        while not end_reached:
            # extract speaker's title
            split_content = re.split("<!--¦-->", remainder, 1)
            title = split_content[0]
            # extract speaker's name
            name = remove_html_tags(split_content[0])
            # print(name + "; ")
            # extract speech raw
            split2 = re.split("<!--†-->", split_content[1], 1)
            speech_raw = split2[0]
            # print(speech_raw + "\n")

            # extract paragraphs
            split3 = extract_first_paragraph(speech_raw)
            write_speech_paragraph(name, split3[0])

            speech_ended = False
            while not speech_ended:
                split3 = extract_next_paragraph(split3[1])
                if split3[0]:
                    write_speech_paragraph(name, split3[0])
                if len(split3) < 2:
                    speech_ended = True

            if len(split2) == 1:
                end_reached = True
            else:
                remainder = split2[1]
# Revisions:
# 1) Separation of paragraphs
# 2) The period symbol (.) and comma symbol (,) need to be close to the previous word without space
# 3) Highlighting areas for a phrase

from pathlib import Path
import pandas as pd
from bs4 import Comment, BeautifulSoup as Soup
import os
from os import listdir

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def processcsv(file): 
    # V2 - Modify variable for different files
    file_to_open = input_folder / file

    # V2 - To detect empty cells as new paragraph
    df = pd.read_csv(file_to_open, header=0).fillna(value="PARA")

    text = """"""
    close = '</span>'

    # define dictionary for HTML code of text colours
    thisdict = {
        "ORG": """<span style="background-color: Tomato">""",
        "PER": """<span style="background-color: SkyBlue">""",
        "LOC": """<span style="background-color: BurlyWood">""",
        "DATE": """<span style="background-color: MediumOrchid">""",
        "MISC": """<span style="background-color: Chartreuse">"""
    }

    # prepare HTML code for text bssed on NER id and concatenate to "text"
    for i in range(len(df)):

        if df["NER"][i] == "PER":
            text += thisdict["PER"] + df["word"][i] + close + ' '
        elif df["NER"][i] == "ORG":
            text += thisdict["ORG"] + df["word"][i] + close + ' '
        elif df["NER"][i] == "LOC":
            text += thisdict["LOC"] + df["word"][i] + close + ' '
        elif df["NER"][i] == "DATE":
            text += thisdict["DATE"] + df["word"][i] + close + ' '
        elif df["NER"][i] == "MISC":
            text += thisdict["MISC"] + df["word"][i] + close + ' '
        elif df["NER"][i] == "PARA":
            text += """<p></p>"""
        else:
            if df["word"][i].isalpha() == True:
                text += str(df["word"][i]) + ' '

            # V2 - no spaces for punctuation
            else:
                text = text.rstrip()
                text += str(df["word"][i]) + ' '

    html = open(template, 'r')
    htmlcode = html.read()
    soup = Soup(htmlcode, 'html.parser')
    insert = Soup(text, 'html.parser')

    # remove exisiting paragraphs
    for i in soup.find_all('p'):
        i.decompose()

    # insert "text" into header
    for i in soup.find_all('h2'):
        if "Text" in i.text:
            i.insert_after(insert)

    # remove comments from HTML file
    div = soup.find('body')
    for element in div(text=lambda text: isinstance(text, Comment)):
        element.extract()

    # V2 - save edits to HTML file
    output = file.replace("input", "output")
    output = output.replace(".csv",".html")
    output = os.path.join(output_folder, output)  
    Html_file = open(output, "w")
    Html_file.write(str(soup))
    Html_file.close()

output_folder = Path.cwd() / "./phase_1_output"
template = Path.cwd() / "./template-v2.html"
input_folder = Path.cwd() / "./phase_1_input"
filenames = find_csv_filenames(input_folder)

for file in filenames:
    processcsv(file)
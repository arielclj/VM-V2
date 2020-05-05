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
    "1": """<span style="background-color: Tomato">""",
    "2": """<span style="background-color: SkyBlue">""",
    "3": """<span style="background-color: BurlyWood">""",
    "4": """<span style="background-color: MediumOrchid">""",
    "5": """<span style="background-color: Chartreuse">""",
    "6": """<span style="background-color: plum">""",
    "7": """<span style="background-color: gold">""",
    "8": """<span style="background-color: red">""",
    "9": """<span style="background-color: royalblue">"""
    }

    # prepare HTML code for text bssed on event_type id and concatenate to "text"
    for i in range(len(df)):
        text += """<P>"""
        if "1" in df["event_type"][i]:
            text += thisdict["1"] + df["paragraph"][i] + close + ' '
        elif "2" in df["event_type"][i]:
            text += thisdict["2"] + df["paragraph"][i] + close + ' '
        elif "3" in df["event_type"][i]:
            text += thisdict["3"] + df["paragraph"][i] + close + ' '   
        elif "4" in df["event_type"][i]:
            text += thisdict["4"] + df["paragraph"][i] + close + ' '
        elif "5" in df["event_type"][i]:
            text += thisdict["5"] + df["paragraph"][i] + close + ' '
        elif "6" in df["event_type"][i]:
            text += thisdict["6"] + df["paragraph"][i] + close + ' '
        elif "7" in df["event_type"][i]:
            text += thisdict["7"] + df["paragraph"][i] + close + ' '
        elif "8" in df["event_type"][i]:
            text += thisdict["8"] + df["paragraph"][i] + close + ' '
        elif "9" in df["event_type"][i]:
            text += thisdict["9"] + df["paragraph"][i] + close + ' '
        elif df["event_type"][i] == "PARA":
            text += """<p></p>"""
        else:
            if df["paragraph"][i].isalpha() == True:
                text += str(df["paragraph"][i]) + ' '
        
            # V2 - no spaces for punctuation
            else:
                text = text.rstrip()
                text += str(df["paragraph"][i]) + ' '
        text += """</P>"""

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

output_folder = Path.cwd() / "./phase_2_output"
template = Path.cwd() / "./template-v2.html"
input_folder = Path.cwd() / "./phase_2_input"
filenames = find_csv_filenames(input_folder)

for file in filenames:
    processcsv(file)

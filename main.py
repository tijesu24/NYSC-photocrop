# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import fitz
import re

filepath = "docs/No1/ppa_Letter (4).pdf"


with fitz.open(filepath ) as doc:
    for page in doc:

        text = ''
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: block[1])  # sort vertically ascending

        for b in blocks:
            text += b[4] # the text part of each block
        temp = re.findall("^STATE CODE: \S+", text, re.MULTILINE)[0]
        temp = temp.split(": ")[1]
        temp = temp.split("/")[-1]
        print(temp)


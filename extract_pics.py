# STEP 1
# import libraries
import fitz
import io
import re
from PIL import Image

# STEP 2
# file path you want to extract images from
PATH_TO_PDF = "docs/No2/ppa_Letter (11).pdf"
output_folder = "docs/No2/output"

def save_pictures(filepath, state_codes):
    # open the file
    pdf_file = fitz.open(filepath)

    # STEP 3
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):

        # get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images()




        #save image
        xref = image_list[1][0]

        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]

        # get the image extension
        image_ext = base_image["ext"]

        image = Image.open(io.BytesIO(image_bytes))
        save_path = output_folder + "/" + str(state_codes[page_index]) + "."+image_ext
        print(f"Saving image on page {page_index} as {save_path}")

        image.save(save_path)


def find_state_codes(PATH_TO_PDF):
    state_codes = []
    with fitz.open(PATH_TO_PDF) as doc:
        for page in doc:

            text = ''
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda block: block[1])  # sort vertically ascending

            for b in blocks:
                text += b[4]  # the text part of each block
            temp = re.findall("^STATE CODE: \S+", text, re.MULTILINE)[0]
            temp = temp.split(": ")[1]
            temp = temp.split("/")[-1]

            state_codes.append(temp)

        return state_codes

if __name__ == "__main__":

    state_codes = find_state_codes(PATH_TO_PDF)
    save_pictures(PATH_TO_PDF, state_codes)
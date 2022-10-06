from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, StringVar, Button, INSERT
from tkinter.ttk import Frame, Label, Entry
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
from auto_text import TextExtension

import fitz
import io
import re
from PIL import Image


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.input_val_var = StringVar()
        self.output_val_var = StringVar()
        self.log_message = StringVar()
        self.init_directory = "/"
        self.txt = None
        self.initUI()

    def select_input_file(self):
        filetypes = (
            ('pdf files', '*.pdf'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=self.init_directory,
            filetypes=filetypes)

        splits = filename.split("/")
        splits = splits[:-1]
        self.init_directory = ("/".join(splits))

        # showinfo(
        #     title='Selected File',
        #     message=filename
        # )
        self.input_val_var.set(filename)

    def select_output_folder(self):
        folder = fd.askdirectory(title="Browse files", initialdir=self.init_directory)

        # showinfo(
        #     title='Selected Folder',
        #     message=folder
        # )

        self.output_val_var.set(folder)

    def initUI(self):
        self.master.title("Extract images")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)
        out_label = Label(frame1, text="Select Input File...", width=20)
        out_label.pack(side=LEFT, padx=5, pady=5)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        input_button = Button(
            frame2,
            text='Browse files',
            command=self.select_input_file
        )
        input_button.pack(expand=True)

        entry1 = Entry(frame2, width=7, state="readonly", textvariable=self.input_val_var)
        entry1.pack(fill=X, padx=5, expand=True)
        # self.input_val_var.set("entry1")
        print(self.input_val_var.get())

        frame3 = Frame(self)
        frame3.pack(fill=X)
        out_label = Label(frame3, text="Select Output Folder...", width=20)
        out_label.pack(side=LEFT, padx=5, pady=5)

        frame4 = Frame(self)
        frame4.pack(fill=BOTH, expand=True)

        # lbl2 = Label(frame4, text="Author", width=6)
        # lbl2.pack(side=LEFT, padx=5, pady=5)

        output_button = Button(
            frame4,
            text='Browse folders',
            command=self.select_output_folder
        )
        output_button.pack(expand=True)

        entry2 = Entry(frame4, width=7, state="readonly", textvariable=self.output_val_var)
        entry2.pack(fill=X, padx=5, expand=True)

        frame5 = Frame(self)
        frame5.pack(fill=BOTH, expand=True)

        self.txt = TextExtension(frame5,textvariable=self.log_message)
        self.txt.pack(fill=BOTH, pady=5, padx=5, expand=True)


        frame6 = Frame(self)
        frame6.pack(fill=BOTH, expand=True)
        output_button = Button(
            frame4,
            text='Extract',
            command=self.extract_pics
        )
        output_button.pack(expand=True)

    def save_pictures(self,filepath, state_codes, output_folder):
        # open the file
        pdf_file = fitz.open(filepath)

        # STEP 3
        # iterate over PDF pages
        for page_index in range(len(pdf_file)):
            # get the page itself
            page = pdf_file[page_index]
            image_list = page.get_images()

            # save image
            xref = image_list[1][0]

            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # get the image extension
            image_ext = base_image["ext"]

            image = Image.open(io.BytesIO(image_bytes))
            save_path = output_folder + "/" + str(state_codes[page_index]) + "." + image_ext

            status = self.log_message.get()
            if status == None: status = ""
            curr_status = f"Saving image on page {page_index+1} as {str(state_codes[page_index])}.{image_ext}"
            status = status + "\n" + curr_status
            self.log_message.set(status)
            image.save(save_path)
            print(curr_status)
            self.txt.update()

    def find_state_codes(self, PATH_TO_PDF):
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

    def extract_pics(self):
        self.log_message.set("")
        if self.input_val_var.get() == "" or self.output_val_var.get() == "":
            showerror(
                title= "Invalid",
                message="You have to select a file or folder"
            )
        else:
            try:
                state_codes = self.find_state_codes(self.input_val_var.get())
            except:
                showerror(
                    title="An error occured",
                    message= "Error occured while trying to read the file.\n Please check the file and try again"

                )
                return

            try:
                self.save_pictures(self.input_val_var.get(), state_codes, self.output_val_var.get())
            except:
                showerror(
                    title="An error occured",
                    message="Error occured while trying to save pictures"
                )
                return

            showinfo(
                title="Status",
                message="Done!"
            )


def main():
    root = Tk()
    root.geometry("700x300+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()

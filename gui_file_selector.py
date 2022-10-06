import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def select_input_file():
    filetypes = (
        ('pdf files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

def select_output_folder():

    folder = fd.askdirectory(title="Select the folder", initialdir='/')


    showinfo(
        title='Selected Folder',
        message=folder
    )


# open button
input_button = ttk.Button(
    root,
    text='Select the File',
    command=select_input_file
)

input_button.pack(expand=True)
output_button = ttk.Button(
 root,
    text='Select the Output',
    command=select_output_folder
)
output_button.pack(expand=True)

# run the application
root.mainloop()
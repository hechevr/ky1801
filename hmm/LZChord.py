import tkinter as tk
from tkinter import filedialog

import hmm2

global root, filepathEntry

def selectInputFile(event):
    global root, filepathEntry
    # filename = filedialog.askopenfilename()
    filename = filedialog.askopenfilename()
    filepathEntry.delete(0, tk.END)
    filepathEntry.insert(0, filename)

    return None

def startFunction():
    global root, filepathEntry
    filename = filepathEntry.get()
    print(filename)
    res, log = hmm2.chordIdentification(filename)

    window = tk.Toplevel(root)
    print(res)
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(window, yscrollcommand=scrollbar.set, width=35, height=30)

    for i in range(len(log)):
        listbox.insert(tk.END, log[i])

    # resultbox = tk.Frame(window, )

    resultbox = tk.Label(window, text=res, font=(None, 16), fg='yellow', bg='black')


    resultbox.pack(side=tk.TOP, fill=tk.BOTH)
    listbox.pack(fill=tk.BOTH)

    scrollbar.config(command=listbox.yview)


    return None

root = tk.Tk()
upFrame = tk.Frame(root)
upFrame.grid(row=0, sticky='news')
middleFrame = tk.Frame(root)
middleFrame.grid(row=1, sticky='news')
downFrame = tk.Frame(root)
downFrame.grid(row=2, sticky='news')

root.wm_title("LZChord")

logo = tk.PhotoImage(file='UI/title.png')
wimg = tk.Label(upFrame, image=logo)

filepathEntry = tk.Entry(middleFrame)
filepathEntry.bind('<1>', func=selectInputFile)
wbutton = tk.Button(downFrame, text="Select", command=startFunction)

wimg.grid(row=0)
filepathEntry.pack(fill=tk.X)
wbutton.pack(fill=tk.X)



root.mainloop()
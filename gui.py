from tkinter import *
from tkinter import filedialog
from twigparse import parse, difflog
import os

root = Tk()
root.title("F2T")
root.geometry()

diff = IntVar()
labelok = Label(root, text="DONE !",fg="green")


def convert():
    labelok.pack_forget()
    fin = pathin.get()

    head, tail = os.path.split(fin)
    fname = tail.split('.',1)
    fout = pathout.get() + '/' + fname[0] + ".twig"

    parse(fin,fout)
    if(diff.get() == 1):
        difflog(fin,fout)
    labelok.pack(side=BOTTOM)


def loadfilein():
    labelok.pack_forget()
    urlin.set(filedialog.askopenfilename())
def loadfileout():
    labelok.pack_forget()
    urlout.set(filedialog.askdirectory())



labelin = Label(root, text="Flexy file path :")
butin = Button(root, text = "Parcourir", command = loadfilein)
urlin = StringVar(root,"/")
pathin = Entry(root,textvariable = urlin)
labelout = Label(root, text="Twig folder path:")
butout = Button(root, text = "Parcourir", command = loadfileout)
urlout = StringVar(root,"/")
pathout = Entry(root,textvariable = urlout)

c = Checkbutton(root, text="Generate diff log", variable=diff)

conv = Button(root, text="Convert", command = convert)



labelin.pack(side=LEFT)
pathin.pack(side=LEFT)
butin.pack(side=LEFT)
labelout.pack(side=LEFT)
pathout.pack(side=LEFT)
butout.pack(side=LEFT)
c.pack(side=BOTTOM)
conv.pack(side=BOTTOM)



root.mainloop()

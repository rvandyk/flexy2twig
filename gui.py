from tkinter import *
from tkinter import filedialog
from twigparse import parse
import os

root = Tk()
root.title("F2T")
root.geometry()


def convert():
    fin = pathin.get()

    head, tail = os.path.split(fin)
    fname = tail.split('.',1)
    fout = pathout.get() + '/' + fname[0] + ".twig"

    parse(fin,fout)

def loadfilein():
    urlin.set(filedialog.askopenfilename())
def loadfileout():
    urlout.set(filedialog.askdirectory())


labelin = Label(root, text="Flexy file path :")
butin = Button(root, text = "Parcourir", command = loadfilein)
urlin = StringVar(root,"/")
pathin = Entry(root,textvariable = urlin)
labelout = Label(root, text="Twig folder path:")
butout = Button(root, text = "Parcourir", command = loadfileout)
urlout = StringVar(root,"/")
pathout = Entry(root,textvariable = urlout)
conv = Button(root, text="Convert", command = convert)



labelin.pack(side=LEFT)
pathin.pack(side=LEFT)
butin.pack(side=LEFT)
labelout.pack(side=LEFT)
pathout.pack(side=LEFT)
butout.pack(side=LEFT)
conv.pack(side=RIGHT)



root.mainloop()

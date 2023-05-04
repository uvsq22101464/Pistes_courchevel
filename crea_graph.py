from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Courchevel")

hauteur = root.winfo_screenheight()
largeur = root.winfo_screenwidth()
print(hauteur, largeur)

image = Image.open('xlarge (0_0).jpg')
image.thumbnail((1000, 1000), Image.BICUBIC)
bg = ImageTk.PhotoImage(image)

frame = Frame(root, width=600, height=400)
canvas = Canvas(frame, width=600, height=400, scrollregion=(0, 0, largeur, hauteur))
x_bar = Scrollbar(frame, orient="horizontal", command=canvas.xview)
y_bar = Scrollbar(frame, orient="vertical", command=canvas.yview)
x_bar.pack(side='bottom', fill='x')
y_bar.pack(side='right', fill='y')
canvas.config(xscrollcommand=x_bar.set, yscrollcommand=y_bar.set)
canvas.pack(expand=True, fill='both')
frame.pack(side="left", fill='both', expand=True)
img = canvas.create_image(0, 0, image=bg, anchor='nw')

x1, y1 = None, None
x2, y2 = None, None
text = ""
taille = 0
dico = {}

def motion(event):
    global status, x1, y1, x2, y2, taille
    x2, y2 = event.x, event.y
    if x1 is not None:
        canvas.create_line(x1, y1, x2, y2)
        taille += (((x2-x1)*2+(y2-y1)*2)**2)**0.5
        x1, y1 = x2, y2
    else:
        x1, y1 = x2, y2

def zero(event=None):
    global status, x1, y1, x2, y2, taille, text, dico
    x1, y1 = None, None
    x2, y2 = None, None
    dico[text] = taille
    canvas.unbind('<Button-1>')
    root.unbind('<Escape>')

def recup_text():
    global text
    text = entry.get()
    entry.delete(0, END)
    canvas.bind('<Button-1>', motion)
    root.bind('<Escape>', zero)

def draw_nodes(event):
    id = canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill='black')
    with open("nodes.txt", "a") as fic:
        fic.write(str(id) + "\t" + str(event.x) + "\t" + str(event.y) + "\n")

def mode_nodes():
    canvas.bind('<Button-1>', draw_nodes)

def load_data():
    with open("nodes.txt", "r") as fic:
        for lines in fic.readlines():
            canvas.create_oval(int(lines.split("\t")[1]) - 5, int(lines.split("\t")[2]) - 5, int(lines.split("\t")[1]) + 5, int(lines.split("\t")[2]) + 5, fill="black")
            #canvas.create_oval(int(lines.split("\t")[1])/2 - 5, int(lines.split("\t")[2])/2 - 5, int(lines.split("\t")[1])/2 + 5, int(lines.split("\t")[2])/2 + 5, fill="black") #pour le vrai truc

label = Label(root, text='Courchevel', height=3, font=('Calibri', 23))
label.pack()
entry = Entry(root)
entry.pack()
button1 = Button(root, text='Valider', command=recup_text)
button1.pack()
label_vide = Label(root)
label_vide.pack()
button2 = Button(root, text='Echap', command=zero)
button2.pack()
button3 = Button(root, text="CREER UN NOEUD", command=mode_nodes)
button3.pack()
button4 = Button(root, text="CHARGER SAVE", command=load_data)
button4.pack()


root.mainloop()
print(dico)

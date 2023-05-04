from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Courchevel")

hauteur = root.winfo_screenheight()
largeur = root.winfo_screenwidth()

image = Image.open('xlarge.jpg')
image.thumbnail((largeur, hauteur), Image.BICUBIC)
bg = ImageTk.PhotoImage(image)
adjust_x =  image.height/798
adjust_y = image.width/1000

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
end_node, start_node = None, None

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
    canvas.unbind('<Button-3>')
    root.unbind('<Escape>')
    return taille

def recup_text(event):
    global text
    text = entry.get()
    canvas.bind('<Button-3>', motion)
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
            canvas.create_oval(float(lines.split("\t")[1])*adjust_x - 5, float(lines.split("\t")[2])*adjust_y - 5, float(lines.split("\t")[1])*adjust_x + 5, float(lines.split("\t")[2])*adjust_y + 5, fill="black")

def find(event):
    if canvas.find_closest(event.x, event.y)[0] != 1:
        return canvas.find_closest(event.x, event.y)[0]
    else:
        raise ValueError("Il faut cliquer sur les cercles sinon c'est faux")
    
def save_arc(event):
    global end_node, start_node, color, taille
    print("go", start_node, end_node)
    with open("nodes.txt", "r+") as fic:
        lines = fic.readlines()
        fic.seek(0)
        fic.truncate()
        for line in lines:
            split = line.split("\t")
            if int(split[0]) == start_node:
                piste = eval(split[-1])
                piste.append((end_node, text, color, taille))    
                content = split[0] + "\t" + split[1] + "\t" + split[2] + "\t" + str(piste) + "\n"
                fic.write(content)
            else:
                fic.write(line)


def draw_arc():
    global text, color
    text = entry.get()
    color = entry2.get()
    #entry.delete(0, END)
    canvas.focus_force()
    canvas.bind('<Button-1>', save_arc)
    canvas.bind('a', recup_start_node)
    canvas.bind('z', recup_end_node)
    canvas.bind('<Button-3>', motion)
    root.bind('<Escape>', zero)

def recup_start_node(event):
    global start_node
    start_node = find(event)
    print(start_node)
    return start_node

def recup_end_node(event):
    global end_node
    end_node = find(event)
    print(end_node)
    return end_node

label = Label(root, text='Courchevel', height=3, font=('Calibri', 23))
label.pack()
entry = Entry(root)
entry.pack()
entry2 = Entry(root)
entry2.pack()
button1 = Button(root, text='Valider', command=draw_arc)
button1.pack()
label_vide = Label(root)
label_vide.pack()
button2 = Button(root, text='Echap', command=zero)
button2.pack()
button3 = Button(root, text="CREER UN NOEUD", command=mode_nodes)
button3.pack()
button4 = Button(root, text="CHARGER SAVE", command=load_data)
button4.pack()

#canvas.bind('<Button-2>', find)

root.mainloop()
print(dico)

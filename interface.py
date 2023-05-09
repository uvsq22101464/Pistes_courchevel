from tkinter import *
from PIL import Image, ImageTk
from algo import *

root = Tk()
root.title("Courchevel")

hauteur = root.winfo_screenheight()
largeur = root.winfo_screenwidth()

image = Image.open('xlarge.jpg')
image.thumbnail((largeur, hauteur), Image.BICUBIC)
bg = ImageTk.PhotoImage(image)
adjust_x =  image.height/798
adjust_y = image.width/1000
start, end = None, None
niveau = "Débutant"

def find(event):
    if canvas.find_closest(event.x, event.y)[0] != 1:
        return canvas.find_closest(event.x, event.y)[0]
    else:
        raise ValueError("Il faut cliquer sur les cercles sinon ça ne marche pas")
    
def reset():
    global start, end
    if start != None:
        canvas.itemconfig(start, fill="black")
        start = None
    if end != None:
        canvas.itemconfig(end, fill="black")
        end = None
    for item in canvas.find_all():
        if item > 141:
            canvas.delete(item)
    return start, end
    

def get_coords(liste):
    liste_coord = []
    for noeuds in liste:
            with open("nodes.txt", "r") as fic:
                for line in fic.readlines():
                    split = line.split("\t")
                    if int(split[0]) == noeuds:
                        x, y = float(split[1]) * adjust_x, float(split[2]) * adjust_y
                        liste_coord.append((x, y))
    return liste_coord

def draw(liste_coord):
    while len(liste_coord) > 1:
        canvas.create_line(liste_coord[0][0], liste_coord[0][1], liste_coord[1][0], liste_coord[1][1], fill="lawngreen", width=3)
        del liste_coord[0]

def starting_point(event):
    global start
    reset()
    start = find(event)
    canvas.itemconfig(start, fill="blue")
    canvas.bind('<Button-1>', ending_point)
    return start

def ending_point(event):
    global end, niveau
    end = find(event)
    canvas.itemconfig(end, fill="red")
    draw(get_coords(dijktra(start, end, niveau)[0]))
    #### faire la liste des chemins
    canvas.bind('<Button-1>', starting_point)
    return end

def debutant():
    global niveau
    niveau = "Débutant"
    label_niveau_select.config(text=niveau)
    return niveau

def aguerri():
    global niveau
    niveau = "Aguerri"
    label_niveau_select.config(text=niveau)
    return niveau

def expert():
    global niveau
    niveau = "Expert"
    label_niveau_select.config(text=niveau)
    return niveau


canvas = Canvas(root, width=600, height=400, scrollregion=(0, 0, largeur, hauteur))
canvas.pack(side="left", expand=True, fill='both')
img = canvas.create_image(0, 0, image=bg, anchor='nw')
label_niveau = Label(root, text="Niveau :", height=3, font=("calibri", 23))
label_niveau.pack(fill="x")
label_niveau_select = Label(root, text="Débutant", height=3, font=("calibri", 23))
label_niveau_select.pack(fill="x")
frame_niveau = Frame(root)
frame_niveau.pack(fill="x")
bouton_debutant = Button(root, text="Débutant", command=debutant)
bouton_aguerri = Button(root, text="Aguerri", command=aguerri)
bouton_expert = Button(root, text="Expert", command=expert)
bouton_debutant.pack(fill="x", side="left", in_=frame_niveau)
bouton_aguerri.pack(before=bouton_debutant, fill="x", side="left", in_=frame_niveau)
bouton_expert.pack(before=bouton_aguerri, fill="x", side="left", in_=frame_niveau)


with open("nodes.txt", "r") as fic:
    for lines in fic.readlines():
        canvas.create_oval(float(lines.split("\t")[1])*adjust_x - 5, float(lines.split("\t")[2])*adjust_y - 5, float(lines.split("\t")[1])*adjust_x + 5, float(lines.split("\t")[2])*adjust_y + 5, fill="black")


canvas.bind('<Button-1>', starting_point)

root.mainloop()

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
    return start, end
    
def starting_point(event):
    global start
    reset()
    start = find(event)
    canvas.itemconfig(start, fill="blue")
    return start

def ending_point(event):
    global end
    end = find(event)
    canvas.itemconfig(end, fill="red")
    print(dijktra(start, end))
    return end


canvas = Canvas(root, width=600, height=400, scrollregion=(0, 0, largeur, hauteur))
canvas.pack(side="left", expand=True, fill='both')
img = canvas.create_image(0, 0, image=bg, anchor='nw')
label_niveau = Label(root, text="Niveau :", height=3, font=("calibri", 23))
label_niveau.pack(fill="x")
label_niveau_select = Label(root, text="", height=3, font=("calibri", 23))
label_niveau_select.pack(fill="x")
frame_niveau = Frame(root)
frame_niveau.pack(fill="x")
bouton_debutant = Button(root, text="Débutant")
bouton_aguerri = Button(root, text="Aguerri")
bouton_expert = Button(root, text="Expert")
bouton_debutant.pack(fill="x", side="left", in_=frame_niveau)
bouton_aguerri.pack(before=bouton_debutant, fill="x", side="left", in_=frame_niveau)
bouton_expert.pack(before=bouton_aguerri, fill="x", side="left", in_=frame_niveau)


with open("nodes.txt", "r") as fic:
    for lines in fic.readlines():
        canvas.create_oval(float(lines.split("\t")[1])*adjust_x - 5, float(lines.split("\t")[2])*adjust_y - 5, float(lines.split("\t")[1])*adjust_x + 5, float(lines.split("\t")[2])*adjust_y + 5, fill="black")


canvas.bind('<Button-1>', starting_point)
canvas.bind('<Button-3>', ending_point)

root.mainloop()
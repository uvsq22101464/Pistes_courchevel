l = ["camion","voiture","chaussures"]
choses = " ".join(l)
print(choses)
a = list(choses)
for i in range(len(a)):
    if a[i] == " ":
        a[i] = "->"
print("".join(a))
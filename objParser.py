import math


faces = []
vertexes = []

path = "object.obj"

FILE = open(f"{path}")

for line in FILE:
    # VERTEXES
    
    if line.startswith("v "):
        parts = line.split()
        if len(parts) == 4:
            x_str, y_str, z_str = parts[1], parts[2], parts[3]
            vertexes.append([round(float(x_str)*10,2), round(float(y_str)*100,2), round(float(z_str)*10,2)])

    # QUAD FACES
    if line.startswith("f "):
        parts = line.split()
        if len(parts) == 5:
            point1, point2, point3, point4 = parts[1], parts[2], parts[3], parts[4]
            point1 = point1.split("/")[0]
            point2 = point2.split("/")[0]
            point3 = point3.split("/")[0]
            point4 = point4.split("/")[0]
            faces.append([vertexes[int(point1)-1], vertexes[int(point2)-1], vertexes[int(point3)-1], vertexes[int(point4)-1]])

FILE.close()
print(faces)
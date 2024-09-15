import pygame
import numpy as np
from math import cos, sin, radians

def parseBasicObj(path, scale):
    faces = []
    vertexes = []


    FILE = open(f"{path}")

    for line in FILE:
        # VERTEXES
        
        if line.startswith("v "):
            parts = line.split()
            if len(parts) == 4:
                x_str, y_str, z_str = parts[1], parts[2], parts[3]
                vertexes.append([round(float(x_str)*scale,2), round(float(y_str)*-scale,5)+100, round(float(z_str)*scale,2)])

        # FACES
        if line.startswith("f "):
            parts = line.split()
            if len(parts) == 4:
                point1, point2, point3= parts[1], parts[2], parts[3]
                point1 = point1.split("/")[0]
                point2 = point2.split("/")[0]
                point3 = point3.split("/")[0]
                faces.append([vertexes[int(point1)-1], vertexes[int(point2)-1], vertexes[int(point3)-1]])
                
            
            if len(parts) == 5:
                point1, point2, point3, point4= parts[1], parts[2], parts[3], parts[4]
                point1 = point1.split("/")[0]
                point2 = point2.split("/")[0]
                point3 = point3.split("/")[0]
                point4 = point4.split("/")[0]
                faces.append([vertexes[int(point1)-1], vertexes[int(point2)-1], vertexes[int(point3)-1], vertexes[int(point4)-1]])
                
        

    FILE.close()
    return faces

def convert(object, FOV):
    convertedPoints = []
    for triangle in object:
        convertedTriangle = []
        for point in triangle:
            x = float(point[0] * FOV / point[2])
            y = float(point[1] * FOV / point[2])
            convertedTriangle.append((x+640, y+360))
        convertedPoints.append(convertedTriangle)
    return convertedPoints

def render(object, screen):
    color = [155,155,155]
    for i, triangle in enumerate(object):
        if color[0] < 255:
            color[0] += 1
        elif color[1] < 255:
            color[1] += 1
        elif color[2] < 255:
            color[2] += 1
        else:
            color = [155,155,155]

        if len(triangle) >= 3:
            pygame.draw.polygon(screen, color, triangle, 5)

def transform(cameraPos, object):
    adjustedObject = []
    for triangle in object:
        adjustedTriangle = []
        for point in triangle:
            adjustedPoint = [0,0,0]
            for i in range(3):
                adjustedPoint[i] = point[i]-cameraPos[i]

            adjustedTriangle.append(adjustedPoint)
        adjustedObject.append(adjustedTriangle)
            
    return adjustedObject

def rotate(cameraRot, object):
    theta_x = cameraRot[0]
    theta_y = cameraRot[1]
    theta_z = cameraRot[2]
    ROTATION_MATRIX_X = np.matrix([[1,      0,              0     ], 
                                   [0, cos(theta_x), -sin(theta_x)],
                                   [0, sin(theta_x), cos(theta_x)]])
    ROTATION_MATRIX_Y = np.matrix([[cos(theta_y), 0, sin(theta_y)],
                                  [0, 1, 0],
                                  [-sin(theta_y), 0, cos(theta_y)]])
    ROTATION_MATRIX_Z = np.matrix([[cos(theta_z), -sin(theta_z), 0],
                                  [sin(theta_z), cos(theta_z), 0],
                                  [0, 0, 1]])
    rotatedObject = []
    for triangle in object:
        rotatedTriangle = []
        for point in triangle:
            rotatedPoint = np.matrix([[point[0]], [point[1]], [point[2]]])
            rotatedPoint = np.dot(ROTATION_MATRIX_X, rotatedPoint)
            rotatedPoint = np.dot(ROTATION_MATRIX_Y, rotatedPoint)
            rotatedPoint = np.dot(ROTATION_MATRIX_Z, rotatedPoint)
            if rotatedPoint[2] > 0:
                rotatedTriangle.append(rotatedPoint)
        rotatedObject.append(rotatedTriangle)

    return rotatedObject
            

def main():
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    cameraPos = [0, 0, -100]
    cameraRot = [0, 0, 0]

    FOV = 70  # Adjust FOV for visible projection

    # DEFINE OBJECT (CUBE)
    #object = [[[100, 100, 100], [200, 200, 100], [100, 200, 100]], [[100, 100, 100], [200, 200, 100], [200, 100, 100]], # FRONT FACE
    #        [[100, 100, 200], [200, 200, 200], [100, 200, 200]], [[100, 100, 200], [200, 200, 200], [200, 100, 200]], # BACK FACE
    #
    #        [[100, 100, 200], [100, 100, 100], [200, 100, 100]], [[100, 100, 200], [200, 100, 100], [200, 100, 200]], # TOP FACE
    #        [[100, 200, 200], [100, 200, 100], [200, 200, 100]], [[100, 200, 200], [200, 200, 100], [200, 200, 200]], # BOTTOM FACE
    #
    #        [[100, 100, 200], [100, 200, 200], [100, 200, 100]], [[100, 100, 200], [100, 200, 100], [100, 100, 200]], # LEFT FACE
    #        [[200, 100, 200], [200, 200, 200], [200, 200, 100]], [[200, 100, 200], [200, 200, 100], [200, 100, 200]]] # RIGHT FACE
    
    object= parseBasicObj("object.obj", 100)

    pygame.init()

    keysPressed = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    keysPressed.append("w")
                if event.key == pygame.K_s:
                    keysPressed.append("s")
                if event.key == pygame.K_a:
                    keysPressed.append("a")
                if event.key == pygame.K_d:
                    keysPressed.append("d")
                if event.key == pygame.K_LEFT:
                    keysPressed.append("left")
                if event.key == pygame.K_RIGHT:
                    keysPressed.append("right")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keysPressed.remove("w")
                if event.key == pygame.K_s:
                    keysPressed.remove("s")
                if event.key == pygame.K_a:
                    keysPressed.remove("a")
                if event.key == pygame.K_d:
                    keysPressed.remove("d")
                if event.key == pygame.K_LEFT:
                    keysPressed.remove("left")
                if event.key == pygame.K_RIGHT:
                    keysPressed.remove("right")

        for key in keysPressed:
            if key == "w":
                cameraPos[0] -= 10*sin(cameraRot[1])
                cameraPos[2] += 10*cos(cameraRot[1])
            elif key == "s":
                cameraPos[0] += 10*sin(cameraRot[1])
                cameraPos[2] -= 10*cos(cameraRot[1])
            if key == "a":
                cameraPos[0] -= 10*cos(cameraRot[1])
                cameraPos[2] += 10*sin(cameraRot[1])
            elif key == "d":
                cameraPos[0] += 10*cos(cameraRot[1])
                cameraPos[2] -= 10*sin(cameraRot[1])
            elif key == "left":
                cameraRot[1] -= -radians(3)
            elif key == "right":
                cameraRot[1] += -radians(3)

        screen.fill("black")


        cubeTransformed = transform(cameraPos, object)
        cubeRotated = rotate(cameraRot, cubeTransformed)
        cubeRendered = convert(cubeRotated, FOV)
        render(cubeRendered, screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

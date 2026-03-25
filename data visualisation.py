import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time 
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 
from ahrs import DCM
from ahrs import Quaternion
# Charger le fichier CSV
data = pd.read_csv("C:\\Users\\knani\\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\\document stage\\arduino_results.csv")
# Extraire les colonnes
Roll_arduino = data['Roll_Arduino']
Pitch_arduino = data['Pitch_Arduino']
Yaw_arduino = data['Yaw_Arduino']

roll_csv = data['Roll_CSV']
pitch_csv = data['Pitch_CSV']
yaw_csv = data['Yaw_CSV']
# Extraire les colonnes pertinentes
#roll = data['Roll_Arduino'].to_numpy()
#pitch = data['Pitch_Arduino'].to_numpy()
#yaw = data['Yaw_Arduino'].to_numpy()

#roll_csv = data['Roll_CSV'].to_numpy()
#pitch_csv = data['Pitch_CSV'].to_numpy()
#yaw_csv = data['Yaw_CSV'].to_numpy()
# Générer le vecteur temps s'il n'existe pas
n = len(data)
fs = 200
t = np.linspace(0, (n-1)/fs, n)
# === Configuration des figures ===
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3 = plt.figure()
ax3d = fig3.add_subplot(111, projection='3d')
# Create a cube
cube = np.array([
    [-2, -1, -1],  # 0
    [2, -1, -1],   # 1
    [2, 1, -1],    # 2
    [-2, 1, -1],   # 3
    [-2, -1, 1],   # 4
    [2, -1, 1],    # 5
    [2, 1, 1],     # 6
    [-2, 1, 1]     # 7
])
cubeTrans = np.transpose(cube)

# Define the faces of the cube
faces = [
    [0, 1, 2, 3],  # Bottom face
    [4, 5, 6, 7],  # Top face
    [0, 1, 5, 4],  # Front face
    [1, 2, 6, 5],  # Right face
    [2, 3, 7, 6],  # Back face
    [3, 0, 4, 7],  # Left face
]

#Define the arrows representing the x, y, and z axes
arrowX = [3,0,0]
arrowY = [0,3,0]
arrowZ = [0,0,3]

# Define the colors for each face
face_colors = ['blue', 'cyan', 'green', 'yellow', 'magenta', 'red']

# Create a figure and 3D axes
def createFigures(frm = None,fig = None):
    global plt3D_1,plt3D_2,plt1D_1,plt1D_2,canvas
    if (fig == None):
        fig = plt.figure()

    plt3D_1 = fig.add_subplot(221, projection='3d')
    plt3D_1.view_init(elev=-160, azim=20, roll=0)

    plt3D_2 = fig.add_subplot(222, projection='3d')
    plt3D_2.view_init(elev=-160, azim=20, roll=0)

    plt1D_1 = fig.add_subplot(223,ylabel="Angle")
    plt1D_2 = fig.add_subplot(224,ylabel="Angle")

    if (frm != None):
        canvas = FigureCanvasTkAgg(fig,master = frm)  
        canvas.draw()
        canvas.get_tk_widget().place(x=3,y=3)
        toolbar = NavigationToolbar2Tk(canvas,frm)
        toolbar.update()
        canvas.get_tk_widget().pack()
    else:
        canvas = None

   
fig, plt1D_1 = plt.subplots()
plt1D_2 = plt1D_1  # pour éviter d'autres erreurs si pltNum ≠ 1


def drawAttitudeArduino(pltNum, t, Roll_arduino, Pitch_arduino, Yaw_arduino, t_max, y_min, y_max):
    plt1D = plt1D_1 if (pltNum == 1) else plt1D_2
    plt1D.cla()
    plt1D.cla()
    plt1D.plot(t, Roll_arduino, 'r--', label="Roll_Arduino")
    plt1D.plot(t, Pitch_arduino, 'g--', label="Pitch_Arduino")
    plt1D.plot(t, Yaw_arduino, 'b--', label="Yaw_Arduino")
    plt1D.set_xlim(0, t_max)
    plt1D.set_ylim(y_min, y_max)
    plt1D.set_xlabel("Temps [s]")
    plt1D.set_ylabel("Angle [°]")
    plt1D.grid()
    plt1D.legend(loc='upper right', fontsize="xx-small", ncol=3, bbox_to_anchor=(0, 0, 1, 1))
def drawAttitudeEstime(pltNum, t, roll_csv, pitch_csv, yaw_csv, t_max, y_min, y_max):
    plt1D = plt1D_2 if (pltNum == 1) else plt1D_1
    plt1D.cla()
    plt1D.cla()
    plt1D.plot(t, roll_csv, 'r-', label="Roll_CSV")
    plt1D.plot(t, pitch_csv, 'g-', label="Pitch_CSV")
    plt1D.plot(t, yaw_csv, 'b-', label="Yaw _CSV")
    plt1D.set_xlim(0, t_max)
    plt1D.set_ylim(y_min, y_max)
    plt1D.set_xlabel("Temps [s]")
    plt1D.set_ylabel("Angle [°]")
    plt1D.grid()
    plt1D.legend(loc='upper right', fontsize="xx-small", ncol=3, bbox_to_anchor=(0, 0, 1, 1))
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

# Exemple d'affichage à l'instant i :
i = len(t) - 1  # ou une boucle avec range
# Plot attitude quaternion components as a function of time 
def drawAttitudeQuat1D(pltNum, t, q_w,q_x,q_y,q_z,t_max,y_min,y_max):
    plt1D = plt1D_1 if (pltNum == 1) else plt1D_2
    plt1D.cla()
    plt1D.plot(t,q_w,'c',label="w")
    plt1D.plot(t,q_x,'r',label="x")
    plt1D.plot(t,q_y,'g',label="y")
    plt1D.plot(t,q_z,'b',label="z")

    plt1D.set_xlim(0,t_max)
    plt1D.set_ylim(y_min,y_max)
  

    plt1D.grid()
    plt1D.legend(loc='upper right',fontsize="xx-small",ncol=3,bbox_to_anchor=(0, 0,1, 1))


# Plot the 3D attitude (angles specified in rad)
def drawAttitude3D(pltNum,roll_csv, pitch_csv, yaw_csv):
    plt3D = plt3D_1 if (pltNum ==1) else plt3D_2
    
    rMat_estime = DCM(rpy=[yaw_csv, pitch_csv, roll_csv])
    rCube = rMat_estime @ cubeTrans
    rotated_cube = np.transpose(rCube)

    rotArrowX = rMat_estime @ arrowX
    rotArrowY = rMat_estime @ arrowY
    rotArrowZ = rMat_estime @ arrowZ

   
    # Clear the current 3D plot
    plt3D.cla()

    #Plot rotated cube
    for face, color in zip(faces, face_colors):
        polygon = plt3D.add_collection3d(art3d.Poly3DCollection([rotated_cube[face]]))
        polygon.set_color(color)
        polygon.set_edgecolor('k')
        polygon.alpha = 50

    # Plot the rotated arrows 
    plt3D.quiver(0,0,0,rotArrowX[0],rotArrowX[1],rotArrowX[2],color='red')
    plt3D.quiver(0,0,0,rotArrowY[0],rotArrowY[1],rotArrowY[2],color='green')
    plt3D.quiver(0,0,0,rotArrowZ[0],rotArrowZ[1],rotArrowZ[2],color='blue')

    
    # Set plot limits to ensure the cube is fully visible
    plt3D.set_xlim(-3, 3)
    plt3D.set_ylim(-3, 3)
    plt3D.set_zlim(-3, 3)

    plt3D.set_xlabel("X")
    plt3D.set_ylabel("Y")
    plt3D.set_zlabel("Z")
    plt3D.grid()

# Plot the 3D attitude (angles specified in rad)
def drawAttitude3D(pltNum, roll_arduino, pitch_arduino, yaw_arduino):
    plt3D = plt3D_1 if (pltNum == 1) else plt3D_2
    
    rMat_arduino = DCM(rpy=[yaw_arduino, pitch_arduino, roll_arduino]) 

    rCube = rMat_arduino @ cubeTrans
    rotated_cube = np.transpose(rCube)

    rotArrowX = rMat_arduino @ arrowX
    rotArrowY = rMat_arduino @ arrowY
    rotArrowZ = rMat_arduino @ arrowZ

   
    # Clear the current 3D plot
    plt3D.cla()

    #Plot rotated cube
    for face, color in zip(faces, face_colors):
        polygon = plt3D.add_collection3d(art3d.Poly3DCollection([rotated_cube[face]]))
        polygon.set_color(color)
        polygon.set_edgecolor('k')
        polygon.alpha = 50

    # Plot the rotated arrows 
    plt3D.quiver(0,0,0,rotArrowX[0],rotArrowX[1],rotArrowX[2],color='red')
    plt3D.quiver(0,0,0,rotArrowY[0],rotArrowY[1],rotArrowY[2],color='green')
    plt3D.quiver(0,0,0,rotArrowZ[0],rotArrowZ[1],rotArrowZ[2],color='blue')

    
    # Set plot limits to ensure the cube is fully visible
    plt3D.set_xlim(-3, 3)
    plt3D.set_ylim(-3, 3)
    plt3D.set_zlim(-3, 3)

    plt3D.set_xlabel("X")
    plt3D.set_ylabel("Y")
    plt3D.set_zlabel("Z")
    plt3D.grid()


# Plot the 3D attitude from Quaternion
def drawAttitudeQuat3D(pltNum, q_w,q_x,q_y,q_z):
    plt3D = plt3D_1 if (pltNum == 1) else plt3D_2
    q = Quaternion(np.array([q_w,q_x,q_y,q_z]))

    rCube = q.rotate(cubeTrans)
    rotated_cube = np.transpose(rCube)

    rotArrowX = q.rotate(arrowX)
    rotArrowY = q.rotate(arrowY)
    rotArrowZ = q.rotate(arrowZ)
       
    # Clear the current 3D plot
    plt3D.cla()

    #Plot rotated cube
    for face, color in zip(faces, face_colors):
        polygon = plt3D.add_collection3d(art3d.Poly3DCollection([rotated_cube[face]]))
        polygon.set_color(color)
        polygon.set_edgecolor('k')
        polygon.alpha = 50

    # Plot the rotated arrows 
    plt3D.quiver(0,0,0,rotArrowX[0],rotArrowX[1],rotArrowX[2],color='red')
    plt3D.quiver(0,0,0,rotArrowY[0],rotArrowY[1],rotArrowY[2],color='green')
    plt3D.quiver(0,0,0,rotArrowZ[0],rotArrowZ[1],rotArrowZ[2],color='blue')

    
    # Set plot limits to ensure the cube is fully visible
    plt3D.set_xlim(-3, 3)
    plt3D.set_ylim(-3, 3)
    plt3D.set_zlim(-3, 3)

    plt3D.set_xlabel("X")
    plt3D.set_ylabel("Y")
    plt3D.set_zlabel("Z")
    plt3D.grid()



def updatePlots(interval=0.02):
    if (canvas != None):
        canvas.draw()
    
    plt.pause(interval)
startTime = time.time()
results = []

if __name__ == '_main_':
    print("Main Function")
    createFigures()

# === Boucle principale ===
for i in range(len(t)):
    rpy_arduino = np.array([Roll_arduino [i], Pitch_arduino [i], Yaw_arduino [i]])
    rpy_estime = np.array([roll_csv[i], pitch_csv[i], yaw_csv[i]])

    print("t =", t[i], " | Arduino:", rpy_arduino, "| Estimé:", rpy_estime)
 # Affichage 3D avec angles estimés
    drawAttitude3D(1, rpy_estime[0], rpy_estime[1], rpy_estime[2])
    drawAttitude3D(2,rpy_arduino[0], rpy_arduino[1], rpy_arduino[2])
    drawAttitudeArduino(ax1, t[:i+1], Roll_arduino[:i+1], Pitch_arduino[:i+1], Yaw_arduino[:i+1],
                    t[-1], -200, 200)

    drawAttitudeEstime(ax2, t[:i+1], roll_csv[:i+1], pitch_csv[:i+1], yaw_csv[:i+1],
                   t[-1], -200, 200)
 

    updatePlots(0.02)
    print("Done in", time.time() - startTime, "s")
    fig.savefig("arduino_plot.png", dpi=300, bbox_inches='tight')

        # ➕ Ajouter les résultats dans une liste
    results.append({
            'time_s': t[i],
            'roll_rad': rpy_estime[0],
            'pitch_rad': rpy_estime[1],
            'yaw_rad': rpy_estime[2],
            'roll_rad': rpy_arduino[0],
            'roll_rad': rpy_arduino[1],
            'roll_rad': rpy_arduino[2],
        })

    print("Done in", time.time() - startTime, "s")

    # ✅ Sauvegarder les résultats dans un fichier CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("resultats_attitude.csv", index=False)
    print("Résultats enregistrés dans 'resultats_attitude.csv'")

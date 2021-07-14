import pandas as pd
import numpy as np
from matplotlib import animation
from functions import *
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 8))
n='10'
type_plot='veld'

n='10'
time,acc,quat=get_data(n)

vel=get_rotation_DFxV(quat,[0,0,9.81],['x','y','z'])

#stationary = get_stationary(acc)
#vel=get_drift(acc,stationary,time)
ax.set(title="Velocidade correta")

labels=['x','y','z']
ax.set(ylabel="Velocidade (m/s)")
ax.set_xlim(0,time.max())
ax.grid()

color=['r','g','b']
for i in range(len(vel.columns)):
    ax.plot(time,vel.iloc[:,i],label=labels[i],color=color[i])
ax.legend(frameon=False,loc='best',ncol=3)

plt.show()

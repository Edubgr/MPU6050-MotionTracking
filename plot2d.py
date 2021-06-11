import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_number = input("What file number? ")
graph_create = "Data_Quaternions.txt"
#graph_create = input("Which graphic do you want to create?")

arq_quat = pd.read_csv("./Datas/data_"+file_number+"/"+graph_create)
quat = arq_quat[['qw','qx','qy','qz']]
time = arq_quat['time']

x = np.linspace(0.0, 5.0)

print(quat)
 
fig, ax = plt.subplots()
ax.set(xlabel='time (s)', ylabel='quat',
       title='Quaternion Orientation')
ax.grid()

ax.set_ylim(ymin=-1.5, ymax=1.5)
ax.set_xlim(xmin=-0.5, xmax=20)
ax.plot(time/1000, quat['qw'], '-')
ax.plot(time/1000, quat['qx'], '-')
ax.plot(time/1000, quat['qy'], '-')
ax.plot(time/1000, quat['qz'], '-')

plt.show()
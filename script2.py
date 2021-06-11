import plotly.graph_objects as go
import pandas as pd
import numpy as np

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z 

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def array_qv (quat):
    Vuvw = pd.DataFrame([[1,0,0]], columns=list('uvw'))
    for i in quat.index:
        q = np.array(quat.loc[i])
        Vuvw = pd.concat([Vuvw,pd.DataFrame([np.array(qv_mult(q,(1,0,0)))], columns=list('uvw'))], ignore_index=True)
    print(Vuvw)
    print(quat)
    return Vuvw

def array_v (time):
    Vxyz = pd.DataFrame([[0,0,0]], columns=list('xyz'))
    for i in time.index:
        t = np.array([time.loc[i]/1000,0,0])
        Vxyz = pd.concat([Vxyz,pd.DataFrame([t], columns=list('xyz'))], ignore_index=True)
    return Vxyz


file_number = input("What file number? ")
graph_create = "Data_Quaternions.txt"
#graph_create = input("Which graphic do you want to create?")

arq_quat = pd.read_csv("./Datas/data_"+file_number+"/"+graph_create)
quat = arq_quat[['qw','qx','qy','qz']]
time = arq_quat['time']

df = pd.concat([array_v(time),array_qv(quat)], axis=1)



fig = go.Figure(data = go.cone(
    x=df['x'],
    y=df['y'],
    z=df['z'],
    u=df['u'],
    v=df['v'],
    w=df['w'],
    colorscale='Blues',
    sizemode="absolute",
    sizeref=2))

fig.update_layout(scene=dict(aspectratio=dict(x=14, y=2, z=2),
                             camera_eye=dict(x=1.2, y=1.2, z=0.6)))

fig.show()


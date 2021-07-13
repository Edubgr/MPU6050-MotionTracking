import pandas as pd
import numpy as np
from scipy import signal as sgn
##################################################
#                   Aux functions                #
##################################################
# Mult quaternion
def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z 
# Mult quaternion
def qq_mult(q1, q2):
    #q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))
# Conjugate for quaternion
def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)
# Return data rotate with DataFrame X Vector
def get_rotation_DFxV (quat,v,name):
    res = pd.DataFrame([],columns=name)
    v = np.append([0]*(4-len(name)),v)
    for i in range(len(quat)):
        q=quat.loc[i].to_numpy()
        if len(name)==4:
            res.loc[i] = qq_mult(q,v)
        else: 
            qq=qq_mult(q,v)
            res.loc[i] = [qq[1],qq[2],qq[3]]
    return res 
# Return data rotate with DataFrame X DataFrame
def get_rotation_DFxDF(quat,data,name):
    res = pd.DataFrame([],columns=name)
    for i in range(len(quat)):
        q1=quat.values[i]
        q2=data.values[i]
        if len(q2)==4:
            res.loc[i] = qq_mult(q1,q2)
        else:
            res.loc[i] = qq_mult(q1,np.append([0],q2))[1:]
    return res 
# Calculate norm
def norm(v):
    n = pd.DataFrame([],columns=['norm'])
    t = 0
    for i in range(v.index.stop):
        for j in range(3):
            t+=v.loc[i][j]**2
        t = np.sqrt(t)
        print(t)
        T = pd.DataFrame([t],columns=['norm'])
        n = n.append(T,ignore_index = True)
        t = 0
    return n
# Remove n% of position or uvw vector
def df_drop(n,data):
    for i in range(len(data)):
        if(i%n!=0):
            data = data.drop(i,axis=0)
    return data#data.reset_index(drop=True)
# Return position and uvw size to quivers in reference a the frames
def get_arrow(pos,uvw,n,skip):
    '''
                                            Apenas se descobrir a norm
    bool_index = n>=index_pos_drop
    for i in range(bool_index.size):
        if bool_index[i]==False:
            break
        n=i
    '''
    n = int(n/skip)
    x = pos['posx'][:n]
    y = pos['posy'][:n]
    z = pos['posz'][:n]
    u = uvw['u'][:n]
    v = uvw['v'][:n]
    w = uvw['w'][:n]
    return x,y,z,u,v,w
# Return position and uvw size to quivers
def get_arrow_one(pos,uvw,n,v_type):
    if v_type=='rotation':
        x = [0,0,0]
        y = [0,0,0]
        z = [0,0,0]
    elif v_type=='static':
        x = pos['posx'][n]
        y = pos['posy'][n]
        z = pos['posz'][n]
    u = uvw['u'][n]
    v = uvw['v'][n]
    w = uvw['w'][n]
    return x,y,z,u,v,w
# Calculate uvw vectors
def get_uvw(size_vector,quat):
    # Rotate quat
    qz = [0.75, -0.05, 0.00, 0.67]
    quat=get_rotation_DFxV(quat,qz,['qw','qx','qy','qz'])
    # Create vector uvw 
    columns=['u','v','w']
    x=get_rotation_DFxV(quat,[size_vector,0,0],columns)
    y=get_rotation_DFxV(quat,[0,size_vector,0],columns)
    z=get_rotation_DFxV(quat,[0,0,size_vector],columns)
    # Create vectors uv2 and position
    uvw = [x,y,z]
    return uvw
# Calculate High or Low Pass filter
def pass_filter(data,type,filtcutoff): 
    res=pd.DataFrame([])  
    name=data.columns.to_numpy() 
    b, a = sgn.butter(1,(2*filtcutoff)/(100),type)
    for i in range(len(data.columns)):
        res[name[i]]=sgn.filtfilt(b,a,data[name[i]])
    return res
# Calculate norm 
def get_norm(data):
    norm = pd.DataFrame([],columns=['norm'])
    t = 0
    for i in range(len(data)):
        for j in range(3):
            t+=data.loc[i][j]**2
        t = np.sqrt(t)
        T = pd.DataFrame([t],columns=['norm'])
        norm = norm.append(T,ignore_index = True)
        t = 0
    return norm
# Calculate integral
def integral(time,data,name):
    ip = 0
    l = pd.DataFrame([np.array([0,0,0])],columns=data.columns.to_numpy())
    for i in range(len(data)-1):
        ip+=(data.loc[i]+data.loc[i+1])*(time[i+1]-time[i])/2
        l = l.append([ip],ignore_index=True)
    l = l.set_axis(name,axis='columns')
    return l
# Calculate velocity integral by removing stationary periods
def integral_vel(data,time,stationary):
    name=['velx','vely','velz']
    ip = 0
    l = pd.DataFrame([np.array([0,0,0])],columns=data.columns.to_numpy())
    for i in range(len(data)-1):
        ip+=(data.loc[i]+data.loc[i+1])*(time[i+1]-time[i])/2
        if stationary[i]!=0:
            ip=pd.DataFrame([np.array([0,0,0])],columns=data.columns.to_numpy())
        l = l.append([ip],ignore_index=True)
    l = l.set_axis(name,axis='columns')
    return l
##################################################
#                   Get datas                    #
##################################################
# Get data (time/acc/quat)
def get_data(n):
    time,acc=get_arc_acc(n)
    time,quat=get_arc_quat(n)
    qz = [0.75, -0.05, 0.00, 0.67]
    cquat=get_rotation_DFxV(quat,qz,['qw','qx','qy','qz'])
    cacc=get_rotation_DFxDF(cquat,acc,['accx','accy','accz'])
    return time, cacc, quat
# Calculate drift
def get_drift(data,stationary,time):
    drift_start=np.where(np.diff(stationary)==-1)
    drift_end=np.where(np.diff(stationary)==1)
    xyz=[[0,0,0]]
    drift_data=pd.DataFrame(np.repeat(xyz,len(data),axis=0),columns=['velx','vely','velz'])  
    for i in range(len(drift_end)):
        ti=drift_start[i][0]
        tf=drift_end[i][0]
        vel_end=data.loc[tf+1]
        tg=(vel_end/(time[tf]-time[ti])).values
        t_drift=time[ti:tf+2]-time[ti]
        drift=pd.DataFrame({'velx': t_drift*tg[0],'vely': t_drift*tg[1],'velz': t_drift*tg[2]})
        drift_data.update(drift)
    return drift_data
# Get Quaternion with archive "Data_Quaternion"
def get_arc_quat(n):
    # Reading the quat data from a CSV file using pandas
    arc = pd.read_csv(("./Datas/data_"+n+"/Data_Quaternions.txt"))
    time = arc[['time']]['time']/1000
    quat = arc[['qw','qx','qy','qz']]
    return time,quat
# Get Accel with archive "Data_LinearAcc"
def get_arc_acc(n):
    # Reading the quat data from a CSV file using pandas
    arc = pd.read_csv(("./Datas/data_"+n+"/Data_LinearAcc.txt"))
    time = arc[['time']]['time']/1000
    acc = arc[['accx','accy','accz']]*9.81/8192
    return time,acc
# Get Accel with archive "Data_Euler"
def get_arc_euler(n):
    # Reading the quat data from a CSV file using pandas
    arc = pd.read_csv(("./Datas/data_"+n+"/Data_Euler.txt"))
    time = arc[['time']]['time']/1000
    euler = arc[['alfa','beta','gama']]
    return time,euler
# Calculate stationary period
def get_stationary(acc):
    # Get norm to accel
    norm = get_norm(acc)
    # Calculate High-Pass filter
    hp = pass_filter(norm,'high',0.001)
    # Value absolute
    hp = hp.abs()
    # Calculate Low-Pass filter
    lp = pass_filter(hp,'low',5)
    # Calculate stationary period
    stationary=lp<0.2
    stationary=(stationary*1)['norm'].to_numpy()
    return stationary
# Calculate velocity real
def get_vel_drift(time,acc):
    # Calculate stationary period
    stationary = get_stationary(acc)
    # Calculate velocity integral
    vel = integral_vel(acc,time,stationary)
    # Calculate integral drift
    drift = get_drift(vel,stationary,time)
    # Remove integral drift
    vel_drift=vel-drift
    return vel_drift




from matplotlib import animation
from functions import *
import numpy as np
import matplotlib.pyplot as plt
###################################################
#                  Plot datas                    #
##################################################
def plot_acc(time,acc,ax):
    stationary = get_stationary(acc)

    labels=['x','y','z','stationary']
    ax.set(ylabel="Acceleration (m/s²)",title ="Acceleration")
    ax.set_xlim(0,time.max())
    #ax.grid()

    color=['r','g','b','y']
    for i in range(len(acc.columns)):
        ax.plot(time,acc.iloc[:,i],label=labels[i],color=color[i],linewidth=0.5)
    ax.plot(time,stationary,label=labels[3],color=color[3],linewidth=1)
    ax.legend(frameon=False,loc='best',ncol=4)
    return ax

def plot_vel(time,acc,ax,v_type):
    if v_type == 'drift':
        vel = get_vel_drift(time,acc)
        ax.set(title="Velocity correct")
    elif v_type == 'pure':
        vel=integral(time,acc,['velx','vely','velz'])
        ax.set(title="Velocity with drift")

    labels=['x','y','z']
    ax.set(ylabel="Velocity (m/s)")
    ax.set_xlim(0,time.max())
    #ax.grid()
  
    color=['r','g','b']
    for i in range(len(vel.columns)):
        ax.plot(time,vel.iloc[:,i],label=labels[i],color=color[i],linewidth=0.5)
    ax.legend(frameon=False,loc='best',ncol=3)
    return ax

def plot_pos(time,acc,ax,v_type):
    if v_type == 'drift':
        vel = get_vel_drift(time,acc)
        pos = integral(time,vel,['posx','posy','posz'])
        ax.set(title="Position correct")
    elif v_type == 'pure':
        vel = integral(time,acc,['velx','vely','velz'])
        pos = integral(time,vel,['posx','posy','posz'])
        ax.set(title="Position with drift")

    labels=['x','y','z']
    ax.set(ylabel="Position(m)")
    ax.set_xlim(0,time.max())
    #ax.grid()

    color=['r','g','b']
    for i in range(len(pos.columns)):
        ax.plot(time,pos.iloc[:,i],label=labels[i],color=color[i],linewidth=0.5)
    ax.legend(frameon=False,loc='best',ncol=3)
    return ax

def plot_quat(time,quat,ax,v_type):
    if v_type == 'correct':
        quat=get_mult_quat_DFxV(quat)
        ax.set(title="Processed quaternion")
    elif v_type == 'pure':
        ax.set(title="Sensor quaternion")

    labels=['w','x','y','z']
    ax.set(ylabel="Quaternion")
    ax.set_ylim(-1.5,1.5)
    ax.set_xlim(0,time.max())
    #ax.grid()

    color=['y','r','g','b']
    for i in range(len(quat.columns)):
        ax.plot(time,quat.iloc[:,i],label=labels[i],color=color[i],linewidth=0.5)
    ax.legend(frameon=False,loc='upper center',ncol=4)
    return ax

def plot_euler(time,quat,ax,v_type):
    if v_type == 'correct':
        quat=get_mult_quat_DFxV(quat)
        euler=get_euler(quat)
        ax.set(title="Sensor euler")
    elif v_type == 'pure':
        euler=get_euler(quat)
        ax.set(title="Processed euler")

    ax.set(title="Euler")
    labels=['alfa','beta','gama']
    ax.set(ylabel="Rad")
    ax.set_ylim(-6.5,+6.5)
    ax.set_xlim(0,time.max())
    #ax.grid()
    color=['r','g','b']
    for i in range(len(euler.columns)):
        ax.plot(time,euler.iloc[:,i],label=labels[i],color=color[i],linewidth=0.5)
    ax.legend(frameon=False,loc='upper center',ncol=3)
    return ax

def plot_animate(fig,ax,time,data,legend):
        color = ['r','g','b','y']
        # Create lines
        lines = []
        for i in range(len(data.columns)):
                lobj = ax.plot([],[],color=color[i],label=legend[i],linewidth=0.8)[0]
                lines.append(lobj)
        # Calculate max axis y
        ylim=np.array([[-0.1,0.1]])
        for i in range(len(data)):
                if i>0:
                        maxy=np.amax(data.iloc[:i].to_numpy())+0.2
                        miny=np.amin(data.iloc[:i].to_numpy())-0.2
                        minmax=[miny,maxy]
                        ylim = np.concatenate((ylim,[minmax]),axis=0)
        # Define animete function
        def animate(frame):
                for i,line in enumerate(lines):
                        line.set_data(time[:frame+1],data.iloc[:frame+1,i])
                ax.set_xlim(max(time[:frame+1]-8), max(time[:frame+1])+2)
                ax.set_ylim(ylim[frame])
                return lines
        # Plot legend
        ax.legend(frameon=False,loc='upper center',ncol=len(legend))
        fig.set_figheight(2.375)
        fig.set_figwidth(6)
        fig.set_dpi(200)
        fig.tight_layout()
        # Return animation
        return animation.FuncAnimation(fig, animate,frames=len(data), interval=10, blit=False)
###################################################
#                  Find plots                    #
##################################################
def find_plot2d_static(ax,type_plot,time,acc,quat):
    if type_plot == 'acc':
        return plot_acc(time,acc,ax)
    elif type_plot == 'vel':
        return plot_vel(time,acc,ax,'pure')
    elif type_plot == 'pos':
        return plot_pos(time,acc,ax,'pure')
    elif type_plot == 'veld':
        return plot_vel(time,acc,ax,'drift')
    elif type_plot == 'posd':
        return plot_pos(time,acc,ax,'drift')
    elif type_plot == 'quat':
        return plot_quat(time,quat,ax,'pure')
    elif type_plot == 'quatc':
        return plot_quat(time,quat,ax,'correct')
    elif type_plot == 'euler':
        return plot_euler(time,quat,ax,'pure')
    elif type_plot == 'eulerc':
        return plot_euler(time,quat,ax,'correct')
    else:
        quit()

def find_plot2d_animation(type_plot,time,acc,quat):
    if type_plot == 'acc':
        fig,ax=plt.subplots()
        ax.set(title="Acceleration")
        labels=['x','y','z']
        ax.set(ylabel="Acceleration (m/s²)",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,acc,labels)
    elif type_plot == 'vel':
        fig,ax=plt.subplots()
        vel = integral(time,acc,['velx','vely','velz'])
        ax.set(title="Velocity with drift")
        labels=['x','y','z']
        ax.set(ylabel="Velocity (m/s)",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,vel,labels)
    elif type_plot == 'pos':
        fig,ax=plt.subplots()
        vel = integral(time,acc,['velx','vely','velz'])
        pos = integral(time,vel,['posx','posy','posz'])
        ax.set(title="Position with drift")
        labels=['x','y','z']
        ax.set(ylabel="Position (m)",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,pos,labels)
    elif type_plot == 'veld':
        fig,ax=plt.subplots()
        vel = get_vel_drift(time,acc)
        ax.set(title="Velocity correct")
        labels=['x','y','z']
        ax.set(ylabel="Velocity(m/s)",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,vel,labels)
    elif type_plot == 'posd':
        fig,ax=plt.subplots()
        vel = get_vel_drift(time,acc)
        pos = integral(time,vel,['posx','posy','posz'])
        ax.set(title="Position correct")
        labels=['x','y','z']
        ax.set(ylabel="Psition (m)",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,pos,labels)
    elif type_plot == 'quat':
        fig,ax=plt.subplots()
        ax.set(title="Sensor quaternion")
        labels=['w','x','y','z']
        ax.set(ylabel="Quaternion",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,quat,labels)
    elif type_plot == 'quatc':
        fig,ax=plt.subplots()
        quat=get_mult_quat_DFxV(quat)
        ax.set(title="Processed quaternion")
        labels=['w','x','y','z']
        ax.set(ylabel="Quaternion",xlabel='Time(s)')
        ax.grid()
        return plot_animate(fig,ax,time,quat,labels)
    elif type_plot == 'euler':
        fig,ax=plt.subplots()
        euler=get_euler(quat)
        ax.set(title="Sensor euler")
        labels=['alfa','beta','gama']
        ax.set(ylabel="Rad",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,euler,labels)
    elif type_plot == 'eulerc':
        fig,ax=plt.subplots()
        quat=get_mult_quat_DFxV(quat)
        euler=get_euler(quat)
        ax.set(title="Processed euler")
        labels=['alfa','beta','gama']
        ax.set(ylabel="Rad",xlabel='Time (s)')
        ax.grid()
        return plot_animate(fig,ax,time,euler,labels)
###################################################
#                  Plot types                    #
##################################################
def plot2d_animated():
    n=input('Folder number: ')
    type_plot=input('Type plot: ')
    return find_plot2d_animation(type_plot,*get_data(n))

def plot2d_static_onecol():
    n=input('Folder number: ')
    time,cacc,quat = get_data(n)
    r=input('Number row: ')
    rows=int(r)
    if rows==1:
        fig, ax = plt.subplots(figsize=(12, 8))
        type_plot=input('Type plot: ')
        ax=find_plot2d_static(ax,type_plot,time,cacc,quat)
        plt.xlabel("Time (s)")
        return fig
    elif rows>1:
        fig, ax = plt.subplots(rows,sharex=True,figsize=(12, 8))
        type_plot=[]
        for i in range(rows):
                type_plot=np.append(type_plot,input('Type plot %d: '%(i+1)))
        for i,t_plot in enumerate(type_plot):
            ax[i]=find_plot2d_static(ax[i],t_plot,time,cacc,quat)
        plt.xlabel("Time (s)")
        return fig
        #plt.tight_layout()

def plot2d_static_threeplot():
    n=input('Folder number: ')
    time,cacc,quat = get_data(n)
    gridsize = (2, 2)
    fig = plt.figure(figsize=(12, 8))
    ax1_name=input('Type big plot: ')
    ax2_name=input('Type small plot 1: ')
    ax3_name=input('Type small plot 2: ')
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2)#, rowspan=2)
    ax1 = find_plot2d_static(ax1,ax1_name,time,cacc,quat)
    ax2 = plt.subplot2grid(gridsize, (1, 0),sharex=ax1)
    ax2 = find_plot2d_static(ax2,ax2_name,time,cacc,quat)
    ax3 = plt.subplot2grid(gridsize, (1, 1),sharex=ax1)
    ax2 = find_plot2d_static(ax3,ax3_name,time,cacc,quat)
    plt.tight_layout()
    return fig

def plot2d_static_moredata():
    rows=input('How many plots: ')
    rows=int(rows)
    if rows<1:
        quit()
    type_plot=[]
    for i in range(rows):
        type_plot=np.append(type_plot,input('Type plot %d: '%(i+1)))
    cols=input('How many datas: ')
    cols=int(cols)
    if cols<=1:
        quit()
    fig, ax = plt.subplots(rows, cols,sharex='col',sharey='row',figsize=(12, 8))
    for i in range(cols):
        n= input('Folder number %d: '%(i+1))
        time,cacc,quat = get_data(n)
        if rows==1:
            ax[i]=find_plot2d_static(ax[i],type_plot[0],time,cacc,quat)
            ax[i].set_xlabel("Time (s)")
        else:
            for j in range(rows):
                ax[j][i]=find_plot2d_static(ax[j][i],type_plot[j],time,cacc,quat)
            ax[rows-1][i].set_xlabel("Time (s)")
    return fig
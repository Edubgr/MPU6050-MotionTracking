from functions import*
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
###################################################
#                  Plot types                    #
##################################################
def plot3d_animate(plot):
    n=input('Folder number: ')
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),figsize=(12, 8)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Plot Animation
    # Get data
    time,acc,quat=get_data(n)
    # Create quivers
    quiverx = ax.quiver(0,0,0,0,0,0,color='r',arrow_length_ratio=0)
    quivery = ax.quiver(0,0,0,0,0,0,color='g',arrow_length_ratio=0)
    quiverz = ax.quiver(0,0,0,0,0,0,color='b',arrow_length_ratio=0)
    text = ax.text(0,0,0,"0", color='black')
    # Rotation
    if plot=='0':
        size_vector=1
        # Get vector uvw
        uvw = get_uvw(size_vector,quat)
        # Set title
        ax.set_title('3D Rotation')   
        # Define var
        size_frame=len(uvw[0])
        # Set values to set_lim
        ax.set_xlim3d(-size_vector,size_vector)
        ax.set_ylim3d(-size_vector,size_vector)
        ax.set_zlim3d(-size_vector,size_vector)
        # Def for rotation
        def update(n):
            nonlocal quiverx
            nonlocal quivery
            nonlocal quiverz
            nonlocal text
            text.remove()
            quiverx.remove()
            quivery.remove()
            quiverz.remove()
            # Set values to quivers
            quiverx = ax.quiver(*get_arrow_one(0,uvw[0],n,'rotation'),color='r',arrow_length_ratio=0)
            quivery = ax.quiver(*get_arrow_one(0,uvw[1],n,'rotation'),color='g',arrow_length_ratio=0)
            quiverz = ax.quiver(*get_arrow_one(0,uvw[2],n,'rotation'),color='b',arrow_length_ratio=0)
            # Set text time
            text = ax.text(0,0,0,"     "+str(time[n]), color='black')
    # Position and rotation
    elif plot=='1' or plot=='2':
        size_vector=0.05
        # Get vector uvw
        uvw = get_uvw(size_vector,quat)
        # Set title
        ax.set_title('3D Position and Rotation') 
        # Define var
        size_frame=len(uvw[0])
        # Get position
        vel=get_vel_drift(time,acc)
        pos=integral(time,vel,['posx','posy','posz'])
        pos_array = np.array((pos['posx'].values, pos['posy'].values, pos['posz'].values))
        # Create line
        line = ax.plot(pos_array[0, 0:1], pos_array[1, 0:1], pos_array[2, 0:1], color='black')[0]
        # Create array to set_lim
        a_minmax=np.array([(-size_vector,size_vector)])
        for i in range(size_frame):
            if i>0:
                max=np.amax(pos_array[:,:i])+size_vector
                min=np.amin(pos_array[:,:i])-size_vector
                #med=(max-min)/2
                minmax = [min, max]
                a_minmax = np.concatenate((a_minmax,[minmax]),axis=0)
        # Create vector with drops
        if plot == "2":
            n_skip=int(input("Number of steps: "))
            pos_drop=df_drop(n_skip,pos)
            xd=df_drop(n_skip,uvw[0])
            yd=df_drop(n_skip,uvw[1])
            zd=df_drop(n_skip,uvw[2])
            uvw_drop = [xd,yd,zd]
        # Def for position and rotation     
        def update(n):
            nonlocal quiverx
            nonlocal quivery
            nonlocal quiverz
            nonlocal text
            text.remove()
            quiverx.remove()
            quivery.remove()
            quiverz.remove()
            # Static
            if plot=="1":
                # Set values to quivers
                quiverx = ax.quiver(*get_arrow_one(pos,uvw[0],n,'static'),color='r',arrow_length_ratio=0)
                quivery = ax.quiver(*get_arrow_one(pos,uvw[1],n,'static'),color='g',arrow_length_ratio=0)
                quiverz = ax.quiver(*get_arrow_one(pos,uvw[2],n,'static'),color='b',arrow_length_ratio=0)
                # Set text time
                text = ax.text(pos['posx'][n],pos['posy'][n],pos['posz'][n],"     "+str(time[n]), color='black')
            # Dynamic
            elif plot=="2":
                #Apenas se descobrir a norm index_pos_drop=np.array(pos_drop.index)
                # Set values to quivers
                quiverx = ax.quiver(*get_arrow(pos_drop,uvw_drop[0],n,n_skip),color='r',arrow_length_ratio=0)
                quivery = ax.quiver(*get_arrow(pos_drop,uvw_drop[1],n,n_skip),color='g',arrow_length_ratio=0)
                quiverz = ax.quiver(*get_arrow(pos_drop,uvw_drop[2],n,n_skip),color='b',arrow_length_ratio=0)
                # Set text time
                text = ax.text(pos['posx'][n],pos['posy'][n],pos['posz'][n],"     "+str(time[n]), color='black')
            # Set values to set_lim
            ax.set_xlim3d(a_minmax[n])
            ax.set_ylim3d(a_minmax[n])
            ax.set_zlim3d(a_minmax[n])
            # Set values to line
            line.set_data(pos_array[0:2, :n])  
            line.set_3d_properties(pos_array[2, :n]) 
    # Create animation
    ax.view_init(elev=45, azim=-45)
    fig.set_figheight(5)
    fig.set_figwidth(7.5)
    return FuncAnimation(fig, update, frames=size_frame, interval=1)

def plot3d_static_pos():
    n=input('Folder number: ')
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),figsize=(12, 8)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Set title
    ax.set_title('3D Position') 
    # Get data
    time,acc,quat=get_data(n)
    size=len(time)
    # Get position
    vel=get_vel_drift(time,acc)
    pos=integral(time,vel,['posx','posy','posz'])
    pos_array = np.array((pos['posx'].values, pos['posy'].values, pos['posz'].values))
    # Plot line
    ax.plot(pos_array[0,:], pos_array[1,:], pos_array[2,:], color='black')
    # Calculate max and min position
    maxmin=[np.amin(pos_array),np.amax(pos_array)]
    # Define 3d lim
    ax.set_xlim3d(maxmin)
    ax.set_ylim3d(maxmin)
    ax.set_zlim3d(maxmin)
    # Set text time
    ax.text(pos['posx'][size-1],pos['posy'][size-1],pos['posz'][size-1],"     "+str(time[size-1]), color='black')
    ax.view_init(elev=89, azim=-90)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    return fig

def plot3d_static_posrot():
    size_vector=0.05
    n=input('Folder number: ')
    n_skip=int(input("Number of steps: "))
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),figsize=(12, 8)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Get data
    time,acc,quat=get_data(n)
    # Set title
    ax.set_title('3D Position and Rotation') 
    # Get position
    vel=get_vel_drift(time,acc)
    pos=integral(time,vel,['posx','posy','posz'])
    pos_array = np.array((pos['posx'].values, pos['posy'].values, pos['posz'].values))
    # Get vector uvw
    uvw = get_uvw(size_vector,quat)
    # Get size
    size=len(uvw[0])
    # Create vector with drops
    pos_drop=df_drop(n_skip,pos)
    xd=df_drop(n_skip,uvw[0])
    yd=df_drop(n_skip,uvw[1])
    zd=df_drop(n_skip,uvw[2])
    uvw_drop = [xd,yd,zd]
    # Plot line
    ax.plot(pos_array[0,:], pos_array[1,:], pos_array[2,:], color='black')
    # Define colors
    color=['r','g','b']
    # Plot quivers
    for i in range(3):
        ax.quiver(*get_arrow(pos_drop,uvw_drop[i],size,n_skip),color=color[i],arrow_length_ratio=0)
    # Calculate max and min position
    maxmin=[np.amin(pos_array)-size_vector,np.amax(pos_array)+size_vector]
    # Define 3d lim
    ax.set_xlim3d(maxmin)
    ax.set_ylim3d(maxmin)
    ax.set_zlim3d(maxmin)
    # Set text time
    ax.text(pos['posx'][size-1],pos['posy'][size-1],pos['posz'][size-1],"     "+str(time[size-1]), color='black')
    ax.view_init(elev=1, azim=-90)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    return fig
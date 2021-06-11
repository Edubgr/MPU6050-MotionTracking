import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']

def plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')


    xx = np.linspace(x, x+dx, 2)
    yy = np.linspace(y, y+dy, 2)
    zz = np.linspace(z, z+dz, 2)

    xx, yy = np.meshgrid(xx, yy)

    ax.plot_surface(xx, yy, z)
    ax.plot_surface(xx, yy, z+dz)

    yy, zz = np.meshgrid(yy, zz)
    ax.plot_surface(x, yy, zz)
    ax.plot_surface(x+dx, yy, zz)

    xx, zz = np.meshgrid(xx, zz)
    ax.plot_surface(xx, y, zz)
    ax.plot_surface(xx, y+dy, zz)
    # ax.set_xlim3d(-dx, dx*2, 20)
    # ax.set_xlim3d(-dx, dx*2, 20)
    # ax.set_xlim3d(-dx, dx*2, 20)
    plt.title("Cube")
    plt.show()

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

vx=(1,0,0)
vy=(0,1,0)
vz=(0,0,1)

quat = np.empty((0,4), float)
time = np.empty((0,1), float)
file_number = input("What file number? ")
graph_create = "Data_Quaternions.txt"
#graph_create = input("Which graphic do you want to create?")

file_data = open("./Datas/data_"+file_number+"/"+graph_create)

for line in file_data:
    aux = line.replace(" ","")
    line = aux.replace("\n","")
    print(line)
    t, w, x, y, z = np.asarray(line.split(","), dtype=np.float64, order='C')
    time=np.vstack((time,t))
    quat=np.vstack((quat,[w,x,y,z]))

def array_qv (quat):
    Vxyz = np.empty((0,3,3), float)
    for i in quat:
        array_vec = np.array([qv_mult(i,vx),qv_mult(i,vy),qv_mult(i,vz)])
        Vxyz=np.vstack((Vxyz,[array_vec]))
    return Vxyz       

def plot_linear_cube(x, y, z, dx, dy, dz, color='red'):
    fig = plt.figure()
    ax = Axes3D(fig)
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
    plt.title('Cube')
    plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D acceleration vector distribution')

x_scale=2
y_scale=1
z_scale=1


ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 0.1, 0.1, 0.5]))

#scale=np.diag([x_scale, y_scale, z_scale, 1.0])
#scale=scale*(1.0/scale.max())
#scale[3,3]=1.0
#def short_proj():
#  return np.dot(Axes3D.get_proj(ax), scale)

#ax.get_proj=short_proj

# Set the bottom and top outside the actual figure limits, 
# to stretch the 3D axis
fig.subplots_adjust(bottom=-0.15,top=1.2)
# Cartesian axes
#ax.quiver(-1, 0, 0, 3, 0, 0, color='#aaaaaa',linestyle='dashed')
#ax.quiver(0, -1, 0, 0,3, 0, color='#aaaaaa',linestyle='dashed')
#ax.quiver(0, 0, -1, 0, 0, 3, color='#aaaaaa',linestyle='dashed')
# Vector before rotation
ax.quiver(0, 0, 0, 1, 0, 0, color='b')
ax.quiver(0, 0, 0, 0, 1, 0, color='r')
ax.quiver(0, 0, 0, 0, 0, 1, color='g')
n=0
for i in array_qv(quat):
    if n%1 == 0:
        print(time[n])
        ax.quiver(time[n]/1000, 0, 0, i[0][0],i[0][1],i[0][2], color='b')
        ax.quiver(time[n]/1000, 0, 0, i[1][0],i[1][1],i[1][2], color='r')
        ax.quiver(time[n]/1000, 0, 0, i[2][0],i[2][1],i[2][2], color='g')
        #plot_linear_cube(0.2*n, 0, 0, i[0][0],i[0][1],i[0][2])
    n+=1

ax.set_xlim([-1, 19])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

fig=plt.figure(figsize=(5,35))

# Set the bottom and top outside the actual figure limits, 
# to stretch the 3D axis
fig.subplots_adjust(bottom=-0.15,top=1.2)
plt.show()
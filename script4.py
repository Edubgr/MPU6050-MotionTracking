import plotly.graph_objects as go

fig = go.Figure(data=go.Cone(x=[1], y=[1], z=[1], u=[0], v=[0.71], w=[-0.71]))

fig.update_layout(scene_camera_eye=dict(x=-0.76, y=1.8, z=0.92))

fig.show()
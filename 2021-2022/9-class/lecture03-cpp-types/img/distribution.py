from plotly.offline import init_notebook_mode
import numpy as np
import plotly.graph_objs as go
import pathlib

init_notebook_mode(connected=False)
fig = go.Figure()
x = np.logspace(-60, 5, base=2.0)
x = np.concatenate((x, -x))
fig.add_trace(go.Scatter(
    x=x, y=np.zeros(x.shape), mode='markers', marker_size=5
))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False, 
                 zeroline=True, zerolinecolor='black', zerolinewidth=2,
                 showticklabels=False)
fig.update_layout(height=200, plot_bgcolor='white', title="Визуализация распределения вещественных чисел на прмяой")
fig.show()
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook
from bokeh.layouts import row
from bokeh.models.widgets import Slider
import numpy as np

output_notebook()

x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))

p = figure(title='Animated Sine Wave', plot_height=300, plot_width=600)
p.line(x='x', y='y', source=source)

def update_data(f):
    x = np.linspace(0, 4*np.pi, 100)
    y = np.sin(x + f*np.pi/4)
    source.data = dict(x=x, y=y)

slider = Slider(start=0, end=1, step=0.1, value=0)
slider.on_change('value', lambda attr, old, new: update_data(new))

layout = row(slider, p)

show(layout)

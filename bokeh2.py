# importing all necessary libraries
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, PreText
from bokeh.layouts import column, row
from bokeh.models import CustomJS
import numpy as np

# create classes and functions

class Earth:
    def __init__(self, mass, radius, x, y):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        # self.pos

class Moon:
    def __init__(self, mass, radius, x, y, theta, r, t=0):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.theta = theta
        self.r = r
        self.t = t

def mu(m1, m2):
    return 6.67408e-11*(m1+m2)

def theta(r,m1,m2,t):
    _mu = mu(m1,m2)
    return _mu**(1/2)*t/r**(3/2)


Moon1 = Moon(7.34767309e22, 1737.4e3, 384400e3, 0,0,3.86e8)
Earth1 = Earth(5.972e24, 6371e3, 0, 0)

t = 0
Moon1.theta = theta(Moon1.r, Earth1.mass, Moon1.mass,t)
Moon1.x = Moon1.r*np.cos(Moon1.theta)
Moon1.y = Moon1.r*np.sin(Moon1.theta)

# Define the plot
p = figure(x_range=(-600e6, 600e6), y_range=(-600e6, 600e6),
    title='Orbit of the Moon around the Earth')

p.xaxis.axis_label = 'x (m)'
p.yaxis.axis_label = 'y (m)'

# Plot the earth
earth_source = ColumnDataSource(data=dict(x=[Earth1.x], y=[Earth1.y]))
p.circle(x="x", y="y", source=earth_source, size=Earth1.radius/1e5, color='blue')

# Plot the moon
moon_source = ColumnDataSource(data=dict(x=[Moon1.x], y=[Moon1.y],period=[27.3]))
p.circle(x="x", y="y", source=moon_source, size=Moon1.radius/1e5, color='gray')

# write text
pre = PreText(text='period')


#create sliders
time_slider = Slider(start=0, end=60, value=0, step=1, title="Time (days)")
m_earth_slider = Slider(start=1, end=1000, value=100, step=1, title="Earth Mass (%)")
m_moon_slider = Slider(start=1, end=1000, value=100, step=1, title="Moon Mass (%)")
d_slider = Slider(start=1, end=1000, value=100, step=1, title="Distance (%)")

callback = CustomJS(args=dict(source=moon_source, time=time_slider,
                              m_earth_slider=m_earth_slider, m_moon_slider=m_moon_slider,
                              d_slider=d_slider, text=pre,
                              r=Moon1.r, m_earth=Earth1.mass, m_moon=Moon1.mass),
                    code="""
    const data = source.data;
    function mu(m1, m2) {
        return 6.67408e-11*(m1+m2);
    }
    function theta(r,m1,m2,t) {
        const _mu = mu(m1,m2);
        return _mu**(1/2)*t/r**(3/2);
    }
    function calc_period(t,theta){
        return 2*Math.PI*t/theta;
    }
    const Earth_mass = m_earth_slider.value/100*m_earth;
    const Moon_mass = m_moon_slider.value/100*m_moon;
    const t = time.value*60*60*24;

    const Moon_theta = theta(r, Earth_mass, Moon_mass,t);
    const Moon_x = r*Math.cos(Moon_theta);
    const Moon_y = r*Math.sin(Moon_theta);

    const x = data['x'];
    const y = data['y'];

    x[0] = Moon_x;
    y[0] = Moon_y;
    const period = calc_period(t,Moon_theta)/60/60/24;
    text.text = "The moon takes: " + period + " day(s) to orbit the earth"; 

    source.change.emit();
""")

time_slider.js_on_change('value', callback)
m_earth_slider.js_on_change('value', callback)
m_moon_slider.js_on_change('value', callback)


layout = row(
    p, 
    column(time_slider, m_earth_slider, m_moon_slider,pre))

show(layout)
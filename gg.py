import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
# create a class for earth
class Earth:
    def __init__(self, mass, radius, x, y):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        # self.pos

class Moon:
    def __init__(self, mass, radius, x, y, theta, r):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.theta = theta
        self.r = r

def mu(m1, m2):
    return 6.67408e-11*(m1+m2)

def theta(r,m1,m2,t):
    _mu = mu(m1,m2)
    return _mu**(1/2)*t/r**(3/2)
# plot the moon
Moon1 = Moon(7.34767309e22, 1737.4e3, 384400e3, 0,0,3.86e8)
Earth1 = Earth(5.972e24, 6371e3, 0, 0)

t = 0
Moon1.theta = theta(Moon1.r, Earth1.mass, Moon1.mass,t)
print(Moon1.theta)
Moon1.x = Moon1.r*np.cos(Moon1.theta)
Moon1.y = Moon1.r*np.sin(Moon1.theta)

print(Moon1.x, Moon1.y)


# plot the earth
fig, ax = plt.subplots()
ax.plot(Earth1.x, Earth1.y, 'o', color='blue', markersize=Earth1.radius/1e5)
line, = ax.plot(Moon1.x, Moon1.y, 'o', color='gray', markersize=Moon1.radius/1e5)
ax.axis(xmin=-600e6,xmax=600e6,ymin=-600e6,ymax=600e6)
ax.set_aspect('equal', 'box')

# make my graph
fig.subplots_adjust(bottom=0.25)

axfreq = fig.add_axes([0.25, 0.15, 0.2, 0.03])
axearthmass = fig.add_axes([0.25, 0.10, 0.2, 0.03])
axmoonmass = fig.add_axes([0.6, 0.15, 0.2, 0.03])
axr = fig.add_axes([0.6, 0.10, 0.2, 0.03])
time_slider = Slider(
    ax=axfreq,
    valmin=0,
    valmax=30,
    valinit=0,
    label='Time (day)',
)
m_earth_slider = Slider(
    ax=axearthmass,
    valmin=1,
    valmax=10,
    valinit=5.97,
    label='Earth Mass (e24 kg)',
)
m_moon_slider = Slider(
    ax=axmoonmass,
    valmin=1,
    valmax=10,
    valinit=7.34,
    label='Moon Mass (e22 kg)',
)
r_slider = Slider(
    ax=axr,
    valmin=0,
    valmax=10,
    valinit=3.86,
    label='Distance (e8 m)',
)
def update(val):
    t = time_slider.val*60*60*24
    Earth1.mass = m_earth_slider.val*1e24
    Moon1.mass = m_moon_slider.val*1e22
    Moon1.r = r_slider.val*1e8
    Moon1.theta = theta(Moon1.r, Earth1.mass, Moon1.mass,t)
    Moon1.x = Moon1.r*np.cos(Moon1.theta)
    Moon1.y = Moon1.r*np.sin(Moon1.theta)
    print(Moon1.x, Moon1.y)
    line.set_ydata(Moon1.y)
    line.set_xdata(Moon1.x)
    fig.canvas.draw_idle()

time_slider.on_changed(update)
m_earth_slider.on_changed(update)
m_moon_slider.on_changed(update)
r_slider.on_changed(update)


plt.show()
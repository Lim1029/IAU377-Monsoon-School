#write me an animation of sine graph
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# %matplotlib inline
fig = plt.figure()
ax = plt.axes(xlim=(0, 2*np.pi), ylim=(-1, 1))
line, = ax.plot([], [], lw=2)
def init():
    line.set_data([], [])
    return line,
def animate(i):
    x = np.linspace(0, 2*np.pi, 1000)
    y = np.sin(x + 0.1 * i)
    line.set_data(x, y)
    return line,
anim = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=200, interval=1, blit=True)    
plt.show()
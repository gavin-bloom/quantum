import matplotlib as mpl
from pylab import *
import numpy as np
from qutip import *
from matplotlib import cm
import imageio

def animate_bloch(states, duration=0.05, save_all=False):

    b = Bloch()

    b.vector_color = ['r']
    b.view = [-40,30]
    images=[]
    try:
        length = len(states)
    except:
        length = 1
        states = [states]
    ## normalize colors to the length of data ##
    nrm = mpl.colors.Normalize(0,length)
    colors = cm.cool(nrm(range(length))) # options: cool, summer, winter, autumn etc.

    ## customize sphere properties ##
    b.point_color = list(colors) # options: 'r', 'g', 'b' etc.
    b.point_marker = ['o']
    b.point_size = [30]
    
    for i in range(length):
        b.clear()
        b.add_states(states[i])
        b.add_states(states[:(i+1)],'point')
        if save_all:
            b.save(dirc='tmp') #saving images to tmp directory
            filename="tmp/bloch_%01d.png" % i
        else:
            filename='temp_file.png'
            b.save(filename)
        images.append(imageio.imread(filename))
    imageio.mimsave('bloch_anim.gif', images, duration=duration)

def main():
    states = []
    x = 1 / (np.sqrt(2))
    #ts = linspace(0,(pi*x*(1/30)),int((pi*x*(1/3))))
    ts = linspace(0,1,10)
    for t in ts:
        t = t * pi * x * (1/30)
        states.append((np.exp(-3j*t)*((x*cos(3*x*t)- 1j*sin(3*x*t))*basis(2,0) + x*cos(3*x*t)*basis(2,1))).unit())
    animate_bloch(states, duration=0.05, save_all=False)

main()
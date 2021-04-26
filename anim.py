import matplotlib as mpl
from pylab import *
import numpy as np
from qutip import *
from matplotlib import cm
import imageio

x = 1 / (np.sqrt(2))
E = 3

def farhi_gutman(x,E,t):
    return (np.exp(E*-1j*t)*((x*cos(E*x*t)- 1j*sin(E*x*t))*basis(2,0) + x*cos(E*x*t)*basis(2,1)))

def scale_t(x,E,t):
    return t * pi * (1/x) * (1/(2*E*10))

def animate_bloch(states, duration=0.05, save_all=False):

    b = Bloch()
    b.xlabel = ['$\\left|+\\right>$', '$\\left|-\\right>$']
    b.ylabel = ['$\\left|i\\right>$','$\\left|-i\\right>$']
    b.zlabel = ['$\\left|0\\right>$', '$\\left|1\\right>$']
    
    b.add_states([farhi_gutman(x,E,0),farhi_gutman(x,E,scale_t(x,E,10))])

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
    #ts = linspace(0,(pi*x*(1/30)),int((pi*x*(1/3))))
    ts = linspace(0,1,10)
    for t in ts:
        t = scale_t(x,E,t)
        states.append(farhi_gutman(x,E,t).unit())
    animate_bloch(states, duration=0.05, save_all=False)

main()
__author__ = "Devrim Celik"
"""
Interative plot, showcasing the FitzHugh_Nagumo Model
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import Button, Slider

#==============================================================================#


def FitzHugh_Nagumo(_I=0.5, a=0.7, b=0.8, tau=1 / 0.08):

    ######### Experimental Setup
    # TIME
    T       =       400                       # total simulation length
    dt      =       0.01                      # step size
    time    =       np.arange(0, T+dt, dt)    # step values

    # CURRENT
    I = np.zeros(len(time))
    I[5000:35000] = _I

    # Memory
    V = np.empty(len(time))
    W = np.empty(len(time))

    # Initial Values
    V[0] = -0.7
    W[0] = -0.5

    for i in range(1, len(time)):
        #calculate membrane potential & resting variable
        V[i] = V[i - 1] + (V[i - 1] - (V[i - 1]**3) / 3 - W[i - 1] + I[i]) * dt
        W[i] = W[i - 1] + ((V[i - 1] + a - b * W[i - 1]) / tau) * dt

    return V, W


def I_values(_I=0.5, time=None):
    I = np.zeros(len(time))
    I[5000:35000] = _I
    return I


#==============================================================================#


def start_FN_sim():
    # time parameters for plotting
    T       =       400                       # total simulation length
    dt      =       0.01                      # step size
    time    =       np.arange(0, T+dt, dt)    # step values

    # initial parameters
    a       = 0.7
    b       = 0.8
    tau     = 1/0.08
    I_init  = 0.5
    # update functions for lines
    V, W = FitzHugh_Nagumo(_I=I_init, a=a, b=b, tau=tau)
    I = I_values(_I=I_init, time=time)

    ######### Plotting
    axis_color = 'lightgoldenrodyellow'

    fig = plt.figure("FitzHugh-Nagumo Neuron", figsize=(14, 7))
    ax = fig.add_subplot(111)
    plt.title("Interactive FitzHugh-Nagumo Neuron Simulation")
    fig.subplots_adjust(left=0.1, bottom=0.32)

    # plot lines
    line = plt.plot(time, V, label="Membrane Potential")[0]
    line3 = plt.plot(time, I, label="Applied Current")[0]
    line2 = plt.plot(time, W, lw=0.3, label="Recovery Variable")[0]

    # add legend
    plt.legend(loc="upper right")

    # add axis labels
    plt.ylabel("Potential [V]/ Current [A]")
    plt.xlabel("Time [s]")

    # define sliders (position, color, inital value, parameter, etc...)
    I_slider_axis = plt.axes([0.1, 0.17, 0.65, 0.03], facecolor=axis_color)
    I_slider = Slider(I_slider_axis, '$I_{ext}$', 0.0, 1.0, valinit=I_init)

    # update functions
    def update(val):
        V, W = FitzHugh_Nagumo(_I=I_slider.val)
        line.set_ydata(V)
        line2.set_ydata(W)
        line3.set_ydata(I_values(I_slider.val, time=time))

    # update, if any slider is moved
    I_slider.on_changed(update)

    # Add a button for resetting the parameters
    reset_button_ax = plt.axes([0.8, 0.02, 0.1, 0.04])
    reset_button = Button(
        reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def reset_button_was_clicked(event):
        I_slider.reset()

    reset_button.on_clicked(reset_button_was_clicked)

    plt.show()


#==============================================================================#

if (__name__ == '__main__'):
    start_FN_sim()

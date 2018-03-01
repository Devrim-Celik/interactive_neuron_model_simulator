__author__ = "Devrim Celik"

"""
Interative plot, showcasing the Izhikevich Model dynamics and the
diverse neuron types it can adapt to
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import  Button, Slider

def Izhikevich_Model(_I = 10, a = 0.02, b = 0.2, c = -65, d = 8):

    ######### Constants
    spike_value = 35                            # Maximal Spike Value

    ######### Experimental Setup
    # TIME
    T               =   1000                    # total simulation length [ms]
    dt              =   0.5                     # step size [ms]
    time            =   np.arange(0, T+dt, dt)  # step values [ms]
    # VOLTAGE
    V               =   np.zeros(len(time))     # array for saving voltage history
    V[0]            =   -70                     # set initial to resting potential
    # RECOVERY
    u               =   np.zeros(len(time))     # array for saving Recovery history
    u[0]            =   -14
    # CURRENT
    I = np.zeros(len(time))
    I[200:1500] = _I

    for t in range(1, len(time)):
        # if we still didnt reach spike potential
        if V[t-1] < spike_value:
            # ODE for membrane potential
            dV      = (0.04 * V[t-1] + 5) * V[t-1] + 140 - u[t-1]
            V[t]    = V[t-1] + (dV + I[t-1]) * dt
            # ODE for recovery variable
            du      = a * (b * V[t-1] - u[t-1])
            u[t]    = u[t-1] + dt * du
        # spike reached!
        else:
            V[t-1] = spike_value    # set to spike value
            V[t] = c                # reset membrane voltage
            u[t] = u[t-1] + d       # reset recovery

    return V

def I_values(_I=10):
    I = np.zeros(len(time))
    I[200:1500] = _I
    return I

if (__name__=='__main__'):
    # time parameters for plotting
    T               =   1000                    # total simulation length [ms]
    dt              =   0.5                     # step size [ms]
    time            =   np.arange(0, T+dt, dt)  # step values [ms]

    # initial parameters
    I_init = 10
    a_init = 0.02
    b_init = 0.2
    c_init = -65
    d_init = 8

    V = Izhikevich_Model()
    I = I_values()



    ######### Plotting
    axis_color = 'lightgoldenrodyellow'

    fig = plt.figure("Simple Izhikevich Neuron", figsize=(14,8))
    ax = fig.add_subplot(111)
    plt.title("Interactive Izhikevich Neuron Simulation")
    fig.subplots_adjust(left=0.1, bottom=0.5)

    # plot lines
    line = plt.plot(time, V, label="Membrane Potential")[0]
    line2 = plt.plot(time, I, label="Applied Current")[0]

    # add legend
    plt.legend(loc = "upper right")

    # add axis labels
    plt.ylabel("Potential [V]/ Current [A]")
    plt.xlabel("Time [s]")

    # define sliders (position, color, inital value, parameter, etc...)
    I_slider_axis = plt.axes([0.1, 0.40, 0.65, 0.03], facecolor=axis_color)
    I_slider = Slider(I_slider_axis, '$I_{ext}$ ', 0.1, 40, valinit=I_init)

    a_slider_axis = plt.axes([0.1, 0.35, 0.65, 0.03], facecolor=axis_color)
    a_slider = Slider(a_slider_axis, '$a$', 0.001, 0.15, valinit=a_init)

    b_slider_axis = plt.axes([0.1, 0.30, 0.65, 0.03], facecolor=axis_color)
    b_slider = Slider(b_slider_axis, '$b$', 0.001, 0.3, valinit=b_init)

    c_slider_axis = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axis_color)
    c_slider = Slider(c_slider_axis, '$c$', -75, -40, valinit=c_init)

    d_slider_axis = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor=axis_color)
    d_slider = Slider(d_slider_axis, '$d$', 0.001, 10, valinit=d_init)

    # update functions
    def update(val):
        line.set_ydata(Izhikevich_Model(I_slider.val, a_slider.val, b_slider.val, c_slider.val, d_slider.val))
        line2.set_ydata(I_values(I_slider.val))

    # update, if any slider is moved
    I_slider.on_changed(update)
    a_slider.on_changed(update)
    b_slider.on_changed(update)
    c_slider.on_changed(update)
    d_slider.on_changed(update)




    ################################################################################
    ########################### REGULAR SPIKING BUTTON #############################
    ################################################################################
    # Add a button for resetting the parameters
    RS_button_ax = plt.axes([0.1, 0.1, 0.15, 0.04])
    RS_button = Button(RS_button_ax, 'REGULAR SPIKING', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def RS_button_was_clicked(event):
        #I_slider.reset()
        a_slider.reset()
        b_slider.reset()
        c_slider.reset()
        d_slider.reset()

    RS_button.on_clicked(RS_button_was_clicked)




    ################################################################################
    ########################### INTRINSICALLY BURSTING BUTTON ######################
    ################################################################################
    # Add a button for resetting the parameters
    IB_button_ax = plt.axes([0.35, 0.1, 0.15, 0.04])
    IB_button = Button(IB_button_ax, 'INTRINSICALLY BURSTING', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def IB_button_was_clicked(event):
        #I_slider.reset()
        a_slider.reset()
        b_slider.reset()
        c_slider.set_val(-55)
        d_slider.set_val(4)

    IB_button.on_clicked(IB_button_was_clicked)




    ################################################################################
    ################################ CHATTERING BUTTON #############################
    ################################################################################
    # Add a button for resetting the parameters
    CH_button_ax = plt.axes([0.6, 0.1, 0.15, 0.04])
    CH_button = Button(CH_button_ax, 'CHATTERING', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def CH_button_was_clicked(event):
        #I_slider.reset()
        a_slider.reset()
        b_slider.reset()
        c_slider.set_val(-50)
        d_slider.set_val(2)

    CH_button.on_clicked(CH_button_was_clicked)




    ################################################################################
    ############################### FAST SPIKING BUTTON ############################
    ################################################################################
    # Add a button for resetting the parameters
    FS_button_ax = plt.axes([0.1, 0.02, 0.15, 0.04])
    FS_button = Button(FS_button_ax, 'FAST SPIKING', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def FS_button_was_clicked(event):
        #I_slider.reset()
        a_slider.set_val(0.1)
        b_slider.reset()
        c_slider.reset()
        d_slider.reset()

    FS_button.on_clicked(FS_button_was_clicked)




    ################################################################################
    ######################### LOW-THRESHOLD SPIKING BUTTON #########################
    ################################################################################
    # Add a button for resetting the parameters
    LTS_button_ax = plt.axes([0.35, 0.02, 0.15, 0.04])
    LTS_button = Button(LTS_button_ax, 'LOW-THRESHOLD SPIKING', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def LTS_button_was_clicked(event):
        #I_slider.reset()
        a_slider.reset()
        b_slider.set_val(0.25)
        c_slider.reset()
        d_slider.reset()

    LTS_button.on_clicked(LTS_button_was_clicked)




    ################################################################################
    ################################# RESONATOR BUTTON #############################
    ################################################################################
    # Add a button for resetting the parameters
    RZ_button_ax = plt.axes([0.6, 0.02, 0.15, 0.04])
    RZ_button_ = Button(RZ_button_ax, 'RESONATOR', color=axis_color, hovercolor='0.975')
    # TODO Does it work?
    # event of resert button being clicked
    def RZ_button_was_clicked(event):
        #I_slider.reset()
        a_slider.set_val(0.1)
        b_slider.set_val(0.26)
        c_slider.reset()
        d_slider.reset()

    RZ_button_.on_clicked(RZ_button_was_clicked)


    plt.show()

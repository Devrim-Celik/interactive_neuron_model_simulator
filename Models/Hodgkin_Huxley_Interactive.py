__author__ = "Devrim Celik"

"""
Interative plot, showcasing the Hodgkin Huxley Neuron Dynmics
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import  Button, Slider
from scipy.integrate import odeint


def HH(_I = 7, C_m = 1., g_Na = 120., g_K = 36., g_Leak = 0.3, E_Na = 50.,
            E_K = -77., E_Leak = -54.387):

    ######### Gating Kinetics
    m_alpha =       lambda V: 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))
    m_beta  =       lambda V: 4.0 * np.exp(-(V + 65.0) / 18.0)
    h_alpha =       lambda V: 0.07 * np.exp(-(V + 65.0) / 20.0)
    h_beta  =       lambda V: 1.0 / (1.0 + np.exp(-(V+35.0) / 10.0))
    n_alpha =       lambda V: 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))
    n_beta  =       lambda V: 0.125 * np.exp(-(V + 65) / 80.0)

    ######### Ion Currents
    I_Na    =       lambda V, m, h:     g_Na * m**3 * h * (V - E_Na)
    I_K     =       lambda    V, n:     g_K * n**4 * (V - E_K)
    I_Leak  =       lambda       V:     g_Leak * (V - E_Leak)

    ######### Experimental Setup
    # TIME
    T       =       400                       # total simulation length
    dt      =       0.1                       # step size
    time    =       np.arange(0, T+dt, dt)    # step values
    # CURRENT

    def I(t):
        return _I*(40<t<300)



    # Function to odeint over
    def change(X, t):
        V, m, h, n = X

        #calculate membrane potential & activation variables
        dV = (I(t) - I_Na(V, m, h) - I_K(V, n) - I_Leak(V)) / C_m
        dm = m_alpha(V) * (1.0 -m ) - m_beta(V) * m
        dh = h_alpha(V) * (1.0 - h) - h_beta(V) * h
        dn = n_alpha(V) * (1.0 - n) - n_beta(V) * n
        return dV, dm, dh, dn


    # integrate over all 4 differential equations, use following initial conditions
    all_changes = odeint(change, [-65, 0.05, 0.6, 0.32], time)
    V = all_changes[:,0]
    m = all_changes[:,1]
    h = all_changes[:,2]
    n = all_changes[:,3]

    return V, m, h, n

def I_values(time=None, _I=7):
    I = np.zeros(len(time))
    I[400:3000] = _I
    return I

def start_HH_sim():
    T       =       400                       # total simulation length
    dt      =       0.1                       # step size
    time    =       np.arange(0, T+dt, dt)    # step values

    #C_m_init     =       1.0         # membrane capacitance [uF/cm^2]
    g_Na_init    =       120.0       # maximum sodium conductance [mS/cm^2]
    g_K_init     =       36.0        # maximum potassium conductance [mS/cm^2]
    g_Leak_init  =       0.3         # maximum leak conductance [mS/cm^2]
    E_Na_init    =       50.0        # sodium nernst reversal potential [mV]
    E_K_init     =       -77.0       # potassium nernst reversal potential [mV]
    E_Leak_init  =       -54.387     # leaks nernst reversal potential [mV]

    I_init       =       15

    V, m, h, n = HH()
    I = I_values(time=time)

    ######### Plotting
    axis_color = 'lightgoldenrodyellow'

    fig = plt.figure("Hodgkin Huxley Neuron", figsize=(14,8))
    ax = fig.add_subplot(211)
    plt.title("Interactive Hodgkin Huxley Neuron Simulation")
    fig.subplots_adjust(left=0.1, bottom=0.25)

    # plot lines
    line = plt.plot(time, V, label="Membrane Potential")[0]
    line2 = plt.plot(time, I, label="Applied Current")[0]

    # add legend
    plt.legend(loc = "upper right")

    # add axis labels
    plt.ylabel("Potential [V]/ Current [A]")
    plt.xlabel("Time [s]")

    ###############
    ax = fig.add_subplot(212)

    line3 = plt.plot(time, m, 'r', label='m')[0]
    line4 = plt.plot(time, h, 'g', label='h')[0]
    line5 = plt.plot(time, n, 'b', label='n')[0]

    plt.ylabel('Gating Value')
    plt.xlabel("Time [s]")
    plt.legend(loc = "upper right")


    # define sliders (position, color, inital value, parameter, etc...)
    I_slider_axis = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axis_color)
    I_slider = Slider(I_slider_axis, '$I_{ext}$ ', 0.0, 7., valinit=I_init)

    gNa_slider_axis = plt.axes([0.1, 0.1, 0.17, 0.03], facecolor=axis_color)
    gNa_slider = Slider(gNa_slider_axis, '$g_{Na}$ ', 80., 160., valinit=g_Na_init)

    gK_slider_axis = plt.axes([0.34, 0.1, 0.17, 0.03], facecolor=axis_color)
    gK_slider = Slider(gK_slider_axis, '$g_{K}$ ', 0., 70., valinit=g_K_init)

    gLeak_slider_axis = plt.axes([0.58, 0.1, 0.17, 0.03], facecolor=axis_color)
    gLeak_slider = Slider(gLeak_slider_axis, '$g_{Leak}$ ', 0., 1., valinit=g_Leak_init)

    ENa_slider_axis = plt.axes([0.1, 0.05, 0.17, 0.03], facecolor=axis_color)
    ENa_slider = Slider(ENa_slider_axis, '$E_{Na}$ ', 20., 80., valinit=E_Na_init)

    EK_slider_axis = plt.axes([0.34, 0.05, 0.17, 0.03], facecolor=axis_color)
    EK_slider = Slider(EK_slider_axis, '$E_{K}$ ', -100., -50., valinit=E_K_init)

    ELeak_slider_axis = plt.axes([0.58, 0.05, 0.17, 0.03], facecolor=axis_color)
    ELeak_slider = Slider(ELeak_slider_axis, '$E_{Leak}$ ', -70, -40, valinit=E_Leak_init)

    def update(val):
        V, m, h, n =  HH(_I=I_slider.val, g_Na = gNa_slider.val,
            g_K = gK_slider.val, g_Leak = gLeak_slider.val,
            E_Na = ENa_slider.val, E_K = EK_slider.val,
            E_Leak = ELeak_slider.val)
        line.set_ydata(V)
        line2.set_ydata(I_values(I_slider.val, time=time))
        line3.set_ydata(m)
        line4.set_ydata(h)
        line5.set_ydata(n)

    # update, if any slider is moved
    I_slider.on_changed(update)
    gNa_slider.on_changed(update)
    gK_slider.on_changed(update)
    gLeak_slider.on_changed(update)
    ENa_slider.on_changed(update)
    EK_slider.on_changed(update)
    ELeak_slider.on_changed(update)

    # Add a button for resetting the parameters
    reset_button_ax = plt.axes([0.8, 0.02, 0.1, 0.04])
    reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def reset_button_was_clicked(event):
        I_slider.reset()
        gNa_slider.reset()
        gK_slider.reset()
        gLeak_slider.reset()
        ENa_slider.reset()
        EK_slider.reset()
        ELeak_slider.reset()

    reset_button.on_clicked(reset_button_was_clicked)

    plt.show()

if (__name__=="__main__"):
    start_HH_sim()

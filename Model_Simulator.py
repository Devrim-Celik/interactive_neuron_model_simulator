__author__ = "Devrim Celik"

import tkinter as tk

if (__name__=="__main__"):
    ####### Initialize root
    root = tk.Tk()
    root.title("Neuron Model Selector")

    ####### Size and Position of GUI
    w = 450
    h = 140
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    ####### Text
    lbl = tk.Label(root, text="Please select the Model you are interested in:")
    lbl.pack()
    lbl.config(font=("MS Sans Serif", 20, "bold"))

    ####### Button events --> corresponds to displaying Model
    def LIF_clicked(): # Leaky Integrate and Fire
        start_LIF_sim()
    def HH_clicked(): # Hodgkin-Huxely
        start_HH_sim()
    def IZ_clicked(): # Izhikevich
        start_IZ_sim()
    def FN_clicked(): # FitzHugh-Nagumo
        start_FN_sim()

    def close_window(root=root): # close window button
        root.destroy()

    ####### Buttons
    LIF_btn = tk.Button(root, text="Leaky Integrate-and-Fire Model",
        command=LIF_clicked, height=1, width=30)
    LIF_btn.pack()

    HH_btn = tk.Button(root, text="Hodgkin-Huxley Model",
        command=HH_clicked, height=1, width=30)
    HH_btn.pack()

    IZ_btn = tk.Button(root, text="Izhikevich Model",
        command=IZ_clicked, height=1, width=30)
    IZ_btn.pack()

    FN_btn = tk.Button(root, text="FitzHugh-Nagumo Model",
        command=FN_clicked, height=1, width=30)
    FN_btn.pack()


    EXIT_btn = tk.Button(root, text="Exit",
        command=close_window, height=1, width=15)
    EXIT_btn.pack()

    ######## Don't know why, but return error if I import them at the start of
    ########   the script
    from Models.LIF_Interactive import start_LIF_sim
    from Models.Hodgkin_Huxley_Interactive import start_HH_sim
    from Models.Izhikevich_Interactive import start_IZ_sim
    from Models.FitzHugh_Nagumo_Interactive import start_FN_sim

    ######## start root
    root.mainloop()

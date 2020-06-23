import numpy as np
import GraphicRepresentation as gr


# loads array from .txt file and plots it
saved_and_loaded = np.loadtxt('privacy7585.txt')
gr.plot_converted(saved_and_loaded)

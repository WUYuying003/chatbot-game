from pyo import *
s = Server().boot()
s.start()
a = Sine(freq=440, mul=0.1).out()
input("Press Enter to stop...")
s.stop()
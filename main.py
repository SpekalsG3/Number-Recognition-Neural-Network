from network import NeuralNetwork
from window import root, paintApp


network = NeuralNetwork()



# root.protocol("WM_DELETE_WINDOW", lambda: network.saveModel("model.json"))
root.mainloop()
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10, 10 + 0.2, 0.2)
y = 2 * x + 1

plt.plot(x, y, label="y = 2x + 1")
plt.title("График линейной функции")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()

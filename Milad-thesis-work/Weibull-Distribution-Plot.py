import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min

# Define shape (k) and scale (λ) parameters
shapes = [2.8, 2.8, 2.8, 2.8, 2.8]  # Example shape parameters
scales = [250, 150, 100, 80, 70]  # Example scale parameters

x = np.linspace(0, 500, 500)  # Range of values for x

plt.figure(figsize=(300, 6))

# Plot Weibull distributions for each shape and scale
for k, λ in zip(shapes, scales):
    pdf = weibull_min.pdf(x, k, scale=λ)  # Compute PDF
    plt.plot(x, pdf, label=f"Shape={k}, Scale={λ}")

plt.xlabel("Time(min)")
plt.ylabel("Failure rate")
plt.title("Weibull Distribution")
plt.legend()
plt.grid()
plt.show()

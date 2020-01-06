import numpy
import xpyplot as plt


x=numpy.random.uniform(0,2,10000)
dx=numpy.random.normal(size=x.shape)
#plt.scatter(x, x+dx, alpha=0.5)
plt.scatter(x, x+dx)
plt.title("test Plot")
plt.savefig("plot1.png")



#######
xpyplot
#######

A small utility library that captures calls to matplotlib's pyplot
interface and saves the data being plotted together with the plotting
commands. In this way it allows easy re-plotting when the user's
otherwise omitted to keep proper record of the data.

For example::

     import xpyplot as plt
     import numpy

     x=numpy.array([1,2,3])
     plt.plot(x, x*2+1)
     plt.savefig("testsample.png")
          

will produce the expected plot ```testsample.png``` but also a script
```testsample.script.py```::

     plot1=numpy.load(open("testsample.plot1.npy", "rb"))
     plot0=numpy.load(open("testsample.plot0.npy", "rb"))
     pyplot.plot(*[plot0, plot1, ], **{}, scalex=True, scaley=True, data=None, )
     pyplot.savefig(fname="testsample.png", )


and two numpy array files ```testsample.plot1.npy``` and
```testsample.plot0.npy```.  Running the generated script will
reproduce the original plot.


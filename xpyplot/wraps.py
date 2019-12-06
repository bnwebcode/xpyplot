import os
import functools
import json
import inspect
import tempfile
import shutil

import numpy

from matplotlib import pyplot


_plotcmds = ["hist"]

# List of accumulated commands
_CL= []
# File descriptors for storing data
_FD= {}
__i=0
# command counter
__c=0


def sarg(n, a):
    "Save argument"
    global _FD, _CL, __i
    if isinstance(a, numpy.ndarray):
        vname=n+str(__i)
        ff=tempfile.NamedTemporaryFile(delete=False)
        _FD[vname]=ff
        numpy.save(ff, a)
        ff.close()
        __i+=1
        return vname
    elif isinstance(a, str):
        return "\"{}\"".format(a)
    else:
        return str(a)

def sargl(n, a):
    "Save argument list"
    res="["
    for x in a:
        res+=sarg(n, x) + ", "
    res+="]"
    return res

def flushdatafiles(pref):
    global _FD, _CL
    for k in _FD:
        tf=_FD[k]
        nf=pref+"."+k+".npy"
        if os.path.exists(nf) and os.path.isfile(nf):
            os.remove(nf)
        # Shutil version cane move between different devices, os can not
        shutil.move(tf.name, nf)
        _CL.insert(0,"{}=numpy.load(open(\"{}\", \"rb\"))\n".format(k, nf))
    _FD={}

def scmd(n, args):
    global _CL
    res="pyplot.{}(".format(n)
    for k in args:
        # We need to trap args and kwargs because pyplot functions
        # like plot are themselves wrappers which do not transfer the
        # wrapped function signatures (only the docstring is
        # copied). Maybe an improvement for matplotlib for future?
        if k == "args":
            res += "*{}".format(sargl(n, args[k])) +", "
        elif k == "kwargs":
            res +=  "**{}".format(args[k]) +", "
        else:
            res +=  "{}=".format(k) + sarg(n, args[k]) +", "
    _CL.append(res+")\n")
    return res

def flush(pref):
    global _CL
    flushdatafiles(pref)
    with open(pref+".script.py", "w") as f:
        for l in _CL:
            f.write(l)
    _CL=[]
    __i=0

def plotw(f):
    "Wrap a plotting-type function"
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        aa=inspect.getcallargs(f, *args, **kwargs)
        scmd(f.__name__, aa)
        return f(*args, **kwargs)
    return wrapper

plotfns=["hist", "plot", "scatter"]

for f in plotfns:
    globals()[f]=plotw(getattr(pyplot, f))



def outw(f):
    "Wrap an output function"
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        kwargs["fname"]=args[0]
        scmd(f.__name__, kwargs)
        flush(os.path.splitext(args[0])[0])
        return f(**kwargs)        
    return wrapper    

savefig=outw(pyplot.savefig)


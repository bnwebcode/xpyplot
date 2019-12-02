import functools
import json
import inspect
import tempfile

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

def flushdatafiles(pref):
    global _FD, _CL
    for k in _FD:
        tf=_FD[k]
        nf=pref+"."+k+".npy"
        os.replace(tf.name, nf)
        _CL.insert(0,"{}=numpy.load(open(\"{}\", \"rb\"))\n".format(k, nf))
    _FD={}

def scmd(n, args):
    global _CL
    res="pyplot.{}(".format(n)
    for k in args:
        if k == "kwargs":
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

def hist(*args, **kwargs):
    aa=inspect.getcallargs(pyplot.hist, *args, **kwargs)
    scmd(pyplot.hist.__name__, aa)
    pyplot.hist(*args, **kwargs)

def savefig(*args, **kwargs):
    kwargs["fname"]=args[0]
    scmd(pyplot.savefig.__name__, kwargs)
    flush(os.path.splitext(args[0])[0])
    pyplot.savefig(**kwargs)

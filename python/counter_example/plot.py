import matplotlib.pyplot as plt; 
from numpy import arange;
from math import sqrt;

def t1(c, u):
	if u==0:
		return 1;
	else:
		return (1-c)/(1-c + c*u**2);
def c(u):
	return 1/(u+1);

for u in [1,.7,.3,.1]:
	xpoints = arange(0,1,.01);
	t1points = [t1(x,u) for x in xpoints];
	plt.plot(xpoints, t1points);
	plt.text(c(u),c(u),r'$c('+str(u)+')$',backgroundcolor = 'white',horizontalalignment='center',
        verticalalignment='center', size = 18);

plt.plot(xpoints,xpoints);

plt.show();
from matplotlib.pyplot import *;
from math import sin, cos,pi;
from random import random;


def a(N,eta = 0,pe = 0):
	g = lambda x: sin(3*x)**3*(cos(4*x))+cos(x**2)**2*sin(x);

	xpoints =  [2*i/N for i in range(1,N)];
	norm = sum([abs(g(i/N)) for i in range(1,N)]);
	ypoints = [abs(g(i/N))/norm for i in range(1,N)];
	if pe!=0:
		if (len(pe)!= N-1):
			return False;
		else:
			ynoise = [(1-eta)*abs(g(i/N))/norm + eta*pe[i-1] for i in range(1,N)];
	else:
		ynoise = 0;
	return {'x':xpoints, 'y':ypoints,'ynoise':ynoise};

def E(N):
	ra =  [random() for i in range(1,N) ];
	norm = sum(ra);
	return [p/norm for p in ra];

def ap(N,eta = 0, pe = 0, name = 'pure_vs_noise.pdf',showval = True):
	ylimit = 1;
	if pe==0:
		points = a(N,eta,pe);
		x = points['x'];
		y = points['y'];
		plot(x,y,'bo--');
		xlim(0,2);
		ylim(0,ylimit);
		#xticks(x,[r'$x_'+str(i)+'$' for i in range(N) ]);
		xticks([x[0],x[N-2]],[r'$a_{0}$', r'$a_{n}$']);
		yticks([0,ylimit],[r'$0$',r'$ '+str(ylimit)+' $']);
		show();
	else:
		points = a(N,eta,pe);
		x = points['x'];
		y = points['y'];
		yno = points['ynoise'];
		p1 = plot(x,y,'bo--');
		p2 = plot(x,yno,'rs--');
		xlim(0,2);
		ylim(0,ylimit);
		xticks([x[0],x[N-2]],[r'$a_{0}$', r'$a_{n}$']);
		yticks([0,ylimit],[r'$0$',r'$ '+str(ylimit)+' $']);
		xlabel(r'$\Omega_A$');
		ylabel(r'$p$')
		legend([r'Pure distribution',r'Noisy distribution with $\eta = '+str(eta)+'$ ']);
		#savefig('/Compilationes/Archius_latex/6e_tfg_Year/tfg/pure_vs_noise.pdf', format='PDF');
		savefig(name, format='PDF');
		if showval:
			show();
		clf();


N=3;
#for i in range(100):
#	ap(N,.5,E(N),showval = False, name = 'effect'+str(i)+'.pdf');
ap(N,.5,E(N));


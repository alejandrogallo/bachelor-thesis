from mpl_toolkits.mplot3d import Axes3D;
import matplotlib.pyplot as plt;
from numpy import sin,cos,pi;
from math import factorial;
from itertools import combinations;
import itertools;



def stock_color(k,N):
	start = tuple(map( lambda x: x/255, (255,0,0) ) );
	end = tuple(map( lambda x: x/255,  	(0,0,255) ) );
	step = tuple(map( lambda x,y: (y-x)/N , start, end ));
	step_color = tuple(map(lambda x,y: x+k*y , start, step ));
	return step_color;
def colors(k):
	col = ['b','g', 'r','c','m','k'];
	ind = int(k%len(col));
	return col[ind];

def combination(N, k ='all'):
	if k=='all':
		return [	[	[set(k),r] for k in list(itertools.combinations(range(1,N+1),r))]	 for r in range(N+1)];
	else:
		r = k;
		return [[set(k),r] for k in list(itertools.combinations(range(1,N+1),r))];

def binomial(N,k):
	if (k>N)or (k<0):
		print("Error in binomial function:::Check the range of the parameters!!");
		return False;
	return int(factorial(N)/(factorial(k)*factorial(N-k)));

def dif(k,N):
	if k!=N:
		return binomial(N,k)-binomial(N,k+1);
	else:
		False;

def Sinpoints(k,N,z, ph =0):
	num = binomial(N,k);
	if k==0 or k==N:
		r =0;
	else:
		r = 1;
	sets = combination(N,k);
	return [[(r*cos(i * 2*pi/num + ph),r*sin(i * 2*pi/num + ph),z),sets[i][0]] for i in range(num)];

def Points(N, phlist = []):
	phs = [0 for i in range(N+1)];
	for i in range(len(phlist)):
		if len(phlist[i])!= 2:
			phs[i]=0;
		else:
			phs[phlist[i][0]] = phlist[i][1];

	return [Sinpoints(k,N,N-z,phs[k]) for k,z in [(t,t) for t in range(N+1)] ];

def Edges(N,phlist = []):
	points = Points(N, phlist);
	segments = [];
	for i in range(N):#we are in the ith floor and want to compare with the i+1
		for element in points[i]:
			for downelement in points[i+1]:
				if element[1].issubset(downelement[1]):
					segments += [[element[0],downelement[0],i]];
	return segments;
		


N = 4;
def construct_graph(N):
	dephasage = [[2,0*pi/4]];
	points = Points(N,dephasage);
	segments = Edges(N,dephasage);
	
	
	
	fig = plt.figure();
	ax = fig.gca(projection='3d');
	
	
	for piso in points:
		for element in piso:
			if(len(element[1])==0):
				Label = r'$S(\emptyset)$';
			elif len(element[1])==1 :
				Label = r'$S('+str(tuple(element[1])[0])+')$';
			else:
				Label = r'$S'+str(tuple(element[1]))+'$';
			ax.text(element[0][0],element[0][1],element[0][2],Label, backgroundcolor = (1,1,1,.7), 
				color = 'black' ,verticalalignment = 'center', horizontalalignment = 'center');
	
	for line in segments:
		ax.plot([line[0][0],line[1][0]],[line[0][1],line[1][1]],[line[0][2],line[1][2] ], 
			color = colors(line[2]));#color = stock_color(line[2],N));
	
	
	
	
	
	
	ax.set_xlim3d(-1, 1)
	ax.set_ylim3d(-1, 1)
	ax.set_zlim3d(0, N)
	
	ax.set(aspect = 1);
	
	
	
	plt.title('Joint-measuring graph for '+str(N)+' effects');
	
	plt.xticks([]);
	plt.yticks([]);
	ax.set_zticks(range(N+1));
	
	ax.set_zlabel('Stories');
	
	plt.show()




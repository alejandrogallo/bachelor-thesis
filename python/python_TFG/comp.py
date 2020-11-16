#Through the whole module N will be the number of effects we would like to consider, and it can 
#have any value from 2 on. 
import cvxopt as cvx;
import picos as pic;
from numpy import kron;
from numpy import zeros;
from numpy import eye;
from numpy import sqrt;
import numpy;
from math import factorial;
from itertools import combinations;
import itertools;


#HERE WE DEFINE THE DEFINING PARAMETERS FOR Gamma_i, 
#N is the number of Gammas that we would like to have, 
#and r goes from 1 to N. 
def Gamma_parameters(r,N):
	#Every step in the production of Gammas has an even number 
	#of Matrices, so we find out, given that we want only N
	#matrices, how many steps would that involve.
	if (N%2 == 0):
			maxstep = int(N/2);
	else:
		maxstep = int((N-1)/2);
	
	if r!=1:
		if (r>N)or (r<=0):
			return False;
		elif r%2==0:
			#print('It\'s pair!!');
			step = int(r/2);
			sigmax = 1;
			sigmay = 0;
		else:
			#print('It\'s even!');
			step = int((r-1)/2);
			sigmax = 0;
			sigmay = 1;
		number_ones = step-1;
		number_sigmaz = maxstep - number_ones -1;
	else:
		#print('is one!');
		step = 0;
		sigmax = 0;
		sigmay=0;
		number_ones = 0;
		number_sigmaz = maxstep;
	return {'step':step,'maxstep':maxstep , 'sigmax':sigmax,'sigmay':sigmay,'number_ones':number_ones,'number_sigmaz':number_sigmaz};


#Here we use the information provided by Gamma_parameters above to construct the actual Gammas.
def Gamma(r,N):
	#Controlclause
	if (r>N)or (r<=0):
		print("Error generating Gammas::: Check the range of the parameters!!");
		return False;
	#This will give us the matrices.
	sigmas = {'sigmax':[[0,1],[1,0]], 'sigmay':[[0,-complex(0,1)],[complex(0,1),0]], 'sigmaz':[[1,0],[0,-1]]};
	parameters = Gamma_parameters(r,N);
	gamma = 1;
	if parameters['number_ones']>0:
		gamma = kron(gamma,eye(2**parameters['number_ones']) );
	if parameters['sigmax']:
		gamma = kron(gamma, sigmas['sigmax']);
	if parameters['sigmay']:
		gamma = kron(gamma, sigmas['sigmay']); 
	for x in range(0,parameters['number_sigmaz']):
		gamma = kron(gamma, sigmas['sigmaz']);
	return gamma; 

def Dimension(N):
	#we study cases for the tensor_steps. If we have k tensor steps, then we have 2k+1 Gammas
	#if N = 2k+1 then the dimension being 2^(2k) will be 2^(N-1) etc...
	if (N%2) == 0:
		return 2**N;
	else:
		return 2**(N-1);

def Dimension_sym(N, case = 'environement'):
	nd =  sqrt(4*Dimension(N));
	if case == 'environement':
		return int(nd**2);
	elif case == 'spanned':
		return int(nd*(nd+1)/2);

def Parameters_number(subset,N, case = 'symmetric'):
	if case =='symmetric':
		return Dimension_sym(N, 'spanned')*(2**subset -subset-1)+1;
	elif case =='hermitian':
		return Dimension(N)*(2**subset -subset-1)+1;
	else:#default is hermitian
		return Dimension_sym(N, 'spanned')*(2**subset -subset-1)+1;

def binomial(N,k):
	if (k>N)or (k<0):
		print("Error in binomial function:::Check the range of the parameters!!");
		return False;
	return factorial(N)/(factorial(k)*factorial(N-k));

def Parts_parametrisation(N):#WECOULD HAVE SOME TROUBE HERE WITH N PAIR OR UNPAIR, LET'S USE ALWAYS PAIR NUMBERS!
	#Here we get the real parametrisation and it will return a list having the following characteristics:
	#List [number of elements selector] [ permutation selector (1,2,3),---, (N-2,N-1,N) eg] [actual permutation (=0) or dimension of the permutation (=1)]
	return [	[	[set(k),r] for k in list(itertools.combinations(range(1,N+1),r))]	 for r in range(N+1)];


def Tensor_steps(N):
	if N%2 ==0:
		return N/2;
	else:
		return (N-1)/2;



def Effect(k,N,eta):
	if eta <0 or eta >1:
		print("Error defining effects::: Eta must be a purity parameter, i.e. must be in [0,1]!\n");
		return False;
	return (0.5)*(eye(2**Tensor_steps(N)) + eta*Gamma(k,N) );


def Index_param_to_index_x(k,t,N):
	d = Dimension_sym(N,'spanned');
	if k<2 or k>N or t>=binomial(N,k):
		print("Error in generating indexes of parametrisation from combinations to x::: Check the ranges of the parameters!\n");
		return False;
	#Here we must consider that t runs from 0 to binomial(N,k)-1 in python. 
	begin = sum([  binomial(N,k) for k in range(2,k)],t)*d+1;
	end = begin + d-1;
	return [begin,end];	


def G_subset(k,t,N,Basis,Combinations,eta=0,mode = 'complex'):
	if mode != 'complex':
		d = Dimension_sym(N, 'environement');
		ds = Dimension_sym(N,'spanned');
	else:
		d = Dimension_sym(N, 'environement');
		ds = d;
	#Let's put security conditions, Combinations must have N+1 elements, since it has 0 element-sets to N-elements sets. 
	if len(Combinations) != N+1:	
		print("Error generating G_subsets::: Combinations must have N+1 elements!\n");
		return False;
	if len(Basis)!= ds : 
		print("Error generating G_subsets::: Check dimension of Basis vector!\n");
	#we initialise G_sub to have of course Parameters_number(N,N) elements. The G_sub[0] is always 0 for k>0.
	zero = cvx.matrix( 0 , ( int(sqrt(d)), int(sqrt(d)) ) ); 
	G_sub = [zero for l in range(Parameters_number(N,N))];
	h_sub = zero;
	if k==0:
		#Here we have the inequality involving lambda. For the first parameter we need eye(sqrt(Dimension(N)))
		G_sub[0] = eye(sqrt(d));
		#We write here the h part, which is the negative of the sum of all effects
		h_sub = sum([complex_to_real(Effect(j,N,eta)) for j in range(1,N+1)]);
		for q in range(2,N+1):
			for T in range(binomial(N,q)):
				indexes = Index_param_to_index_x(q,T,N);
				iRange = xrange(indexes[0],indexes[1]);
				for i in iRange:
					G_sub[i] = (-1)**Combinations[q][T][1]*Basis[i-iRange[0] ];
	#the following algorithm is valid for k>=1
	elif k>=1:
		#For the lambda parameter is also 0 at the beginning 
		G_sub[0] = zero;
		#NOW we construct the h matrix, which is only different from zero if k==1, and if k==1 it will be the corresponding k effect. 
		if k==1:
			#here is t+1 because t goes from 0 to n-1 for k = 1
			h_sub = complex_to_real(Effect(t+1,N,eta));
		#Here we make zero for all subset which have less or equal cardinality than the considered at the moment
		for q in range(2,k+1):
			for T in range(binomial(N,q)):
				indexes = Index_param_to_index_x(q,T,N);
				iRange = xrange(indexes[0],indexes[1]);
				for i in iRange:
					if q!=k and T!=t:	
						G_sub[i] = zero;
					else:
						G_sub[i] = Basis[i-iRange[0] ];
		#Now we process the subsets of higher cardinality
		for q in range(k+1,N+1):
			for T in range(binomial(N,q)):
				indexes = Index_param_to_index_x(q,T,N);
				iRange = xrange(indexes[0],indexes[1]);
				if Combinations[k][t][0].issubset(Combinations[q][T][0]):
					for i in iRange:
						##error, we must have (-1)**(|A|-|Omega|)
						G_sub[i] = (-1)**(Combinations[q][T][1]-k)*Basis[i-iRange[0] ];
				else:
					for i in iRange:
						G_sub[i] = zero;
	else:
		print("Error in k::: it must be 0,1 or >=2");
		return False;
	return {"G":[-j for j in G_sub], "h":h_sub};


def from_list_to_cvxopt_matrix(A,N):	
	if type(A) is list:
		#return cvx.matrix([list(reshape(k, len(k)**2  ) )	 for k in A 	]);
		he= cvx.matrix([cvx.matrix(k,(1,Dimension_sym(N,'environement') )) for k in A]);
		return he;
	else:
		print("Error converting list into cvxopt matrices.\n");


def Ghc(N,Basis,Combinations,eta=0):
	c = cvx.matrix([1] + [0 for j in range(1, Parameters_number(N,N))], tc = 'd');
	G = [];
	h = [];
	for q in range(0,N+1):
		for t in range(0, binomial(N,q)):
			T = G_subset(q,t,N,Basis,Combinations,eta);
			G += [from_list_to_cvxopt_matrix(T['G'],N)];
			h += [cvx.matrix(T['h'], tc = 'd')];
	return {'c':c, 'G':G, 'h':h};

#We think it as afunction because it's easier than the hermitian ones.
def Sym_basis( N,k=1, all = False):
	d  = Dimension_sym(N, 'environement');
	dn = int(sqrt(d));
	dim = Dimension_sym(N, 'spanned');
	if k>dim:	
		print('Error constructing the symmetric basis::: there are only n(n+1)/2 elements, k should not be greater than that!!');
		return False;
	if not all:
		j=0;
		for i in range(dn,0,-1):
			j+=i;
			if k<=j:	
				#it means that it is in the dn-i row in python notation
				row = dn-i;
				#the -1 is for the python notation
				column = dn + k-j-1;
				if column == row:
					return cvx.spmatrix([1],[row],[column],(dn,dn));
				else:	
					return cvx.spmatrix([1,1],[row, column],[column,row],(dn,dn));
	else:
		return [Sym_basis(N, k = i) for i in range(1,dim+1)];


def Herm_basis(N,k=1, all = False):
	d  = Dimension(N);
	dn = int(sqrt(d));
	if k>d:	
		print('Error constructing the hermitian basis::: there are only n^2 elements, k should not be greater than that!!');
		return False;
	if not all:
		j=0;
		for i in range(1,dn+1):
			j=i*dn;
			if k<=j:
				#it means that it is in the dn-i row in python notation
				row = i-1;
				column = dn + k-j-1;
				#Under the diagional or above?
				if column<row:
					return cvx.spmatrix([complex(0,-1),complex(0,1)],[row, column],[column,row],(dn,dn));
				else:
					if column == row:
						return cvx.spmatrix([1],[row],[column],(dn,dn));
					else:	
						return cvx.spmatrix([1,1],[row, column],[column,row],(dn,dn));
	else:
		return [Herm_basis(N,i) for i in range(1,d+1)];


def complex_separate(A):
	#A should be a cvx.sparse matrix or a cvx.matrix 
	if type(A) is cvx.base.matrix or type(A) is cvx.base.spmatrix:
		if A.typecode =='z':
			return [A.real(), A.imag()];
		else:
			return [A,cvx.matrix(0 , A.size )];
	else:
		print('Error separating matric in complex and real::: it must be of type cvx.base.matrix or cvx.base.spmatrix!!');
		return False;

def complex_to_real(L):
	if type(L) is list and len(L) ==2:	#It is [real, imag]
		return cvx.sparse([[L[0],-L[1]],[-L[1],L[0]]]);
	else:
		li = complex_separate(cvx.matrix(L));
		return complex_to_real(li);


def compare(A,B = []):
	if type(B) is list:
		C = A.trans();
	else:
		C= B;
	if A.size == C.size:
		d = A.size[0];
		d = d**2;	
		for i in xrange(d):
			t = (A[i] == C[i]);
			if t==False:
				return False;
		return True;

N = 2;
T = Parts_parametrisation(N);
Q = Sym_basis(N, all = True);
eta = .4;

pepe = Ghc(N,Q,T,eta);
c = pepe['c'];
G = pepe['G'];
h = pepe['h'];
g = lambda x: complex_to_real(Effect(x,N,eta));






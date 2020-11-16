import cvxopt as cvx;
import picos as pic;


P = pic.Problem();

A = cvx.matrix([-4,2,2,9]);
I = cvx.matrix([[1,0],[0,1]]);

t = P.add_variable('t',1);

#P.set_objective('min',t);
#P.add_constraint(t*I-A>>0);




#def Basis_combinations(N):
#	#we initialize the list A
#	start_dimension = 4; 
#	A = [[i] for i in range(start_dimension) ];
#	for i in range(1,Tensor_steps(N)):
#		A = [  [ A[r]+[k] for k in range(start_dimension) ] for r in range(len(A))];
#		B = [ ];
#		for x in range(len(A)):
#			B = B+A[x];
#		A = B;
#	return A;
#
#def Basis_maker(N):
#	d = Dimension(N);
#	tensor_steps = Tensor_steps(N);
#	combinations = Basis_combinations(N);
#	sigmas = [eye(2),[[0,1],[1,0]], [[0,-complex(0,1)],[complex(0,1),0]], [[1,0],[0,-1]]];
#	result = [];
#
#	for x in combinations:
#		dummy = 1;
#		for i in x:
#			dummy = kron(dummy, sigmas[i]);
#		result = [dummy] + result;
#
#	return result;
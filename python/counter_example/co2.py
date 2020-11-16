from math import sqrt, ceil;

#Definition of the formula for the eigenvalues. There is an optional parameter, mode, 
#which one can change to give us only the +-solutions or the maximum of both eigenvalues. 
#By default it is set to max. 
def eig(alpha,beta,t,u,mode = 'max'):
	#calculate the part with and without the square root of the formula.
	no_sqrt = (alpha - t + 2 - beta)/2;
	yes_sqrt = (sqrt((beta+alpha-t)**2-4*beta*(alpha-t)*u**2))/2;
	#cases considering the different values of the mode parameter.
	if mode == 'plus':
		value = no_sqrt+yes_sqrt;
		return value;
	elif mode == 'minus':
		value = no_sqrt-yes_sqrt;
		return value;
	elif mode == 'max':
		#this will return the norm, i.e. the maximum of the eigenvalues. 
		value = max(no_sqrt+yes_sqrt, no_sqrt-yes_sqrt);
		return value;
	else:
		return False;

def c(u):
	return 1/(u+1);

def t1(c, u):
	if u==0:
		return 1;
	else:
		return (1-c)/(1-c + c*u**2);

def tconstraint(alpha,beta,u):
	t1ab = t1(beta,u);
	t1ba = t1(alpha,u);
	if alpha <=t1ab:
		constraint_ab = alpha;
	else:
		constraint_ab = t1ab;
	if beta <= t1ba:
		constraint_ba = beta;
	else:
		constraint_ba = t1ba;
	return {'constraint_ab':constraint_ab, 'constraint_ba':constraint_ba};


#This function will look for suitable points for which the norm varies in dependence of 
#the permutation of alpha and beta. 
def look_for_points(N,all = False, count = False):
	#we create a grid in (0,1) of N-2 points. 
	precision = 5;
	total_points = (N+1)*(N+1)*N;
	perc_step = 0;
	count_total = 0;
	count_dif =0;
	count_great_great=0;
	count_great_less=0;
	count_less_less=0;
	count_less_great=0;
	eq_count_great_great=0;
	eq_count_great_less=0;
	eq_count_less_less=0;
	eq_count_less_great=0;
	for i in range(0,N+1):
		for j in range(0,N+1):
			#u is in [0,1)
			for k in range(1,N+1):
				alpha = round((1-i/N)*1 + (i/N)*0,precision);
				beta = round((1-j/N)*1 + (j/N)*0,precision);
				u =round((1-k/N)*1 + (k/N)*0,precision);
				constraint = tconstraint(alpha,beta,u);
				tab = round(constraint['constraint_ab'],precision);
				tba = round(constraint['constraint_ba'],precision);
				ab = round(eig(alpha, beta, tab,u),precision);
				ba = round(eig(beta,alpha,tba,u),precision);
				if (alpha < t1(beta,u)) and (beta > t1(alpha,u)):
					print('fuck!!');
					print(alpha,beta);
				count_total+=1;
				#Percentage
				if count_total/total_points >= perc_step:
					print(str(ceil(100*perc_step))+'%');
					perc_step += .1;
				if ab != ba:
					count_dif+=1;
					points = {'alpha':alpha, 'beta':beta, 'u':u, 'tab':tab, 'tba':tba, 'ab':ab, 'ba':ba};
					if all:
						#print(points);
						if alpha > t1(beta,u):
							if beta > t1(alpha,u):
								count_great_great+=1;
								#print('\\hline '+str(alpha)+' & '+str(beta)+' & '+str(round(t1(alpha,u),2))+' & '+str(round(t1(beta,u),2))+' & '+str(u)+' & '+str(ab)+' & '+str(ba)+' & yes'+' \\\\' );
							elif beta < t1(alpha,u):
								count_great_less+=1;
						elif alpha < t1(beta,u):
							if beta > t1(alpha,u):
								count_less_great+=1;
							elif beta < t1(alpha,u):
								count_less_less+=1;
						#else:
							#print('alpha = beta!');
					#else:
						#When we only want a suitable point, we get the first suitable point. 
						#return points; 
				else:
					if all:
						#print(points);
						if alpha > t1(beta,u):
							if beta > t1(alpha,u):
								eq_count_great_great+=1;
								#if(alpha!=beta):
								#	print('fuck!');
								#	print(alpha,beta,u,t1(beta,u),t1(alpha,u));
							elif beta < t1(alpha,u):
								eq_count_great_less+=1;
								#print(alpha,beta,u,t1(beta,u),t1(alpha,u));
						elif alpha < t1(beta,u):
							if beta > t1(alpha,u):
								eq_count_less_great+=1;
							elif beta < t1(alpha,u):
								eq_count_less_less+=1;

	#print('We didin\'t find any suitable matches!! :(');
	if(count and all):
		print('---------------------');
		print('total points = '+str(count_total));
		print('\ntotal suitable points = '+str(count_dif));
		print('   total great great points = '+str(count_great_great));
		print('   total great less points = '+str(count_great_less));
		print('   total less great points = '+str(count_less_great));
		print('   total less less points = '+str(count_less_less));
		print('\ntotal nonsuitable points = '+str(count_total-count_dif));
		print('   total great great points = '+str(eq_count_great_great));
		print('   total great less points = '+str(eq_count_great_less));
		print('   total less great points = '+str(eq_count_less_great));
		print('   total less less points = '+str(eq_count_less_less));


	return False;

look_for_points(100,all=True, count = True)
#print(look_for_points(10,all=False))



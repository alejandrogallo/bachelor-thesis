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
def t1(c, u):
	if u==0:
		return 1;
	else:
		return (1-c)/(1-c + c*u**2);
#This is to calculate the constraint, we just compare t1(beta) and alpha
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
	#We return the values in the format of a dictionary
	return {'constraint_ab':constraint_ab, 'constraint_ba':constraint_ba};
#This function will look for suitable points for which the norm varies in dependence of 
#the permutation of alpha and beta. 
#If count is set to true then we will count the numbers that are in the different 
#sets M<<, M<> or M>>
def look_for_points(N,all = False, count = False):
	#we create a grid in (0,1) of N-2 points. 
	#The precision we will use is 5 decimal places
	precision = 5;
	#the number of total points (alpha,beta,u) which are looked
	total_points = (N+1)*(N+1)*N;
	#help variable for the percentage process
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
				count_total+=1;
				#Percentage process
				if count_total/total_points >= perc_step:
					print(str(ceil(100*perc_step))+'%');
					perc_step += .1;
				if ab != ba:
					count_dif+=1;
					points = {'alpha':alpha, 'beta':beta, 'u':u, 'tab':tab, 'tba':tba, 'ab':ab, 'ba':ba};
					if all:
						if alpha > t1(beta,u):
							if beta > t1(alpha,u):
								count_great_great+=1;
							elif beta < t1(alpha,u):
								count_great_less+=1;
						elif alpha < t1(beta,u):
							if beta > t1(alpha,u):
								count_less_great+=1;
							elif beta < t1(alpha,u):
								count_less_less+=1;
					else:
						#When we only want a suitable point, we get the first suitable point. 
						return points; 
				else:
					if all:
						if alpha > t1(beta,u):
							if beta > t1(alpha,u):
								eq_count_great_great+=1;
							elif beta < t1(alpha,u):
								eq_count_great_less+=1;
						elif alpha < t1(beta,u):
							if beta > t1(alpha,u):
								eq_count_less_great+=1;
							elif beta < t1(alpha,u):
								eq_count_less_less+=1;
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
look_for_points(10,all=True, count = True)



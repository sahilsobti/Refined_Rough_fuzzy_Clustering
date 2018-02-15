import numpy as np
import csv
import operator
import math
import copy
class cluster:
	w_low = 0.7
	w_up  = 0.3	
	def __init__(self):
		self.lower=[]
		self.upper=[]
		self.boundary=[]
		self.lower_extra=[]
		self.boundary_extra=[]
                self.sum_low_membership=0
                self.sum_up_membership=0
                self.upper_membership=[]
	def add_lower(self,val,row=None):
		self.lower.append(row)
		row =[i * val for i in row]
		self.lower_extra.append(row)
		self.sum_low_membership=self.sum_low_membership+val
	def add_boundary(self,val, row=None):
		self.boundary.append(row)
		self.upper_membership.append(val)
		row =[i * val for i in row]
		self.boundary_extra.append(row)
		self.sum_up_membership=self.sum_up_membership+val
	def show(self):
		print "lower bound"
		print len(self.lower)
		print "boundary bound "
		print len(self.boundary)
	def find_new_cluster(self):
 	   #	self.boundary = [row for row in self.upper if row not in self.lower]
		sum1 =  map(sum, zip(*self.lower_extra))
		term1=[]
		len1 = len(self.lower)
		len2 = len(self.boundary)
	#	print "length of lower",len1
	#	print "length of boundary",len2
		if len1 == 0:
		        print "some lower bound = 0"
		        kaka=raw_input()
		if len2 > 0:
			term2=[]
			sum2  =  map(sum, zip(*self.boundary_extra))
			term1 = calculation(cluster.w_low,self.sum_low_membership,sum1)
			term2 =  calculation(cluster.w_up,self.sum_up_membership,sum2)
		        term1=np.array(term1)
		        term2=np.array(term2)	
		        sum_total =  map(sum,zip(term1,term2))
			return sum_total	 
		else:
			new_w_low = 1
			term1 = calculation(new_w_low,self.sum_low_membership,sum1)	
			return term1 
	def delete(self):
		del self.lower[:]
		del self.upper[:]
		del self.boundary[:]
		del self.boundary_extra[:]
		del self.lower_extra[:]
		del self.upper_membership[:]
		self.sum_low_membership=0
		self.sum_up_membership=0
	def add_up_low(self,x=None):
		self.lower.append(x)
		self.upper.append(x)
	def calculate_S(self,D=None):
		len1=len(self.lower)
		len2=len(self.boundary)
		g=[]
		for l in self.lower:
			distances =(l - D)**2
			distances=distances.sum(axis=-1)
			g.append(distances)
		g=np.array(g)
		summ1=np.sum(g)
		if len1 > 0 and len2 > 0: 
			term1 = float(cluster.w_low*summ1)/float(len1)
			g1=[]
			for l in self.boundary:
				distances =(l - D)**2
			        for ab in self.upper_membership:
			                distances =[pop * ab for pop in distances]
				distances=np.array(distances)
				distances=distances.sum(axis=-1)
				g1.append(distances)
			g1=np.array(g1)
			summ2=np.sum(g1)
			term2 =float(cluster.w_up * summ2)/float(self.sum_up_membership)
			self.s=np.add(term1,term2)
		else:
			term1 = float(summ1)/float(len1)
			self.s=term1	
	def compare_lower(self, a=None):
	        a=np.array(a)
	        for row in self.lower:
	               row=np.array(row)
	               if (row == a).all():
	                        return 1
	        return 0
	def compare_boundary(self,a=None):
	        a=np.array(a)
	        for row in self.boundary:
	               row=np.array(row)
	               if (row == a).all():
	                        return 1
	        return 0                        	                				
def calculation(weight,leng1,summ = None):
	final_cal = []
	for val in summ:	
			final_cal.append((weight*val)/leng1)
        return final_cal
def checkforequal(a=None,b=None):
	a=np.array(a)
	b=np.array(b)
	if (a==b).all():
		return 1
	else:
		return 0
def change_precision(p,a=None):
	m=[]
	for row in a:
		y=[]
		for val in row:
			val=float(val)	
			val=round(val,p)
			y.append(val)
		m.append(y)
	return m
def distancee(A=None,B=None):
	distances =(A-B)**2
	distances=distances.sum(axis=-1)
	distances=np.sqrt(distances)
	return distances
def summ_cluster_data_distances(**dist):
        return sum(dist.values())
				
if __name__ =='__main__':
	threshold = 0.01
	count=1
	reader=np.array(list(csv.reader(open("sample.txt","r"),delimiter=',')))	
	X=copy.deepcopy(reader[:,:])
	X=np.array(X).astype('float')
	rows=len(X)
	cols=len(X[0])
	print rows
	print cols
	print "Enter the number of clusters you want"
        k = input()	
  	V=np.zeros((k,cols))
	V=np.array(X).astype('float')
	V=copy.deepcopy(X[:k,:])
	c=[]
        for i in xrange(0,k):
		c.append(cluster())
	first=10
	second=10+k
#	print len(X)
	for i in xrange(0,k):
	        new_x=copy.deepcopy(X[first:second,:])       
	        for x in new_x:
	                x=x.tolist()
	                c[i].add_lower(1,x)
	        first=second+1
	        second=second+k+1
	for i in xrange(0,k):
	        c[i].show()        
	#calculating the distance between the cluster centers and the data points
	dist={}
	U={}
	flag = 1
	while flag == 1:
		if count > 1:
			for xx in xrange(0,k):
				c[xx].delete()	
		print "count is" 
		print count 	
		for i in xrange(0,rows):
			dist.clear()   #you can use dist = {} also
			U.clear()
			deno=0
			for j in xrange(0,k):		
				distances =distancee(X[i,:],V[j,:])
				dist[j]=distances**2
		#	print dist
		#       sum_val=summ_cluster_data_distances(dist)
	#	        print "distances are",dist
		        mini_key=min(dist.iteritems(), key=operator.itemgetter(1))[0]
		        if dist[mini_key] == 0:
		                c[int(mini_key)].add_lower(1,X[i,:].tolist())
		        else:
		                for pp in xrange(0,k):
		                        for ij in xrange(0,k):
		                                deno = deno+((dist[pp]/dist[ij])**2)
		                        U[pp]=1/deno
		                        deno=0
			     #  print "U is",U
	                      # print "sum of U is ",sum(U.values())
	                   	#kka=raw_input()
			        first_max_key=max(U.iteritems(), key=operator.itemgetter(1))[0]
	   		        first_max_value=U[first_max_key]
			        del U[first_max_key]    	# can also use U.pop('key')
		                second_max_key=max(U.iteritems(), key=operator.itemgetter(1))[0]
        	                second_max_value=U[second_max_key]
 			        diff=(first_max_value-second_max_value)
	#		        print "first_max_value :",first_max_value
	#		        print "second_max_value :",second_max_value
			    #   print "diff",diff
			        if diff < threshold :
			                c[int(first_max_key)].add_boundary(first_max_value,X[i,:].tolist())
                		        c[int(second_max_key)].add_boundary(second_max_value,X[i,:].tolist())
	                        		
	                       	else:
				        c[int(first_max_key)].add_lower(1,X[i,:].tolist())

		V_new = []
		del V_new[:] 	#for future, delete all elements
        	for i2 in xrange(0,k):
			V_new.append(c[i2].find_new_cluster())
        	#checking cluster distance
        	V_new=np.array(V_new)
        	for i3 in xrange(0,k):
        	        for j in xrange(0,k):
        	                if i3 == j:
        	                        continue
     #   	                print "distance between %d cluster and %d cluster is" %(i3+1,j+1)
      #  	                print distancee(V_new[i3,:],V_new[j,:])
                               
        	V_new=V_new.tolist()
        	# end
        	V=V.tolist()
		V_new=change_precision(5,V_new)
		print "comparing clusters result"
		print checkforequal(V,V_new)
		if checkforequal(V,V_new):
			flag = 0
		else:
			flag = 1
		if flag == 1:
			V = copy.deepcopy(V_new)
		count=count+1
		V=np.array(V)
	
	print "final clusters are :"
	print V
	kak=raw_input()
	print "Final answer is \n"
		
	for i in xrange(0,k):
			print "The lower bound and upper bound of %s cluster is " %(i+1)
			c[i].show()
	
	#calculate DB index	
	for i in xrange(0,k):      
		c[i].calculate_S(V[i,:])
	p=[]
	total_sum=[]
	for i in xrange(0,k):
		del p[:]
		for j in xrange(0,k):
		        if j == i:
		                continue
			p.append(float(np.add(c[j].s,c[i].s))/float(distancee(V[j,:],V[i,:])))
		total_sum.append(max(p))
	total_sum=np.array(total_sum)
	DB=float(np.sum(total_sum))/float(k)
	print "DB index is" , DB
	#finish DB index
	total_sum=total_sum.tolist()
	del total_sum[:]
	#calculate D index
	S_list=[]
	for i in xrange(0,k):
	        S_list.append(float(c[i].s))
	max_s=float(max(S_list))        
	for i in xrange(0,k):
	        del p[:]
	        for j in xrange(0,k):
	                if j ==i:
	                        continue
	                p.append(float(distancee(V[j,:],V[i,:]))/max_s)
	        total_sum.append(min(p))
	D_index=min(total_sum)   
        print "DUNN or D index is ", D_index
        #making one absolute V_new matrix
        Vabs=copy.deepcopy(V)
        coll=len(V[j])
        for j in xrange(0,k):
                for tt in xrange(0,coll):
                        Vabs[j][tt]=int(math.ceil(V[j][tt]))
        print "final absolue clusters are :"
	print Vabs
        #making half of V_new matrix 
        Vhalf=copy.deepcopy(V)
        for j in xrange(0,k):
                for tt in xrange(0,coll):
                        Vhalf[j][tt]=Vhalf[j][tt]/2
        #making the image 
        image_matrix=[]
        for i in xrange(0,rows):
                flagg=0
                averag=[it*0 for it in xrange(0,coll)]
                for j in xrange(0,k):
                         if c[j].compare_lower(X[i,:]):
                                print "lower",j                
                                image_matrix.append(Vabs[j])
                         elif c[j].compare_boundary(X[i,:]):
                                print "boundary",j
                                averag = map(sum,zip(averag,Vhalf[j]))
                                flagg=flagg+1
                if flagg==2:
                        for i in xrange(0,coll):
                                averag[i]=int(math.ceil(averag[i]))          
                        image_matrix.append(averag) 
        print "rows is :",len(image_matrix)
        print "cols is :",len(image_matrix[0])                                                                    
        print image_matrix[0]
        kp=raw_input()
        image_matrix=change_precision(0,image_matrix)
        image_matrix=np.array(image_matrix).astype('int32')
        print "finally"
        print image_matrix[0]
        np.savetxt("foo.csv",image_matrix,delimiter=",")

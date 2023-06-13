#
hours<-seq(0,24,1)
demand<-c(0,2370,2252,1644,1740,2475,3644,5020,7053,6850,5877,5699,5960,5844,5946,6384,6302,7521,8426,9150,7330,5494,3669,3271,2556)
accumulate<-function{vector1,vector2}{
	n<-length(vector1)
	# fill vector 2 with zeros
	vector2<-rep(0,n)
	vector[1]<-vector1[1]+0.0
	for (i in 2:n) vector2[i]<-vector2[i-1]+vector1[i]
	return(vector2)}
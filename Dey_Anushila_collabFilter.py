import sys
from operator import itemgetter

"Opening input file"
file_name = sys.argv[1]
user = str(sys.argv[2])
nb = int(sys.argv[3])
k = int(sys.argv[4])
	
"Reading input file"
doc = open(file_name).read()
	
"Removing Newline Characters"
newfile=doc.splitlines()
	
"Removing tabs"
newlist=[]
for x in newfile:
	newlist.append(x.split('\t'))
newlist=sorted(newlist, key=itemgetter(1,2))

"Listing All Movies"
movielist=[]
for i in range(0, len(newlist)):
	if newlist[i][2] not in movielist:
		movielist.append(newlist[i][2])
movielist=sorted(movielist)

"Creating a Dictionary with movie as key and users who rated the corresponding movies as values"
movieuserdict={}

for m in movielist:
	for i in range(0,len(newlist)):
		if m==newlist[i][2]:
			if m not in movieuserdict:
				movieuserdict[m]=[]
			movieuserdict[m].append(newlist[i][0])

"Rating User Movie"
ratingsdic={}
for n in newlist:
	ratingsdic[n[0]+n[2]]=n[1]

"Calculating Weights of all movies with each other"
allweights={}
allweights2={}
numerator=0.0
den1=0.0
den2=0.0
ratingsi=0.0
ratingsj=0.0
avgratingsi=0.0
avgratingsj=0.0
coorate=[]
for m in movielist: # Movie1
	if m not in allweights: 
		allweights[m]=[]
	for m2 in movielist: #Movie2
		if m!=m2:
			coorate=list(set(movieuserdict[m]).intersection(set(movieuserdict[m2]))) #users who rated both Movie1 and Movie2
			for c in coorate:
				ratingsi+=float(ratingsdic[c+m])
				ratingsj+=float(ratingsdic[c+m2])
			if len(coorate)!=0:
				avgratingsi=ratingsi/len(coorate)
				avgratingsj=ratingsj/len(coorate)
			for u in movieuserdict[m]:
				if u in movieuserdict[m2]:
					numerator+=(float(ratingsdic[u+m])-(avgratingsi)) * (float(ratingsdic[u+m2])-(avgratingsj))
					den1+=(float(ratingsdic[u+m])-(avgratingsi)) **2
					den2+=(float(ratingsdic[u+m2])-(avgratingsj)) **2
			if (den1 ** 0.5) * (den2 ** 0.5)!=0:
				finalden=(den1 ** 0.5) * (den2 ** 0.5)
				total=numerator/finalden
				allweights[m].append([m2,total])
			elif (den1 ** 0.5) * (den2 ** 0.5)==0:
				allweights[m].append([m2,0.0])
			numerator=0.0
			den2=0.0
			den1=0.0
			ratingsi=0.0
			ratingsj=0.0

for key in allweights:
	allweights[key].sort(key=itemgetter(0))
	allweights[key].sort(key=itemgetter(1), reverse=True)

# for key,value in allweights.items():
# 	print(key)
# 	for x in allweights[key]:
# 		print(x)

"Finding rated and unrated movies for a given user"
unratedmovies=[]
ratedmovies=[]
for i in range(0, len(newlist)):
	if newlist[i][0]==user:
		ratedmovies.append(newlist[i][2])

unratedmovies=sorted(list(set(movielist)-set(ratedmovies)))

"Finding Similarity"
count=0
newnum=0.0
newden=0.0
similarity=[]
for u in unratedmovies:
	for key in allweights:
		if key == u:
			for i in range(0,len(allweights[key])):
				if count!=nb:
					if user+allweights[key][i][0] in ratingsdic:
						count+=1
						newnum+=float(ratingsdic[user+allweights[key][i][0]])*allweights[key][i][1]
						newden+=abs(allweights[key][i][1])
			count=0
			if newden!= 0:
				psim=round(float(newnum/newden),5)
			else:
				psim=0.0
			newnum=0.0
			newden=0.0
			similarity.append((u,psim))

similarity.sort(key=itemgetter(0))
similarity.sort(key=itemgetter(1), reverse=True)
	
for i in range(0,k):
	print(similarity[i][0],similarity[i][1])
"""
---------------------------------------------------------
This Script Calculates the Distance Matrix between
Features of a data set.

Inputs: Command line Inputs: data set file
        in csv format.

Output: A csv file listing distances. The o/p file is
        named "distanceMatrix_<inputfile>.csv"
        
---------------------------------------------------------

"""

from sys import argv
script, inputFile = argv

from pandas import read_csv,DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn import pipeline

print "\n\nPlease Enter the number of components desired for SVD.\n"

nComp = int(raw_input("nComponents = "))

train = read_csv(inputFile)

y = train.median_relevance.values
train = train.drop(['median_relevance', 'relevance_variance'], axis=1)

traindata = list(train.apply(lambda x:'%s %s %s' % (x['query'],x['product_title'], x['product_description']),axis=1))

# tfidf vectorizer

tfv = TfidfVectorizer(min_df=3,  max_features=None,strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1, 2), use_idf=1,smooth_idf=1,sublinear_tf=1,stop_words = 'english')

tfv.fit(traindata)
X =  tfv.transform(traindata)

#Initialize model Variables#

tSVD = TruncatedSVD(n_components=nComp)      # Initialize SVD
scl = StandardScaler()                     # Initialize the standard scaler 

model = pipeline.Pipeline([('tSVD',tSVD),('scl',scl)])

model.fit(X)

distMatrix = pairwise_distances(X.todense(),metric='minkowski')

distMatrix_csv = DataFrame(distMatrix)
outputFile = "distanceMatrix_"+inputFile 
distMatrix_csv.to_csv(outputFile,index=False)

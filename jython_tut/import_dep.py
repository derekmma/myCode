'''
A simple implementation of Sentiment Analysis using
Stanford CoreNLP (http://stanfordnlp.github.io/CoreNLP)
in Python using Jython (http://www.jython.org)
'''
import sys

# Add all the CoreNLP jars to the search path. I basically ran the 
#following command in the unzipped stanford core nlp directory:
# find -iname "*.jar" > dep

dep_file = open("dep")
jar_list = dep_file.read().splitlines()
for jar in jar_list: sys.path.append(jar)
dep_file.close()

# There could be a better way of adding the jars; adding to the 
# CLASSPATH environment variable could be one alternative.

# Import the Classes needed for Sentiment Analysis
from edu.stanford.nlp.ling import CoreAnnotations
from edu.stanford.nlp.neural.rnn import RNNCoreAnnotations
from edu.stanford.nlp.pipeline import Annotation
from edu.stanford.nlp.pipeline import StanfordCoreNLP
from edu.stanford.nlp.sentiment import SentimentCoreAnnotations

# Import the Properties class from java to set the Properties
# required to create the CoreNLP pipeline
from java.util import Properties
props = Properties()
props.setProperty('annotators','tokenize,ssplit,pos,parse,sentiment')
pipeline = StanfordCoreNLP(a)

# Obtain sentiment of argument string passed to Annotation. Please see 
# the Java tutorial file packaged with the source code and the links
# mentioned above for specifics and explanations.

annotation = Annotation('java is good, python is also good, but Jython is absolutely amazing.')

pipeline.annotate(annotation)
sentences = annotation.get(CoreAnnotations.SentencesAnnotation)
# ps if running interactively in a Jython Session,
# try type(sentences). ;)

for sentence in sentences:
    tree = sentence.get(SentimentCoreAnnotations.SentimentAnnotatedTree)
    score = RNNCoreAnnotations.getPredictedClass(tree)
    print '\nString being analysed = %s ' %sentence
    print 'Sentiment Score = %s' %score

# The algorithm for calculating the sentiment returns scores 
# as {0:'Very Negative' , 1: 'Negative' , 
#     2: 'Neutral', 3: 'Positive' , 4: 'Very Postive'}

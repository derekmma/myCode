from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from nltk.stem.porter import PorterStemmer

def StemmedCorpus(ip,index,columns):
    """
    Description: This function accepts an input Pandas data frame and performs data Stemming using the Porter Stemming Algorithm

    Inputs:
           ip      : A Pandas DataFrame. 
                     !! The data if taken from a csv file should be imported using the .fillna("") method!!
           index   : number of rows of the DataFrame 
           columns : List of the Column Labels of the input Dataframe
    
    Output:
           Returns a DataFrame of stemmed input data
           

    """
    stemmed_ip = DataFrame(index=index,columns=columns)
    stemmer = PorterStemmer()
    colCount=1
    temp = ""
    for j in columns:
        if (colCount == 1): temp = "q"
        if (colCount == 3): temp = "z"
        if (colCount == 3): temp = ""
        colCount+=1
        for i in index:
            s = (" ").join([temp + z for z in BeautifulSoup(ip[j][i]).get_text(" ").split(" ")])
            s = (" ").join([stemmer.stem(z) for z in s.split(" ")])
            s = re.sub("[^a-zA-Z0-9]"," ", s)
            stemmed_ip[j][i] = s
    return stemmed_ip


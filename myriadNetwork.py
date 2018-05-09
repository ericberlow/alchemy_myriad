# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os.path
import pandas as pd
import sys
sys.path.append("../Tag2Network/tag2network")  # add Tag2Network directory
from Network.BuildNetwork import buildTagNetwork


# define paths
datapath = "data"
resultspath = "results"
namebase="myriad"
inname = os.path.join(datapath, "myriad.csv")
outname = os.path.join(resultspath, namebase+"Network.xlsx")
nodesname = os.path.join(resultspath, namebase+"Nodes.csv")
edgesname = os.path.join(resultspath, namebase+"Edges.csv")


print("Reading and cleaning data")
df = pd.read_csv(inname)

renameDic = {
        'Position title': 'Position',
        'Which of the following best describes you?': 'Sector',
        'What are you hoping to get out of your Myriad experience? (Select top 4)': 'Conference Goals',
        'Which of the Myriad themes are you most interested in? (select 2)': 'Themes of Interest',
        'Which of the following topics are you most interested in? (Choose four)': 'Health',
        'Which of the following topics are you most interested in? (Choose four).1': 'City',
        'Which of the following topics are you most interested in? (Choose four).2': 'Money',
        'Which of the following topics are you most interested in? (Choose four).3': 'Work',
        'Which of the following topics are you most interested in? (Choose four).4': 'Culture',
        'Which of the following topics are you most interested in? (Choose four).5': 'Play',
        'Which of the following topics are you most interested in? (Choose four).6': 'Food'            
        }
df.rename(columns = renameDic, inplace=True)


df['Name'] = df['First name'] + " " + df['Last name']

tagCols = ['Health','City','Money','Work','Culture','Play','Food']

df['Tags'] = df[tagCols].apply(lambda x: '|'.join(x.dropna().values.tolist()), axis=1)
df['tagList'] = df['Tags'].str.split('|')  # convert tag string to list of tags for buildTatNetwork

# reorder and clean columns
keepCols = [ 'Name', 'Tags', 'Sector', 'Position', 
             'Company name', 'Conference Goals',
             'Themes of Interest',  'Bio', 'Email', 
             'LinkedIn', 'Twitter', 'Avatar', 
             'First name', 'Last name','tagList']               
df = df[keepCols]


print("Building affinity network and writing output files to %s"%resultspath)
# toFile writes Nodes and Edges csv files
# outname writes Nodes and Edges to sheets in one excel file
# idf is "inverse document frequency" - if True it downweights common tags
tagAttr = 'tagList'
dropCols = []
idf = False


buildTagNetwork(df, color_attr="Cluster", tagAttr=tagAttr, dropCols=dropCols, 
                outname=outname,idf=idf,
                nodesname=nodesname, edgesname=edgesname, 
                plotfile=None,
                toFile=True, doLayout=True, draw=False)


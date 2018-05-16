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
namebase="Myriad_15May_IDF_remNoTags_"
inname = os.path.join(datapath, "AppData_Tues 15May 940pm.csv")
outname = os.path.join(resultspath, namebase+"Network.xlsx")
nodesname = os.path.join(resultspath, namebase+"Nodes.csv")
edgesname = os.path.join(resultspath, namebase+"Edges.csv")
plotname = os.path.join(resultspath, namebase+"Plot.pdf")

print("Reading and cleaning data")
df = pd.read_csv(inname)

# rename tag questions 
renameDic = {
        'Position title': 'Position',
        'Which of the following best describes you?': 'Sector',
        'What are you hoping to get out of your Myriad experience? (Choose two)': 'Conference Goals',
        'Which of the Myriad themes are you most interested in? (Choose two)': 'Themes of Interest',
        'Which of the following topics are you most interested in? (Choose four)': 'Health',
        'Which of the following topics are you most interested in? (Choose four).1': 'City',
        'Which of the following topics are you most interested in? (Choose four).2': 'Money',
        'Which of the following topics are you most interested in? (Choose four).3': 'Work',
        'Which of the following topics are you most interested in? (Choose four).4': 'Culture',
        'Which of the following topics are you most interested in? (Choose two)': 'Play',
        'Which of the following topics are you most interested in? (Choose four).5': 'Food'            
        }
df.rename(columns = renameDic, inplace=True)

# concatenate tags from tag categories into one pipe-separated string of tags
tagCols = ['Health','City','Money','Work','Culture','Play','Food'] # list of tag categores
df['Tags'] = df[tagCols].apply(lambda x: '|'.join(x.dropna().values.tolist()), axis=1) # join into pipe-separated string
df['Tags'] = df['Tags'].apply(lambda x: x.replace('Automation / Artificial Intelligence', 'Automation')) # shorten tag label
df['Tags'] = df['Tags'].apply(lambda x: x if x != '' else "No Tags") # add 'no tags' for all cases where no replies
df['tagList'] = df['Tags'].str.split('|')  # convert tag string to list of tags for buildTatNetwork

# add new columns - number of tags, node label, twitter format
df['nTags'] = df['tagList'].apply(lambda x: len(x)) #count tags
df['Label'] = df['First name'] + " " + df['Last name']
df['Twitter'] = df['Twitter'].str.replace('https://twitter.com/', '') #remove url and keep username



# reorder and list columns to keep for final output
keepCols = [ 'Label', 'Tags', 'Sector', 'Position', 
             'Company name', 'Conference Goals',
             'Themes of Interest',  'Bio', 'Email', 
             'LinkedIn', 'Twitter', 'Avatar', 
             'First name', 'Last name','tagList', 'nTags','Health','City','Money','Work','Culture','Play','Food']               
df = df[keepCols]

# remove people with no tags
df = df[df['Tags'] != "No Tags"]
df.to_excel(resultspath+"test.xlsx")
print("Building affinity network and writing output files to %s"%resultspath)

# Build affinity network from tags - 
#This calles the Tag2Network function which requires a list of tags for each entity
# other parameters:
    # 'toFile' writes Nodes and Edges csv files named by 'nodesname' and 'edgesname'
    # 'outname' writes Nodes and Edges to sheets in one excel file
    # 'idf' is "inverse document frequency" - if True it downweights common tags
    # 'doLayout' runs t-SNE network layout 
    # 'plotfile' is the network viz output file as pdf if 'None' then no file created
    # 'draw' = True will draw the network viz plot in the console
    
tags = 'tagList'
dropCols = []
idf = True


buildTagNetwork(df, color_attr="Cluster", tagAttr=tags, dropCols=dropCols, 
                outname=outname,idf=idf,
                nodesname=None, edgesname=None, 
                plotfile=plotname,
                toFile=True, doLayout=True, draw=True)


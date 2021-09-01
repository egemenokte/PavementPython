# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 09:48:01 2020

@author: egeme
used to import xlsx into dict format
"""
import pandas as pd
import pickle
import os

def importxlsx(filepath) :
    ##If picklefilename is 0, it does not pickle
    print('Getting Files Ready') 
    excel_file_str = filepath #structure info
    # this will read the first sheet into df
    
    print('Reading Files. Please be patient') 
    xls = pd.ExcelFile(excel_file_str)

    
    # Get The names
    Names = xls.sheet_names
    # to read all sheets to a map so that it can be accessed later
    Data= {}
    print('Importing Data') 
    totallen=len(Names)
    c=0
    for sheet_name in Names: #for structure
        Data[sheet_name] = xls.parse(sheet_name)
        c=c+1
        print('Data Import ' ,str(round(c/totallen*100)),'%' )
        
    return Data

def importpickle(filepath) : #imports in picklefiles

    filename = '../PickleData/'+filepath
    infile = open(filename,'rb')
    Data = pickle.load(infile)
    infile.close()
        
    return Data

def importpicklepath(filepath) : #imports in picklefiles

    filename = filepath
    infile = open(filename,'rb')
    Data = pickle.load(infile)
    infile.close()
        
    return Data

def exportpickle(Data,filepath) : #imports in picklefiles

    filename = '../PickleData/'+filepath
    outfile = open(filename,'wb')
    pickle.dump(Data,outfile)
    outfile.close() 
    print('Data Exported') 
        
    return 

def runme(): #Main run file
    filename = 'Bucket_PredictEstar.xlsx'
    Data = importxlsx(filename,'EstarPredictor')
    
    filename = 'Problematic Sections for data.xlsx'
    Data = importxlsx(filename,'ProblematicSections')
    return Data

if __name__ == "__main__":
    Data = runme()

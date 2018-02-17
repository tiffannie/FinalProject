import os
import subprocess
import pandas as pd
import csv
import numpy as np
import math
'''
create data table with
rank year and pitches

iterate through pitch_files folder and parse through the file names.
'''

def getYear(song_name):
    tokens = song_name.split("_")
    print tokens[0]
    return tokens[0]

'''
parameter: string song name
parses name to get numerical ranking
returns ranking as int
'''
def getRank(song_name):
    parts_of_fileName = song_name.split("_")
    print int(parts_of_fileName[1])
    return int(parts_of_fileName[1])

'''
There are two choruses created in the chorus extraction. This tells which one it is, the first
or second.
'''
def getChorusNum(song_name):
    tokens = song_name.split("_")
    chorusNum = tokens[2].split(".")
    print chorusNum[0]
    return chorusNum[0]

'''
Parameters: text file name
returns an array with the pitches in each file (contents of txt file)
'''
def getPitchesList(path):
    pitch_file = open(path,'r')
    with pitch_file as f:
        pitches = f.readlines()
    #pitch file has two columns. time stamp and pitch. This returns only pitch.
    # you may also want to remove whitespace characters like `\n` at the end of each line
    pitches = [x.split(" ", 1)[1].strip() for x in pitches]
    return pitches

'''
parameters array of pitches (in str format)
returns tuple with the min pitch in the first index of array and max pitch as 2nd element
'''
def minMaxPitch(pitch_file):
    path = "/home/tiffannie/music-project/music-project/pitch_files/"
    path = os.path.join(str(path),str(pitch_file))
    pitches = getPitchesList(path)
    min_max = []
    for x in pitches:
        if x == "0.000000":
            #print (000000)
            pass
        else:
            min_max.append(float(x))
    return min(min_max), max(min_max)

'''
generates list of files with pitches
'''
def getPitchFileList():
    pitch_file_list = []
    #creates a safe file path. gets home/tiffannie/music-project/songFolders/2000
    songDir = ("/home/tiffannie/music-project/music-project/pitch_files/")
    #print "SONGDIR" + songDir
     #puts every file name in an array
    pitch_file_list = os.listdir(songDir)
    #sorting the songs in numerical order by rank. 100 is next to ten though
    pitch_file_list.sort()
    #print song_mp3_list
    return pitch_file_list

'''
generates list of files with features
'''
def getFeatureFileList():
    feature_file_list = []
    #creates a safe file path
    featureDir = ("/home/tiffannie/music-project/stFeatures/")
    #puts every file name in an array
    feature_file_list = os.listdir(featureDir)
    #sorting the feature files in numerical order by rank. 100 is next to ten though
    feature_file_list.sort()
    return feature_file_list

'''
Take in CSV, transform to dataframe and label the columns 1-34 for each of the features for easy
column extraction

it's adding about 10 more rows to the end of the csv file than what shows up in libre. do I care? .....
'''
def featureLabeledDF(funky_file):
    featureDir = os.path.join("/home/tiffannie/music-project/stFeatures/",funky_file)
    df = pd.read_csv(featureDir,sep = ',',names =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34'])
  
    return df

'''
Parameters: Dataframe with many rows.
Returns: average of the column in a single row as an array
current problem, it returns the values in scientific notation. must fix later on in the process
'''
def getAverageOfFeatures(file_name):
    big_DF = featureLabeledDF(file_name)
    col_names = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34']
    avg_vals = []
    for col in big_DF:
        big_DF[col] = big_DF[col].mean()
    avg_vals = np.append(avg_vals, big_DF.iloc[0])
    return avg_vals

'''
Formula from answer given by J. W. Perry at bottom of page on https://math.stackexchange.com/questions/930232/how-to-find-the-number-of-semitones-between-two-frequencies

Test this method with A4 (440.0) and D5 (587.33) https://pages.mtu.edu/~suits/notefreqs.html

Note: there, theoretically, are an infinite number of semitones between two frequencies

parameters: two floats. (min and max pitch)
returns: float representing the number of semitones between the min and max pitch
'''
def getTotalSemitones(minny, maxxy):
    #maxxy = float("{0:.3f}".format(maxxy))
    #minny = float("{0:.3f}".format(minny))
    logz = math.log((maxxy/minny), 2)
    n = 12 * logz   
    return float("{0:.3f}".format(n))


'''
Dataset must be created in two parts. Compile pitch section- created with Aubio python module. Then, compile feature section- created with pyAudioAnalysis python module.

Place both compilations into dataframes. Concatenate the two dataframes to have each song's info as well as the features extracted with pyAudioAnalysis.

Save to a pickle file for easy reading in for machine learning model building. (Not saving to csv, because when saved to a csv, the first 10 values/rows are omitted in the final CSV. Still not sure why)
'''


if __name__=="__main__":

    #get lists of files.
    pitchDir = ("/home/tiffannie/music-project/music-project/pitch_files/")
    featuresDir = ("/home/tiffannie/music-project/stFeatures/")
    pitch_file_list = getPitchFileList()
    feature_file_list = getFeatureFileList()


    #initialize dataframes 
    pitch_data = pd.DataFrame()
    feature_data = pd.DataFrame()

    #compile feature data. save to feature_data dataframe******************************************

    #loop through feature files
    for index in range(0, len(feature_file_list)):
        #get array of features for song
        list_of_features = getAverageOfFeatures(feature_file_list[index]) 
        #initialize temporary dataframe with labeled columns.
        df2 = pd.DataFrame(columns=[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34']])
        #make each array a row in the temp. dataframe
        df2.loc[0] = list_of_features
        #add the temp. dataframe as a row in the final feature_data dataframe.
        feature_data = feature_data.append(df2)

    print feature_data.head(5)

    #similar process for pitch files****************************************************************

    for song in range(0,len(pitch_file_list)):
        #pitch files will be used to label each row in master dataframe
        #pitch dataframe will have label of each song

        chorus_num = getChorusNum(pitch_file_list[song])
        year = getYear(pitch_file_list[song])
        rank = getRank(pitch_file_list[song])
        min_pitch = minMaxPitch(pitch_file_list[song])[0]
        max_pitch = minMaxPitch(pitch_file_list[song])[1]
        num_semitones = getTotalSemitones(min_pitch,max_pitch)
        #create and fill temporary dataframe.
        df = pd.DataFrame([[chorus_num, year, rank, min_pitch, max_pitch, num_semitones]],columns=['chorus_num','year','rank','min pitch','max pitch','semitones'])
        #print df.head(5)
        #add the temp. dataframe o the final pitch_data dataframe
        pitch_data = pitch_data.append(df)

    #do and print some checks to make sure everything lines up 
    #print len(pitch_data)
    #print pitch_data.head(2)
    #print feature_data.head(2)

    #COMBINE master feature and pitch dataframes ***************************************************
    massa = pd.concat([pitch_data, feature_data], axis = 1)
    print massa.tail(20)
    print massa.shape
    #massa.to_csv("masterPitchDataFrame.csv", sep=',',index = True) #missing 10 values

    #SAVE TO PICKLE FILE ***************************************************************************
    massa.to_pickle("masterPitchDataFrame.pkl")


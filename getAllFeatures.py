import os
import subprocess

'''
returns list of song names
'''
def getMP3List():
	song_mp3_list = []
	for i in range(2000, 2006):
		#songDir = os.path.join("home","tiffannie","music-project","songFolders", str(i))
		#creates a safe file path. gets home/tiffannie/music-project/songFolders/2000
		songDir = os.path.join(os.getcwd(), "music-project","songFolders", "chorus_mp3","failed",str(i))
		#puts every file name in an array
		song_mp3_list = os.listdir(songDir)
		#sorting the songs in numerical order by rank. 100 is next to ten though
		song_mp3_list.sort()
		#print song_mp3_list
		yield(song_mp3_list)


'''
parameters: song name as string and folder name as string
extracts features from each MP3 file using the pyAudioAnalysis module (featureExtractionFile function to be exact)

see https://github.com/tyiannak/pyAudioAnalysis/wiki/3.-Feature-Extraction for further reading
'''

def getFeatures(song_name, folder_name):
	feature_extraction_path = os.path.join(os.getcwd(), "audioAnalysis.py")
        #feature_extraction_path = ("/home/tiffannie/music-project/audioAnalysis.py")
	#print "PITCH EXTRACTION PATH" + pitch_extraction_path
	chorus_path = os.path.join(os.getcwd(), "music-project","songFolders","chorus_mp3","failed",str(folder_name),song_name)
	feature_output_file = os.path.join(os.getcwd(), "stFeatures",str(song_name))
	cmdLine = subprocess.Popen([feature_extraction_path, "featureExtractionFile", "-i", chorus_path, "-mw", "1.0", "-ms", "1.0", "-sw", "0.050", "-ss", "0.050", "-o", feature_output_file])
	cmdLine.communicate()
	#cmdLine.terminate()

if __name__=="__main__":
	#mp3List = getMP3List() this is a function
	i = 2000
	for song in getMP3List():
		for s in song:
			getFeatures(s,i)
		i += 1

		print("done")

import os
import subprocess

'''
returns list of mp3 files to loop through
'''

def getMP3List():
	song_mp3_list = []
	for i in range(2000, 2006):
		songDir = os.path.join("/home/tiffannie/music-project/songFolders/chorus_mp3/failed", str(i))
		#puts every file name in an array
		song_mp3_list = os.listdir(songDir)
		#sorting the songs in numerical order by rank. 100 is next to ten though
		song_mp3_list.sort()
		#print song_mp3_list
		yield(song_mp3_list)

'''
parameters: song name as string and folder name as string

call aubiopitch function on each song.

'''
def getPitch(song_name, folder_name):
	#print "PITCH EXTRACTION PATH" + pitch_extraction_path
	song_path = os.path.join("/home/tiffannie/music-project/songFolders/chorus_mp3/failed/",str(folder_name),str(song_name))
        #print "SONG PATH" + song_path
	
        #rename file
        pitchFile = song_name.replace(".mp3", ".txt")
	output_file_path = os.path.join("/home/tiffannie/music-project/music-project/pitch_files",pitchFile)
        #run AUBIOPITCH function from Aubio module on each song and save output to a file.
	with open(output_file_path, "w+") as OP:
		cmdLine = subprocess.Popen(["aubiopitch","-i",song_path], stdout = OP)
		cmdLine.communicate()
	#cmdLine.terminate()

if __name__=="__main__":
	#mp3List = getMP3List() this is a function
	i = 2000
	for song in getMP3List():
		for s in song:
		    	getPitch(s,i)
		i += 1
		print ("done")



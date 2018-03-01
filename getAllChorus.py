import os
import subprocess


'''
returns list of song names
'''
def getSongNames():
	song_name_list = []
	for i in range(2001, 2006):
		#creates a safe file path. gets home/tiffannie/music-project/songFolders/2000
		songDir = os.path.join(os.getcwd(), "music-project","songFolders",str(i))
		#puts every file name in an array
		song_name_list = os.listdir(songDir)
		#sorting the songs in numerical order by rank. 100 is next to ten though
		song_name_list.sort()
		yield(song_name_list)

'''
parameters: song name as string and folder name as string
extracts chorus from each MP3 file using the pyAudioAnalysis module (thumbnail function to be exact)

see https://pages.mtu.edu/~suits/notefreqs.html at the bottom of the page for further reading
'''

def getChorus(song_name, folder_name):
        print(" done")
	mp3_path = os.path.join(os.getcwd(), "audioAnalysis.py")
	song_path = os.path.join(os.getcwd(), "music-project", "songFolders",str(folder_name),song_name)
	cmdLine = subprocess.Popen([mp3_path, "thumbnail", "-i", song_path, "-s", "40", "-y", str(folder_name)])
	cmdLine.communicate()
	#cmdLine.terminate()
if __name__=="__main__":
	i = 2000
	for song in getSongNames():
		for s in song:
			getChorus(s,i)
		i += 1

		print(str(s) +" done")

from pygame import mixer
class MusicPlayer():
    def __init__(self):
        mixer.init()
        self.songs = ["No Song", "beta_club.mp3", "didnt_i.mp3", "my_vibe.mp3", "notion.mp3", "170.mp3"] # list of song paths
        self.names = ["No Song", "Beta Club", "Didn't I", "My Vibe", "Notion", "170"]   # song names
        self.bpms = [0, 107, 150, 94, 160, 170] # song bpm
        self.curSongIdx = 0 # start at first song
    
    def getBpm(self):   
        return self.bpms[self.curSongIdx]   # return cur song bpm

    def load(self, song):
        mixer.music.pause() # pause music if playing
        if song != "No Song": # if song selecter
            mixer.music.load("mp3/"+song) # load song and play
            mixer.music.play()
    
    def reload(self): # same as load but just reloads current song
        mixer.music.pause() 
        song = self.songs[self.curSongIdx]
        if song != "No Song":
            mixer.music.load("mp3/"+song)
            mixer.music.play()
    
    def pause(self): # pause song
        mixer.music.stop()
    
    def up(self): 
        self.curSongIdx += 1 # cycle to next song
        self.curSongIdx = int(self.curSongIdx % len(self.songs)) # modulus idx for wrap around
        self.load(self.songs[self.curSongIdx]) # load song
        return self.names[self.curSongIdx] # return song name

    def down(self):
        self.curSongIdx -= 1 # same as up but cycle to previous song
        self.curSongIdx = int(self.curSongIdx % len(self.songs))
        self.load(self.songs[self.curSongIdx])
        return self.names[self.curSongIdx]



        

        
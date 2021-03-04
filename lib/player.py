import xbmc


class Player(xbmc.Player):
    def __init__(self):
        self.playing = False
        self.last_file = None
        xbmc.Player.__init__(self)

    def setLastFile(self, file):
        self.last_file = file

    def getLastFile(self):
        return self.last_file

    def setPlaying(self, playing):
        self.playing = playing

    def isPlaying(self):
        return self.playing

    def onAVStarted(self):
        if self.isPlayingVideo():
            self.playing = True

    def onPlayBackStopped(self):
        self.playing = False
        self.last_file = None

    def onPlayBackEnded(self):
        self.playing = False
        self.last_file = None

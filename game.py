class Game:

    def __init__(self):
        self.name = ""
        self.peakPlayers = 0
        self.hoursPlayed = 0
        self.appUrl =''
        self.genres = []
        self.descriptionText = []
        self.price = 0
        self.clasification = ""

    def hoursPlayedPerPeakPlayer(self):
        return self.hoursPlayed/self.peakPlayers


    def to_dict(self):
        return {
            'name':self.name,
            'peakPlayers':self.peakPlayers,
            'hoursPlayed':self.hoursPlayed,
            'price':self.price,
            'genres':self.genres
        }
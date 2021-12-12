class ZCB:
    def __init__(self, game=None, data=None):
        if data is not None:
            self._initFromData(game, data)

    def _initFromData(self, game, data):
        self.data = data
        #print(data[:10])

    def save(self, game):
        return self.data
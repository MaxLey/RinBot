
class MessageHandler:

    bot = None

    def __init__(self):
        #TODO database integration of awaiting and symbol
        #TODO own user ID
        self.awaiting = {}
        self.ownID = ""

    def get_symbol(self):
        return self.symbol

    def sendMessage(self, channelID, message):
        #TODO actually send the message
        return

    def handleMessage(self, user, userID, channelID, message, evt):
        if userID is self.ownID:
            return
        if (userID, channelID) in self.awaiting.keys():
            self.awaiting[(userID, channelID)].continue_chain()


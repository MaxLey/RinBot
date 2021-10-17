class MessageChain:

    #TODO database integration

    def __init__(self, user, channel, message_handler):
        self.step = 0
        self.user = user
        self.channel = channel
        self.message_handler = message_handler

    def continue_chain(self, message):
        return
        # TODO make abstract





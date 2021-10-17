from MessageChain import MessageChain
from models.Character import Character


class CharCreateChain(MessageChain):

    def __init__(self, user, user_id, channel_id, message_handler):
        super().__init__(user, user_id, channel_id, message_handler)
        self.character = Character()

    def continue_chain(self, message):
        #TODO verify abort procedure works, add checks to proper values
        if message[0] is self.message_handler.get_symbol():
            reply = self.user + ", you're still creating a character! Please finish or type " + self.message_handler.get_symbol() + "abort to cancel the process."
            self.step -= 1
            return
        if self.step is 0:
            reply = "What is your character's name?"
        if self.step is 1:
            self.character.name = message
            reply = "How old is your character?"
        if self.step is 2:
            self.character.age = message
            reply = "How tall is your character?"
        if self.step is 3:
            self.character.height = message
            reply = "What gender is your character?"
        if self.step is 4:
            self.character.gender = message
            reply = "What pronouns does your character use? Please format your reply as \"She/Her\", \"They/Them\", etc."



        self.message_handler.message(self.channel_id, reply)
        self.step += 1



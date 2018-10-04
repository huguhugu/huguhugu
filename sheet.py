# sheet class

class Sheet:
    def __init__(self, bpm, notes):
        self.bpm = bpm
        self.notes = notes
    def __str__(self):
        ret_str = 'bpm : {}\n'.format(self.bpm)
        for note in self.notes:
            ret_str += '{}\n'.format(note)
        return ret_str
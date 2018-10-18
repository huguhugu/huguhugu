# sheet class

class Sheet:
    def __init__(self, bpm, lines):
        self.bpm = bpm
        self.lines = lines
    def __str__(self):
        ret_str = 'bpm : {}\n'.format(self.bpm)
        for i, line in enumerate(self.lines):
            ret_str += 'Line {} start\n'.format(i+1)
            for note in line:
                ret_str += '{}\n'.format(note)
            ret_str += 'Line {} end\n'.format(i+1)
        return ret_str
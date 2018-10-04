# sheet parser
# input : txt file

from parse import parse
from sheet import Sheet

class SheetParserError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Parser:
    def __init__(self, sheet_loc):
        self.sheet_loc = sheet_loc
        self.possible_beats = [1, 2, 4, 8, 16, 32, 64]
        self.possible_tones = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.merge = False

    # Check if tone 
    def tone_checker(self, tone, i):
        return tone

    # If beat is not allowed value, raise error.
    # Or, return ms.
    def beat_checker(self, beat, bpm, i):
        try:
            index = self.possible_beats.index(beat)
        except:
            raise SheetParserError('Line {}'.format(beat), 'Note beat can only be 1, 2, 4, ... , 64.')
        else:
            times = 2 ** (2 - index)
            print('times '+str(times))
        ms = 1000.0/self.freq * times
        print('ms ' + str(ms))
        print('rounded ms ' + str(int(round(ms))))
        return int(round(ms))
    
    def parse(self):
        
        # Read sheet file
        sheet = open(self.sheet_loc, 'r')
        notes = sheet.readlines()
        sheet.close()

        # Find notes between START and END
        try:
            start_index = notes.index('START\n')
        except:
            raise SheetParserError('No START token.','Sheet should be placed between START and END')
        else:
            notes = notes[start_index+1:]
        
        try:
            end_index = notes.index('END\n')
        except:
            raise SheetParserError('No END token.','Sheet should be placed between START and END')
        else:
            notes = notes[:end_index]

        # Check bpm
        bpm_parse = parse('bpm: {:d}', notes[0])
        if bpm_parse is None:
            raise SheetParserError('No bpm.', 'bpm should be specified after START. ex) bpm: 120')
        bpm = bpm_parse[0]
        if bpm > 180:
            raise SheetParserError('Too big bpm', 'bpm should be less or equal than 180.')
        if bpm < 40 :
            raise SheetParserError('Too small bpm', 'bpm should be greater or equal than 40')
        
        # Set freq
        self.freq = bpm/60.0

        # Convert notes
        converted_notes = []
        for i, note in enumerate(notes[1:]):
            # Parse note
            p = parse('({}, {:d})', note)
            if p is None:
                raise SheetParserError('Line {} : {}'.format(i, note), 'Note format error.')

            # tone, beat check
            tone, beat = p

            # If note need to be merged with previous note,
            if self.merge:
                tone = self.tone_checker(tone, i)
                prev_tone = converted_notes[-1][0]
                if tone != prev_tone:
                    raise SheetParserError('Line {} : {}'.format(i, note), 'Different tones can\'t be merged.')
                beat_ms = self.beat_checker(beat, bpm, i)
                prev_note = converted_notes[-1]
                converted_notes[-1] = (prev_note[0], prev_note[1] + beat_ms)
                self.merge = False

            # If note is 'rest' note,
            elif tone == 'rest':
                beat_ms = self.beat_checker(beat, bpm, i)
                converted_notes.append((tone, beat_ms))

            # If note is merge, set merge flag & continue
            elif tone == 'merge':
                self.merge = True
                continue

            # O.w.
            else:
                beat_ms = self.beat_checker(beat, bpm, i)
                tone = self.tone_checker(tone, i)
                converted_notes.append((tone, beat_ms))        
        
        # Return
        return Sheet(bpm, converted_notes)
        
        

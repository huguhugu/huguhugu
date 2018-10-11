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
        self.possible_tones = {
            'a': 'a',
            'as': 'as',
            'af': 'es',
            'b': 'b',
            'bs': 'c',  # octave increased.
            'bf': 'as',
            'c': 'c',
            'cs': 'cs',
            'cf': 'b',  # octave decreased.
            'd': 'd',
            'ds': 'ds',
            'df': 'cs',
            'e': 'e',
            'es': 'f',
            'ef': 'ds',
            'f': 'f',
            'fs': 'fs',
            'ff': 'e',
            'g': 'g',
            'gs': 'gs',
            'gf': 'fs'
        }
        self.min_octave = 1
        self.max_octave = 5
        self.merge = False

    # Check whether tone is valid, return procesed tone.
    # tone : c3, cf3, ... (string)
    # i : line number of sheet
    def tone_checker(self, tone, i):
        try:
            if len(tone) == 2:
                octave = int(tone[1])
                tone = tone[0]
                if tone == 'bs':
                    octave += 1
                elif tone == 'cf':
                    octave -= 1
                tone = self.possible_tones[tone]
            elif len(tone) == 3:
                octave = int(tone[2])
                tone = tone[0:2]
                if tone == 'bs':
                    octave += 1
                elif tone == 'cf':
                    octave -= 1
                tone = self.possible_tones[tone]
            else:
                raise SheetParserError(
                    'Line {} : {}'.format(i, tone), 'The tone is not valid.')
        except KeyError:
            raise SheetParserError('Line {} : {}'.format(
                i, tone), 'The tone is not valid.')
        if octave < self.min_octave or octave > self.max_octave:
            raise SheetParserError('Line {}'.format(
                i), 'The octave is not valid.')
        return tone + str(octave)

    # If beat is not allowed value, raise error.
    # Or, return millisecond.
    # beat : 1, 2, 4, ... (int)
    # bpm : bpm (int)
    def beat_checker(self, beat, bpm, i):
        try:
            index = self.possible_beats.index(beat)
        except:
            raise SheetParserError('Line {}'.format(
                i), 'Note beat can only be 1, 2, 4, ... , 64.')
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
            raise SheetParserError(
                'No START token.', 'Sheet should be placed between START and END')
        else:
            notes = notes[start_index+1:]

        try:
            end_index = notes.index('END\n')
        except:
            raise SheetParserError(
                'No END token.', 'Sheet should be placed between START and END')
        else:
            notes = notes[:end_index]

        # Check bpm
        bpm_parse = parse('bpm: {:d}', notes[0])
        if bpm_parse is None:
            raise SheetParserError(
                'No bpm.', 'bpm should be specified after START. ex) bpm: 120')
        bpm = bpm_parse[0]
        if bpm > 180:
            raise SheetParserError(
                'Too big bpm', 'bpm should be less or equal than 180.')
        if bpm < 40:
            raise SheetParserError(
                'Too small bpm', 'bpm should be greater or equal than 40')

        # Set freq
        self.freq = bpm/60.0

        # Convert notes
        converted_notes = []
        for i, note in enumerate(notes[1:]):
            # Parse note
            p = parse('({}, {:d})', note)
            if p is None:
                raise SheetParserError('Line {} : {}'.format(
                    i, note), 'Note format error.')

            # tone, beat check
            tone, beat = p

            # If note need to be merged with previous note,
            if self.merge:
                tone = self.tone_checker(tone, i)
                prev_tone = converted_notes[-1][0]
                if tone != prev_tone:
                    raise SheetParserError('Line {} : {}'.format(
                        i, note), 'Different tones can\'t be merged.')
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

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
        self.DEFAULT_VOLUME = 5
        

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
            elif len(tone) >= 4:
                return tone
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
            # print('times '+str(times))
        ms = 1000.0/self.freq * times
        # print('ms ' + str(ms))
        # print('rounded ms ' + str(int(round(ms))))
        return int(round(ms))

    # Parse each line
    # line : list of note
    # i : Number of LINE
    def parse_line(self, line, i, bpm):
        converted_notes = []
        merge = False
        current_bar_length = 0
        bar_start = False
        for i, note in enumerate(line):
            if note == 'BARSTART\n':
                current_bar_length = 0
                if bar_start:
                    raise SheetParserError('LINE {} : {}'.format(
                        i, note), 'Bar error.')
                bar_start = True
                continue
            if note == 'BAREND\n':
                if not bar_start:
                    raise SheetParserError('LINE {} : {}'.format(
                        i, note), 'Bar error.')
                bar_start = False
                left_length = self.length_of_bar - current_bar_length
                if left_length > 0:
                    converted_notes.append(('rest', left_length, 5))
                    continue
                elif left_length == 0:
                    continue
                else:
                    raise SheetParserError('LINE {} : {}'.format(
                        i, note), 'Bar length exceeds. {:d} < {:d}'.format(self.length_of_bar, current_bar_length))

            # Parse note
            p = parse('({}, {:d}, {:d})', note)
            if p is None:
                p = parse('({}, {:d})', note)
                if p is None:
                    raise SheetParserError('LINE {} : {}'.format(
                        i, note), 'Note format error.')
                else:
                    tone, beat = p
                    volume = self.DEFAULT_VOLUME
            else:
                tone, beat, volume = p

            # If note need to be merged with previous note,
            if merge:
                tone = self.tone_checker(tone, i)
                prev_tone = converted_notes[-1][0]
                if tone != prev_tone:
                    raise SheetParserError('LINE {} : {}'.format(
                        i, note), 'Different tones can\'t be merged.')
                beat_ms = self.beat_checker(beat, bpm, i)
                prev_note = converted_notes[-1]
                converted_notes[-1] = (prev_note[0], prev_note[1] + beat_ms, prev_note[2])
                merge = False
                current_bar_length += beat_ms

            # If note is 'rest' note,
            elif tone == 'rest':
                beat_ms = self.beat_checker(beat, bpm, i)
                converted_notes.append((tone, beat_ms, volume))
                current_bar_length += beat_ms

            # If note is merge, set merge flag & continue
            elif tone == 'MERGE':
                merge = True
                continue
            
            elif tone == 'ITER':
                notesnum, iternum = beat, volume
                iter_notes = converted_notes[-notesnum:]
                # Calculate iterlen
                iterlen = 0
                for note in iter_notes:
                    iterlen += note[1]
                for i in range(iternum-1):
                    iter_notes.extend(iter_notes[0:notesnum])
                converted_notes = converted_notes[:-notesnum] + iter_notes
                current_bar_length += iterlen * (iternum -1)

            # O.w.
            else:
                beat_ms = self.beat_checker(beat, bpm, i)
                tone = self.tone_checker(tone, i)
                converted_notes.append((tone, beat_ms, volume))
                current_bar_length += beat_ms

        return converted_notes

    def parse(self):

        # Read sheet file
        sheet = open(self.sheet_loc, 'r')
        read_lines = sheet.readlines()
        sheet.close()

        # Find sheet START and END
        try:
            start_index = read_lines.index('START\n')
        except:
            raise SheetParserError(
                'No START token.', 'Sheet should be placed between START and END')
        else:
            read_lines = read_lines[start_index+1:]

        try:
            end_index = read_lines.index('END\n')
        except:
            raise SheetParserError(
                'No END token.', 'Sheet should be placed between START and END')
        else:
            read_lines = read_lines[:end_index]
        
        # Check bpm
        bpm_parse = parse('bpm: {:d}', read_lines[0])
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

        # Check bar length
        bar_parse = parse('bar: {:d}/{:d}', read_lines[1])
        if bar_parse is None:
            raise SheetParserError(
                'No bar.', 'bar should be specified after bpm. ex) bar: 4/4')
        # Calculate bar length
        base_beat = bar_parse[1]
        num_of_beat = bar_parse[0]
        self.length_of_bar = self.beat_checker(base_beat, bpm, 0) * num_of_beat
        
        # Exclude bpm and bar
        read_lines = read_lines[2:]

        # Find lines START and END
        lines = [] # Found lines
        line = [] # List to store notes
        line_started = False
        for i, token in enumerate(read_lines):
            # If comment, pass
            if token.startswith('#'):
                continue
            if (not line_started) and (token == 'LINESTART\n'):
                line_started = True
                line = []
            elif line_started and token == 'LINEEND\n':
                if not len(line) > 0:
                    raise SheetParserError('Line {}'.format(i), 'Line should consist of at least one note.')
                else:
                    line_started = False
                    lines.append(line)
            elif token == 'BARSTART\n' or token == 'BAREND\n':
                line.append(token)
            else:
                p = parse('({}, {:d})', token)
                if p is None:
                    raise SheetParserError('Line {} : {}'.format(
                        i, token), 'Note format error.')
                line.append(token)
        if line_started:
            raise SheetParserError('Line error', 'Line not finished after LINESTART')
        if not len(lines) > 0:
            raise SheetParserError('Line error', 'At least one line should exist.')
        
        # Convert lines
        converted_lines = []
        for i, line in enumerate(lines):
            converted_lines.append(self.parse_line(line, i+1, bpm))

        # Return
        return Sheet(bpm, converted_lines)

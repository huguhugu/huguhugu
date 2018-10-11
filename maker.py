from moviepy.editor import concatenate_videoclips, VideoFileClip, ColorClip
from pydub import AudioSegment
from sheet import Sheet
import os

class MakerError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Maker(object):
    def __init__(self, sht, *args, **kwargs):
        self.sheet = sht
        self.result = ''

    def make(self):
        clips = []
        for note in self.sheet.notes:
            if note[0] == 'rest':
                blank = ColorClip((1920, 1080), (0, 0, 0), duration=note[1]/1000)
                clips.append(blank)
            for root, dir, files in os.walk('./note'):
                for file in files:
                    filename, ext = os.path.splitext(file)
                    if note[0] == filename:
                        clipped = self.clip('./note/'+file, note[1])
                        clips.append(clipped)
        result = concatenate_videoclips(clips)
        self.result = './result/'+'result.mp4'
        result.write_videofile(self.result)


    def clip(self, path, duration):
        if duration <= 0:
            print("Maker : Duration is shorter than 0")
            return

        sample_array = AudioSegment.from_file(path).get_array_of_samples()
        loudest_index = sample_array.index(max(sample_array))
        start_index = loudest_index
        end_index = len(sample_array)
        duration_index = int(duration*100)
        # Cut Duration
        if (end_index-loudest_index) < duration_index:
            print("Maker : Note is shorter than Duration")
        else:
            start_index = loudest_index - 10*100
            end_index = loudest_index + duration_index - 10*100

        output = VideoFileClip(path).subclip(start_index*0.00001, end_index*0.00001)
        return output

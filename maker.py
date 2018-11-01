from moviepy.editor import concatenate_videoclips, VideoFileClip, clips_array, ImageClip, ColorClip, AudioFileClip
from sheet import Sheet
import os
from moviepy.audio.fx.volumex import volumex

hard_sheet = [
  [('g3', 476),('e3', 476),('e3', 476),('rest', 476),('f3', 476),('d3', 476),('d3', 476),('rest', 476),('c3', 476),('d3', 476),('e3', 476),('f3', 476),('g3', 476),('g3', 476),('g3', 357),('rest', 476)],
  [('g3', 476),('e3', 476),('e3', 476),('rest', 476),('f3', 476),('d3', 476),('d3', 476),('rest', 476),('c3', 476),('d3', 476),('e3', 476),('f3', 476),('g3', 476),('g3', 476),('g3', 357),('rest', 476)],
]

class MakerError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Maker(object):
    def __init__(self, sht, name='result', *args, **kwargs):
        self.sheet = sht
        self.result = ''
        self.name = name

    def make(self):
        videos = []
        for notes in self.sheet.lines:
            clips = []
            for note in notes:
                if note[0] == 'rest':
                    #t = clips[-1].end
                    #img = ImageClip(clips[-1].get_frame(t), duration=note[1]/1000)
                    img = ColorClip((1920, 1080), (0, 0, 0), duration=note[1]/1000)
                    clips.append(img)
                for root, dir, files in os.walk('./note'):
                    for file in files:
                        filename, ext = os.path.splitext(file)
                        if note[0] == filename:
                            clipped = self.clip('./note/'+file, note[1], note[2])
                            clips.append(clipped)
            video = concatenate_videoclips(clips)
            videos.append([video])
        result = clips_array(videos)
        self.result = './result/'+this.name+'.mp4'
        result.write_videofile(self.result)


    def clip(self, path, duration, volume=5, rest=False):
        if duration <= 0:
            print("Maker : Duration is shorter than 0")
            print('Maker :'+path)
            print('Maker :'+duration)
            return

        sample_array = AudioFileClip(path).to_soundarray()
        sample_array = sample_array[:,0].tolist()
        loudest_index = sample_array.index(max(sample_array))
        start_index = loudest_index
        end_index = len(sample_array)
        duration_index = int(duration*44.1) # 44.1 per 1ms
        # Cut Duration
        if (end_index-loudest_index) < duration_index:
            print("Maker : Note is shorter than Duration")
            print('Maker :'+path)
            print('Maker :'+duration)
        else:
            start_index = loudest_index #- 10*100
            end_index = loudest_index + duration_index #- 10*100

        output = VideoFileClip(path).subclip(start_index/44100, end_index/44100)
        volume / 5 # 5 is default
        audio = output.audio
        audio = audio.fx(volumex, volume)
        output = output.set_audio(audio)
        return output

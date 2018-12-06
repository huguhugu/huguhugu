from moviepy.editor import concatenate_videoclips, VideoFileClip, clips_array, ImageClip, ColorClip, AudioFileClip, CompositeAudioClip
from sheet import Sheet
import os
from moviepy.audio.fx.volumex import volumex
import time

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
        self.loaded_videos = {} # key : notename
        self.clipped_videos = {} # key : (notename, duration, volume)
        self.magic = 2.0

    # video - VideoFileClip instance
    # duration - ms ex) 333ms
    # volume - int 1 to 10
    def clip(self, video, duration, volume=5, rest=False):
        duration_sec = duration/1000

        if duration <= 0:
            print("Maker : Duration is shorter than 0")
            print('Maker :'+path)
            print('Maker :'+duration)
            exit(1)

        if video.end < duration_sec:
            print("Video is shorter than video")
            print("Finename : "+video.filename)
            exit(1)

        # sample_array = AudioFileClip(path).to_soundarray()
        # sample_array = sample_array[:,0].tolist()
        # loudest_index = sample_array.index(max(sample_array))
        # start_index = loudest_index
        # end_index = len(sample_array)
        # duration_index = int(duration*44.1) # 44.1 per 1ms
        # # Cut Duration
        # if (end_index-loudest_index) < duration_index:
        #     print("Maker : Note is shorter than Duration")
        #     print('Maker :'+path)
        #     print('Maker :'+duration)
        # else:
        #     start_index = loudest_index #- 10*100
        #     end_index = loudest_index + duration_index #- 10*100
        # output = VideoFileClip(path).subclip(start_index/44100, end_index/44100)

        output = video.subclip(0, duration_sec)
        volume = volume / 5 # 5 is default
        audio = output.audio
        audio = audio.fx(volumex, volume)
        output = output.set_audio(audio)
        return output

    def load_video(self, path):
        start_time = time.time()
        result = VideoFileClip(path)
        end_time = time.time()
        print("Reading "+path+" took "+str(end_time-start_time)+" secs.")
        return result

    def get_video(self, note_name, duration, volume):
        # If video already clipped
        if (note_name, duration, volume) in self.clipped_videos:
            return self.clipped_videos[(note_name, duration, volume)]

        # If video not clipped, but already loaded
        if note_name in self.loaded_videos:
            target_video = self.loaded_videos[note_name]
            clipped_video = self.clip(target_video, duration, volume)
            self.clipped_videos[(note_name, duration, volume)] = clipped_video
            return self.clipped_videos[(note_name, duration, volume)]
        
        # Need to load video
        for root, dir, files in os.walk('./note'):
            for file in files:
                filename, ext = os.path.splitext(file)
                if note_name == filename:
                    # Save loaded video
                    self.loaded_videos[note_name] = self.load_video('./note/'+file)
                    self.clipped_videos[(note_name, duration, volume)] = self.clip(self.loaded_videos[note_name], duration, volume)
                    return self.clipped_videos[(note_name, duration, volume)]
        
        # If not returned, no target video exists.
        # Exit program
        print("NO VIDEO !!! : "+note_name)
        exit(1)

    def make(self):
        videos = []
        for notes in self.sheet.lines:
            clips = []
            for note in notes:
                if note[0] == 'rest':
                    img = ColorClip((720, 404), (0, 0, 0), duration=note[1]/1000)
                    clips.append(img)
                    continue
                target_video = self.get_video(note[0], note[1], note[2])
                clips.append(target_video)
            
            video = concatenate_videoclips(clips).margin(10)
            videos.append(video)
        num_of_lines = len(self.sheet.lines)
        if num_of_lines == 1:
            result = videos[0]
        elif num_of_lines == 2:
            result = clips_array([[videos[0]],
                             [videos[1]]])
        elif num_of_lines == 4:
            result = clips_array([[videos[0], videos[1]],
                             [videos[2], videos[3]]])
        else:
            print("Num of lines should be 1, 2, or 4")
            exit(1)

        self.result = './result/'+self.name+'.mp4'
        result.write_videofile(self.result)

        

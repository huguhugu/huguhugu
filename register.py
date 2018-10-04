from moviepy.editor import *
from pydub import AudioSegment
import os.path

class Register(object):

    def __init__(self, path=None, duration=0.5, *args, **kwargs):
        if os.path.isfile(path):
            print("Register : " + path + " is existed")
        else:
            print("Register : Wrong path")
        self.duration = duration
        self.path = path

    def set_duration(self, t):
        self.duration = t

    def set_path(self, path):
        if os.path.isfile(path):
            print("Register : " + path + " is existed")
        else:
            print("Register : Wrong path")
        self.path = path

    def clip(self):

        if self.duration <= 0:
            print("Register : Duration is shorter than 0")
            return

        sample_array = AudioSegment.from_file(self.path).get_array_of_samples()
        loudest_index = sample_array.index(max(sample_array))
        start_index = 0
        end_index = loudest_index
        duration_index = int(self.duration*50000)
        # Cut Duration
        if loudest_index < (duration_index):
            end_index = 2*loudest_index
        else:
            start_index = loudest_index - duration_index
            end_index = loudest_index + duration_index

        output = VideoFileClip(self.path).subclip(start_index*0.00001, end_index*0.00001)
        output.write_videofile("output.mp4")

c1 = VideoFileClip("out.mp4")
c2 = VideoFileClip("output.mp4")
c_l = [c2,c2,c2,c2,c1,c1,c2,c2,c2,c2,c1,c1,c2,c2,c2,c1,c1,c2,c2,c1,c1]
f = concatenate_videoclips(c_l)
f.write_videofile("test.mp4")

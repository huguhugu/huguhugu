from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
import os.path
import shutil

class Register(object):
    def __init__(self, path=None, note='c3', *args, **kwargs):
        self.note = note
        self.path = None
        self.register(path)

    def register(self, path):
        if os.path.isfile(path):
            print("Register : " + path + " is existed")
            _, ext = os.path.splitext(path)
            self.path = './note/'+self.note+'.mp4'
            sample = VideoFileClip(path)
            sample.resize((720, 480))

            volume = 0.5
            audio = AudioFileClip(path)
            audio_array = audio.to_soundarray()
            audio_array = audio_array[:, 0].tolist()
            max_sound = max(audio_array)
            loudest_index = audio_array.index(max_sound)
            scale = volume / max_sound
            audio = audio.fx(volumex, scale)

            sample = sample.set_audio(audio)
            sample = sample.subclip(loudest_index/44100, sample.end)
            sample.write_videofile(self.path)
        else:
            print("Register : Wrong path")

    def set_note(self, note):
        if self.path:
            _, ext = os.path.splitext(self.path)
            shutil.move(self.path, './note/'+note+ext)
            self.path = './note/'+note+ext
            self.note = note

    def set_path(self, path):
        if os.path.isfile(path):
            print("Register : " + path + " is existed")
            _, ext = os.path.splitext(path)
            self.path = './note/'+self.note+ext
            shutil.copyfile(path, self.path)
        else:
            print("Register : Wrong path")

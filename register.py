from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
import os.path
import shutil

class Register(object):
    def __init__(self, path=None, note='c3', *args, **kwargs):
        self.note = note
        self.path = None
        if os.path.isfile(path):
            print("Register : " + path + " is existed")
            _, ext = os.path.splitext(path)
            self.path = './note/'+note+'.mp4'
            sample = VideoFileClip(path)
            sample.resize((720,480))

            volume = 0.5
            audio = AudioFileClip(path)
            audio_array = audio.to_soundarray()
            scale = volume / max(audio_array[:, 0])
            audio = audio.fx(volumex, scale)
            sample = sample.set_audio(audio)
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

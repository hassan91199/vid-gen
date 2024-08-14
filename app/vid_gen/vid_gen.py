import os
import traceback

from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.config.languages import EDGE_TTS_VOICENAME_MAPPING
from shortGPT.engine.content_video_engine import ContentVideoEngine
from shortGPT.gpt import gpt_chat_video

class VidGen:
    def __init__(self):
        self.isVertical = True
        self.voice_module = EdgeTTSVoiceModule('en-AU-WilliamNeural')
        self.language = 'English'
        self.script = ""
        self.video_folder = None
        self.video_id = ""

    def generate_script(self, message):
        self.script = gpt_chat_video.generateScript(message, self.language)
        return self.script

    def correct_script(self, correction):
        self.script = gpt_chat_video.correctScript(self.script, correction)
        return self.script

    def make_video(self, progress=None):
        videoEngine = ContentVideoEngine(voiceModule=self.voice_module, script=self.script, isVerticalFormat=self.isVertical, id=self.video_id)
        num_steps = videoEngine.get_total_steps()
        progress_counter = 0

        def logger(prog_str):
            if progress:
                progress(progress_counter / num_steps, f"Creating video - {progress_counter} - {prog_str}")

        videoEngine.set_logger(logger)
        for step_num, step_info in videoEngine.makeContent():
            if progress:
                progress(progress_counter / num_steps, f"Creating video - {step_info}")
            progress_counter += 1

        video_path = videoEngine.get_video_output_path()
        return video_path

# Example usage:
# vid_gen = VidGen()
# vid_gen.generate_script("Your video description here")
# vid_gen.make_video()
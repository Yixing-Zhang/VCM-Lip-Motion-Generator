from queue import Queue
import threading
import time
import pyaudio
import numpy as np

from voca.utils.inference import inference_realtime


class LipMotionGenerator(object):
    """
    This class generates lip motion data.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    enabled = False
    motionQueue = None
    generateThread = None
    lock = None

    audioStream = None

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            self.motionQueue = Queue(10000)
            self.enabled = False
            self.generateThread = threading.Thread(target=self.GenerateLipMotion)
            self.lock = threading.Lock()
            self.ds_fname = "./voca/ds_graph/deepspeech-0.5.0-models/output_graph.tflite"
            self.tf_model_fname = "xxxx"

            self.__class__.__first_init = False

    def Enable(self):
        if self.audioStream is None:
            print("Audio Stream not set, cannot enable Lip Motion Generator.")
            return False
        else:
            self.enabled = True
            self.motionQueue.queue.clear()
            self.generateThread.start()
            print("Enabled Lip Motion Generator.")

            return True

    def Disable(self):
        self.enabled = False
        self.motionQueue.queue.clear()
        self.generateThread.join()
        print("Disabled Lip Motion Generator.")

    def SetAudioStream(self, audio):
        if not self.enabled:
            self.audioStream = audio
            print("Set Audio Stream.")
        else:
            print("Disable the generation first before changing audio stream.")

    def GetLipMotionData(self):
        if not self.motionQueue.empty():
            return self.motionQueue.get_nowait()
        else:
            return None

    def GenerateLipMotion(self):
        previous_state_c = np.zeros([1, 2048], dtype=np.float32)
        previous_state_h = np.zeros([1, 2048], dtype=np.float32)
        while self.enabled:
            # lipMotion is a Json to better contain just 52 blendshapes (or even better to be only blendshapes
            # related to lip motion), other data fields are useless

            # Audio Stream
            audio_data = self.audioStream.read(14700)
            decode_data = np.frombuffer(audio_data, 'int16')
            lipMotion, previous_state_c, previous_state_h = inference_realtime(self.tf_model_fname, self.ds_fname,
                                                                               decode_data, 44100, previous_state_c,
                                                                               previous_state_h)

            # 所有blendshapes记得乘100，rokoko里blendshapes的范围是0-100
            # print(lipMotion)

            # Logic for generating lip motion
            if not self.motionQueue.full():
                for i in range(lipMotion.shape[0]):
                    self.motionQueue.put_nowait(lipMotion[i])

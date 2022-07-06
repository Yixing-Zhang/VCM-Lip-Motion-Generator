import json
import threading

import NetworkManager
import LipMotionGenerator


class Replacer(object):
    """
    This class replace lip motion data with generated motion data.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    networkManager = None
    lipMotionGenerator = None

    frame_count = 0
    enabled = False
    terminated = False

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            self.networkManager = NetworkManager.NetworkManager()
            self.lipMotionGenerator = LipMotionGenerator.LipMotionGenerator()
            self.frame_count = 0
            self.enabled = False
            self.terminated = False
            self.__class__.__first_init = False

    def SetAudioStream(self, audio):
        self.lipMotionGenerator.SetAudioStream(audio)

    def Enable(self):
        self.enabled = True
        self.frame_count = 0
        result = self.lipMotionGenerator.Enable()
        if result:
            print("Enable Replacer.")
        else:
            print("Replacer Enabling Failed.")

    def Disable(self):
        self.enabled = False
        self.frame_count = 0
        self.lipMotionGenerator.Disable()
        print("Disable Replacer.")

    def start(self):
        t = threading.Thread(target=self.ReplaceAndForward)
        t.start()
        print("Start Replacer.")

    def Terminate(self):
        self.Disable()
        self.terminated = True
        print("Terminate Replacer.")

    def ReplaceAndForward(self):
        # 得想办法加入多线程操作，考虑写一个UI。在这个函数运行的同时能通过UI来Enable和Disable，开启和关闭替换原始数据
        generatedData = None
        while True:
            if self.terminated:
                break

            # Read live motion data from Rokoko
            data, addr = self.networkManager.Receive()
            data = json.loads(data)
            # print(data)

            # If to replace
            if self.enabled:
                # Read generated motion data
                if self.frame_count % 5 == 0:
                    generatedData = self.lipMotionGenerator.GetLipMotionData()

                # Replace live motion facial data with generated data
                data["scene"]["actors"][0]["face"] = generatedData["scene"]["actors"][0]["face"]
                # print(data)

            # Send final motion data
            data = json.dumps(data).encode()
            self.networkManager.Send(data)

        self.networkManager.Terminate()

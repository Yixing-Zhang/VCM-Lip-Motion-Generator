import json
import threading
import time

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
    UI = None

    forwardThread = None

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
            self.UI = None
            self.forwardThread = threading.Thread(target=self.ReplaceAndForward)
            self.frame_count = 0
            self.enabled = False
            self.terminated = False
            self.__class__.__first_init = False

    def SetAudioStream(self, audio):
        self.lipMotionGenerator.SetAudioStream(audio)

    def Enable(self):
        self.frame_count = 0
        result = self.lipMotionGenerator.Enable()
        if result:
            print("Enabled Replacer.")
        else:
            print("Replacer Enabling Failed.")
        self.enabled = result
        return result

    def Disable(self):
        self.frame_count = 0
        result = self.lipMotionGenerator.Disable()
        if result:
            print("Disabled Replacer.")
        else:
            print("Replacer Disabling Failed.")
        self.enabled = not result
        return result

    def Start(self):
        self.forwardThread.start()
        print("Started Replacer.")

    def Terminate(self):
        print("Terminating Replacer.")
        if self.enabled:
            self.Disable()
        self.terminated = True
        self.forwardThread.join()

    def ReplaceAndForward(self):
        # 得想办法加入多线程操作，考虑写一个UI。在这个函数运行的同时能通过UI来Enable和Disable，开启和关闭替换原始数据
        print("Started Forwarding.\n", end='')
        generatedData = None
        timeout = time.time() + 5

        while not self.terminated:
            # Read live motion data from Rokoko
            received = self.networkManager.Receive()
            if received is None:
                if time.time() > timeout:
                    print("No incoming motion data. Please check Rokoko Studio live streaming configuration.\n", end='')
                    timeout = time.time() + 5
                    if self.enabled:
                        print("Timeout after no receiving for 5 seconds. Disabling replacer.\n", end='')
                        if self.Disable():
                            self.UI.btn1.setText("Enable")
                            self.UI.btn1.setChecked(True)
                        else:
                            self.UI.btn1.setText("Disable")
                            self.UI.btn1.setChecked(False)
                continue

            timeout = time.time() + 5
            data = received[0]
            addr = received[1]
            data = json.loads(data)
            # print(data)

            # If to replace
            if self.enabled:
                # Read generated motion data
                if self.frame_count % 5 == 0:
                    generatedData = self.lipMotionGenerator.GetLipMotionData()
                    print("Generated Data: ", generatedData, "\n", end='')

                # Replace live motion facial data with generated data
                if generatedData is not None:
                    # print(data)
                    for key in generatedData:
                        data["scene"]["actors"][0]["face"][key] = generatedData[key]
                    # print(data)

            # Send final motion data
            # print(data)
            data = json.dumps(data).encode()
            self.networkManager.Send(data)
            self.frame_count += 1
            self.frame_count %= 5
        self.networkManager.Terminate()
        print("Terminated Replacer.\n", end='')

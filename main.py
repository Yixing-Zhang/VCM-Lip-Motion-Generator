import time

import Replacer

if __name__ == '__main__':
    print("Start")
    start_time = time.time()

    replacer = Replacer.Replacer()
    replacer.start()

    # 用UI控制Enable和disable替换功能，以及更改audio stream，和结束程序
    audio = 1
    replacer.SetAudioStream(audio)
    replacer.Enable()
    time.sleep(1)
    replacer.Disable()
    replacer.Terminate()

    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))

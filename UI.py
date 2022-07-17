import sys
from PyQt5.QtWidgets import *
import pyaudio
import Replacer


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        layout = QVBoxLayout()
        self.resize(500, 200)
        self.setWindowTitle("choose")

        self.Replacer = Replacer.Replacer()
        self.Replacer.start()

        self.btn1 = QPushButton("Enable")
        self.btn1.setCheckable(True)
        self.btn1.toggle()
        self.btn1.clicked.connect(self.btnstate)
        layout.addWidget(self.btn1)

        self.btn2 = QPushButton("Terminate")
        self.btn2.clicked.connect(lambda: self.whichbtn(self.btn2))
        layout.addWidget(self.btn2)

        self.lbl1 = QLabel("")
        self.lbl2 = QLabel("SetAudioStream:")
        self.cb = QComboBox()
        self.cb.addItem("--")
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            if p.get_device_info_by_index(i)['hostApi'] == 0 and p.get_device_info_by_index(i)['maxInputChannels'] > 0:
                self.cb.addItem(p.get_device_info_by_index(i)['name'])
        self.cb.currentIndexChanged.connect(self.selectionchange)
        layout.addWidget(self.lbl1)
        layout.addWidget(self.lbl2)
        layout.addWidget(self.cb)

        self.setLayout(layout)

    def btnstate(self):
        if self.btn1.isChecked():
            if self.Replacer.Disable():
                self.btn1.setText("Enable")
                self.btn1.setChecked(True)
            else:
                self.btn1.setText("Disable")
                self.btn1.setChecked(False)
        else:
            if self.Replacer.Enable():
                self.btn1.setText("Disable")
                self.btn1.setChecked(False)
            else:
                self.btn1.setText("Enable")
                self.btn1.setChecked(True)

    def whichbtn(self, btn):
        if btn.text() == 'Terminate':
            self.Replacer.Terminate()
            self.close()

    def selectionchange(self):
        if self.cb.currentText() != '--':
            p = pyaudio.PyAudio()
            for i in range(p.get_device_count()):
                if p.get_device_info_by_index(i)['name'] == self.cb.currentText():
                    break
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100,
                            frames_per_buffer=1024, input=True, input_device_index=i)
            self.Replacer.SetAudioStream(audio=stream)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    btnDemo = Form()
    btnDemo.show()
    sys.exit(app.exec_())

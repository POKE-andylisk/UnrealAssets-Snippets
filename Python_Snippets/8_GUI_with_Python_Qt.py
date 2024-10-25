# a simple prototype that uses the pyqt5 library to connect unreal with qt-based guit
# make sure the basic_ui.ui file is in the same directory as this script
#  
import unreal
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic

editor_level_lib = unreal.EditorLevelLibrary()

class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        ui_file = os.path.join(os.path.dirname(__file__),"basic_ui.ui")
        self.widget = uic.loadUi(ui_file, self)

        # set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())

        # find the interaction elements (XML structure)
        self.text_l = self.widget.findChild(QLineEdit, "textBox_L")
        self.text_r = self.widget.findChild(QLineEdit, "textBox_R")
        self.checkbox = self.widget.findChild(QCheckBox, "checkBox")

        # find and assign slider
        self.slider = self.widget.findChild(QSlider, "slider")
        self.slider.sliderMoved.connect(self.sliderMoved)

        # find buttons and set up handlers
        self.btn_ok = self.widget.findChild(QPushButton, "okButton")
        self.btn_ok.clicked.connect(self.ok_clicked)
        self.btn_cancel = self.widget.findChild(QPushButton, "cancelButton")
        self.btn_cancel.clicked.connect(self.cancel_clicked)

    def sliderMoved(self):
        slider_value = self.slider.value()

        # move the selected actor according to the slider value
        selected_actors = editor_level_lib.get_selected_level_actors()

        if len(selected_actors) > 0:
            actor = selected_actors[0]

            # get old transform, change y axis avlue and write back
            new_transform = actor.get_actor_transform()
            new_transform.translation.y = slider_value

            actor.set_actor_transform(new_transform,True,True)

        unreal.log(slider_value)

    # triggered on click of okButton
    def ok_clicked(self):
        text_l = self.text_l.text()
        text_r = self.text_r.text()
        is_checked = self.checkbox.isChecked()

        unreal.log("Text left value: {}".format(text_l))
        unreal.log("Text right value: {}".format(text_r))
        unreal.log("Checkbox value: {}".format(is_checked))
    
    # triggered on click of cancelButton
    def cancel_clicked(self):
        unreal.log("cancel clicked")
        self.close()

    

app = None
if not QApplication.instance():
    app = QApplication(sys.argv)
UIWindow = window()
UIWindow.show()
# sys.exit(app.exec_())


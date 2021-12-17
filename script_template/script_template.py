'''
Script Name: Script Template
Script Version: 1.0
Flame Version: 2020
Written by: Michael Vaglienty
Creation Date: MM.DD.YY
Update Date: MM.DD.YY

Custom Action Type: Batch

Description:

    Template for flame python script with QT window

    Config sections can be deleted if config file not needed

To install:

    Copy script into /opt/Autodesk/shared/python/script_template
'''

from __future__ import print_function
from PySide2 import QtWidgets, QtCore
import xml.etree.ElementTree as ET
import os

VERSION = 'v1.0'

SCRIPT_PATH = '/opt/Autodesk/shared/python/script_template'

#-------------------------------------#
# QT UI Classes

class FlameLabel(QtWidgets.QLabel):
    """
    Custom Qt Flame Label Widget

    For different label looks set label_type as: 'normal', 'background', or 'outline'

    To use:

    label = FlameLabel('Label Name', 'normal', window)
    """

    def __init__(self, label_name, label_type, parent_window, *args, **kwargs):
        super(FlameLabel, self).__init__(*args, **kwargs)

        self.setText(label_name)
        self.setParent(parent_window)
        self.setMinimumSize(150, 28)
        self.setMaximumHeight(28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on label_type

        if label_type == 'normal':
            self.setStyleSheet('QLabel {color: #9a9a9a; border-bottom: 1px inset #282828; font: 14px "Discreet"}'
                               'QLabel:disabled {color: #6a6a6a}')
        elif label_type == 'background':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet('QLabel {color: #9a9a9a; background-color: #393939; font: 14px "Discreet"}'
                               'QLabel:disabled {color: #6a6a6a}')
        elif label_type == 'outline':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet('QLabel {color: #9a9a9a; background-color: #212121; border: 1px solid #404040; font: 14px "Discreet"}'
                               'QLabel:disabled {color: #6a6a6a}')

class FlameButton(QtWidgets.QPushButton):
    """
    Custom Qt Flame Button Widget

    To use:

    button = FlameButton('Button Name', do_when_pressed, window)
    """

    def __init__(self, button_name, do_when_pressed, parent_window, *args, **kwargs):
        super(FlameButton, self).__init__(*args, **kwargs)

        self.setText(button_name)
        self.setParent(parent_window)
        self.setMinimumSize(QtCore.QSize(110, 28))
        self.setMaximumSize(QtCore.QSize(150, 28))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(do_when_pressed)
        self.setStyleSheet('QPushButton {color: #9a9a9a; background-color: #424142; border-top: 1px inset #555555; border-bottom: 1px inset black; font: 14px "Discreet"}'
                           'QPushButton:pressed {color: #d9d9d9; background-color: #4f4f4f; border-top: 1px inset #666666; font: italic}'
                           'QPushButton:disabled {color: #747474; background-color: #353535; border-top: 1px solid #444444; border-bottom: 1px solid #242424}'
                           'QToolTip {color: black; background-color: #ffffde; border: black solid 1px}')

class FlameLineEdit(QtWidgets.QLineEdit):
    """
    Custom Qt Flame Line Edit Widget

    Main window should include this: window.setFocusPolicy(QtCore.Qt.StrongFocus)

    To use:

    line_edit = FlameLineEdit('Some text here', window)
    """

    def __init__(self, text, parent_window, *args, **kwargs):
        super(FlameLineEdit, self).__init__(*args, **kwargs)

        self.setText(text)
        self.setParent(parent_window)
        self.setMinimumHeight(28)
        self.setMinimumWidth(110)
        # self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet('QLineEdit {color: #9a9a9a; background-color: #373e47; selection-color: #262626; selection-background-color: #b8b1a7; font: 14px "Discreet"}'
                           'QLineEdit:focus {background-color: #474e58}'
                           'QLineEdit:disabled {color: #6a6a6a; background-color: #373737}'
                           'QToolTip {color: black; background-color: #ffffde; border: black solid 1px}')

#-------------------------------------#
# Main Script

class ScriptTemplate(object):

    def __init__(self, selection):
        import flame

        print ('>' * 20, 'script template %s' % VERSION, '<' * 20, '\n')

        # Paths

        self.config_path = os.path.join(SCRIPT_PATH, 'config')
        self.config_xml = os.path.join(self.config_path, 'config.xml')

        # Load config file

        self.config()

        # Open main window

        self.main_window()

    def config(self):

        def get_config_values():

            # Get settings from saved config.xml file

            xml_tree = ET.parse(self.config_xml)
            root = xml_tree.getroot()

            # Get Settings from config XML

            for setting in root.iter('script_template_settings'):
                self.setting_01 = setting.find('setting_01').text
                self.setting_02 = setting.find('setting_02').text

            print ('>>> config loaded <<<\n')

        def create_config_file():

            # Create config.xml file with default settings

            if not os.path.isdir(self.config_path):
                try:
                    os.makedirs(self.config_path)
                except:
                    message_box('Unable to create folder:<br>%s<br>Check folder permissions' % self.config_path)

            if not os.path.isfile(self.config_xml):
                print ('>>> config file does not exist, creating new config file <<<')

                config = """
<settings>
    <script_template_settings>
        <setting_01>Some Value Here</setting_01>
        <setting_02>Some Value Here</setting_02>
    </script_template_settings>
</settings>"""

                with open(self.config_xml, 'a') as config_file:
                    config_file.write(config)
                    config_file.close()

        if os.path.isfile(self.config_xml):
            get_config_values()
        else:
            create_config_file()
            if os.path.isfile(self.config_xml):
                get_config_values()

    def main_window(self):

        def save_config():

            # Save settings to config file

            xml_tree = ET.parse(self.config_xml)
            root = xml_tree.getroot()

            setting_01 = root.find('.//setting_01')
            setting_01.text = self.line_edit.text()

            xml_tree.write(self.config_xml)

            print ('>>> config saved <<<\n')

            self.window.close()

            message_box('Config Saved')

        self.window = QtWidgets.QWidget()
        self.window.setMinimumSize(QtCore.QSize(400, 150))
        self.window.setMaximumSize(QtCore.QSize(400, 150))
        self.window.setWindowTitle('Script Template %s' % VERSION)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.setStyleSheet('background-color: #313131')

        # Center window in linux

        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.window.move((resolution.width() / 2) - (self.window.frameSize().width() / 2),
                         (resolution.height() / 2) - (self.window.frameSize().height() / 2))

        # Labels

        self.label = FlameLabel('This is a label', 'normal', self.window)

        self.line_edit = FlameLineEdit(self.setting_01, self.window)

        # Buttons

        self.save_btn = FlameButton('Save', save_config, self.window)
        self.cancel_btn = FlameButton('Cancel', self.window.close, self.window)

        #------------------------------------#

        # Window Layout

        self.grid = QtWidgets.QGridLayout()
        self.grid.setVerticalSpacing(5)
        self.grid.setHorizontalSpacing(5)
        self.grid.setMargin(20)

        self.grid.addWidget(self.label, 1, 0)
        self.grid.addWidget(self.line_edit, 1, 1)

        self.grid.addWidget(self.cancel_btn, 6, 0)
        self.grid.addWidget(self.save_btn, 6, 1)

        self.window.setLayout(self.grid)

        # ----------------------------------------------

        self.window.show()

        return self.window

def message_box(message):

    msg_box = QtWidgets.QMessageBox()
    msg_box.setMinimumSize(400, 100)
    msg_box.setText(message)
    msg_box_button = msg_box.addButton(QtWidgets.QMessageBox.Ok)
    msg_box_button.setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box_button.setMinimumSize(QtCore.QSize(80, 28))
    msg_box.setStyleSheet('QMessageBox {background-color: #313131; font: 14pt "Discreet"}'
                          'QLabel {color: #9a9a9a; font: 14pt "Discreet"}'
                          'QPushButton {color: #9a9a9a; background-color: #424142; border-top: 1px inset #555555; border-bottom: 1px inset black; font: 14pt "Discreet"}'
                          'QPushButton:pressed {color: #d9d9d9; background-color: #4f4f4f; border-top: 1px inset #666666; font: italic}')
    msg_box.exec_()

    print ('>>> %s <<<\n' % message)

def get_main_menu_custom_ui_actions():

    return [
        {
            'name': 'pyFlame',
            'actions': [
                {
                    'name': 'Script Template',
                    'execute': ScriptTemplate,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]

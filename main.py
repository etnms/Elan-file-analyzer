from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QWidget, QCheckBox, QScrollArea, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from write_stats import WriteStats

'''
UI class for the app.
'''

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.foldername = None
        
        layout = QVBoxLayout()

        layout_folder_selection = QVBoxLayout()
        layout_folder_selection.setContentsMargins(0, 0, 0, 20)
        layout_tier = QVBoxLayout()
        layout_tier.setContentsMargins(0, 0, 0, 20)
        layout_output = QVBoxLayout()
        layout_output.setContentsMargins(0, 0, 0, 20)
        layout_checkboxes = QVBoxLayout()
        layout_checkboxes.setContentsMargins(0, 0, 0, 20)
        layout_specific_value = QVBoxLayout()
        layout_specific_value.setContentsMargins(0, 0, 0, 20)

        # Window style
        self.setWindowTitle('Elan file reader')
        self.setStyleSheet('background-color: #323232')
        self.setMinimumSize(QSize(1000, 600))

        # Browsing button
        button_browse = QPushButton('Browse files')
        button_browse.setMinimumHeight(40)
        button_browse.setFixedWidth(200)
        button_browse.clicked.connect(self.open_file_dialog)
        button_browse.setStyleSheet('QPushButton { font-size: 20px; background-color: #A6A6A6;' 
        'border-style: 2px solid #323232; border-radius: 10px} QPushButton:hover {font-size: 20px; background-color: #8A8A8A}')    

        # Selecting the folder UI
        self.selected_folder_label = QLabel('Selected folder: ')
        self.selected_folder_label.setStyleSheet('color: white; text-align: center; font-size: 20px')
        self.selected_folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Checkbox for subfolders
        self.subfolders = QCheckBox("Search in subfolders")
        self.subfolders.setStyleSheet('QCheckBox {font-size: 20px; color: white} QCheckBox::indicator { width: 1.5em; height: 1.5em;}')

        # First elements in the layout
        layout_folder_selection.addWidget(button_browse, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_folder_selection.addWidget(self.selected_folder_label)
        layout_folder_selection.addWidget(self.subfolders)
        layout_folder_selection.setSpacing(20)
       
        # Tier to search UI
        label_tier = QLabel('Tier to search')
        label_tier.setStyleSheet('color: white; font-size: 20px')
        self.search_value = QLineEdit()
        self.search_value.setStyleSheet('color: white; font-size: 20px; padding: 4px; border: 2px solid white; border-radius: 10px;')

        layout_tier.addWidget(label_tier)
        layout_tier.addWidget(self.search_value)

        # Output UI
        filename_label = QLabel('Output file name')
        filename_label.setStyleSheet('color: white; font-size: 20px')
        self.filename = QLineEdit()
        # Check for change in filename in case of an error to hide the error label
        self.filename.textChanged.connect(self.hide_filename_error)
        self.filename.setStyleSheet('color: white; font-size: 20px; padding: 4px; border: 2px solid white; border-radius: 10px;')

        layout_output.addWidget(filename_label)
        layout_output.addWidget(self.filename)

        # Checkboxes for optional parameters 
        self.time_info_checkbox = QCheckBox('Time information')
        self.time_info_checkbox.toggled.connect(lambda checked: checked and self.all_words_checkbox.setChecked(False))
        self.time_info_checkbox.setStyleSheet('QCheckBox {font-size: 20px; color: white} QCheckBox::indicator { width: 1.5em; height: 1.5em;}')

        self.specific_string_checkbox = QCheckBox('Looking for specific value inside a tier')
        self.specific_string_checkbox.toggled.connect(self.show_selected_input)
        self.specific_string_checkbox.toggled.connect(lambda checked : checked and self.all_words_checkbox.setChecked(False))
        self.specific_string_checkbox.setStyleSheet('QCheckBox {font-size: 20px; color: white} QCheckBox::indicator { width: 1.5em; height: 1.5em;}')

        self.all_words_checkbox = QCheckBox("Get values for all words in files")
        self.all_words_checkbox.toggled.connect(lambda checked: checked and self.specific_string_checkbox.setChecked(False))
        # Uncheck all time information since it won't work
        self.all_words_checkbox.toggled.connect(lambda checked: checked and  self.time_info_checkbox.setChecked(False))
        self.all_words_checkbox.setStyleSheet('QCheckBox {font-size: 20px; color: white} QCheckBox::indicator { width: 1.5em; height: 1.5em;}')
     
        layout_checkboxes.addWidget(self.time_info_checkbox)
        layout_checkboxes.addWidget(self.specific_string_checkbox)
        layout_checkboxes.addWidget(self.all_words_checkbox)

        # UI to look for a specific string in a tier
        self.specific_value_label = QLabel('Specific value to search:')
        self.specific_value_label.setStyleSheet('color: white; font-size: 20px')
        self.specific_value_input = QLineEdit()
        self.specific_value_input.setStyleSheet('color: white; font-size: 20px; padding: 4px; border: 2px solid white; border-radius: 10px;')

        # Hide specific value items as they are optional, checkbox to show them
        self.specific_value_label.hide()
        self.specific_value_input.hide()

        layout_specific_value.addWidget(self.specific_value_label)
        layout_specific_value.addWidget(self.specific_value_input)

        # Generate CSV button
        generate_csv_btn = QPushButton('Generate CSV')
        generate_csv_btn.setMinimumHeight(40)
        generate_csv_btn.setFixedWidth(200)
        generate_csv_btn.setStyleSheet('QPushButton { font-size: 20px; background-color: #78A1C4;' 
        'border-style: 2px solid #323232; border-radius: 10px;} QPushButton:hover {font-size: 20px; background-color: #678AA8}')    
        generate_csv_btn.setContentsMargins(0,0,0,0)
        generate_csv_btn.clicked.connect(self.create_csv_file)

        # Error text if conditions to create files are not meant
        self.error_label = QLabel('Error')
        self.error_label.setStyleSheet('color: #FF6C64; font-size: 18px')
        self.error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Hide the label by default, only show if there's an error
        self.error_label.hide()

        # Validation label if file was created successfully
        self.success_label = QLabel('File successfully created')
        self.success_label.setStyleSheet('color: #48C708; font-size: 18px')
        self.success_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Hide the label by default, only show when file is created
        self.success_label.hide()

        # Display layout
        layout.addLayout(layout_folder_selection)
        layout.addLayout(layout_tier)
        layout.addLayout(layout_output)
        layout.addLayout(layout_checkboxes)
        layout.addLayout(layout_specific_value)

        layout.addWidget(generate_csv_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        layout.addWidget(self.success_label)
        
        layout.setContentsMargins(60, 20, 60, 20)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)


    def open_file_dialog(self):
        self.foldername = str(QFileDialog.getExistingDirectory(self, 'Choose a folder'))
        self.selected_folder_label.setText(f'Selected folder: {self.foldername}')

        # If previous error then hide text
        if (self.error_label.text() == 'Error: no folder has been selected' and self.foldername != '' and self.foldername != None):
            self.error_label.hide()


    def create_csv_file(self):
        if self.look_for_errors() == True:
            return
        if WriteStats.write_stats(
            self.search_value.text(), 
            self.time_info_checkbox.isChecked(), 
            self.filename.text(), 
            self.foldername, 
            self.specific_string_checkbox.isChecked(), 
            self.specific_value_input.text(),
            self.all_words_checkbox.isChecked(),
            self.subfolders.isChecked()) == False: # If file is already opened
                self.error_label.setText('Error: a file with the same name is already opened')
                self.error_label.show()
                return
        
        self.error_label.hide()
        
        # Update success label text with name of the file
        self.success_label.setText(f'File "{self.filename.text()}.csv" successfully created')
        self.success_label.show()


    def show_selected_input(self, state):
        if (state):
            self.specific_value_label.show()
            self.specific_value_input.show()
        else:
            self.specific_value_label.hide()
            self.specific_value_input.hide()


    def look_for_errors(self):
        if (self.foldername == None or self.foldername == ''):
            self.error_label.show()
            self.error_label.setText('Error: no folder has been selected')
            return True
        elif (self.filename.text() == ''):
            self.error_label.show()
            self.error_label.setText('Error: the file needs a valid name')
            return True


    def hide_filename_error(self):
        if (self.filename != '' and self.foldername != None and self.foldername != ''):
            self.error_label.hide()


# Define font for the app
custom_font = QFont('Verdana')
QApplication.setFont(custom_font)

app = QApplication([])

if __name__ == '__main__':
    window = MainWindow()
    window.show()

    app.exec()
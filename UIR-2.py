import os

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox

def check(line): #Adding to special symbols '\'
    to_replace = ["#", "~", "=", "{", "}"]
    
    for char in to_replace:
        line = line.replace(char, "\\" + char)

    return line

def convert_to_gift(file_path):
    # Open the input file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Create an empty list to store the converted lines
    converted_lines = []

    # Initialize a counter to keep track of the current question number
    question_number = 0
    question_text = []
    
    # Loop through each line in the input file
    for i, line in enumerate(lines):
        line = line.strip()
        
        if len(line) == 0:
            i += 1
        
        # Check if the line starts with a number followed by a dot
        elif line[0].isdigit() and line[1] == '.':
            
                # Get the question text
                question_text = line[3:]
                # Increment the question number counter
                question_number += 1
                num = plus = 0
                
                # Initialize a list to store the answers
                answers = []
                
                for ans in lines[i+1:]:
                    ans = ans.strip()
                    if ans.startswith('+'):
                        plus += 1
                    elif len(ans) == 0:
                        break
                    num += 1

                if plus == 1:
                   
                    # Single-choice question
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        if ans.startswith('+'):
                            answers.append('='+ans[1:])
                        elif len(ans) == 0:
                            break
                        else:
                            answers.append('~'+ans[0:])
                            
                    # Convert the answers list to a string and add it to the converted lines
                    converted_lines.append("::Вопрос {}:: {} {{\n{}\n}}\n\n\n".format(question_number, question_text, "\n".join(answers)))
                
                elif (plus > 1) and (plus != num):
                    #Multiple-choise question
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        if ans.startswith('+'):
                            answers.append(f'~%{round(100/plus, 1)}%{ans[1:]}')
                        elif len(ans) == 0:
                            break
                        else:
                            answers.append(f'~%-{round(100/(num-plus), 1)}%{ans[0:]}')
                                           
                    # Convert the answers list to a string and add it to the converted lines
                    converted_lines.append("::Вопрос {}:: {} {{\n{}\n}}\n\n\n".format(question_number, question_text, "\n".join(answers)))
                
                elif (plus > 1) and (plus == num):
                    #Short-answer question
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        if len(ans) == 0:
                            break
                        else:
                            answers.append('='+ans[1:])
                                           
                    # Convert the answers list to a string and add it to the converted lines
                    converted_lines.append("::Вопрос {}:: {} {{\n{}\n}}\n\n\n".format(question_number, question_text, "\n".join(answers)))

                else:
                    #Matching questions
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        parts = ans.split(' - ')
                        if len(parts) == 2:
                            answers.append("={0} -> {1}".format(parts[0], parts[1]))
                        elif len(ans) == 0:
                            break
                            
                    # Convert the answers list to a astring and add it to the converted lines
                    converted_lines.append("::Вопрос {}:: {} {{\n{}\n}}\n\n\n".format(question_number, question_text, "\n".join(answers)))
                    
    # Create a new file path for the output file
    output_file_path = file_path.replace('.txt', '_gift.txt')


    # Write the converted lines to the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.writelines(converted_lines)
        print('File saved as %s' % output_file_path)

    return output_file_path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the two buttons and a text area
        self.select_button = QPushButton('Select Input File', self)
        self.convert_button = QPushButton('Convert to GIFT', self)
        self.exit_button = QPushButton('Exit', self)
        self.text_area = QTextEdit(self)

        # Connect the buttons to their respective functions
        self.select_button.clicked.connect(self.select_file)
        self.convert_button.clicked.connect(self.convert_to_gift)
        self.exit_button.clicked.connect(self.close)

        # Create a vertical layout and add the buttons and text area to it
        vbox = QVBoxLayout()
        vbox.addWidget(self.select_button)
        vbox.addWidget(self.convert_button)
        vbox.addWidget(self.text_area)
        vbox.addWidget(self.exit_button)

        # Set the layout for the main window
        self.setLayout(vbox)
            
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Input File')
        if file_path:
            self.file_path = file_path
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()
                self.text_area.setText(file_contents)
            except IOError:
                QMessageBox.critical(self, 'Error', 'Failed to open file.')
        else:
            QMessageBox.critical(self, 'Error', 'Please select a file.')


    def convert_to_gift(self):
        if self.file_path:
            print(f'Converting input file: {self.file_path}')
            gift_content = convert_to_gift(self.file_path)
            QMessageBox.information(self, 'Success', 'Conversion completed successfully.')
        else:
            QMessageBox.critical(self, 'Error', 'Please select an input file first.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

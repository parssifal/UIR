import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox, QComboBox

def check(line): #Добавление '\' к специальным символам
    to_replace = ["#", "~", "=", "{", "}"]
    
    for char in to_replace:
        line = line.replace(char, "\\" + char)

    return line

def convert_to_gift(file_contents, file_path):
    lines  = file_contents.split('\n')
    
    # Создание пустого списка для хранения конвертированных строк
    converted_lines = []
    # Создание счетчика для отслеживания номера текущего вопроса
    question_number = 0
    # Создание пустого списка для хранения текста вопроса
    question_text = []
    # Создание пустого списка для хранения слов текста вопроса
    words = []
    # Создание пустого списка для хранения название вопроса
    question_name = []
    
    # Перебор каждой строки входного файла
    for i, line in enumerate(lines):
        line = line.strip()
        
        if len(line) == 0:
            i += 1
        
        # Проверяем начинается ли строка с цифры и точки
        elif line[0].isdigit() and line[1] == '.':
            
                # Получаем текст вопроса
                question_text = line[3:]
                # Делим текст вопроса на слова
                words = question_text.split()
                # Создаем название вопроса из первых 5 слов текста вопроса
                question_name = " ".join(words[:5])
                # Увеличиваем счетчик номера вопроса
                question_number += 1
                # Создаем счетчики для определения типа вопроа
                num = plus = 0
                
                # Соаздем список для хранения ответов
                answers = []
                
                # Проходим по ответам текущего вопроса и определяем его тип
                for ans in lines[i+1:]:
                    ans = ans.strip()
                    if ans.startswith('+'):
                        plus += 1
                    elif len(ans) == 0:
                        break
                    num += 1

                if plus == 1:
                   
                    # Вопрос с одним ответом
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        if ans.startswith('+'):
                            answers.append('='+ans[1:])
                        elif len(ans) == 0:
                            break
                        else:
                            answers.append('~'+ans[0:])
                            
                    # Преобразование списка ответов в строки и запись в список конвертированных строк
                    converted_lines.append("::{}:: {} {{\n{}\n}}\n\n\n".format(question_name, question_text, "\n".join(answers)))
                    
                elif (plus > 1) and (plus != num):
                    # Вопрос с множественными ответами
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        if ans.startswith('+'):
                            answers.append(f'~%{round(100/plus, 1)}%{ans[1:]}')
                        elif len(ans) == 0:
                            break
                        else:
                            answers.append(f'~%-{round(100/(num-plus), 1)}%{ans[0:]}')
                                           
                    # Преобразование списка ответов в строки и запись в список конвертированных строк
                    converted_lines.append("::{}:: {} {{\n{}\n}}\n\n\n".format(question_name, question_text, "\n".join(answers)))

                elif (plus > 1) and (plus == num):
                    # Вопрос с коротким ответом
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        if len(ans) == 0:
                            break
                        else:
                            answers.append('='+ans[1:])
                                           
                    # Преобразование списка ответов в строки и запись в список конвертированных строк
                    converted_lines.append("::{}:: {} {{\n{}\n}}\n\n\n".format(question_name, question_text, "\n".join(answers)))

                else:
                    # Вопрос на соответсвие
                    for ans in lines[i+1:]:
                        ans = ans.strip()
                        ans = check(ans)
                        parts = ans.split(' - ')
                        if len(parts) == 2:
                            answers.append("={0} -> {1}".format(parts[0], parts[1]))
                        elif len(ans) == 0:
                            break
                            
                    # Преобразование списка ответов в строки и запись в список конвертированных строк
                    converted_lines.append("::{}:: {} {{\n{}\n}}\n\n\n".format(question_name, question_text, "\n".join(answers)))
                    
    # Создаем новый путь для выходного файла
    output_file_path = file_path.replace('.txt', '_gift.txt')

    # Записываем конвертированнные линии в выходной файл
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.writelines(converted_lines)

    return output_file_path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

       # Создаем кнопки
        self.select_button = QPushButton("Выберите файл", self)
        self.convert_button = QPushButton("Конвертировать", self)
        self.exit_button = QPushButton("Выход", self)
        self.yes_button = QPushButton("Да", self)
        self.no_button = QPushButton("Нет", self)
        self.skip_button = QPushButton("Показать/Пропустить", self)
        self.back_button = QPushButton("Назад", self)
        self.go_to_button = QPushButton("Перейти", self)
        
        # Создаем комбинированный виджет и пустой список вопросов
        self.question_combo = QComboBox(self)
        self.questions = []
        
        # Создаем текстовое поле
        self.text_area = QTextEdit(self)
        
        # Устанавливаем размер шрифта
        font = self.text_area.font()
        font.setPointSize(16)  # Устанавливаем размер шрифта в 16 точек

        # Устанавливаем шрифт для текстовой области
        self.text_area.setFont(font)
        
        self.yes_button.setStyleSheet("background-color: green; color: white;")
        self.no_button.setStyleSheet("background-color: red; color: white;")
        self.exit_button.setStyleSheet("background-color: maroon; color: white;")

        # Соединяем кнопки с соответсвующими функциями
        self.select_button.clicked.connect(self.select_file)
        self.convert_button.clicked.connect(self.convert_to_gift_func)
        self.exit_button.clicked.connect(self.close)
        self.yes_button.clicked.connect(self.yes_func)
        self.no_button.clicked.connect(self.no_func)
        self.skip_button.clicked.connect(self.skip_func)
        self.back_button.clicked.connect(self.back_func)
        self.go_to_button.clicked.connect(self.go_to_question_func)

        # Создаем вертикальный слой для размещения 4 кнопок (2 ряда по 2 кнопки в каждом ряду)
        top_layout = QVBoxLayout()
        top1_layout = QHBoxLayout()
        top1_layout.addWidget(self.select_button)
        top1_layout.addWidget(self.convert_button)
        top2_layout = QHBoxLayout()
        top2_layout.addWidget(self.question_combo)
        top2_layout.addWidget(self.go_to_button)
        
        # Создаем объекты QVBoxLayout для top1_layout и top2_layout
        top1_v_layout = QVBoxLayout()
        top2_v_layout = QVBoxLayout()
        
        # Добавляем QHBoxLayout в соответствующие QVBoxLayout
        top1_v_layout.addLayout(top1_layout)
        top2_v_layout.addLayout(top2_layout)

        # Добавляем QVBoxLayout во второй вертикальный слой
        top_layout.addLayout(top1_v_layout)
        top_layout.addLayout(top2_v_layout)
        
        # Создаем вертикальный слой для размещения 4 кнопок (2 ряда по 2 кнопки в каждом ряду)
        bottom_layout = QVBoxLayout()
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(self.no_button)
        row1_layout.addWidget(self.yes_button)
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(self.back_button)
        row2_layout.addWidget(self.skip_button)
        
        # Создаем объекты QVBoxLayout для row1_layout и row2_layout
        row1_v_layout = QVBoxLayout()
        row2_v_layout = QVBoxLayout()

        # Добавляем QHBoxLayout в соответствующие QVBoxLayout
        row1_v_layout.addLayout(row1_layout)
        row2_v_layout.addLayout(row2_layout)

        # Добавляем QVBoxLayout во второй вертикальный слой
        bottom_layout.addLayout(row1_v_layout)
        bottom_layout.addLayout(row2_v_layout)

        # Создаем вертикальный слой для размещения всех элементов
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.text_area)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.exit_button)

        # Создаем слой для основного окна
        self.setLayout(main_layout)

        # Список для хранения вопросов
        self.question_list = []
        # Список для хранения вопросов, на которые пользователь ответил "Да"
        self.answered_questions = []
        # Создаем счетчик для вопросов
        self.i = 0 

    def show_next_question(self):
        if self.i <= (len(self.question_list) - 1):
            i = self.i
            next_question = self.question_list.__getitem__(i)  # Получаем следующий вопрос
            self.text_area.clear()  # Очищаем text_area перед показом нового вопроса
            self.text_area.append(next_question)
        else:
            self.text_area.clear()  # Если вопросов больше нет, очищаем text_area

    def add_to_array(self):
        if self.i <= (len(self.question_list) - 1):
            i = self.i
            self.answered_questions.append("{}\n\n".format(self.question_list.__getitem__(i)))  # Добавляем вопрос в список ответов
            self.i += 1

    def skip_question(self):
        file_path = self.file_path
        # Создаем новый путь для выходного файла
        output_file_path = file_path.replace('.txt', '_new.txt')

        # Записываем выбранные вопросы в выходной файл по новому пути
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.writelines(self.answered_questions)
        
        # Выводиим выбранные вопросы на текствоое поле 
        self.file_contents = '\n'.join(self.answered_questions)
        self.text_area.setText(self.file_contents)

    def select_file(self):
        # Получаем файл
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Input File')
        if file_path:
            self.file_path = file_path
            try:
                # Читаем данные из файла
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_thing = file.read()
                # Создаем массив для хранения вопросов
                self.arrays = [block.strip().split('\n') for block in file_thing.split('\n\n')]
                if self.arrays is not None:
                    for array in self.arrays:
                        self.question_list.append('\n'.join(array))
                        self.question_combo.addItem(str(array[0]))

                    # Показываем первый вопрос
                    self.show_next_question()

            except IOError:
                QMessageBox.critical(self, 'Error', 'Не получилось открыть файл.')
        else:
            QMessageBox.critical(self, 'Error', 'Пожалуйста выберите файл.')
    
    def convert_to_gift_func(self):
        if self.file_path:
            file_contetns = self.file_contents
            file_path = self.file_path
            gift_content = convert_to_gift(file_contetns, file_path)
            QMessageBox.information(self, 'Success', 'Конвертация выполнена успешно.')
        else:
            QMessageBox.critical(self, 'Error', 'Пожалуйста сначала выберите файл.')

    def yes_func(self):
        self.add_to_array()
        self.show_next_question()

    def no_func(self):
        self.i += 1
        self.show_next_question()

    def skip_func(self):
        self.skip_question()
    
    def back_func(self):
        self.show_next_question()
    
    def go_to_question_func(self):
        # В этой функции вы можете реализовать переход к выбранному вопросу и отобразить его содержимое в текстовом поле
        selected_question = self.question_combo.currentText()
        for i, array in enumerate(self.arrays):
            if str(array[0]) == selected_question:
                self.text_area.clear()
                self.i = i
                self.text_area.append(self.question_list.__getitem__(i))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setGeometry(200, 200, 800, 600)
    main_window.show()
    sys.exit(app.exec_())


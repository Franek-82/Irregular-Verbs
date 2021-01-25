#!/usr/bin/python3.6

import sys, os, random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,
                             QFrame, QGroupBox, QApplication, QPushButton, QAction, QTextEdit,
                             QMessageBox, QTabWidget)
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSlot


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.phase = ' Запоминаие слов'
        my_box = QVBoxLayout()
        box1 = QGroupBox()
        box2 = QGroupBox()
        box3 = QGroupBox()
        self.qle1 = QLineEdit(self)
        self.qle2 = QLineEdit(self)
        self.qle3 = QLineEdit(self)
        self.lbl_phase = QLabel()
        self.lbl_phase.setFixedHeight(20)
        self.from_lbl = QFrame()
        self.from_lbl.setFrameShape(4)
        self.rulbl = QLabel()
        self.rulbl.setFixedHeight(100)
        lbl1 = QLabel('Infinitive')
        lbl1.setFixedWidth(100)
        lbl2 = QLabel('Past Indefinite')
        lbl2.setFixedWidth(100)
        lbl3 = QLabel('Participle II')
        lbl3.setFixedWidth(100)
        self.okBt = QPushButton('Запомнил')
        self.okBt.setFixedSize(270, 50)
        self.help_Bt = QPushButton('Подсказка')
        self.help_Bt.setFixedSize(150, 30)
        hbox1 = QHBoxLayout()  # Конейнеры
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        hbox1.addWidget(lbl1)
        hbox1.addWidget(self.qle1)
        hbox2.addWidget(lbl2)
        hbox2.addWidget(self.qle2)
        hbox3.addWidget(lbl3)
        hbox3.addWidget(self.qle3)
        box1.setLayout(hbox1)
        box2.setLayout(hbox2)
        box3.setLayout(hbox3)
        my_box.addWidget(self.lbl_phase)
        my_box.addWidget(self.from_lbl)
        my_box.addWidget(self.rulbl)
        my_box.addWidget(box1)
        my_box.addWidget(box2)
        my_box.addWidget(box3)
        my_box.addSpacing(70)
        my_box.addWidget(self.okBt, alignment=Qt.AlignCenter)
        my_box.addSpacing(15)
        my_box.addWidget(self.help_Bt, alignment=Qt.AlignCenter)

        self.rulbl.setFont(QFont('OldEnglish', 20))
        self.rulbl.setAlignment(Qt.AlignCenter)
        self.qle1.setFont(QFont('OldEnglish', 15))
        self.qle1.setAlignment(Qt.AlignHCenter)
        self.qle2.setFont(QFont('OldEnglish', 15))
        self.qle2.setAlignment(Qt.AlignHCenter)
        self.qle3.setFont(QFont('OldEnglish', 15))
        self.qle3.setAlignment(Qt.AlignHCenter)
        self.setLayout(my_box)


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.w = MyWidget()
        self.setCentralWidget(self.w)
        self.createToolBars()
        col = QColor(139, 69, 19)
        self.w.lbl_phase.setStyleSheet("QWidget { color: %s }" % col.name())
        self.w.lbl_phase.setText(self.w.phase)
        self.save_change = False  # Сохранение не нужно
        self.show_message = True # При сохранении показывать сообщение
        self.n = 4  # Кол-во слов за фазу
        self.cycle_first = True  # Первый цикл запоминания
        self.w.okBt.clicked.connect(self.phase_one)

        list_file = os.listdir(".")
        try:
            if "save_words.txt" in list_file:
                file = open("save_words.txt")
                if not file.readline():
                    file = open("verbs.txt", "r")
            else:
                file = open("verbs.txt", "r")
            file.seek(0)
            self.all_words = []
            self.all_words_to_save = []
            for line in file:
                lines = line.split()
                self.all_words.append(lines)  # список
                self.all_words_to_save.append(line)  # строка
            file.close()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибака", "Файл отсутсвует.")
            quit()
        except OSError:
            QMessageBox.warning(self, "Ошибака",
                                "Неустановленная ошибка открытия файла.")
            quit()
        self.begin()
        self.resize(450, 420)
        self.setMaximumSize(700, 550)
        self.setWindowTitle('Программа изучения непр. глаголов')
        self.show()

    def create_word(self):
        global word
        word = self.li_four[self.i]
        self.w.rulbl.setText(word[0])
        self.i += 1
        self.statusBar().showMessage("Слово " + str(self.i))

    def show_word(self):
        self.w.qle1.setText(word[1])
        self.w.qle2.setText(word[2])
        self.w.qle3.setText(word[3])

    def begin(self):
        self.phase = ' Запоминаие слов'
        self.i = 0
        self.li_four = []
        # Создание списка индексов слов на случай сохранения
        self.indexes_for_del = []
        self.count_of_words = len(self.all_words)
        if self.count_of_words:
            if self.count_of_words < 4:  # Фаза с остатком слов
                self.n = self.count_of_words
            print("Всего слов в этой фазе: ", self.n)
            for k in range(self.n):
                j = random.randint(0, len(self.all_words)-1)
                self.li_four.append(self.all_words[j])
                self.indexes_for_del.append(j)
                del self.all_words[j]
            self.w.okBt.grabKeyboard()
            self.phase_one()
        else:
            message = "Все слова пройдены."
            QMessageBox.information(self, 'В файле больше нет слов.', message)
            quit()

    def action(self):
        self.x = 0
        self.w.qle1.clear()
        self.w.qle2.clear()
        self.w.qle3.clear()
        col = QColor(255, 255, 255)
        self.w.qle1.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.w.qle2.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.w.qle3.setStyleSheet("QWidget { background-color: %s }" % col.name())
        if self.i < self.n:  # если № элем. li_four меньше всех слов в фазе
            self.create_word()
            self.w.qle1.setFocus()
        else:                # Переход на первую фазу
            # Удаление пройденных слов из списка для сохранения
            for index in self.indexes_for_del:
                del self.all_words_to_save[index]
            self.w.okBt.setEnabled(True)
            self.save_change = True
            self.begin()

    @pyqtSlot()
    def phase_one(self):  # Слот и метод
        if self.i < self.n:
            self.w.qle1.setReadOnly(True)
            self.w.qle2.setReadOnly(True)
            self.w.qle3.setReadOnly(True)
            self.w.okBt.setFocus()
            self.w.help_Bt.setVisible(False)
            self.create_word()
            self.show_word()
        else:
            self.w.qle1.setReadOnly(False)
            self.w.qle2.setReadOnly(False)
            self.w.qle3.setReadOnly(False)
            self.w.lbl_phase.setText(' Проверка знания слов')
            self.i = 0  # i - номер элем. списка, состоящего из списков (li_four)
            self.x = 0
            self.w.help_Bt.setVisible(True)
            self.w.okBt.releaseKeyboard()
            self.w.okBt.setEnabled(False)  # Скрытие кнопки
            self.action()
            if self.cycle_first:
                self.phase_two()

    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            self.help()

    @pyqtSlot()
    def help(self):
        #print("В фокусе: ", app.focusWidget())
        if self.w.qle1.text() != word[1]:
            self.w.qle1.setText(word[1])
            qle_name = self.w.qle1
        elif self.w.qle2.text() != word[2]:
            self.w.qle2.setText(word[2])
            qle_name = self.w.qle2
        elif self.w.qle3.text() != word[3]:
            self.w.qle3.setText(word[3])
            qle_name = self.w.qle3
        else:
            return
        qle_name.setFocus()  # Установка фокуса на строке с подсказкой
        self.verification(qle_name)

    def phase_two(self):
        print("phase_two")
        self.cycle_first = False
        self.w.help_Bt.clicked.connect(self.help)
        self.w.qle1.textEdited[str].connect(self.processing)
        self.w.qle2.textEdited[str].connect(self.processing)
        self.w.qle3.textEdited[str].connect(self.processing)

    @pyqtSlot()
    def processing(self):
        my_sender = self.sender()  # Устанавливает источник сигнала
        if my_sender == self.w.qle1:
            if self.w.qle1.text() == word[1]:
                self.verification(my_sender)
        elif my_sender == self.w.qle2:
            if self.w.qle2.text() == word[2]:
                self.verification(my_sender)
        elif my_sender == self.w.qle3:
            if self.w.qle3.text() == word[3]:
                self.verification(my_sender)

    def verification(self, my_sender):
            self.focusNextChild()  # Смещение фокуса на следующий компонет
            col = QColor(255, 228, 196)
            my_sender.setStyleSheet("QWidget { background-color: %s }" % col.name())
            self.x += 1
            if self.x == 3:
                QTimer.singleShot(1200, self.action)

    def createToolBars(self):
        self.toolBar = self.addToolBar("List total")
        self.toolBar.setMovable(False)
        self.listAct = QAction(QIcon('text.png'), "Список непройденных слов", self, triggered=self.list_method)
        self.toolBar.addAction(self.listAct)
        self.saveAct = QAction(QIcon('save.png'), "Сохранить", self, triggered=self.save_method)
        self.toolBar.addAction(self.saveAct)
        self.infoAct = QAction(QIcon('info.png'), "Информация", self, triggered=self.info_method)
        self.toolBar.addAction(self.infoAct)
        self.helpAct = QAction(QIcon('help.png'), "Справка", self, triggered=self.help_method)
        self.toolBar.addAction(self.helpAct)

    @pyqtSlot()
    def find_word(self):
        self.answers_widget.clear()
        if self.qle_widget.text():
            words = []
            enter_text = self.qle_widget.text().lower()
            n = len(enter_text)
            for line in self.all_words_to_save:
                line_list = line.split(" ", 2)
                if enter_text == line_list[1][:n]:
                    #  Список слов, первые буквы которых
                    #  совпадают с введенными пользователем.
                    words.append(line)
            if words:
                for el in words:
                    list_el = el.split()
                    # txt.setStyleSheet("QTextEdit {color:red}")
                    word = "<font size='4'><pre><font color='red'>{0:11}</font>{1:11}{2:11}{3:12}</pre></font>".\
                        format(list_el[1], list_el[2], list_el[3], list_el[0])
                    self.answers_widget.append(word.rstrip())
            else:
                self.answers_widget.setText("В списке нет слов, начинающихся с такой буквы.")

    def list_method(self):
        l_window = QWidget(parent=self, flags=Qt.Window)
        page1 = QWidget()
        self.qle_widget = QLineEdit(self)
        lbl = QLabel("Поиск английских глаголов (в форме Infinitive):")
        lbl.setAlignment(Qt.AlignBottom)
        self.txt_widget = QTextEdit()
        self.answers_widget = QTextEdit()
        self.answers_widget.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.answers_widget.setFixedHeight(280)
        self.txt_widget.setFont(QFont("Courier"))
        #self.txt_widget.setFontPointSize(20)
        self.txt_widget.setReadOnly(True)
        self.answers_widget.setReadOnly(True)
        #  Сортировка списка слов по алфавиту
        self.all_words_to_save.sort(key=lambda element: element[0].lower())
        for line in self.all_words_to_save:
            # Отображение слов без учета регистра. Рус. слово - с бол. буквы.
            line = line.rstrip().capitalize()
            l_line = line.split(" ", 1)  # Возвращает лист из 2 строк
            total_line = "{0:16} {1}".format(l_line[0], l_line[1])
            self.txt_widget.append(total_line)
        self.w.okBt.releaseKeyboard()
        self.qle_widget.setFocus()
        self.qle_widget.textEdited[str].connect(self.find_word)

        tab = QTabWidget(l_window)
        horbox = QHBoxLayout(l_window)
        horbox.addWidget(tab)
        verbox = QVBoxLayout(l_window)
        verbox.addWidget(self.answers_widget)
        verbox.addWidget(lbl)
        verbox.addWidget(self.qle_widget)
        page1.setLayout(verbox)

        tab.addTab(self.txt_widget, "Список слов")
        tab.addTab(page1, "Поиск слова")
        tab.setElideMode(Qt.ElideLeft)
        tab.setCurrentIndex(0)

        l_window.setWindowTitle('Непройденные слова')
        l_window.setFixedWidth(450)
        l_window.resize(450, 450)
        l_window.show()

    def help_method(self):
        QMessageBox.about(self, "Программа изучения непр. глаголов \n",
                          "Автор программы: Канаброцкий Франтишек \n"
                          "Программа является бесплатной \nrick11@yandex.ru, 2018")

    def info_method(self):
        message = "Программа запоминания английских глаголов содержит 100 слов.\n " \
                  "Добавить или удалить отдельные слова можно в файле verbs.txt" \
                  " (находится в папке с программой).\n" \
                  "Чтобы перейти к следующему слову, можно нажимать пробел.\n"\
                  "Если забыли перевод глагола на английский, \nнажмите клавишу Ctrl или" \
                  " на окне программы кнопку 'Подсказка'."
        QMessageBox.about(self, "Информация", message)

    def save_method(self):
        if self.save_change:
            with open("save_words.txt", "w") as file:
                for el in self.all_words_to_save:
                    file.write(el)
                message = "Сохранено в файл."  # file.name
            self.save_change = False
        else:
            message = "Нет слов для сохранения."
        if not self.show_message:
            return
        QMessageBox.information(self, 'Сохранение', message)

    def maybeSave(self):
        ret = QMessageBox.warning(self, "Сохранение изменений", "Сохранить изменения?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if ret == QMessageBox.Save:
            self.show_message = False
            self.save_method()
        if ret == QMessageBox.Cancel:
            return False
        return True

    def closeEvent(self, event):
        if self.save_change:  # self.all_words_to_save
            if self.maybeSave():
                event.accept()
            else:
                event.ignore()

    """def past(self, text):
        if text == "77":
            col = QColor(175, 238, 238)
            self.qle2.setStyleSheet("QWidget { background-color: %s }" % col.name())
            self.x += 1
            if self.x == 2:
                self.action()

    def partic(self, text):
        if text == "77":
            col = QColor(175, 238, 238)
            self.qle3.setStyleSheet("QWidget { background-color: %s }" % col.name())
            self.x += 1
            if self.x == 3:
                self.action()"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())

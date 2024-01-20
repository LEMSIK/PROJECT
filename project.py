import sys #импортируем библиотеку sys
from datetime import datetime # импортируем библиотеку для работы сдатой и временим
# импортируем библиотеку PyQt5 для работы с дизайном
from PyQt5 import uic, QtCore, QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QButtonGroup, QRadioButton, QMessageBox, QInputDialog


class Question:
    # класс для работы с вопроосами
    
    def __init__(self, question, correct_answer, answers):
        self.question = question
        self.correct_answer = correct_answer
        self.answers = answers

    def check_answer(self, answer): 
        # класс для проверки ответов

        if answer == self.correct_answer:
            return True
        return False


class Quiz(QMainWindow):
    # главный класс нашего приложения

    def __init__(self, quiz: 'list[Question]'):
        super().__init__()
        name, ok_pressed = QInputDialog.getText(self, 'Регистрация', 'Введите Ваше имя')
        if ok_pressed:
            self.name = name.strip()
        else:
            self.name = ''
        uic.loadUi("project.ui", self)  # Загружаем дизайн

        central_widget = QWidget()
        central_widget.setLayout(self.verticalLayout)
        self.setCentralWidget(central_widget) # делаем так что бы виджеты растягивались вместе с экраном
       
        self.quiz = quiz
        self.answers = QButtonGroup(self)
        self.answers.addButton(self.answer1, id=0)
        self.answers.addButton(self.answer2, id=1)
        self.answers.addButton(self.answer3, id=2)
        self.answers.addButton(
            QRadioButton(self), id=3
        )  # Добавляю дополнительную кнопку, которая будет нажата, если ни один вариант не выбран

        self.prevButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
        self.setup() # устанавливаем начальные значение
    
    def setup(self):
        # Установка переменных, начало работы

        self.q = 0
        self.options = [3 for _ in range(len(quiz))]
        for button in self.answers.buttons():
            button.setHidden(False)
        self.answers.button(3).setHidden(True)
        self.prevButton.setText("назад")
        self.nextButton.setText("далее")
        self.prevButton.setHidden(False)
        self.nextButton.setHidden(False)
        self.display_question()
   
    def display_question(self):
        # отображаем вопрос и варианты ответов

        self.answers.button(self.options[self.q]).setChecked(True) # отображаем отмеченный и запомненные варианты ответов
       
        question = self.quiz[self.q]
        self.question.setText(question.question)
        self.answer1.setText(question.answers[0])
        self.answer2.setText(question.answers[1])
        #прячем треью кнопку если только два варианта ответа
        if len(question.answers) > 2:
            self.answer3.setHidden(0)
            self.answer3.setText(question.answers[2])
        else:
            self.answer3.setHidden(2)
   
    def previous(self):
        # переключаем на предыдущий вопрос или начинаем тест заново

        if self.prevButton.text() == "Пройти тест снова":
            self.setup()
        else:
            self.options[self.q] = self.answers.checkedId() # Запоминаем выбор
            self.q = max(0, self.q - 1) # Не даем q выйти за диапазон
            self.display_question()
   
    def next(self):
        # переключаем на следующий вопрос или завершаем тест

        self.options[self.q] = self.answers.checkedId()
        if self.q == len(self.quiz) - 1:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Подтверждение')
            msgBox.addButton('Да', QMessageBox.AcceptRole)
            msgBox.addButton('Нет', QMessageBox.RejectRole)
            msgBox.setText("Вы хотите завершить тест?")
            result = msgBox.exec_()
            if result == QMessageBox.AcceptRole:
                self.end()
        else:
            self.q = min(len(self.quiz) - 1, self.q + 1)
            if self.q == len(self.quiz) - 1:
                self.nextButton.setText('завершить')
                self.display_question()
            else:
                self.nextButton.setText('далее')
                self.display_question()
    
    def end(self):
        # Завершение теста

        for btn in self.answers.buttons():
            btn.setHidden(True)# прячем все кнопки для выбора ответов
        self.nextButton.setHidden(True)
        self.prevButton.setText("Пройти тест снова")
        result = 0
        for i in range(len(self.quiz)):# считаем результат в балах
            if self.quiz[i].check_answer(self.options[i]):# проверяем ответ
                result += 1
        res_in_procents = round(result / len(self.quiz) * 100)# считаем проценты и округляем 
        # выбор цвета

        b = 50
        if res_in_procents >= 60:
            r = 50
            g = 150
        else:
            r = 250
            g = 50
        color = (r, g, b)
        text = f"Ваш результат составил {res_in_procents}%. Вы {'не ' if res_in_procents < 60 else ''}прошли тест"
        if self.name:
            text = f"{self.name}, " + text
        self.question.setText(f'<p style="color: rgb{color}">{text}</p>')# выводим результат с нужным цветом

        #записываем результат в текстовый файл
        if self.name:
            dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            with open('результаты теста.txt', 'a', encoding='utf-8') as f:
                f.write(f'{self.name}, Вы прошли тест {dt}\nВаш результат равен {res_in_procents}% или {result} правильных ответов из {len(self.quiz)} вопросов\n\n')


if __name__ == "__main__": #делаем так чтобы наше приложение не запускалось с других файлов
    # делаем так чтобы приложение хорошо выглядело на больших экранах
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
     # вопросы с ответами
    quiz = [
        Question('1. Действия оператора при мигании жёлтой сигнальной лампы регенерации сажевого фильтра?',
                 1,
                 ['''а) Не обращаю внимания, продолжаю работу,
по возвращении в гараж сообщу об этом обслуживающему персоналу.''',
                  '''б) Проверю показания уровня сажи на мониторе двигателя,
если прожиг не запускается и показания выросли более 100%,
то прекращу работу, заглушу двигатель в ближайшем подходящем месте и
сообщу о неисправности обслуживающему персоналу.''']),
        Question("2. Что означает горящая жёлтая сигнальная лампа регенерации сажевого фильтра?", 0, ["а) Происходит регенерация сажевого фильтра", "б) Предупреждение о необходимости / скором начале регенерации сажевого фильтра",
                "в) Ошибка сажевого фильтра"]),
        Question("3. Что может означать мигающая жёлтая сигнальная лампа регенерации сажевого фильтра?", 2, ["а) Происходит регенерация сажевого фильтра", "б) Предупреждение о необходимости / скором начале регенерации сажевого фильтра", " в) Ошибка сажевого фильтра"]),
        Question("4. Передвижение машины с подключенным к пульту силовым кабелем допускается:", 1, ["а) Только в положении передачи ’’дорога’’ (’’заяц’’)", " б) Только в положении передачи ’’бездорожье’’ (’’черепаха’’)", "в) Передача выбирается в соответствии с состоянием конкретной дороги"]),
        Question("5. Включение тумблера активации кабельного барабана необходимо:", 0, [" а) При езде задом с подключенным к пульту силовым кабелем", "б) При езде вперёд с подключенным к пульту силовым кабелем", "в) Для активации кнопки ручной смотки кабельного барабана"]),
        Question("6. Можно ли производить остановку машины стояночным тормозом?", 2, ["а) Нельзя ни при каких обстоятельствах", "б) Можно всегда, если скорость машины не превышает 5км/ч", "в) Можно только в аварийной ситуации, когда неисправны рабочие тормоза, т. к. это сильно изнашивает тормозной механизм."]),
        Question("7. Разрешается ли переезд машины с не до конца поднятыми лапами или не до конца сдвинутыми траверсами?", 2, ["а) Можно, если речь идёт о переезде в соседнюю камеру", "б) Можно, если расстояние не превышает 25м", "в) Запрещено"]),
        Question("8. Разрешается ли начинать работу на машине, не проверив уровни рабочих жидкостей?", 1, ["а) Разрешается, т. к. проверка носит рекомендательный характер", "б) Запрещается", "в) Разрешается, если уже как минимум 7 дней подряд уровень жидкостей был в норме"]),
        Question("9. Разрешается ли работа на машине с неисправным звуковым сигналом?", 1, ["а) Разрешается при условии, что исправен дальний свет для подачи сигналов другим операторам", "б) Не разрешается"]),
        Question("10. Горящая зелёная сигнальная лампа на разъединителе аккумуляторной батареи означает:", 2, ["а) Неисправность разъединителя", "б) Можно включать разъединитель","в) Можно выключить разъединитель"]),
        Question("11. Разрешено ли глушить дизельный двигатель машины аварийной стоповой кнопкой?", 1, ["а) Можно всегда, если машина остановлена, и активирован стояночный тормоз", " б) Можно только в аварийной ситуации"]),
        Question("12. Можно ли глушить дизельный двигатель машины в процессе регенерации сажевого фильтра?", 1, ["а) Можно всегда", "б) Можно только в аварийной ситуации",]),
        Question("13. Переключение селектора направления движения хода возможно только:", 1, ["а) При скорости менее 5км/ч", "б) При полной остановке","в) Не имеет значения, т. к. машина сама автоматически управляет приводом хода"]),
        Question("14. Оператор производит контроль технического состояния эксплуатируемой машины:", 0, ["а) В начале и конце каждой смены", "б) Раз в неделю","в) По мере необходимости в течение рабочей смены"]),
        Question("15. Ежесменное техобслуживание и ответственность за техническое состояние машины на смене лежит:", 2, ["а) На мастере участка", "б) На механике","в) На операторе"]),
        Question("16. Хранить инструменты или запчасти в кабине:", 0, ["а) Запрещено", "б) Разрешено"]),
        Question("17. При временной или вынужденной парковке машины вне зоны постоянного гаражирования необходимо:", 0, ["а) Оставить машину со включенными габаритными огнями и сигнальными маячками", "б) По возможности предупредить других рабочих,\nнаходящихся в данной рабочей зоне","в) Предупредить лицо надзора или диспетчера шахты если остановка произошла на маршруте общего пользования"]),
        Question("18. Разрешается ли работа на машине с неисправной системой регенерации сажевого фильтра?", 0, ["а) Запрещено", "б) Разрешено"]),
        Question("19. Какие действия являются правильными при необычном / нерегулярном поведении машины?", 1, ["а) Внимательно наблюдать, чем всё закончится", "б) Незамедлительно остановить машину нажатием аварийной стоповой кнопки"]),
    ]
    # запускаем приложение 
    app = QApplication(sys.argv) 
    ex = Quiz(quiz)
    ex.show()
    sys.exit(app.exec_())
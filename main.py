import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount

        # Стоит использовать прямую логику, она лучше читается и более понятна
        # Например:
        # if date:
        #     self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        # else:
        #     self.date = dt.datetime.now().date()
        self.date = (
            # now() возвращает datetime, который приходится приводить к date.
            # Можно сразу получить сегодняшнюю дату: dt.date.today()
            #
            # if и not Должны быть на одной строке. Их переносят на след.
            # строку вместе с условием:
            # dt.datetime.now().date()
            # if not date
            # else
            # dt.datetime.strptime(date, '%d.%m.%Y').date())
            dt.datetime.now().date() if
            not
            # формат даты стоит вынести или в константу в отдельный файл, или
            # в атрибут класса: он может использоваться в нескольких
            # местах внутри класса. И менять потом проще, если потребуется.
            # class Record:
            #     DATE_FORMAT = '%d.%m.%Y'
            # ...
            # dt.datetime.strptime(date, DATE_FORMAT).date()
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # Весь метод можно написать, используя sum:
    # today = dt.date.today()
    # return sum(record.amount for record in self.records if record.date == today)
    def get_today_stats(self):
        today_stats = 0
        # Не стоит именовать переменные как классы, имя переменной должно
        # начинаться с маленькой буквы. Тут стоит назвать ее record
        # Тем более что класс Record описан чуть выше
        for Record in self.records:
            # Cтоит использовать в таких случаях dt.date.today()
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # По аналогии с методом get_today_stats, этот тоже можно
    # переписать с использованием sum()
    def get_week_stats(self):
        week_stats = 0
        # Если упростить условие в if'е ниже, то переменная today не потребуется,
        # можно просто написать dt.date.today() - record.date
        # ну и, конечно, тоже стоит использовать в таких случаях dt.date.today()
        today = dt.datetime.now().date()
        for record in self.records:
            # это условие можно упростить так: if 7 > (today - record.date).days >= 0
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции должен быть оформлен в виде Docstring, см. Требования к коду
    # (https://docs.google.com/document/d/1s_FqVkqOASwXK0DkOJZj5RzOm4iWBO5voc_8kenxXbw/edit)
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Имя переменной должно говорить о том, что хранит переменная
        # x - не говорящее имя, стоит переименовать ее во что-то вроде calories_remained
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Согласно требованиям к коду бэкслеши для переноса использовать нельзя.
            # Можно избавиться от этого, обернув возвращаемое в круглые скобки.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Тут скобки не нужны
            return('Хватит есть!')


class CashCalculator(Calculator):
    # float можно задать просто строковым литералом, вот так:
    # USD_RATE = 60.0
    #
    # Имена этих двух переменных хорошо говорят о том,
    # что в них лежит, комментарии к ним излишни
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # По условию задачи метод должен принимать только один (кроме self, конечно)
    # аргумент - currency. Поскольку USD_RATE и EURO_RATE - аттрибуты класса,
    # передавать их не нужно, они доступны через self
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Перед этим if нужно добавить пустую строку, чтобы отделить блок возврата результата
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Это выражение тут не имеет смысла: это проверка на то, равен ли остаток 1 рублю
            # Результат сравнения никуда не сохраняется и не оказывает на результат
            # выполнения метода никакого влияния
            cash_remained == 1.00
            currency_type = 'руб'
        # Перед этим if нужно добавить пустую строку, чтобы отделить блок возврата результата
        if cash_remained > 0:
            return (
                # Неконсистентно: чуть ниже для вывода числа с двумя знаками после запятой
                # используется format. В данном случае дело вкуса, но стоит использовать
                # единый способ везде, если возможно.
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # else тут уже не нужен: может выполниться только одна
        # ветка if'а, и внутри всех if выполняется return
        elif cash_remained < 0:
            # Согласно требованиям к коду бэкслеши для переноса использовать нельзя.
            # Можно обернуть в круглые скобки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Этот метод ничем не отличается от метода get_week_stats
    # из суперкласса, нет необходимости его перегружать
    def get_week_stats(self):
        super().get_week_stats()

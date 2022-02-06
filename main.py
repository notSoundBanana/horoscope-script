import urllib.request

# Словари для вариативного ввода пользователя

signsEnRus = {
    "aries": "Овен",
    "taurus": "Телец",
    "gemini": "Близнецы",
    "cancer": "Рак",
    "leo": "Лев",
    "virgo": "Дева",
    "libra": "Весы",
    "scorpio": "Скорпион",
    "sagittarius": "Стрелец",
    "capricorn": "Козерог",
    "aquarius": "Водолей",
    "pisces": "Рыбы"
}

signsRusEn = {
    "овен": "aries",
    "телец": "taurus",
    "близнецы": "gemini",
    "рак": "cancer",
    "лев": "leo",
    "дева": "virgo",
    "весы": "libra",
    "скорпион": "scorpio",
    "стрелец": "sagittarius",
    "козерог": "capricorn",
    "водолей": "aquarius",
    "рыбы": "pisces"
}


def check_sign(astro_sign):  # Проверка языка, который использовал пользователь при вводе
    return astro_sign in signsRusEn.keys() or astro_sign in signsEnRus.keys()


class Main:
    def __init__(self, astro_sign):
        self.astro_sign = astro_sign

    def main(self) -> str:
        # Кидаем request на сайт с гороскопами
        link = urllib.request.urlopen('https://1001goroskop.ru/?znak={}'.format(self.astro_sign.lower()))
        lines = []

        # Все данные о гороскопе находятся под тегами <td><span>...
        for line in link.readlines():
            pos = line.find(b'<td><span>')
            if pos != -1:
                lines.append(line)

        link.close()

        # Переводим bytes в str
        for i in range(len(lines)):
            lines[i] = lines[i].decode('cp1251')

        # Можно работать как с обычной строкой
        for i in range(len(lines)):
            # Убираем всё лишнее
            lines[i] = lines[i].replace(
                ('<td><span><img src="/img/zodiak/foto/sovm/{}_s.jpg" width="300"' +
                 ' height="200" class="img_left" id="tomini"').format(
                    self.astro_sign.lower()),
                '')
            lines[i] = lines[i].replace(
                ('alt="{} &ndash; гороскоп на сегодня | 1001 ГОРОСКОП"' +
                 ' itemprop="image" /></span><div itemprop="description"><p>').format(
                    signsEnRus.get(self.astro_sign)), "")
            lines[i] = lines[i].replace(
                ('</p></div><div class="subscr gray">Гороскоп на сегодня: <a href="//1001goroskop.ru/?metodika/"' +
                 ' title="О методике составления ежедневных гороскопов" itemprop="author">Дмитрий Зима</a></div></td>'),
                '')

            lines[i] = lines[i].replace(
                ('</p></div><div class="subscr gray"><a href="//1001goroskop.ru/?metodika/" title="О методике'
                 ' составления ежедневных гороскопов" itemprop="author">'
                 'Д. и Н. Зима для *1001 гороскоп*</a></div></td>'),
                '')

            lines[i] = lines[i].replace('\n', ' ')

        # Приводим строку в читаемый вид
        lines = str(*lines).split()
        return "{} гороскоп на сегодня:\n".format(signsEnRus.get(self.astro_sign.lower())) + " ".join(lines)


# Обработка пользовательского ввода
user_input = str(input("Знак?\n")).lower()
while not check_sign(user_input):
    print("Неверно введен знак зодиака\nПовторите попытку")
    user_input = str(input("\nЗнак?\n")).lower()
if user_input[0] in "йцукенгшщзхъфывапролджэёячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮ":
    user_input = signsRusEn.get(user_input.lower())

print(Main(user_input).main())

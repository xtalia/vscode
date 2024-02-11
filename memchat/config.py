GRANTED = ['184944023', '348971882', '587612412', '529194639', '540312' ,'6212781520','6672281848']

UPDATE_TRIGGERS = ["обновить", "update", "j,yjdbnm", "помощь"]

# тестовой функции
TEST_TRIGGERS = ["test", "тест", "/test"]

# калькулятора цен по карте, в рассрочку и пр
CALCULATE_TRIGGERS = ["калькулятор", "calculator", "rfkmrekznjh", "calc", "кальк", "сфдс", "кл", "cl", "сд", "rk",
                      "/calculator", "скидка", "crblrf", '/discount']

# обрезчика серийника
SN_TRIGGERS = ["сн", "sn", "серийник", "ын", "ыт", "cy", "/sn"]

# трейдин-опросника
TRADEIN_TRIGGERS = ["трейдин", "tradein", "nhtqlby", "tn", "тн", "ет", "ny", "/tradein"]

# счетчика крупных купюр
MEGACALC_TRIGGERS = ["мегакалькулятор", "мега", "mega", "mc", "ьс", "мк", "megacalc", "/megacalc"]

# списка работающих сегодня или завтра
WW_TRIGGERS = ["кто работает", "кто", "rnj", "/whowork"]

# курса валют
USD_RATE_COMMANDS = ['курс доллара', 'курс', 'kurs', 'rehc', '/usdrub']

# genpdf
GENPDF_TRIGGERS = ['/generate_pdf','трейдинпдф','genpdf','генпдф', "трейдиндок"]

# avitoclassificator
CLASSIFICATOR_TRIGGERS = ['/classificator', "авито","classificator", "классификатор", "клс","rkc", "cls", "сды"]

SITE_TRIGGERS = ['xxx','ччч']

PRICEUP_TRIGGERS = ['костыль','rjcnskm']

# who_work
WW_LINK = "https://docs.google.com/spreadsheets/d/13KUmHtRXYbXjBE7KQ_4MFQ5VsgUYqu2heURY1y2NwiE/edit#gid=0"
WW_PLACES = {
        "У": "😎 как Управляющий",
        "М": "🙂 как Менеджер",
        "M": "🙂 как Менеджер",
        "РБ": "🏪 в ТЦ Рубин",
        "Р": "🏪 на Рахова",
        "К": "🏪 на Казачьей",
        "Ч": "🏪 на Чернышевского",
        "C": "🏪 в ТЦ СитиМолл",
        "С": "🏪 в ТЦ СитиМолл",
        "И": "😱 как SMM",
        "1": "🧑‍💼 Работает",
        "А": "👀 Шатает Авито",
        "114": "🛠️ на Чернышевского 📞114",
        "111": "🛠️ в ТЦ Рубин 📞111",
        "104": "🛠️ на Казачьей 📞104",
        "107": "🛠️ на Казачьей, Старший(-ая) 📞107",
        "К-100": "🏪 на Казачьей 📞100",
        "К-101": "🏪 на Казачьей 📞101",
        "Р-116": "🏪 на Рахова 📞116",
        "Р-117": "🏪 на Рахова 📞117",
        "РБ-111" : "🏪 в ТЦ Рубин 📞117",
        "Ч-114": "🏪 На Чернышевского 📞114",
        "С130": "🏪 в ТЦ СитиМолл 📞131",
        "С131": "🏪 в ТЦ СитиМолл 📞131",
        "С132": "🏪 в ТЦ СитиМолл 📞132",
        "300" : "🏪 Никитинская 44 📞300",
        "310" : "⛵ Галерея Чижова 📞310",
        "311" : "⛵ Галерея Чижова 📞311"
    }
# hatikoenchanced
replacement_dict = {
    "Магазин Балаково, Ленина 76" : "🛒🅱 Ленина 76",
    "Магазин Саратов, Б. Казачья, 23/27" : "🛒🆂 Б. Казачья 23-27",
    "Магазин Саратов Рахова 149/157" : "🛒🆂 Рахова 149-157",
    "Магазин Саратов ТЦ СитиМолл" :  "🛒🆂 СитиМолл",
    "Магазин-Сервис Саратов, ТЦ Рубин" : "🛒🆂 ТЦ Рубин",
    "Магазин Воронеж, Никитинская, 44"  : "🛒🆅 Никитинская 44",
    "Магазин Воронеж,Центр Галереи Чижова" : "🛒🆅 Галерея Чижова",
    "Магазин Липецк, пр-кт Победы, 74" : "🅻 пр-кт Победы 74",
    "3 Транз Врн - Мск": "📦 Транз Врн ⬅️➡️ Мск",
    "Транзит 5 (Сер-Сер)": "📦 Транзит 5 (Сер-Сер)",
    "1 Транз Сар - Мск": "📦 Транз Сар ⬅️➡️ Мск",
    "Нераспределённый": "📦❓ Нераспределённый",
    "1 Транз Мск - Сар": "📦 Транз Мск ⬅️➡️ Сар",
    "Основной склад Москва": "🏬 Основной склад Москва",
    "Транзитные склады": "🏬 Транзитные склады",
    "2 Транз Мск - Лип": "📦 Транз Мск ⬅️➡️ Лип",
    "3 Транз Мск - Врн": "📦 Транз Мск ⬅️➡️ Врн",
    "4 Транз Сар - Бал": "📦 Транз Сар ⬅️➡️ Бал",
    "4 Транз Бал - Сар": "📦 Транз Бал ⬅️➡️ Сар"
}

# genpdf
questions = {
    'DocNumber': 'Введите номер договора:',
    'Date': None,
    'name': 'Введите ФИО и номер телефона КЛИЕНТА:',
    'model': 'Введите модель устройства:',
    'SN': 'Введите серийный номер:',
    'SellPrice': 'Введите цену выкупа:',
    'SellPriceFull': None,
    'PDS': 'Введите серию паспорта:',
    'PDN': 'Введите номер паспорта:',
    'PDW': 'Введите дату выдачи паспорта и орган, выдавший:',
    'PDA': 'Введите адрес проживания:',
    'WhoBuy': 'Менеджер, который принимает (Фамилия Инициалы):'
}
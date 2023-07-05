from telebot import types
import re

class PhonePrices:
    def __init__(self, sheet_url, client):
        # Initialize instance variables
        self.sheet_url = sheet_url
        self.client = client
        self.sheet_name = "Для заполнения iPhone"

        # Import data from Google Sheets
        self.data = self._import_data()

        # Get column indices for relevant fields
        self.model_index = self.headers.index("Модель")
        self.memory_index = self.headers.index("Память")
        self.price_index = self.headers.index("Идеальная цена")
        self.screen_index = self.headers.index("Замена экрана")
        self.battery_index = self.headers.index("Замена аккумулятора")
        self.device_only_index = self.headers.index("Только устройство")
        self.device_box_index = self.headers.index("устройство+коробка")
        self.back_cover_index = self.headers.index("Замена задней крышки")

        # Get models and their memory options
        self.models = self._get_models()

    def _import_data(self):
        # Open the Google Sheets document by URL
        sheet = self.client.open_by_url(self.sheet_url).worksheet(self.sheet_name)

        # Get all values from the sheet
        data = sheet.get_all_values()

        # Strip whitespace from headers
        self.headers = [header.strip() for header in data[0]]

        # Return the data
        return data

    def _get_models(self):
        models = {}
        # Loop through all data rows except for the header row
        for row in self.data[1:]:
            model = row[self.model_index]
            memory = row[self.memory_index]
            # If the model hasn't been added to the dictionary yet, add it with its first memory option
            models.setdefault(model, [memory])
            # Otherwise, add the memory option to the existing model's list of options
            if memory not in models[model]:
                models[model].append(memory)
        return models

    def get_memory_options(self, model):
        # Check if the model exists in the data
        if model not in self.models:
            raise ValueError(f"Модель '{model}' не найдена")

        # Return the list of memory options for the given model
        return self.models[model]

    def get_price(self, model, memory, options=None):
        # Loop through all data rows except for the header row
        for row in self.data[1:]:
            # Check if the row corresponds to the given model and memory
            if row[self.model_index] == model and row[self.memory_index] == memory:
                # Calculate the base price of the phone without any additional options
                price = float(row[self.price_index])
                if options is None:
                    return price

                # Calculate the total price of the phone with the additional options
                total_price = price
                option_indices = {
                    "Замена экрана": self.screen_index,
                    "Замена аккумулятора": self.battery_index,
                    "Только устройство": self.device_only_index,
                    "устройство+коробка": self.device_box_index,
                    "Замена задней крышки": self.back_cover_index
                }
                for option in options:
                    total_price += float(row[option_indices[option]])
                return total_price

        # If no matching row is found, return None
        return None
    
    def handle_tradein(self, bot, message):
        # send_debug_message(f"{message.from_user.id} запросил Трейдин")
        models = self.models.keys()
        model_buttons = types.InlineKeyboardMarkup(row_width=2)
        for model in models:
            button = types.InlineKeyboardButton(text=model, callback_data=f"model:{model}")
            model_buttons.add(button)
        bot.send_message(message.chat.id, "Выберите модель:", reply_markup=model_buttons)

    def handle_model_callback(self, bot, call):
        model = call.data.split(":")[1]
        memory_options = self.get_memory_options(model)
        if not memory_options:
            bot.send_message(call.message.chat.id, f"Для модели '{model}' не найдено вариантов памяти")
            return
        memory_buttons = types.InlineKeyboardMarkup(row_width=2)
        for memory in memory_options:
            button = types.InlineKeyboardButton(text=memory, callback_data=f"memory:{memory}")
            memory_buttons.add(button)
        bot.send_message(call.message.chat.id, f"Выберите память для модели '{model}':", reply_markup=memory_buttons)
        bot.answer_callback_query(callback_query_id=call.id)

    def handle_memory_callback(self, bot, call):
        model_pattern = r"'(.*?)'"
        model = re.search(model_pattern, call.message.text).group(1)
        memory = call.data.split(":")[1]
        options = []
        message = bot.send_message(call.message.chat.id, "Введите емкость аккумулятора (в процентах):")
        bot.register_next_step_handler(message, self.handle_battery_capacity, bot, model, memory, options)
        bot.answer_callback_query(callback_query_id=call.id)

    def handle_battery_capacity(self, message, bot, model, memory, options):
        try:
            battery_capacity = int(message.text)
            if battery_capacity < 85:
                options.append("Замена аккумулятора")
            message = bot.send_message(message.chat.id, "Только устройство? (да / нет):")
            bot.register_next_step_handler(message, self.handle_device_only, bot, model, memory, options)
        except ValueError:
            bot.send_message(message.chat.id, "Емкость аккумулятора должна быть числом. Пожалуйста, введите число:")

    def handle_device_only(self, message, bot, model, memory, options):
        if message.text.lower() == "да" or "lf":
            options.append("Только устройство")
        message = bot.send_message(message.chat.id, "Устройство+коробка? (да / нет):")
        bot.register_next_step_handler(message, self.handle_display, bot, model, memory, options)

    def handle_display(self,message, bot, model, memory, options):
        if message.text.lower() == "да" or "lf":
            options.append("устройство+коробка")
        message = bot.send_message(message.chat.id,"Замена экрана (да / нет):")
        bot.register_next_step_handler(message ,self.handle_device_box ,bot ,model ,memory ,options)

    def handle_device_box(self,message ,bot, model, memory, options):
        if message.text.lower() == "да" or "lf":
            options.append("Замена экрана")
        message = bot.send_message(message.chat.id,"Замена задней крышки? (да / нет):")
        bot.register_next_step_handler(message ,self.handle_back_cover ,bot ,model,memory,options)

    def handle_back_cover(self,message,bot, model, memory, options):
        if message.text.lower() == "да" or "lf":
            options.append("Замена задней крышки")
        total_price = self.get_price(model,memory,options)
        response = f"* Модель: {model}, Память: {memory}\n"
        response += f"* Цена в Трейдин: до {total_price:.0f} рублей\n"
        response += f"*На что повлияла цена:\n {options}\n*Если состояние неудовлетворительное,\nто уточни у сервисных менеджеров"
        bot.send_message(message.chat.id,response)
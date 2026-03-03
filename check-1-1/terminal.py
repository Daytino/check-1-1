import order as order_class
import pizza as pizza_class

BOLD = '\033[1m'
RESET = '\033[0m'

ORDERS = []

class Terminal:
    def __init__(self):
        self.order = None
        self.MAX_CMD_ID = 5

        self.ERROR_MESSAGES = {
            "VALUE_ERROR": "Вы ввели неверные данные",
            "NOT_ENOUGH_VALUES": "В vы ввели неполные данные"
            }
        self.GREETING_MESSAGE = "Cписок команд:\n" \
                                "1. Сделать заказ\n" \
                                "2. Узнать статус заказа\n" \
                                "3. Закрыть терминал\n" \
                                "4. Вывести это сообщение"       
        self.START_ORDER_MESSAGE = ""
        self.ORDER_STATUS_CHECK_MESSAGE = ""

    def do_order_greeting(self, do_make_order_instance : bool = False) -> None:
        if do_make_order_instance:
            self.order = order_class.Order()

        print("Доступные виды пиццы:")

        pizza_types = pizza_class.get_pizza_types()
        self.order.display_pizza_properties_and_get_cost_total(pizza_types)
        print("Выберите пиццу, введя её номер (указан возле названия).")
        
        user_choice = self.request_and_check_user_input(1, len(pizza_class.get_pizza_types()))

        self.make_order(pizza_types[int(user_choice) - 1])

    def make_order(self, pizza_type = None) -> None:
        chosen_pizza = pizza_type

        print(f'Вы выбрали пиццу "{chosen_pizza.name}". Выберите размер:')
        print("1. 25 см - Маленькая (на 30% дешевле стандартной)\n" \
              "2. 30 см - Стандартная\n" \
              "3. 35 см - Большая (на 36% дороже стандартной)")
            
        user_choice = self.request_and_check_user_input(1, 3)
        
        chosen_pizza.change_diameter(int(user_choice))

        print(f"Размер пиццы: {chosen_pizza.change_diameter(int(user_choice))} см")
        
        print(f'Выберите тип теста:')
        print("1. Тонкое (на 5% дешевле стандартного)\n" \
              "2. Стандартное")

        user_choice = self.request_and_check_user_input(1, 2)
        
        chosen_pizza.change_dough_thickness(int(user_choice))
        print(f"Выбрано {chosen_pizza.change_dough_thickness(int(user_choice)).lower()} тесто")
        print("Пицца добавлена в заказ. Список доступных команд:\n" \
             "1. Добавить выбранную пиццу в заказ\n" \
             "2. Отменить добавление пиццы")
        
        user_choice = self.request_and_check_user_input(1, 2)
        
        if int(user_choice) == 1:
            self.order.add_object_to_content(chosen_pizza)
            print("Пицца добавлена в заказ")
        else:
            print("Добавление пиццы отменено")
        
        self.approve_order()
    
    def approve_order(self) -> None:
        is_first_pizza = len(self.order.content) == 0
        if not is_first_pizza:
            self.order.display_content()
            print("Вы хотите продолжить пополнение заказа?\n" \
                "1. Да, хочу\n" \
                "2. Нет, я готов сделать заказ и оплатить его\n" \
                "3. Я отменяю заказ")
            
            user_choice = self.request_and_check_user_input(1, 3)
        else:
            print("Вы хотите продолжить пополнение заказа?\n" \
                "1. Да, хочу\n" \
                "2. Нет, не хочу")
            
            user_choice = self.request_and_check_user_input(1, 2)

        if int(user_choice) == 1:
            self.do_order_greeting()
        elif int(user_choice) == 2:
            if not is_first_pizza:
                self.order_new = order_class.Order(self.order.content.copy())
                self.order_new.add_order()
                self.order_new.display_content(True)
                self.order.clear_content()
            else:
                pass
        else:
            print("Вы уверены, что хотите отменить заказ? y/n")
            while True:
                user_input = input()
                if self.is_user_input_valid(user_input, 3):
                    break
            
            if user_input.lower() == "y":
                self.order.clear_content()
            else:
                self.approve_order()

    def do_order_status_check(self) -> None:
        print("Введите номер заказа:")
        user_choice = self.request_and_check_user_input(1, 10*10)
        order_class.display_order_status(int(user_choice))
    
    def exit_terminal(self) -> None:
        print("Вы уверены, что хотите выйти? y/n")

        while True:
            user_input = input()
            if user_input == "q":
                return
            elif self.is_user_input_valid(user_input, 3):
                break
        
        if user_input.lower() == "y":
            print(f"До свидания!")
            exit(0)

    def activate_function_by_cmd_id(self, cmd_id : int) -> None:
        if cmd_id == 1:
            self.do_order_greeting(True)
        elif cmd_id == 2:
            self.do_order_status_check()
        elif cmd_id == 3:
            self.exit_terminal()
        else:
            print(self.GREETING_MESSAGE)

    def is_user_input_valid(self, user_input : str, cmd_id : int) -> bool:
        if cmd_id == 0:
            try:
                int(user_input)
            except ValueError:
                print(self.ERROR_MESSAGES["VALUE_ERROR"])
            else:
                if not 1 <= int(user_input) <= self.MAX_CMD_ID:
                    print(self.ERROR_MESSAGES["VALUE_ERROR"])
                else:
                    return True
        elif cmd_id == 3:
            if user_input.lower() in "yn":
                return True

            print('Введите y [yes] или n [no]')
        
        return False

    def request_and_check_user_input(self, start_value : int, end_value : int) -> str:
        def range_check(self, user_input : str, start_value : int, end_value : int) -> bool:
            try:
                int(user_input)
            except ValueError:
                print(self.ERROR_MESSAGES["VALUE_ERROR"])
            else:
                if not start_value <= int(user_input) <= end_value:
                    print(self.ERROR_MESSAGES["VALUE_ERROR"])
                else:
                    return True
            
            return False
        user_input = input()
        while not range_check(self, user_input, start_value, end_value):
            user_input = input()
        
        return user_input
        
    def interface(self, showMessage : bool = False) -> None:
        if showMessage:
            print(self.GREETING_MESSAGE)

        user_input = input()
        while not self.is_user_input_valid(user_input, 0):
            user_input = input()

        cmd_id = int(user_input)
        self.activate_function_by_cmd_id(cmd_id)
        print("--------------------")
        self.interface()


terminal = Terminal()
terminal.interface(True)
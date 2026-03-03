from inflector import inflect_with_num

# --Константы--
# Словарь указывает на свойства размеров
# Формат: {Размер: (диаметр (см), множитель цены)}
PIZZA_SIZE_PROPERTIES = {"Маленькая": (25, 0.7),
                        "Стандартная": (30, 1), 
                        "Большая": (35, 1.36)}

DOUGH_THICKNESS_PROPERTIES = {"Тонкое": 0.95,
                              "Стандартное": 1}

COST_SAUCES = {"Томатный": 80, 
               "Сливочный": 160, 
               "Барбекю": 140}

COST_INGREDIENTS = {"Томаты": 50, 
                    "Острый_перец": 70,
                    "Моцарелла": 200,
                    "Пармезан": 200,
                    "Колбаса": 150, 
                    "Ветчина": 150, 
                    "Лосось": 250, 
                    "Креветки": 300,
                    "Орегано": 10,
                    "Розмарин": 10}

STATUS_MESSAGES = {0: "Пицца проходит сборку",
                   1: "Пицца в печи",
                   2: "Пицца упакована",
                   3: "Пицца в пути",
                   4: "Пицца доставлена",
                   5: "Пицца лежит на столе. Забирайте!"}


class Pizza:
    def __init__(self, 
                 name : str = "Pizza", 
                 dough_thickness : str = "Стандартное",
                 diameter: int = PIZZA_SIZE_PROPERTIES["Стандартная"][0],
                 cost_multiplier : float = PIZZA_SIZE_PROPERTIES["Стандартная"][1] * DOUGH_THICKNESS_PROPERTIES["Стандартное"],
                 sauce : str = "Томатный",
                 ingredients : tuple[str] = ["Моцарелла"]):
        self.name = name
        self.dough_thickness = dough_thickness
        self.diameter = diameter
        self.cost_multiplier = cost_multiplier
        self.sauce = sauce
        self.ingredients = ingredients
        self.status = 0
        self.status_metadata = {self.do_collect: 0,
                                self.do_cook: 1,
                                self.do_pack: 2,
                                self.do_send: 3,
                                self.do_deliver: 4,
                                self.do_notify: 5}

    def get_status_check(self, func) -> bool:        
        if self.status == None:
            return True
        if self.status >= self.status_metadata[func]:
            return False
        else:
            return True
        
    def do_collect(self) -> None:
        if self.get_status_check(self.do_collect):
            print("Пицца собрана")
            self.status = self.status_metadata[self.do_collect]
        else:
            print("Пицца уже собрана")

    def do_cook(self, minutes : int = 15) -> None:
        if self.get_status_check(self.do_cook):
            if self.status != self.status_metadata[self.do_collect]:
                print("Сначала соберите пиццу")
                return None
            print(f"Пицца будет готовиться в течение {minutes} {inflect_with_num(minutes, ('минут', 'минуты'))}")
            self.status = self.status_metadata[self.do_cook]
        else:
            if self.status == self.status_metadata[self.do_cook]:
                print("Пицца уже готовится")
            else:
                print("Пицца уже готова")
    
    def do_pack(self) -> None:
        if self.get_status_check(self.do_pack):
            if self.status != self.status_metadata[self.do_cook]:
                print("Сначала приготовьте пиццу")
                return None
            print(f"Пицца упакована")
            self.status = self.status_metadata[self.do_pack]
        else:
            print("Пицца уже упакована")

    def do_send(self) -> None:
        if self.get_status_check(self.do_send):
            if self.status != self.status_metadata[self.do_pack]:
                print("Сначала упакуйте пиццу")
                return None
            self.status = self.status_metadata[self.do_send]
            print(f"Пицца отправлена в путь")
        else:
            print(f"Пицца уже отправлена")
    
    def do_deliver(self) -> None:
        if self.get_status_check(self.do_deliver):
            if self.status != self.status_metadata[self.do_send]:
                print("Пицца ещё не отправлена")
                return None
            self.status = self.status_metadata[self.do_deliver]
            print(f"Пицца доставлена")
        else:
            print(f"Пицца уже доставлена")
    
    def do_notify(self) -> None:
        if self.get_status_check(self.do_notify):
            if self.status != self.status_metadata[self.do_pack]:
                print("Пицца ещё не готова")
                return None
            self.status = self.status_metadata[self.do_notify]
            print(f"Пицца готова")
        else:
            print(f"Пицца готова")
    
    def change_diameter(self, index : int) -> int:
        self.cost_multiplier /= list(filter(lambda x: x[0] == self.diameter, [i for i in PIZZA_SIZE_PROPERTIES.values()]))[0][1]
        self.diameter = PIZZA_SIZE_PROPERTIES[list(PIZZA_SIZE_PROPERTIES.keys())[index - 1]][0]
        self.cost_multiplier *= PIZZA_SIZE_PROPERTIES[list(PIZZA_SIZE_PROPERTIES.keys())[index - 1]][1]
        return self.diameter

    def change_dough_thickness(self, index : int) -> str:
        self.cost_multiplier /= DOUGH_THICKNESS_PROPERTIES[self.dough_thickness]
        self.dough_thickness = list(DOUGH_THICKNESS_PROPERTIES.keys())[index - 1]
        self.cost_multiplier *= DOUGH_THICKNESS_PROPERTIES[self.dough_thickness]
        return list(DOUGH_THICKNESS_PROPERTIES.keys())[index - 1]

    def get_status(self) -> str:
        return STATUS_MESSAGES[self.status]
    
    def get_cost(self) -> int:
        cost_total = 0
        cost_total += COST_SAUCES[self.sauce]
        for ingredient in self.ingredients:
            cost_total += COST_INGREDIENTS[ingredient]
        cost_total *= self.cost_multiplier
        return int(cost_total)

    def __add__(self, other : object):
        return Pizza(ingredients=tuple(set(self.ingredients) | set(other.ingredients)))

    def __sub__(self, other):
        return Pizza(ingredients=tuple(set(self.ingredients) - set(other.ingredients)))
        
    

class BBQ(Pizza):
    def __init__(self, 
                 name : str = "Барбекю", 
                 dough_thickness : str = "Стандартное",
                 diameter: int = PIZZA_SIZE_PROPERTIES["Стандартная"][0],
                 cost_multiplier : float = PIZZA_SIZE_PROPERTIES["Стандартная"][1] * DOUGH_THICKNESS_PROPERTIES["Стандартное"]):
        super().__init__(name, 
                         dough_thickness,
                         diameter, 
                         cost_multiplier, 
                         "Барбекю", 
                         ("Моцарелла", "Колбаса", "Ветчина", "Острый_перец"))


class Seagifts(Pizza):
    def __init__(self, 
                 name : str = "Дары моря", 
                 dough_thickness : str = "Стандартное",                 
                 diameter : int = PIZZA_SIZE_PROPERTIES["Стандартная"][0], 
                 cost_multiplier : float = PIZZA_SIZE_PROPERTIES["Стандартная"][1] * DOUGH_THICKNESS_PROPERTIES["Стандартное"]):
        super().__init__(name, 
                         dough_thickness,
                         diameter, 
                         cost_multiplier, 
                         "Сливочный", 
                         ("Моцарелла", "Креветки", "Розмарин"))


class Pepperoni(Pizza):
    def __init__(self, 
                 name : str = "Пепперони", 
                 dough_thickness : str = "Стандартное",
                 diameter : int = PIZZA_SIZE_PROPERTIES["Стандартная"][0], 
                 cost_multiplier : float = PIZZA_SIZE_PROPERTIES["Стандартная"][1] * DOUGH_THICKNESS_PROPERTIES["Стандартное"]):
        super().__init__(name, 
                         dough_thickness,
                         diameter, 
                         cost_multiplier, 
                         "Томатный", 
                         ("Моцарелла", "Колбаса", "Острый_перец"))


def get_pizza_types() -> list:
    return [Pepperoni(), BBQ(), Seagifts()]

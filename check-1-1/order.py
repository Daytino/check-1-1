from pizza import Pizza

ORDERS = {0: object}
BOLD = '\033[1m'
RESET = '\033[0m'

class Order:
    def __init__(self, content : list[object] = []):
        self.id = max(list(ORDERS.keys())) + 1
        self.content = content
    
    def add_object_to_content(self, object) -> None:
        self.content.append(object)
    
    def delete_object_from_content(self, object) -> None:
        self.content.remove(object)

    def clear_content(self) -> None:
        self.content.clear()
    
    def add_order(self) -> None:
        ORDERS[self.id] = self

    def display_pizza_properties_and_get_cost_total(self, pizza_list : list[object]) -> int:
        cost_total = 0
        for i, pizza in enumerate(pizza_list):
            cost_pizza = pizza.get_cost()
            print(f"{i + 1}. Тип пиццы: {pizza.name}\n"
                  f"Диаметр: {pizza.diameter} см\n"
                  f"Тип теста: {pizza.dough_thickness.lower()}\n"
                  f"Соус: {pizza.sauce.lower()}\n"
                  f"Ингредиенты: {', '.join([i.lower() for i in pizza.ingredients])}\n"
                  f"Цена: {cost_pizza}\n"
                  f"{'-' * 35}")
            cost_total += pizza.get_cost()
        
        return cost_total
    
    def display_content(self, is_complete : bool = False) -> None:
        print("Заказ состоит из: ")
        self.display_pizza_properties_and_get_cost_total(self.content)
        cost_total = self.display_pizza_properties_and_get_cost_total(self.content)
        print(f"Цена заказа: {cost_total}")
        if is_complete:
            print(f"Номер заказа: {BOLD}{self.id}{RESET}")


def display_order_status(order_id : int) -> None:
    if not order_id in ORDERS.keys():
        print("Такого заказа нет")
        return
    order_object : object = ORDERS[order_id]
    order_object.display_content(True)
    

def delete_order(id : int) -> None:
    ORDERS.remove(id)


def get_orders() -> list[int]:
    return ORDERS

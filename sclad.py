import tkinter as tk
from tkinter import messagebox
# Класс для представления товара
class Product:
    def __init__(self, name: str, quantity: int, price: float):
        self.name = name
        self.quantity = quantity
        self.price = price

    def update_quantity(self, amount: int):
        """Обновляет количество товара"""
        if self.quantity + amount < 0:
            raise ValueError("Недостаточное количество товара на складе.")
        self.quantity += amount

    def __str__(self):
        return f"{self.name}, Количество: {self.quantity}, Цена: {self.price} руб."
# Класс для управления складом
class Warehouse:
    def __init__(self):
        self.products = []

    def add_product(self, name: str, quantity: int, price: float):
        """Добавляет новый товар на склад"""
        if any(product.name == name for product in self.products):
            raise ValueError(f"Товар '{name}' уже существует на складе.")
        self.products.append(Product(name, quantity, price))

    def list_products(self):
        """Возвращает список товаров на складе"""
        return "\n".join(str(product) for product in self.products)

    def remove_product(self, name: str):
        """Удаляет товар со склада по имени"""
        for product in self.products:
            if product.name == name:
                self.products.remove(product)
                return f"Товар '{name}' удален."
        raise ValueError(f"Товар '{name}' не найден.")

    def update_product_quantity(self, name: str, amount: int):
        """Обновляет количество товара"""
        for product in self.products:
            if product.name == name:
                product.update_quantity(amount)
                return f"Количество товара '{name}' обновлено."
        raise ValueError(f"Товар '{name}' не найден.")

    def total_inventory_value(self):
        """Возвращает общую стоимость товаров на складе"""
        return sum(product.price * product.quantity for product in self.products)
# Графический интерфейс
class WarehouseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Управление складом")
        self.warehouse = Warehouse()

        # Поля для ввода данных
        self.name_label = tk.Label(master, text="Название товара:")
        self.name_label.pack()
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        self.quantity_label = tk.Label(master, text="Количество:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.pack()

        self.price_label = tk.Label(master, text="Цена:")
        self.price_label.pack()
        self.price_entry = tk.Entry(master)
        self.price_entry.pack()

        # Кнопка для добавления товара
        self.add_button = tk.Button(master, text="Добавить товар", command=self.add_product)
        self.add_button.pack()

        # Кнопка для отображения товаров
        self.list_button = tk.Button(master, text="Показать товары", command=self.show_products)
        self.list_button.pack()

        # Кнопка для удаления товара
        self.remove_button = tk.Button(master, text="Удалить товар", command=self.remove_product)
        self.remove_button.pack()

        # Кнопка для обновления количества товара
        self.update_button = tk.Button(master, text="Обновить количество", command=self.update_product)
        self.update_button.pack()

        # Текстовое поле для отображения списка товаров
        self.product_display = tk.Text(master, height=10, width=50)
        self.product_display.pack()

    def add_product(self):
        """Добавляет товар на склад через GUI"""
        try:
            name = self.name_entry.get().strip()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            if not name or quantity <= 0 or price <= 0:
                raise ValueError("Некорректные данные.")
            self.warehouse.add_product(name, quantity, price)
            messagebox.showinfo("Информация", "Товар успешно добавлен.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.clear_entries()

    def show_products(self):
        """Отображает все товары на складе через GUI"""
        products = self.warehouse.list_products()
        self.product_display.delete(1.0, tk.END)
        self.product_display.insert(tk.END, products if products else "Нет товаров на складе.")

    def remove_product(self):
        """Удаляет товар со склада через GUI"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название товара.")
            return
        try:
            result = self.warehouse.remove_product(name)
            messagebox.showinfo("Информация", result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.clear_entries()

    def update_product(self):
        """Обновляет количество товара на складе через GUI"""
        name = self.name_entry.get().strip()
        try:
            amount = int(self.quantity_entry.get())
            if not name or amount == 0:
                raise ValueError("Некорректные данные.")
            result = self.warehouse.update_product_quantity(name, amount)
            messagebox.showinfo("Информация", result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.clear_entries()

    def clear_entries(self):
        """Очищает поля ввода"""
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

# Главная функция для запуска приложения
def main():
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

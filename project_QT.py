import csv
import datetime
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QTableWidget, QDialog, QMainWindow, QTableWidgetItem, QWidget, \
    QComboBox, QMessageBox, QFileDialog, QLabel, QHeaderView, QAbstractItemView

rows_list_warehouse = []
rows_list_customers = []
number_actions_warehouse = []
number_actions_customers = []


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project_Qt.ui', self)
        app.setWindowIcon(QIcon('business.ico'))
        self.con = sqlite3.connect('project_db.sqlite')
        self.cur = self.con.cursor()
        self.pixmap = QPixmap("Покупка.jpeg")
        self.label.setPixmap(self.pixmap)
        self.pixmap_2 = QPixmap("Продажа.jpeg")
        self.label_2.setPixmap(self.pixmap_2)

        self.message_buy = QMessageBox()
        self.message_sell = QMessageBox()
        self.message_error_not_int = QMessageBox()
        self.message_error_null = QMessageBox()
        self.message_error_product_null = QMessageBox()
        self.message_error_more_warehouse = QMessageBox()
        self.message_error_not_delete = QMessageBox()
        self.message_error_import_warehouse = QMessageBox()
        self.message_error = QMessageBox()
        self.message_delete_warehouse = QMessageBox()
        self.message_delete_customers = QMessageBox()
        self.message_success = QMessageBox()
        self.message_success_import = QMessageBox()
        self.message_success_export = QMessageBox()

        self.window_warehouse()
        self.window_customers()
        self.window_sell_product()
        self.window_sell_buy()
        self.window_buy_product()
        self.button()
        self.message()

    def message(self):
        self.message_success.setIcon(QMessageBox.Information)
        self.message_success.setWindowTitle("Успешно")
        self.message_success.setText("Вы удалили строку.")
        self.message_success_import.setIcon(QMessageBox.Information)
        self.message_success_import.setWindowTitle("Успешно")
        self.message_success_import.setText("Вы импортировали данные в таблицу.")
        self.message_success_export.setIcon(QMessageBox.Information)
        self.message_success_export.setWindowTitle("Успешно")
        self.message_success_export.setText("Вы экспортировали данные.")
        self.message_error_not_delete.setIcon(QMessageBox.Warning)
        self.message_error_not_delete.setWindowTitle("Ошибка")
        self.message_error_not_delete.setText("Невозможно удалить выбранную строку, выберите другую.")
        self.message_error_import_warehouse.setIcon(QMessageBox.Warning)
        self.message_error_import_warehouse.setWindowTitle("Ошибка")
        self.message_error_import_warehouse.setText("Импорт не был произведен.")
        self.message_delete_customers.setIcon(QMessageBox.Information)
        self.message_delete_customers.setWindowTitle("Подтвердите действие")
        self.message_delete_customers.setText("Вы действительно хотите удалить строку?")
        self.message_delete_customers.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.message_delete_warehouse.setIcon(QMessageBox.Information)
        self.message_delete_warehouse.setWindowTitle("Подтвердите действие")
        self.message_delete_warehouse.setText("Вы действительно хотите удалить строку?")
        self.message_delete_warehouse.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.message_error_not_int.setIcon(QMessageBox.Warning)
        self.message_error_not_int.setWindowTitle("Ошибка")
        self.message_error_not_int.setText("Введите целое, неотрицательное количество товара.")
        self.message_error_null.setIcon(QMessageBox.Warning)
        self.message_error_null.setWindowTitle("Ошибка")
        self.message_error_null.setText("Введите значение больше 0.")
        self.message_error_product_null.setIcon(QMessageBox.Warning)
        self.message_error_product_null.setWindowTitle("Ошибка")
        self.message_error_product_null.setText("На складе этот товар закончился. Приобрите его, прежде чем продавать.")
        self.message_error_more_warehouse.setIcon(QMessageBox.Warning)
        self.message_error_more_warehouse.setWindowTitle("Ошибка")
        self.message_error_more_warehouse.setText("Выбранное вами количество товара отсутствует на складе.")
        self.message_sell.setIcon(QMessageBox.Information)
        self.message_sell.setWindowTitle("Выполненно")
        self.message_sell.setText("Вы успешно продали товар.")
        self.message_buy.setIcon(QMessageBox.Information)
        self.message_buy.setWindowTitle("Выполненно")
        self.message_buy.setText("Вы успешно купили товар.")
        self.message_error.setIcon(QMessageBox.Warning)
        self.message_error.setWindowTitle("Ошибка")
        self.message_error.setText("Вы не выбрали строку.")

    def button(self):
        self.customers_table.clicked.connect(self.clicked_customers_table)
        self.warehouse_table.clicked.connect(self.clicked_warehouse_table)
        self.button_buy.clicked.connect(self.func_buy)
        self.button_sell.clicked.connect(self.func_sell)
        self.button_editing_warehouse.clicked.connect(self.button_clicked_row_warehouse)
        self.button_add_warehouse.clicked.connect(self.button_clicked_row_warehouse)
        self.button_editing_customers.clicked.connect(self.button_clicked_row_customers)
        self.button_add_customers.clicked.connect(self.button_clicked_row_customers)
        self.button_delete_customers.clicked.connect(self.button_clicked_delete_customers)
        self.button_delete_warehouse.clicked.connect(self.button_clicked_delete_warehouse)
        self.message_delete_warehouse.accepted.connect(self.row_warehouse)
        self.button_export_warehouse.clicked.connect(self.button_export)
        self.button_import_warehouse.clicked.connect(self.button_import)
        self.button_export_customers.clicked.connect(self.button_export)
        self.button_import_customers.clicked.connect(self.button_import)
        self.button_export_product_sell.clicked.connect(self.button_export)
        self.button_export_product_buy.clicked.connect(self.button_export)
        self.message_delete_customers.accepted.connect(self.row_customers)

    def window_warehouse(self):
        goods_info = self.cur.execute(
            """SELECT * FROM warehouse""").fetchall()
        self.warehouse_table.setColumnCount(5)
        self.warehouse_table.setRowCount(len(goods_info))
        self.warehouse_table.setHorizontalHeaderLabels(
            ['ID Товара', 'Наименование', 'Количество на складе', 'Цена закупки', 'Цена продажи'])
        for i, j in zip(goods_info, range(0, len(goods_info))):
            self.warehouse_table.setItem(j, 0, QTableWidgetItem(str(i[0])))
            self.warehouse_table.setItem(j, 1, QTableWidgetItem(str(i[1])))
            self.warehouse_table.setItem(j, 2, QTableWidgetItem(str(i[2])))
            self.warehouse_table.setItem(j, 3, QTableWidgetItem(str(i[3])))
            self.warehouse_table.setItem(j, 4, QTableWidgetItem(str(i[4])))
        self.warehouse_table.resizeColumnsToContents()
        self.warehouse_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.warehouse_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def window_customers(self):
        customers_info = self.cur.execute(
            """SELECT * FROM customers""").fetchall()
        self.customers_table.setColumnCount(6)
        self.customers_table.setRowCount(len(customers_info))
        self.customers_table.setHorizontalHeaderLabels(
            ['ID Клиента', 'Имя', 'Фамилия', 'Отчество', 'Выручка с клиента', 'Чистая Прибыль с клиента'])
        for i, j in zip(customers_info, range(0, len(customers_info))):
            self.customers_table.setItem(j, 0, QTableWidgetItem(str(i[0])))
            self.customers_table.setItem(j, 1, QTableWidgetItem(str(i[1])))
            self.customers_table.setItem(j, 2, QTableWidgetItem(str(i[2])))
            self.customers_table.setItem(j, 3, QTableWidgetItem(str(i[3])))
            self.customers_table.setItem(j, 4, QTableWidgetItem(str(i[4])))
            self.customers_table.setItem(j, 5, QTableWidgetItem(str(i[5])))
        self.customers_table.resizeColumnsToContents()
        self.customers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.customers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def window_sell_product(self):
        sell_product_info = self.cur.execute(
            """SELECT product.id_purchase, warehouse.product_name, product.price_sell, 
            product.count_product, product.date_sell, product.sum  
            FROM product
            INNER JOIN warehouse
                ON product.id_product = warehouse.id_product;""").fetchall()
        sell_customer_info = self.cur.execute(
            """SELECT customers.name, customers.last_name, customers.patronymic
            FROM product
            INNER JOIN customers
                ON product.id_customers = customers.id_customers;""").fetchall()
        self.sell_product_table.setColumnCount(7)
        self.sell_product_table.setRowCount(len(sell_product_info))
        self.sell_product_table.setHorizontalHeaderLabels(
            ['ID Продажи', 'Клиент', 'Наименование товара', 'Цена Продажи', 'Количество', 'Дата', 'Сумма'])
        for i, j in zip(sell_product_info, range(0, len(sell_product_info))):
            self.sell_product_table.setItem(j, 0, QTableWidgetItem(str(i[0])))
            self.sell_product_table.setItem(j, 1, QTableWidgetItem(str(sell_customer_info[j][0] + " " +
                                                                       sell_customer_info[j][1] + " " +
                                                                       sell_customer_info[j][2])))
            self.sell_product_table.setItem(j, 2, QTableWidgetItem(str(i[1])))
            self.sell_product_table.setItem(j, 3, QTableWidgetItem(str(i[2])))
            self.sell_product_table.setItem(j, 4, QTableWidgetItem(str(i[3])))
            self.sell_product_table.setItem(j, 5, QTableWidgetItem(str(i[4])))
            self.sell_product_table.setItem(j, 6, QTableWidgetItem(str(i[5])))
        self.sell_product_table.resizeColumnsToContents()
        self.sell_product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.sell_product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def window_buy_product(self):
        buy_product_info = self.cur.execute(
            """SELECT product_buy.id_purchase_buy, warehouse.product_name, product_buy.price_product_buy, 
            product_buy.amount_buy, product_buy.date_buy, product_buy.sum_buy
            FROM product_buy
            INNER JOIN warehouse
                ON product_buy.id_product = warehouse.id_product;""").fetchall()
        self.buy_product_table.setColumnCount(6)
        self.buy_product_table.setRowCount(len(buy_product_info))
        self.buy_product_table.setHorizontalHeaderLabels(
            ['ID Покупки', 'Наименование товара', 'Цена закупки', 'Количество', 'Дата', 'Сумма'])
        for i, j in zip(buy_product_info, range(0, len(buy_product_info))):
            self.buy_product_table.setItem(j, 0, QTableWidgetItem(str(i[0])))
            self.buy_product_table.setItem(j, 1, QTableWidgetItem(str(i[1])))
            self.buy_product_table.setItem(j, 2, QTableWidgetItem(str(i[2])))
            self.buy_product_table.setItem(j, 3, QTableWidgetItem(str(i[3])))
            self.buy_product_table.setItem(j, 4, QTableWidgetItem(str(i[4])))
            self.buy_product_table.setItem(j, 5, QTableWidgetItem(str(i[5])))
        self.buy_product_table.resizeColumnsToContents()
        self.buy_product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.buy_product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def window_sell_buy(self):
        product = self.cur.execute(
            """SELECT product_name FROM warehouse""").fetchall()
        customers = self.cur.execute(
            """SELECT name, last_name, patronymic FROM customers""").fetchall()
        for i in range(len(product)):
            self.product_buy.addItem(product[i][0])
            self.product_sell.addItem(product[i][0])
        for i in range(len(customers)):
            self.customers_sell.addItem(customers[i][0] + " " + customers[i][1] + " " + customers[i][2])

    def func_buy(self):
        name = str(self.product_buy.currentText())
        count = self.count_product_buy.text()
        if not count.isdecimal():
            self.message_error_not_int.exec()
        elif int(count) <= 0:
            self.message_error_null.exec()
        else:
            count = int(count)
            product_name_buy_id = self.cur.execute(
                f"""SELECT id_product FROM warehouse
                WHERE product_name = '{name}'""").fetchall()
            amount = self.cur.execute(
                f"""SELECT amount FROM warehouse
                WHERE product_name = '{name}'""").fetchall()
            purchase_price = self.cur.execute(
                f"""SELECT purchase_price FROM warehouse
                WHERE product_name = '{name}'""").fetchall()
            self.cur.execute(
                f"""UPDATE warehouse SET amount = {int(amount[0][0]) + count}
                WHERE product_name = '{name}'""")
            self.cur.execute(
                f"""INSERT INTO product_buy (id_product, price_product_buy, amount_buy, 
                date_buy, sum_buy)
                VALUES ( {int(product_name_buy_id[0][0])}, {float(purchase_price[0][0])}, {count},
                '{datetime.datetime.now().date()}', {round(count * float(purchase_price[0][0]), 2)});""")
            self.con.commit()
            self.buy_product_table.setColumnCount(0)
            self.buy_product_table.setRowCount(0)
            self.warehouse_table.setColumnCount(0)
            self.warehouse_table.setRowCount(0)
            self.window_warehouse()
            self.window_buy_product()
            self.message_buy.exec()

    def func_sell(self):
        customer_name = self.customers_sell.currentText().split()
        product_name = str(self.product_sell.currentText())
        count_product = self.count_product_sell.text()
        if not count_product.isdecimal():
            self.message_error_not_int.exec()
        elif int(count_product) <= 0:
            self.message_error_null.exec()
        else:
            count_product = int(count_product)
            customer_name_id = self.cur.execute(
                f"""SELECT id_customers FROM customers
                WHERE name = '{str(customer_name[0])}'""").fetchall()
            product_name_id = self.cur.execute(
                f"""SELECT id_product FROM warehouse
                WHERE product_name = '{product_name}'""").fetchall()
            amount_product = self.cur.execute(
                f"""SELECT amount FROM warehouse
                WHERE product_name = '{product_name}'""").fetchall()
            if int(amount_product[0][0]) == 0:
                self.message_error_product_null.exec()
            elif count_product > int(amount_product[0][0]):
                self.message_error_more_warehouse.exec()
            else:
                price_buy_product = self.cur.execute(
                    f"""SELECT purchase_price FROM warehouse
                    WHERE product_name = '{product_name}'""").fetchall()
                price_sell_product = self.cur.execute(
                    f"""SELECT selling_price FROM warehouse
                    WHERE product_name = '{product_name}'""").fetchall()
                profit = self.cur.execute(
                    f"""SELECT profit FROM customers
                    WHERE name = '{str(customer_name[0])}'""").fetchall()
                proceeds = self.cur.execute(
                    f"""SELECT proceeds FROM customers
                    WHERE name = '{str(customer_name[0])}'""").fetchall()
                difference = (float(price_sell_product[0][0]) - float(price_buy_product[0][0])) * count_product + float(
                    profit[0][0])
                summa = round(float(price_sell_product[0][0]) * count_product, 2)
                self.cur.execute(
                    f"""UPDATE warehouse SET amount = {int(int(amount_product[0][0]) - count_product)}
                    WHERE product_name = '{product_name}'""")
                self.cur.execute(
                    f"""UPDATE customers SET proceeds = {round(summa + float(proceeds[0][0]), 2)}
                    WHERE name = '{str(customer_name[0])}'""")
                self.cur.execute(
                    f"""UPDATE customers SET profit = {round(difference, 2)}
                    WHERE name = '{str(customer_name[0])}'""")
                self.cur.execute(
                    f"""INSERT INTO product (id_customers, id_product, price_sell, count_product, 
                    date_sell, sum)
                    VALUES ({int(customer_name_id[0][0])}, '{int(product_name_id[0][0])}', 
                    {float(price_sell_product[0][0])},{count_product},'{datetime.datetime.now().date()}', {summa});""")
                self.con.commit()
                self.warehouse_table.setColumnCount(0)
                self.warehouse_table.setRowCount(0)
                self.sell_product_table.setColumnCount(0)
                self.sell_product_table.setRowCount(0)
                self.customers_table.setColumnCount(0)
                self.customers_table.setRowCount(0)
                self.window_customers()
                self.window_sell_product()
                self.window_warehouse()
                self.message_sell.exec()

    def button_import(self):
        if self.sender().text() == "Импорт товаров из CSV":
            x = 0
            file_name_warehouse = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "CSV Files(*.csv)")
            if file_name_warehouse[0] == '':
                pass
            else:
                with open(f'{file_name_warehouse[0]}', 'r') as f:
                    dr = csv.DictReader(f, delimiter=";")
                    try:
                        data_to_db = [(i['id_product'], i['product_name'], i['amount'], i['purchase_price'],
                                       i['selling_price']) for i in dr]
                    except KeyError:
                        x = -1
                    if x != -1:
                        for i in range(len(data_to_db)):
                            try:
                                self.cur.execute(
                                    f"""INSERT INTO warehouse (id_product, product_name, amount,
                                    purchase_price, selling_price)
                                    VALUES ({data_to_db[i][0]}, '{data_to_db[i][1]}', {data_to_db[i][2]}, 
                                    {data_to_db[i][3]}, {data_to_db[i][4]});""")
                                self.con.commit()
                            except sqlite3.Error:
                                x += 1
                                continue
                        if x == len(data_to_db):
                            self.message_error_import_warehouse.exec()
                        else:
                            self.product_buy.clear()
                            self.product_sell.clear()
                            self.customers_sell.clear()
                            self.window_sell_buy()
                            self.warehouse_table.setColumnCount(0)
                            self.warehouse_table.setRowCount(0)
                            self.window_warehouse()
                            self.message_success_import.exec()
                    else:
                        self.message_error_import_warehouse.exec()
        else:
            x = 0
            file_name_customers = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "CSV Files(*.csv)")
            if file_name_customers[0] == '':
                pass
            else:
                with open(f'{file_name_customers[0]}', 'r') as f:
                    dr = csv.DictReader(f, delimiter=";")
                    try:
                        data_to_db = [(i['id_customers'], i['name'], i['last_name'], i['patronymic'],
                                       i['proceeds'], i['profit']) for i in dr]
                    except KeyError:
                        x = -1
                    if x != -1:
                        for i in range(len(data_to_db)):
                            try:
                                self.cur.execute(
                                    f"""INSERT INTO customers (id_customers, name, last_name,
                                                patronymic, proceeds, profit)
                                                VALUES ({data_to_db[i][0]}, '{data_to_db[i][1]}', '{data_to_db[i][2]}', 
                                                '{data_to_db[i][3]}', {data_to_db[i][4]}, {data_to_db[i][5]});""")
                                self.con.commit()
                            except sqlite3.Error:
                                print(1)
                                x += 1
                                continue
                        if x == len(data_to_db):
                            self.message_error_import_warehouse.exec()
                        else:
                            self.product_buy.clear()
                            self.product_sell.clear()
                            self.customers_sell.clear()
                            self.window_sell_buy()
                            self.customers_table.setColumnCount(0)
                            self.customers_table.setRowCount(0)
                            self.window_customers()
                            self.message_success_import.exec()
                    else:
                        self.message_error_import_warehouse.exec()

    def button_export(self):
        if self.sender().text() == "Экспорт товаров в CSV":
            file_name_warehouse = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "CSV Files(*.csv)")
            if file_name_warehouse[0] == '':
                pass
            else:
                data = self.cur.execute("SELECT * FROM warehouse")
                with open(f'{file_name_warehouse[0]}', 'w') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(['id_product', 'product_name', 'amount', 'purchase_price', 'selling_price'])
                    writer.writerows(data)
                self.message_success_export.exec()
        elif self.sender().text() == "Экспорт книги продаж в CSV":
            file_name_warehouse = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "CSV Files(*.csv)")
            if file_name_warehouse[0] == '':
                pass
            else:
                data = self.cur.execute("""SELECT product.id_purchase, customers.name, customers.last_name, 
                customers.patronymic, warehouse.product_name, product.price_sell, 
                product.count_product, product.date_sell, product.sum
                FROM product
                INNER JOIN warehouse
                    ON product.id_product = warehouse.id_product
                INNER JOIN customers
                    ON product.id_customers = customers.id_customers;""")
                with open(f'{file_name_warehouse[0]}', 'w') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(['id_purchase', 'name', 'last_name', 'patronymic', 'product_name',
                                     'price_sell', 'count_product', 'date_sell', 'sum'])
                    writer.writerows(data)
                self.message_success_export.exec()
        elif self.sender().text() == "Экспорт книги покупок в CSV":
            file_name_warehouse = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "CSV Files(*.csv)")
            if file_name_warehouse[0] == '':
                pass
            else:
                data = self.cur.execute(
                    """SELECT product_buy.id_purchase_buy, warehouse.product_name, product_buy.price_product_buy, 
                    product_buy.amount_buy, product_buy.date_buy, product_buy.sum_buy
                    FROM product_buy
                    INNER JOIN warehouse
                        ON product_buy.id_product = warehouse.id_product;""")
                with open(f'{file_name_warehouse[0]}', 'w') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(['id_purchase_buy', 'product_name', 'price_product_buy', 'amount_buy', 'date_buy',
                                     'sum_buy'])
                    writer.writerows(data)
                self.message_success_export.exec()
        else:
            file_name_customers = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "CSV Files(*.csv)")
            if file_name_customers[0] == '':
                pass
            else:
                data = self.cur.execute("SELECT * FROM customers")
                with open(f'{file_name_customers[0]}', 'w') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(['id_customers', 'name', 'last_name', 'patronymic', 'proceeds', 'profit'])
                    writer.writerows(data)
                self.message_success_export.exec()

    def clicked_warehouse_table(self):
        rows = sorted(set(index.row() for index in self.warehouse_table.selectedIndexes()))
        for row in rows:
            rows_list_warehouse.append(row)

    def clicked_customers_table(self):
        rows = sorted(set(index.row() for index in self.customers_table.selectedIndexes()))
        for row in rows:
            rows_list_customers.append(row)

    def button_clicked_row_warehouse(self):
        if self.sender().text() != "Изменить данные":
            number_actions_warehouse.append(0)
            dialog_editing = DialogEditingWarehouse()
            dialog_editing.exec()
            self.product_buy.clear()
            self.product_sell.clear()
            self.customers_sell.clear()
            self.window_sell_buy()
            self.warehouse_table.setColumnCount(0)
            self.warehouse_table.setRowCount(0)
            self.window_warehouse()
        else:
            if len(rows_list_warehouse) != 0:
                count_row = int(rows_list_warehouse[-1])
                id_goods = self.cur.execute(
                    f"""SELECT id_product FROM warehouse""").fetchall()
                if count_row + 1 > len(id_goods):
                    self.message_error.exec()
                else:
                    number_actions_warehouse.append(1)
                    dialog_editing = DialogEditingWarehouse()
                    dialog_editing.exec()
                    self.product_buy.clear()
                    self.product_sell.clear()
                    self.customers_sell.clear()
                    self.window_sell_buy()
                    self.warehouse_table.setColumnCount(0)
                    self.warehouse_table.setRowCount(0)
                    self.window_warehouse()
            else:
                self.message_error.exec()

    def button_clicked_row_customers(self):
        if self.sender().text() != "Изменить данные":
            number_actions_customers.append(0)
            dialog_editing = DialogEditingCustomers()
            dialog_editing.exec()
            self.product_buy.clear()
            self.product_sell.clear()
            self.customers_sell.clear()
            self.window_sell_buy()
            self.customers_table.setColumnCount(0)
            self.customers_table.setRowCount(0)
            self.window_customers()
        else:
            if len(rows_list_customers) != 0:
                count_row = int(rows_list_customers[-1])
                id_customers = self.cur.execute(
                    f"""SELECT id_customers FROM customers""").fetchall()
                if count_row + 1 > len(id_customers):
                    self.message_error.exec()
                else:
                    number_actions_customers.append(1)
                    dialog_editing = DialogEditingCustomers()
                    dialog_editing.exec()
                    self.product_buy.clear()
                    self.product_sell.clear()
                    self.customers_sell.clear()
                    self.window_sell_buy()
                    self.customers_table.setColumnCount(0)
                    self.customers_table.setRowCount(0)
                    self.window_customers()
            else:
                self.message_error.exec()

    def button_clicked_delete_warehouse(self):
        if len(rows_list_warehouse) != 0:
            count_row = int(rows_list_warehouse[-1])
            id_goods = self.cur.execute(
                f"""SELECT id_product FROM warehouse""").fetchall()
            if count_row + 1 > len(id_goods):
                self.message_error.exec()
            else:
                self.message_delete_warehouse.show()
        else:
            self.message_error.exec()

    def button_clicked_delete_customers(self):
        if len(rows_list_customers) != 0:
            count_row = int(rows_list_customers[-1])
            id_customers = self.cur.execute(
                f"""SELECT id_customers FROM customers""").fetchall()
            if count_row + 1 > len(id_customers):
                self.message_error.exec()
            else:
                self.message_delete_customers.show()
        else:
            self.message_error.exec()

    def row_warehouse(self):
        product = self.cur.execute(
            f"""SELECT id_product FROM warehouse""").fetchall()
        product_buy = self.cur.execute(
            f"""SELECT id_product FROM product_buy""").fetchall()
        product_buy = [product_buy[i][0] for i in range(len(product_buy))]
        product_sell = self.cur.execute(
            f"""SELECT id_product FROM product""").fetchall()
        product_sell = [product_sell[i][0] for i in range(len(product_sell))]
        count_row = int(rows_list_warehouse[-1])
        if count_row + 1 > len(product):
            pass
        else:
            id_product = int(product[count_row][0])
            if id_product in product_buy or id_product in product_sell:
                self.message_error_not_delete.show()
            else:
                self.cur.execute(
                    f"""DELETE from warehouse WHERE id_product = {id_product}""")
                self.con.commit()
                self.product_buy.clear()
                self.product_sell.clear()
                self.customers_sell.clear()
                self.window_sell_buy()
                self.warehouse_table.setColumnCount(0)
                self.warehouse_table.setRowCount(0)
                self.window_warehouse()
                self.message_success.show()

    def row_customers(self):
        customer = self.cur.execute(
            f"""SELECT id_customers FROM customers""").fetchall()
        customer_sell = self.cur.execute(
            f"""SELECT id_customers FROM product""").fetchall()
        customer_sell = [customer_sell[i][0] for i in range(len(customer_sell))]
        count_row = int(rows_list_customers[-1])
        if count_row + 1 > len(customer):
            pass
        else:
            id_customer = int(customer[count_row][0])
            if id_customer in customer_sell:
                self.message_error_not_delete.show()
            else:
                self.cur.execute(
                    f"""DELETE from customers WHERE id_customers = {id_customer}""")
                self.con.commit()
                self.product_buy.clear()
                self.product_sell.clear()
                self.customers_sell.clear()
                self.window_sell_buy()
                self.customers_table.setColumnCount(0)
                self.customers_table.setRowCount(0)
                self.window_customers()
                self.message_success.show()


class DialogEditingCustomers(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('dialog_editing_customers.ui', self)
        self.con = sqlite3.connect('project_db.sqlite')
        self.cur = self.con.cursor()
        if number_actions_customers[-1] != 1:
            self.setWindowTitle("Введите данные нового клиента")
            self.name_customer.setText("Имя")
            self.last_name_customer.setText("Фамилия")
            self.patronymic_customer.setText("Отчество")
            self.message_access_add = QMessageBox()
            self.message_access_add.setIcon(QMessageBox.Information)
            self.message_access_add.setWindowTitle("Успешно")
            self.message_access_add.setText("Вы добавили нового клиента.")
            self.accepted.connect(self.button_clicked_add)
        else:
            self.count_row = int(rows_list_customers[-1])
            self.setWindowTitle("Изменение данных клиента")
            self.message_error_no_editing_customers = QMessageBox()
            self.message_error_no_editing_customers.setIcon(QMessageBox.Warning)
            self.message_error_no_editing_customers.setWindowTitle("Ошибка")
            self.message_error_no_editing_customers.setText("Вы не внесли изменения в строку.")
            self.message_success_customers = QMessageBox()
            self.message_success_customers.setIcon(QMessageBox.Information)
            self.message_success_customers.setWindowTitle("Успешно")
            self.message_success_customers.setText("Вы внесли изменения в строку %d." % (self.count_row + 1))
            self.name = self.cur.execute(
                f"""SELECT name FROM customers""").fetchall()
            self.last_name = self.cur.execute(
                f"""SELECT last_name FROM customers""").fetchall()
            self.patronymic = self.cur.execute(
                f"""SELECT patronymic FROM customers""").fetchall()
            self.name_customer.setText(str(self.name[self.count_row][0]))
            self.last_name_customer.setText(str(self.last_name[self.count_row][0]))
            self.patronymic_customer.setText(str(self.patronymic[self.count_row][0]))
            self.accepted.connect(self.button_clicked_editing)

    def button_clicked_add(self):
        id_product = self.cur.execute(
            """SELECT id_customers FROM customers""").fetchall()
        name_user = self.name_customer.text()
        last_name_user = self.last_name_customer.text()
        patronymic_user = self.patronymic_customer.text()
        self.cur.execute(
            f"""INSERT INTO customers (id_customers, name, last_name, 
                patronymic, proceeds, profit)
                VALUES ({int(id_product[-1][0] + 1)}, '{name_user}', '{last_name_user}',
                ' {patronymic_user}', 0, 0);""")
        self.con.commit()
        self.con.close()
        self.message_access_add.exec()

    def button_clicked_editing(self):
        name_user = self.name_customer.text()
        last_name_user = self.last_name_customer.text()
        patronymic_user = self.patronymic_customer.text()
        if str(name_user) == str(self.name[self.count_row][0]) and str(last_name_user) == str(
                self.last_name[self.count_row][0]) and str(patronymic_user) == str(
                self.patronymic[self.count_row][0]):
            self.message_error_no_editing_customers.exec()
        else:
            self.cur.execute(
                f"""UPDATE customers SET name = '{str(name_user)}'
                WHERE name = '{self.name[self.count_row][0]}'""")
            self.cur.execute(
                f"""UPDATE customers SET last_name = '{str(last_name_user)}'
                WHERE name = '{self.name[self.count_row][0]}'""")
            self.cur.execute(
                f"""UPDATE customers SET patronymic = '{str(patronymic_user)}'
                WHERE name = '{self.name[self.count_row][0]}'""")
            self.con.commit()
            self.con.close()
            self.message_success_customers.exec()


class DialogEditingWarehouse(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('dialog_editing_warehouse.ui', self)
        self.con = sqlite3.connect('project_db.sqlite')
        self.cur = self.con.cursor()
        self.message_error_buy_more_sell = QMessageBox()
        self.message_error_buy_more_sell.setIcon(QMessageBox.Warning)
        self.message_error_buy_more_sell.setWindowTitle("Ошибка")
        self.message_error_buy_more_sell.setText("Цена закупки не может быть больше цены продажи.")
        if number_actions_warehouse[-1] != 1:
            self.setWindowTitle("Введите данные новой строки")
            self.name_line_warehouse.setText("Наименование товара")
            self.message_access_add_warehouse = QMessageBox()
            self.message_access_add_warehouse.setIcon(QMessageBox.Information)
            self.message_access_add_warehouse.setWindowTitle("Успешно")
            self.message_access_add_warehouse.setText("Вы добавили новую строку.")
            self.count_line_warehouse.setValue(int(0))
            self.buy_line_warehouse.setValue(float(0.01))
            self.sell_line_warehouse.setValue(float(0.02))
            self.accepted.connect(self.button_clicked_add)
        else:
            self.count_row = int(rows_list_warehouse[-1])
            self.setWindowTitle("Изменение данных строки")
            self.message_error_no_editing_warehouse = QMessageBox()
            self.message_error_no_editing_warehouse.setIcon(QMessageBox.Warning)
            self.message_error_no_editing_warehouse.setWindowTitle("Ошибка")
            self.message_error_no_editing_warehouse.setText("Вы не внесли изменения в строку.")
            self.message_success_warehouse = QMessageBox()
            self.message_success_warehouse.setIcon(QMessageBox.Information)
            self.message_success_warehouse.setWindowTitle("Успешно")
            self.message_success_warehouse.setText("Вы внесли изменения в строку %d." % (self.count_row + 1))
            self.name = self.cur.execute(
                f"""SELECT product_name FROM warehouse""").fetchall()
            self.count = self.cur.execute(
                f"""SELECT amount FROM warehouse""").fetchall()
            self.buy = self.cur.execute(
                f"""SELECT purchase_price FROM warehouse""").fetchall()
            self.sell = self.cur.execute(
                f"""SELECT selling_price FROM warehouse""").fetchall()
            self.name_line_warehouse.setText(str(self.name[self.count_row][0]))
            self.count_line_warehouse.setValue(int((self.count[self.count_row][0])))
            self.buy_line_warehouse.setValue(float((self.buy[self.count_row][0])))
            self.sell_line_warehouse.setValue(float((self.sell[self.count_row][0])))
            self.accepted.connect(self.button_clicked_editing)

    def button_clicked_add(self):
        id_product = self.cur.execute(
            """SELECT id_product FROM warehouse""").fetchall()
        name_user = self.name_line_warehouse.text()
        count_user = self.count_line_warehouse.text()
        buy_price_user = self.buy_line_warehouse.text().split(",")
        buy_price_user = float(buy_price_user[0] + "." + buy_price_user[1])
        sell_price_user = self.sell_line_warehouse.text().split(",")
        sell_price_user = float(sell_price_user[0] + "." + sell_price_user[1])
        if float(buy_price_user) > float(sell_price_user):
            self.message_error_buy_more_sell.exec()
        else:
            self.cur.execute(
                f"""INSERT INTO warehouse (id_product, product_name, amount, 
                    purchase_price, selling_price)
                    VALUES ({int(id_product[-1][0] + 1)}, '{name_user}', {count_user},
                    {buy_price_user}, {sell_price_user});""")
            self.con.commit()
            self.con.close()
            self.message_access_add_warehouse.exec()

    def button_clicked_editing(self):
        name_user = self.name_line_warehouse.text()
        count_user = self.count_line_warehouse.text()
        buy_price_user = self.buy_line_warehouse.text().split(",")
        buy_price_user = buy_price_user[0] + "." + buy_price_user[1]
        sell_price_user = self.sell_line_warehouse.text().split(",")
        sell_price_user = sell_price_user[0] + "." + sell_price_user[1]
        if float(buy_price_user) > float(sell_price_user):
            self.message_error_buy_more_sell.exec()
        else:
            if str(name_user) == str(self.name[self.count_row][0]) and int(count_user) == int(
                    self.count[self.count_row][0]) and float(buy_price_user) == float(
                self.buy[self.count_row][0]) and float(
                    sell_price_user) == float(self.sell[self.count_row][0]):
                self.message_error_no_editing_warehouse.exec()
            else:
                self.cur.execute(
                    f"""UPDATE warehouse SET product_name = '{str(name_user)}'
                            WHERE product_name = '{str(self.name[self.count_row][0])}'""")
                self.cur.execute(
                    f"""UPDATE warehouse SET amount = {int(count_user)}
                            WHERE product_name = '{str(self.name[self.count_row][0])}'""")
                self.cur.execute(
                    f"""UPDATE warehouse SET purchase_price = {float(buy_price_user)}
                            WHERE product_name = '{str(self.name[self.count_row][0])}'""")
                self.cur.execute(
                    f"""UPDATE warehouse SET selling_price = {float(sell_price_user)}
                            WHERE product_name = '{str(self.name[self.count_row][0])}'""")
                self.con.commit()
                self.con.close()
                self.message_success_warehouse.exec()


def exception_hook(exctype, value, traceback):
    traceback_formated = traceback.format_exception(exctype, value, traceback)
    traceback_string = "".join(traceback_formated)
    print(traceback_string, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())

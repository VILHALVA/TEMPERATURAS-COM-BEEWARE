import os
import sqlite3
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'conversoes.db')

def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_origem TEXT NOT NULL,
            valor_origem REAL NOT NULL,
            tipo_destino TEXT NOT NULL,
            valor_destino REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()

class ConversorTemperaturaApp(toga.App):
    def startup(self):
        self.initialize_database()

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        self.tipo_origem = toga.Selection(items=['Celsius', 'Fahrenheit', 'Kelvin'], style=Pack(padding=5))
        self.valor_origem = toga.TextInput(style=Pack(flex=1, padding=5))
        self.tipo_destino = toga.Selection(items=['Celsius', 'Fahrenheit', 'Kelvin'], style=Pack(padding=5))
        self.valor_destino = toga.TextInput(readonly=True, style=Pack(flex=1, padding=5))

        converter_button = toga.Button('CONVERTER', on_press=self.converter_temperatura, style=Pack(padding=5))
        salvar_button = toga.Button('SALVAR', on_press=self.salvar_conversao, style=Pack(padding=5))

        button_box = toga.Box(style=Pack(direction=ROW, padding=5))
        button_box.add(converter_button)
        button_box.add(salvar_button)

        main_box.add(self.tipo_origem)
        main_box.add(self.valor_origem)
        main_box.add(self.tipo_destino)
        main_box.add(self.valor_destino)
        main_box.add(button_box)

        self.main_window.show()

    def initialize_database(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_origem TEXT NOT NULL,
                valor_origem REAL NOT NULL,
                tipo_destino TEXT NOT NULL,
                valor_destino REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def converter_temperatura(self, widget):
        try:
            valor_origem = float(self.valor_origem.value)
        except ValueError:
            self.main_window.info_dialog('Erro', 'Por favor, insira um valor numérico para a temperatura.')
            return

        tipo_origem = self.tipo_origem.value
        tipo_destino = self.tipo_destino.value

        if tipo_origem == tipo_destino:
            self.valor_destino.value = self.valor_origem.value
            return

        if tipo_origem == 'Celsius':
            if tipo_destino == 'Fahrenheit':
                valor_convertido = (valor_origem * 9/5) + 32
            elif tipo_destino == 'Kelvin':
                valor_convertido = valor_origem + 273.15
        elif tipo_origem == 'Fahrenheit':
            if tipo_destino == 'Celsius':
                valor_convertido = (valor_origem - 32) * 5/9
            elif tipo_destino == 'Kelvin':
                valor_convertido = (valor_origem - 32) * 5/9 + 273.15
        elif tipo_origem == 'Kelvin':
            if tipo_destino == 'Celsius':
                valor_convertido = valor_origem - 273.15
            elif tipo_destino == 'Fahrenheit':
                valor_convertido = (valor_origem - 273.15) * 9/5 + 32

        self.valor_destino.value = f'{valor_convertido:.2f}'

    def salvar_conversao(self, widget):
        tipo_origem = self.tipo_origem.value
        valor_origem = float(self.valor_origem.value)
        tipo_destino = self.tipo_destino.value
        valor_destino = float(self.valor_destino.value)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO conversoes (tipo_origem, valor_origem, tipo_destino, valor_destino)
            VALUES (?, ?, ?, ?)
        ''', (tipo_origem, valor_origem, tipo_destino, valor_destino))

        conn.commit()
        conn.close()

        self.main_window.info_dialog('Conversão Salva', 'A conversão foi salva com sucesso.')

def main():
    return ConversorTemperaturaApp('conversor_temperatura', 'com.example.conversortemperatura')

if __name__ == '__main__':
    main().main_loop()

import psycopg2
import datetime
import pandas as pd

class DataBase():
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
    host="dpg-cheebkt269v75d7pvf70-a.oregon-postgres.render.com",
    database="db_ajosca",
    user="gvieira",
    password="U7ZhdOQx1HmDFT63OGAzGDXIJlZH8uQz"
)
        self.c = self.conn.cursor()

    def Criar_db(self):
        self.c.execute('CREATE TABLE lic_especial (Numero_Interno SMALLINT, Nome VARCHAR(30), data_limite TIMESTAMP, motivo VARCHAR(50))')
        self.c.execute('CREATE TABLE baixados (Numero_Interno SMALLINT, Nome VARCHAR(30))')
        self.c.execute('CREATE TABLE Quantitativo (Ano_Escolar VARCHAR(5), Total_do_Ano SMALLINT, Total_a_bordo SMALLINT)')
        self.conn.commit()

    def Inserir_data(self, table, **kwargs):
        if table == 'lic':
            self.c.execute(f''' INSERT INTO lic_especial (Numero_Interno, Nome, data_limite, motivo) VALUES (%s, %s, %s, %s)''', 
            (kwargs["Numero_Interno"], f'{kwargs["Nome"]}', kwargs["data_limite"], f"{kwargs['motivo']}"))
        elif table == 'baixados':
            self.c.execute(f'''INSERT INTO baixados (Numero_Interno, Nome) VALUES (%s, %s)''',
                           (kwargs["Numero_Interno"], f"{kwargs['Nome']}"))
        else:
            sql = 'SELECT * FROM Quantitativo'
            df = pd.read_sql(sql, self.conn)
            if len(df) != 0:
                self.Delete_data('Quantitativo')
            for d in range(4, 0, -1):
                self.c.execute(f'''INSERT INTO Quantitativo (Ano_Escolar, Total_do_Ano, Total_a_bordo) VALUES (%s , %s, %s)''', ('CA', kwargs["total_CA"], kwargs["quant_CA_a_bordo"])) if d == 4 else self.c.execute(f'''INSERT INTO Quantitativo (Ano_Escolar, Total_do_Ano, Total_a_bordo) VALUES (%s, %s, %s)''', (f'{d} Ano', kwargs[f"total_{d}_ano"], kwargs[f"a_bordo_{d}_ano"]))

        self.conn.commit()

    def Delete_data(self, table, **kwargs):
        if table == 'lic':
            sql = "SELECT * FROM lic_especial"
            df = pd.read_sql(sql, self.conn)
            for line in df.index:
                day_limit = df.loc[line][2]
                if day_limit < datetime.datetime.today():
                    self.c.execute(f"DELETE FROM lic_especial WHERE Numero_Interno = %s", (df.loc[line][0],))
        elif table == 'baixados':
            self.c.execute(f'DELETE FROM baixados WHERE Numero_Interno = %s', (kwargs["Numero_Interno"],))
        else:
            for i in range(0, 4):
                self.c.execute(f'DELETE FROM Quantitativo WHERE Ano_Escolar = %s', ('CA',)) if i == 0 else self.c.execute(f'DELETE FROM Quantitativo WHERE Ano_Escolar = %s', (f'{i} Ano',))
        self.conn.commit()

    def Excluir_Banco(self):
        self.c.execute('DROP TABLE lic_especial')
        self.c.execute('DROP TABLE baixados')
        self.c.execute('DROP TABLE Quantitativo')


    def Retirar_data(self, table):
        if table == 'lic':
            sql = "SELECT * FROM lic_especial"
            df = pd.read_sql(sql, self.conn)
            lic_list, disp_dom = '', ''
            for line in df.index:
                pessoa = {'Numero_Interno': df.loc[line][0], 'Nome': df.loc[line][1], 'data_regresso': df.loc[line][2], 'motivo': df.loc[line][3]}
                pessoa['data_regresso'] = f"{int(pessoa['data_regresso'].day):02d}/{int(pessoa['data_regresso'].month):02d} às {int(pessoa['data_regresso'].hour):02d}:{int(pessoa['data_regresso'].minute):02d}"
                if pessoa['motivo'] == 'Dispensa Domiciliar':
                    disp_dom += f"{pessoa['Numero_Interno']} {pessoa['Nome']}  Regresso em -> {pessoa['data_regresso']}\n"
                if pessoa['motivo'] == 'Licença Especial':
                    lic_list += f"{pessoa['Numero_Interno']} {pessoa['Nome']}  Regresso em -> {pessoa['data_regresso']}\n"
            return lic_list, disp_dom
        elif table == 'baixados':
            sql = 'SELECT * FROM baixados'
            df = pd.read_sql(sql, self.conn)
            baixados_list = ''
            for line in df.index:
                person = {'Numero_Interno': df.loc[line][0], 'Nome': df.loc[line][1]}
                baixados_list += f'{person["Numero_Interno"]} - {person["Nome"]}\n'
            return baixados_list
        else:
            sql = 'SELECT * FROM Quantitativo'
            df = pd.read_sql(sql, self.conn)
            quant_no_cn = ''
            df.set_index('ano_escolar', inplace=True)
            for year in df.index:
                quant_no_cn += f'{year:<5} ------ {df.loc[year][0]:<3} ------ {df.loc[year][1]:<3}\n'
            quant_no_cn = 'Segue o quantitativo a bordo do corpo de alunos e de cada ano:\n' + 'Turma ------ Total ------ A bordo\n' + f'{quant_no_cn}'
            return quant_no_cn


#if __name__ == '__main__':
#    while True:
#        DataBase().Delete_data('lic')

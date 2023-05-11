import gspread 
from google.oauth2 import service_account
import os
import pandas as pd
from datetime import datetime
import requests
from planilha import achar_copia_do_dia, dia_da_semana


scopes = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive"
]

json_file = os.path.join('tokens', 'credentials.json')

def login():
    credentials = service_account.Credentials.from_service_account_file(json_file)
    scoped_credentials = credentials.with_scopes(scopes)
    gc = gspread.authorize(scoped_credentials)
    return gc


def pegar_quantitativo(refeicao):
    date_week = dia_da_semana()
    word_list = len(refeicao.split(' '))
    if word_list == 3:
        refeicao = f'{refeicao.split()[0][0]}.{refeicao.split()[-1][0]}'
    elif word_list == 1:
        refeicao = f'{refeicao[0]}'
    quantitativo = {}
    string_quant = ''
    if str(refeicao).upper() == 'C.M':
        refeicao = 'P.A'
    gc = login()
    datas = achar_copia_do_dia()
    sheet = gc.open(f"Previa {datas[0].day:02d}/{datas[0].month:02d} a {datas[1].day:02d}/{datas[1].month:02d}")
    page = sheet.worksheet('Q')
    for col in range(3, 31, 4):
        if  page.cell(row=8, col=col).value == date_week:
            for ref in range(col, col + 4):
                if page.cell(row=9, col=ref).value ==  str(refeicao).upper():
                    for row in range(10, 16):
                        quantitativo[page.cell(row=row, col=2).value] = page.cell(row=row, col=ref).value
    for value in quantitativo.items():
        string_quant += f'{value[0]} ---- {value[1]}\n'
                    
    return string_quant

    

def pegar_nominal(refeicao):
    date_week = dia_da_semana()
    word_list = len(refeicao.split(' '))
    if word_list == 3:
        refeicao = f'{refeicao.split()[0][0]}.{refeicao.split()[-1][0]}'
    elif word_list == 1:
        refeicao = f'{refeicao[0]}'
    
    nominal = {}
    gc = login()
    datas = achar_copia_do_dia()
    sheet = gc.open(f'Previa {datas[0].day:02d}/{datas[0].month:02d} a {datas[1].day:02d}/{datas[1].month:02d}')
    page = sheet.worksheet('CONTROLE')
    total_de_alunos = {i: int(page.cell(row=7-i, col=2).value) for i in range(1, 4)}
    for ano in range(3, 0, -1):
        page = sheet.worksheet(f'P{ano}')
        data = page.get_values(f'A6:AD{int(total_de_alunos[ano])+7}')
        df = pd.DataFrame(data)
        for day in range(2, 30, 4):
            if df.iloc[0][day] == date_week:
                for ref in range(day, day + 4):
                    if df.iloc[1][ref] == str(refeicao).upper():
                        for person in df[df[ref] == 'Sim'][[0, 1]].values:
                            nominal[person[0]] = person[1]
    lista_nominal = ''
    for person in nominal.items():
        lista_nominal += f'{person[0]} {person[1]}\n'
    return lista_nominal


def pegar_numero_de_alunos():
    gc = login()
    datas = achar_copia_do_dia()
    sheet = gc.open(f'Previa {datas[0].day:02d}/{datas[0].month:02d} a {datas[1].day:02d}/{datas[1].month:02d}')
    page = sheet.worksheet(f'CONTROLE')
    quant_CA = page.cell(row=3, col=2).value
    quant_3ano = page.cell(row=4, col=2).value
    quant_2ano = page.cell(row=5, col=2).value
    quant_1ano = page.cell(row=6, col=2).value
    return {'CA':quant_CA, '3 Ano': quant_3ano, '2 Ano': quant_2ano, '1 Ano': quant_1ano}




def pegar_arriou(): 
	url = "https://sunrise-sunset-times.p.rapidapi.com/getSunriseAndSunset"

	date = datetime.today()
	data = f'{date.year}-{date.month:02d}-{date.day:02d}'


	querystring = {"date":f"{data}","latitude":"-23.0172014","longitude":"-44.3297915","timeZoneId":"America/Sao_Paulo"}

	headers = {
		"X-RapidAPI-Key": "9ef86b20aemsh91db636783341d4p15c002jsn2e038cb6e374",
		"X-RapidAPI-Host": "sunrise-sunset-times.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	resposta = response.json()
	arriou = resposta['sunset'].split('T')[1][:5]
	
	
	return arriou

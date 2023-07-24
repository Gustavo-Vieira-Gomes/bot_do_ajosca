import gspread 
import datetime


scopes = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive"
]


def achar_copia_do_dia():
    dia = datetime.datetime.today()
    if dia.weekday() < 4:
        inicio_previa = dia - datetime.timedelta(7) + datetime.timedelta(4 - dia.weekday())
    else:
        inicio_previa = dia + datetime.timedelta(dia.weekday() - 4)
    if dia.weekday() > 3:
        fim_previa = dia + datetime.timedelta(10 - dia.weekday())
    else:
        fim_previa = dia + datetime.timedelta(3 - dia.weekday())
    
    return inicio_previa, fim_previa


def dia_da_semana():
    dia = datetime.datetime.today().weekday()
    if dia == 0:
        return 'SEGUNDA'
    elif dia == 1:
        return 'TERÇA'
    elif dia == 2:
        return 'QUARTA'
    elif dia == 3:
        return 'QUINTA'
    elif dia == 4:
        return 'SEXTA'
    elif dia == 5:
        return 'SÁBADO'
    else:
        return 'DOMINGO'



def copiar_previa():
    gc = gspread.service_account(filename='C:\\Users\\gviei\\Projetos Python\\VsCodeProjects\\Meus Projetos\BotDs\\tokens\\credentials.json')
    while True:
        data = datetime.datetime.today()
        if data.weekday() == 2 and data.hour == 12 and data.minute == 0:
            inicio_previa = data + datetime.timedelta(2)
            fim_previa = data + datetime.timedelta(8)
            try:
                gc.copy('14fcP-kflCXoj1UiPwPMb9NrmyRd-WbdfjMbtmMmI-nQ', f'Previa {inicio_previa.day:02d}/{inicio_previa.month:02d} a {fim_previa.day:02d}/{fim_previa.month:02d}') 
            except:
                pass
        if data.weekday() == 4 and data.hour == 12 and data.minute == 0:
            inicio_previa = data - datetime.timedelta(7)
            fim_previa = data - datetime.timedelta(1)
            for spreadsheet in gc.list_spreadsheet_files():
                if spreadsheet['name'] == f'Previa {inicio_previa.day:02d}/{inicio_previa.month:02d} a {fim_previa.day:02d}/{fim_previa.month:02d}':
                    id_ = spreadsheet['id']
            try:
                gc.del_spreadsheet(id_)
            except:
                pass
    
import lightbulb
import string
import requests
from Func_auxiliares import *
from banco_de_dados import DataBase

bot = lightbulb.BotApp(token=open('tokens/tokens_bot.txt', 'r').read(),
default_enabled_guilds = (int(open('tokens/ds_channel_id.txt', 'r').read())))





#Mostrar Clima
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open('tokens/open_weather_key', 'r').read()

@bot.command
@lightbulb.option('pais', 'País', type=str)
@lightbulb.option('cidade', 'Cidade', type=str)
@lightbulb.command('clima', 'Informe uma localidade para saber seu clima.')
@lightbulb.implements(lightbulb.SlashCommand)

async def clima(ctx):
    country = ctx.options.pais
    CITY = string.capwords(ctx.options.cidade) + ',' + country[0:2].lower()
    url = BASE_URL + 'q=' + CITY + '&APPID=' + API_KEY
    response = requests.get(url).json()
    temp_media = f"{(float(response['main']['temp']) - 273):.2f}" # Temperatura em kelvin
    sensation_termica = f"{(float(response['main']['feels_like']) - 273):.2f}" # Sensação térmica
    temp_min = f"{(float(response['main']['temp_min']) - 273):.2f}" # Temp Minima
    temp_max = f"{(float(response['main']['temp_max']) - 273):.2f}" # Temp maxima
    umidade = f"{response['main']['humidity']}%" # umidade
    vel_vento = f"{response['wind']['speed']}kt" # Vento
    await ctx.respond(f'A temperatura média no momento é: {temp_media}ºC\nA sensação térmica no momento é: {sensation_termica}ºC\nA temperatura máxima prevista para hoje é: {temp_max}ºC\nA temperatura mínima prevista para hoje é: {temp_min}ºC\nA umidade de hoje é: {umidade}\nA velocidade do vento hoje é:{vel_vento}')



@bot.command
@lightbulb.option('refeicao', 'Qual Refeição deseja', type=str)
@lightbulb.command('pegar_quantitativo', 'Pega o Quantitativo da refeição desejada.')
@lightbulb.implements(lightbulb.SlashCommand)

async def pegar_quant(ctx: lightbulb.Context):
    ref = str(ctx.options.refeicao)
    await ctx.respond('Estou buscando, aguarde um pouco!')
    try:
        qnt = pegar_quantitativo(ref)
    except Exception as error:
        await ctx.respond(f'Não consegui pegar o quantitativo, me desculpe.2\n{error}3')
        print(error)
    else:
        await ctx.respond(f'{qnt}')


@bot.command
@lightbulb.option('refeicao', 'Refeição')
@lightbulb.command('pegar_nominal', 'Pega a Lista nominal da refeição')
@lightbulb.implements(lightbulb.SlashCommand)

async def pegar_nom(ctx):
    ref = str(ctx.options.refeicao)
    await ctx.respond('Estou pegando os nomes, aguarde um pouco!')
    try:
        nominal = pegar_nominal(ref)
    except Exception as error:
        await ctx.respond(f'Não consegui pegar a lista nominal, me desculpe.\n{error}')
    else:
        await ctx.respond(f'{nominal}')


@bot.command
@lightbulb.command('pegar_arriou', 'Pega o horário do arriou no referido dia')
@lightbulb.implements(lightbulb.SlashCommand)
async def pegar_horario_arriou(ctx):
    horario = pegar_arriou()
    await ctx.respond(f'{horario}')



@bot.command
@lightbulb.option('horario', 'horário de regresso do militar')
@lightbulb.option('mes', 'mês do regresso')
@lightbulb.option('dia_de_regresso', 'Dia em que o militar estará regressando')
@lightbulb.option('nome', 'Nome do militar que está licenciando Especial')
@lightbulb.option('numero_interno', 'Número Interno do militar que está licenciando Especial')
@lightbulb.command('adicionar_lic_especial', 'Adiciona o militar que licou especial ao Banco de Dados')
@lightbulb.implements(lightbulb.SlashCommand)

async def adicionar_lic(ctx):
    day = ctx.options.dia_de_regresso
    mes = ctx.options.mes
    hora = ctx.options.horario.split(':')
    mes = mes.replace('0', '') if mes[0] == '0' else mes 
    day = day.replace('0', '') if mes[0] == '0' else day
    for i in range(0, 2):
        hora[i] = hora[i].replace('0', '') if hora[i][0] == '0' else hora[i]
        if hora[i] == '':
            hora[i] = 0 
    data = datetime(year=datetime.today().year, month=int(mes), day=int(day), hour=int(hora[0]), minute=int(hora[1]))
    DataBase().Inserir_data('lic', Numero_Interno=ctx.options.numero_interno, Nome=ctx.options.nome, data_limite=data, motivo='Licença Especial')
    await ctx.respond(f'Adicionei o Aluno na lista de alunos em lic especial')

@bot.command
@lightbulb.option('horario', 'horário de regresso do militar')
@lightbulb.option('mes', 'mês do regresso')
@lightbulb.option('dia_de_regresso', 'Dia em que o militar estará regressando')
@lightbulb.option('nome', 'Nome do militar que está de dispensa domiciliar')
@lightbulb.option('numero_interno', 'Número Interno do militar que está de dispensa domiciliar')
@lightbulb.command('adicionar_dispensado_domiciliar', 'Adiciona um militar que está dispensado em casa na lista')
@lightbulb.implements(lightbulb.SlashCommand)
async def adicionar_dispensado_domiciliar(ctx):
    day = ctx.options.dia_de_regresso
    mes = ctx.options.mes
    hora = ctx.options.horario.split(':')
    mes = mes.replace('0', '') if mes[0] == '0' else mes 
    day = day.replace('0', '') if mes[0] == '0' else day
    for i in range(0, 2):
        hora[i] = hora[i].replace('0', '') if hora[i][0] == '0' else hora[i]
        if hora[i] == '':
            hora[i] = 0 
    data = datetime(year=datetime.today().year, month=int(mes), day=int(day), hour=int(hora[0]), minute=int(hora[1]))
    DataBase().Inserir_data('lic', Numero_Interno=ctx.options.numero_interno, Nome=ctx.options.nome, data_limite=data, motivo='Dispensa Domiciliar')
    await ctx.respond(f'Adicionei o Aluno na lista de alunos em Dispensa Domiciliar')


@bot.command
@lightbulb.command('listar_lic_e_dispensa', 'Lista os Alunos que permanecem de Licença especial')
@lightbulb.implements(lightbulb.SlashCommand)
async def listar_lic(ctx):
    data = DataBase().Retirar_data('lic')
    if data[0] == '' and data[1] == '':
        await ctx.respond('Nenhum aluno está de licenciamento especial nem dispensa domiciliar')
    else:
        final_string = 'Os seguintes alunos estão com Licença especial:\n' + data[0] + 'Os seguintes alunos estão com dispensa domiciliar:\n' + data[1]
        await ctx.respond(f'{final_string}')


@bot.command
@lightbulb.option('nome', 'Nome do aluno baixado')
@lightbulb.option('numero_interno', 'Número Interno do aluno baixado')
@lightbulb.command('adicionar_aluno_baixado', 'Adiciona um aluno baixado ao banco de dados')
@lightbulb.implements(lightbulb.SlashCommand)
async def adicionar_baixado(ctx):
    nome = ctx.options.nome
    numero_interno = ctx.options.numero_interno
    DataBase().Inserir_data('baixados', Numero_Interno=numero_interno, Nome=nome)
    await ctx.respond(f'Adicionei o ACN {numero_interno} {nome} na lista de alunos baixados com sucesso!')

@bot.command
@lightbulb.command('listar_alunos_baixados', 'Lista os alunos que estão baixados até agora')
@lightbulb.implements(lightbulb.SlashCommand)
async def listar_baixados(ctx):
    data = DataBase().Retirar_data('baixados')
    if data == '':
        await ctx.respond('Nenhum aluno está baixado no momento')
    else:
        final_string = 'Os seguintes alunos estão baixados:\n' + data
        await ctx.respond(f'{final_string}')

@bot.command
@lightbulb.option('numero_interno', 'Número Interno do aluno que saiu da enfermaria')
@lightbulb.command('excluir_baixado', 'Exclui o aluno que saiu da enfermaria da lista de baixados')
@lightbulb.implements(lightbulb.SlashCommand)
async def excluir_baixado(ctx):
    numero_interno = ctx.options.numero_interno
    DataBase().Delete_data('baixados', Numero_Interno=numero_interno)
    await ctx.respond(f'O referido aluno foi retirado da lista de baixados com sucesso!')
    

@bot.command
@lightbulb.option('quantitativo_3_ano', 'Quantitativo a bordo do 3º Ano')
@lightbulb.option('quantitativo_2_ano', 'Quantitativo a bordo do 2º Ano')
@lightbulb.option('quantitativo_1_ano', 'Quantitativo a bordo do 1º Ano')
@lightbulb.command('atualizar_quantitativo', 'Atualiza o Quantitativo de alunos a bordo de cada ano')
@lightbulb.implements(lightbulb.SlashCommand)
async def atualizar_quantitativo(ctx):
    _3ano_abordo = ctx.options.quantitativo_3_ano
    _2ano_abordo = ctx.options.quantitativo_2_ano
    _1ano_abordo = ctx.options.quantitativo_1_ano
    quant_ca =  int(_3ano_abordo) + int(_2ano_abordo) + int(_1ano_abordo)
    await ctx.respond('Um momento, atualizando o quantitativo.')
    quant_total = pegar_numero_de_alunos()
    try:
        DataBase().Inserir_data('Quantitativo', total_CA=quant_total['CA'], quant_CA_a_bordo=quant_ca, total_3_ano=quant_total['3 Ano'], a_bordo_3_ano=_3ano_abordo,
                                total_2_ano=quant_total['2 Ano'], a_bordo_2_ano=_2ano_abordo, total_1_ano=quant_total['1 Ano'], a_bordo_1_ano=_1ano_abordo)
    except Exception as error:
        await ctx.respond('Não consegui atualizar o quantitativo, sinto muito.')
    else:
        await ctx.respond('Atualizei o quantitativo com sucesso')


@bot.command
@lightbulb.command('mostrar_quantitativo', 'Apresenta o Quantitativo a bordo no Colégio')
@lightbulb.implements(lightbulb.SlashCommand)
async def listar_quantitativo(ctx):
    data = DataBase().Retirar_data('Quantitativo')
    await ctx.respond(f'{data}')


bot.run()

# ### Covid-19 en Argentina

import pandas as pd

url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'
dataCovid = pd.read_csv(url, encoding = "UTF-16-LE")

#Exploración de los datos
print(dataCovid.columns)


dataCovid.head(3)


#Indice datetime type
idx = pd.to_datetime(dataCovid.fecha_apertura, format='%Y/%m/%d')
#Reemplazar índice
dataCovid = dataCovid.set_index(idx)
#Eliminar la columna 
data = dataCovid.drop('fecha_apertura',axis=1)
data.head()

positivo = dataCovid.loc[dataCovid.clasificacion_resumen=='Confirmado']
negativo = dataCovid.loc[dataCovid.clasificacion_resumen=='Descartado']

#Positivos
casoP = {}
casoP['daily_cases'] = positivo.clasificacion_resumen.groupby(positivo.index).count()
casoP['daily_cum_cases'] = casoP['daily_cases'].cumsum()
casoP = pd.DataFrame(casoP)
casoP.tail()

import matplotlib.pyplot as plt

with plt.style.context('dark_background'):
    fig, ax = plt.subplots(figsize=(20,10))

    ax.plot(casoP.daily_cum_cases)
    ax.set_xlabel('')
    ax.set_ylabel('Casos (+) Confirmados')
    ax.set_title("ACUM. DIARIA COVID19 EN ARG.")

    eventos = [(pd.Timestamp("2020-03-20"), 'Fase I'),
               (pd.Timestamp("2020-04-01"), 'Fase II'),
               (pd.Timestamp("2020-04-14"), 'Fase III'),
               (pd.Timestamp("2020-05-11"), 'Fase IV'),
               (pd.Timestamp("2020-05-25"), 'Fase V'),
               (pd.Timestamp("2020-06-08"), 'Fase VI'),
               (pd.Timestamp("2020-07-01"), 'Fase VII')]

    for d, l in eventos:
        ax.annotate(l, xy=(d, casoP.daily_cum_cases[d]), 
        xytext=(d, casoP.daily_cum_cases[d]*1.1), color='white',
        arrowprops=dict(headwidth=10, headlength=10, width=1, facecolor='white', shrink=0.05),
        horizontalalignment='center', verticalalignment='top')


#Descomposición de la curva por Sexo
M = positivo.loc[(positivo.edad_años_meses=='Años') & (positivo.sexo=='M')]
M = pd.concat([M.sexo, M.edad], axis=1).dropna().sort_values('edad',ascending=True)
M = M.sexo.groupby(M.index).count().cumsum()


F = positivo.loc[(positivo.edad_años_meses=='Años') & (positivo.sexo=='F')]
F = pd.concat([F.sexo, F.edad], axis=1).dropna().sort_values('edad',ascending=True)
F = F.sexo.groupby(F.index).count().cumsum()

sexo_edad = pd.concat([M,F], axis=1).fillna(0)
sexo_edad.columns = ['M', 'F']
with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 5]
    sexo_edad.plot.bar(stacked=True)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Discriminación por sexo')
    plt.legend(labels=['M', 'F'])
    plt.show()


#Edad de los Grupos Contagiados
M = positivo.loc[(positivo.edad_años_meses=='Años') & (positivo.sexo=='M')]
M = pd.concat([M.sexo, M.edad], axis=1).dropna().sort_values('edad',ascending=True)
M = M.sexo.groupby(M.edad).count()


F = positivo.loc[(positivo.edad_años_meses=='Años') & (positivo.sexo=='F')]
F = pd.concat([F.sexo, F.edad], axis=1).dropna().sort_values('edad',ascending=True)
F = F.sexo.groupby(F.edad).count()

edad = pd.concat([M,F], axis=1).fillna(0)
edad.columns = ['M', 'F']
with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 5]
    edad.plot.bar(stacked=True)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Distribución Grupos de Contagio')
    plt.legend()
    plt.show()


caba = positivo.loc[(positivo.carga_provincia_nombre=='CABA')]
caba.clasificacion_resumen.groupby(caba.index).count()

#Curva CABA vs PBA
caba = positivo.loc[(positivo.carga_provincia_nombre=='CABA')]
pba = positivo.loc[(positivo.carga_provincia_nombre=='Buenos Aires')]

casos = {}
casos['caba'] = caba.clasificacion_resumen.groupby(caba.index).count()#.cumsum()
casos['pba'] = pba.clasificacion_resumen.groupby(pba.index).count()#.cumsum()
casos['suma'] = casos['caba'] + casos['pba']
casos = pd.DataFrame(casos)


with plt.style.context('dark_background'):
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(casos.caba, c="w",ls='-',lw=1 ,label='CABA')
    ax.plot(casos.pba, c="w",ls="solid",lw=0.5,label='PBA')
    ax.plot(casos.suma, c="r",ls="solid",lw=1.5,label='Total')
    ax.plot(casos.index, [casos.suma.median()]*len(casos),ls="-.",lw=0.4,label="Median")
    ax.legend()
    ax.set_xlabel('')
    ax.set_ylabel('Casos (+) Confirmados')
    ax.set_title("CABA vs PBA")


#Tasa de crecimiento de contagios
g = (casos.suma.cumsum().pct_change()*100).to_frame()

with plt.style.context('dark_background'):
    fig, ax = plt.subplots(figsize=(20,5))

    ax.plot(g['2020-04':],c="w")
    ax.axhline(g.suma.median(),lw=1)
    ax.set_xlabel('')
    ax.set_ylabel('Tasa %')
    ax.set_title("Tasa de Contagios")
    ax.legend(['% Contagios','Mediana'])


data.cuidado_intensivo.value_counts()

data.clasificacion_resumen.value_counts()


#CASOS POSITIVOS CON/SIN ASISTENCIA RESPIRATORIA POR PROVINCIAS
provincia = str('Buenos Aires')
asistencia = str('NO')

positivo_prov = positivo.loc[positivo.residencia_provincia_nombre==provincia]
positivo_asis = positivo_prov.loc[positivo_prov.asistencia_respiratoria_mecanica==asistencia]
positivo_asis = positivo_asis.clasificacion_resumen.groupby(positivo_asis.index).count()
positivo_asis = pd.DataFrame(positivo_asis)

with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 5]
    positivo_asis.plot(kind='line',color='white')
    plt.legend('')
    plt.xlabel('')
    plt.ylabel(f'Pacientes con Asist. Resp. = :{asistencia}')
    plt.title(f'Contagios Diarios Confirmados en {provincia}')
plt.show()


#Promedio de pacientes contagiados con/sin asistencia respiratoria
provincia = str('Buenos Aires')
asistencia = str('NO')

positivo_prov = positivo.loc[positivo.residencia_provincia_nombre==provincia]
positivo_asis = positivo_prov.loc[positivo_prov.asistencia_respiratoria_mecanica==asistencia]
positivo_asis = positivo_asis.clasificacion_resumen.groupby(positivo_asis.index).count()
positivo_asis = pd.DataFrame(positivo_asis)

print(f'En {provincia} el promedio Diario de pacientes que {asistencia} necesitan Asistencia Respiratoria es: {positivo_asis.mean()[0]:.4}')


#Discriminación por ubicación y sexo
provincia = str('CABA')
asistencia = str('SI')
sexo = str('M')


positivo_prov = positivo.loc[positivo.residencia_provincia_nombre==provincia]
positivo_asis = positivo_prov.loc[positivo_prov.asistencia_respiratoria_mecanica==asistencia]
positivo_asis = positivo_asis.loc[positivo_asis.sexo==sexo]
positivo_asis_s = positivo_asis.clasificacion_resumen.groupby(positivo_asis.index).count()
positivo_asis_s = pd.DataFrame(positivo_asis_s)

with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 6]
    positivo_asis_s.plot(kind='line',color='white')
    plt.legend('')
    plt.xlabel('')
    plt.ylabel(f'Pacientes con Asist. Resp. = :{asistencia}')
    plt.title(f'Pacientes Sexo = {sexo} | Contagios Confirmados en {provincia}')
plt.show()


#Segmentación por Grupo
edad['total'] = edad.M + edad.F
edad.loc[(edad.index>=1) & (edad.index <= 8),  'Grupo'] = 'Niño'
edad.loc[(edad.index>=9) & (edad.index <= 16),  'Grupo'] = 'Adolescente'
edad.loc[(edad.index>=17) & (edad.index <= 32), 'Grupo'] = 'Joven'
edad.loc[(edad.index>=33) & (edad.index <= 55), 'Grupo'] = 'Adulto'
edad.loc[(edad.index > 56),  'Grupo'] = 'Viejo'

grupo = edad.total.groupby(edad.Grupo).sum().to_frame()
grupo['%'] = round(grupo.total / edad.total.sum() * 100, 2)
grupo.sort_values('%',ascending=False)



plt.title('Contagios en %')
plt.pie(grupo['%'], labels=grupo.index,autopct='%1.1f%%')
plt.show()


string = 'Tucumán'
x = positivo.loc[(positivo.carga_provincia_nombre==string)]
dic = {}
dic['f:string'] = x.clasificacion_resumen.groupby(x.index).count().cumsum()
df = pd.DataFrame(dic)
df.plot()





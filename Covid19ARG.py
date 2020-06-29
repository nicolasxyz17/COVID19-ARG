# ### Covid-19 en Argentina
import pandas as pd

url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'
dataCovid = pd.read_csv(url, encoding = "UTF-16-LE")
#Exploración de los datos
print(dataCovid.columns)
###############################################################################
dataCovid.head(3)
###############################################################################
#Transformar object type a datetime type
idx = pd.to_datetime(dataCovid.fecha_apertura, format='%Y/%m/%d')
#Defino un índice como 
dataCovid = dataCovid.set_index(idx)
#Eliminar la columna 
data = dataCovid.drop('fecha_apertura',axis=1)
data.head()
################################################################################

# #### CASOS CONFIRMADOS POSITIVOS Y ACUMULADOS

covid_positivo = dataCovid.loc[dataCovid.clasificacion_resumen=='Confirmado']
covid_positivo['fecha'] = pd.to_datetime(covid_positivo.fecha_apertura, format='%Y/%m/%d')
covid_positivo = covid_positivo.set_index('fecha')

casos = {}
casos['daily_cases'] = covid_positivo.clasificacion_resumen.groupby(covid_positivo.index).count()
casos['daily_cum_cases'] = casos['daily_cases'].cumsum()
df_casos = pd.DataFrame(casos)
df_casos
####################################################################################

import matplotlib.pyplot as plt

with plt.style.context('dark_background'):
    fig, ax = plt.subplots(figsize=(20,10))

    ax.plot(df_casos.daily_cum_cases)
    ax.set_xlabel('')
    ax.set_ylabel('Casos (+) Confirmados')
    ax.set_title("ACUM. DIARIA COVID19 EN ARG.")

    eventos = [(pd.Timestamp("2020-03-20"), 'Fase I'),
               (pd.Timestamp("2020-04-01"), 'Fase II'),
               (pd.Timestamp("2020-04-14"), 'Fase III'),
               (pd.Timestamp("2020-05-11"), 'Fase IV'),
               (pd.Timestamp("2020-05-25"), 'Fase V'),
               (pd.Timestamp("2020-06-08"), 'Fase V')]

    for d, l in eventos:
        ax.annotate(l, xy=(d, df_casos.daily_cum_cases[d]), 
        xytext=(d, df_casos.daily_cum_cases[d]*1.5), color='white',
        arrowprops=dict(headwidth=10, headlength=10, width=1, facecolor='white', shrink=0.05),
        horizontalalignment='center', verticalalignment='top')
#######################################################################################

# #### Descomposición de la curva por Sexo

M = covid_positivo.loc[(covid_positivo.edad_años_meses=='Años') & (covid_positivo.sexo=='M')]
M = pd.concat([M.sexo, M.edad], axis=1).dropna().sort_values('edad',ascending=True)
M = M.sexo.groupby(M.index).count().cumsum()


F = covid_positivo.loc[(covid_positivo.edad_años_meses=='Años') & (covid_positivo.sexo=='F')]
F = pd.concat([F.sexo, F.edad], axis=1).dropna().sort_values('edad',ascending=True)
F = F.sexo.groupby(F.index).count().cumsum()

df = pd.concat([M,F], axis=1).fillna(0)

with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 5]
    df.plot.bar(stacked=True)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Discriminación por sexo')
    plt.legend(labels=['M', 'F'])
    plt.show()
    
#################################################################################

# #### Edad de los Grupos Contagiados

M = covid_positivo.loc[(covid_positivo.edad_años_meses=='Años') & (covid_positivo.sexo=='M')]
M = pd.concat([M.sexo, M.edad], axis=1).dropna().sort_values('edad',ascending=True)
M = M.sexo.groupby(M.edad).count()


F = covid_positivo.loc[(covid_positivo.edad_años_meses=='Años') & (covid_positivo.sexo=='F')]
F = pd.concat([F.sexo, F.edad], axis=1).dropna().sort_values('edad',ascending=True)
F = F.sexo.groupby(F.edad).count()

df = pd.concat([M,F], axis=1).fillna(0)
df.columns = ['M', 'F']
with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 5]
    df.plot.bar(stacked=True)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Distribución Grupos de Contagio')
    plt.legend()
    plt.show()


##########################################################################################

# #### TASA DE CRECIMEINTO EN CONTAGIOS

g = (df_casos.daily_cum_cases.pct_change()*100).to_frame()

with plt.style.context('dark_background'):
    fig, ax = plt.subplots(figsize=(20,5))

    ax.plot(g)
    ax.axhline(g.daily_cum_cases.median())
    ax.set_xlabel('')
    ax.set_ylabel('Tasa %')
    ax.set_title("Tasa de Contagios")
    ax.legend(['% Contagios','Mediana'])


####################################################################################


data.cuidado_intensivo.value_counts()

data.clasificacion_resumen.value_counts()

######################################################################################
# #### CASOS POSITIVOS CON/SIN ASISTENCIA RESPIRATORIA POR PROVINCIAS

provincia = str('Buenos Aires')
asistencia = str('NO')

covid_positivo_prov = covid_positivo.loc[covid_positivo.residencia_provincia_nombre==provincia]
covid_positivo_asis = covid_positivo_prov.loc[covid_positivo_prov.asistencia_respiratoria_mecanica==asistencia]
covid_positivo_asis = covid_positivo_asis.clasificacion_resumen.groupby(covid_positivo_asis.index).count()
covid_positivo_asis = pd.DataFrame(covid_positivo_asis)

with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 5]
    covid_positivo_asis.plot(kind='line',color='white')
    plt.legend('')
    plt.xlabel('')
    plt.ylabel(f'Pacientes con Asist. Resp. = :{asistencia}')
    plt.title(f'Contagios Diarios Confirmados en {provincia}')
plt.show()

#######################################################################################
# #### Promedio de pacientes contagiados con/sin asistencia respiratoria

provincia = str('Buenos Aires')
asistencia = str('NO')

covid_positivo_prov = covid_positivo.loc[covid_positivo.residencia_provincia_nombre==provincia]
covid_positivo_asis = covid_positivo_prov.loc[covid_positivo_prov.asistencia_respiratoria_mecanica==asistencia]
covid_positivo_asis = covid_positivo_asis.clasificacion_resumen.groupby(covid_positivo_asis.index).count()
covid_positivo_asis = pd.DataFrame(covid_positivo_asis)

print(f'En {provincia} el promedio Diario de pacientes que {asistencia} necesitan Asistencia Respiratoria es: {covid_positivo_asis.mean()[0]:.4}')


######################################################################################################

#Discriminación por ubicación y sexo
provincia = str('CABA')
asistencia = str('SI')
sexo = str('M')


covid_positivo_prov = covid_positivo.loc[covid_positivo.residencia_provincia_nombre==provincia]
covid_positivo_asis = covid_positivo_prov.loc[covid_positivo_prov.asistencia_respiratoria_mecanica==asistencia]
covid_positivo_asis = covid_positivo_asis.loc[covid_positivo_asis.sexo==sexo]
covid_positivo_asis_s = covid_positivo_asis.clasificacion_resumen.groupby(covid_positivo_asis.index).count()
covid_positivo_asis_s = pd.DataFrame(covid_positivo_asis_s)

with plt.style.context('dark_background'):
    plt.rcParams['figure.figsize'] = [20, 6]
    covid_positivo_asis_s.plot(kind='line',color='white')
    plt.legend('')
    plt.xlabel('')
    plt.ylabel(f'Pacientes con Asist. Resp. = :{asistencia}')
    plt.title(f'Pacientes Sexo = {sexo} | Contagios Confirmados en {provincia}')
plt.show()

#########################################################################################################
# #### Segmentación por Grupo

df['total'] = df.M + df.F
df.loc[(df.index>=1) & (df.index <= 8),  'Grupo'] = 'Niño'
df.loc[(df.index>=9) & (df.index <= 16),  'Grupo'] = 'Adolescente'
df.loc[(df.index>=17) & (df.index <= 32), 'Grupo'] = 'Joven'
df.loc[(df.index>=33) & (df.index <= 55), 'Grupo'] = 'Adulto'
df.loc[(df.index > 56),  'Grupo'] = 'Viejo'

grupo = df.total.groupby(df.Grupo).sum().to_frame()
grupo['%'] = round(grupo.total / df.total.sum() * 100, 2)
grupo.sort_values('%',ascending=False)


plt.title('Contagios en %')
plt.pie(grupo['%'], labels=grupo.index,autopct='%1.1f%%')
plt.show()



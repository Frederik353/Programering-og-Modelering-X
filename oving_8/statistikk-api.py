import matplotlib.pyplot as plt
import requests
import pandas as pd
from pyjstat import pyjstat  # pyjstat er for behandling av JSON-stat


### start funksjoner ###
#  Funksjon for å konvertere til datoformat og sette dette som en Pandas PeriodIndex,
#  Returnerer i tillegg navnet på frekvens-kolonnen


def dateConv(dataframe):
    frekvens, frek_no, frek_en, fmt = findFrequency(dataframe)
    setPeriodIndex(frekvens, frek_no, frek_en, fmt, dataframe)

    #funksjon for for å finne frekvenskolonne


def findFrequency(dataframe):
    frekvenser = ['måned', 'kvartal', 'uke',
                  'år', 'year', 'quarter', 'month', 'week']
    frek_no = ''
    freq_en = ''
    fmt = ''
    for w in frekvenser:
        if w in dataframe.columns:
            if w in ['måned', 'month']:
                frek_no = 'M'
                frek_en = 'M'
                fmt = '%YM%m'
            elif w in ['kvartal', 'quarter']:
                frek_no = 'K'
                frek_en = 'Q'
                fmt = '%YK%q'
            elif w in ['uke', 'week']:
                frek_no = 'U'
                frek_en = 'W'
                fmt = '%YW%W-%w'
            else:
                frek_no = ''
                frek_en = 'A'
            return w, frek_no, frek_en, fmt

# funksjon for å sette index som PeriodIndex,


def setPeriodIndex(frekvens, frek_no, freq_en, fmt, df):
    if frekvens in ['kvartal', 'quarter']:
        # erstatter K med Q, konverterr til datoformat og setter frekensen til Pandas PeriodIndex
        df.index = pd.PeriodIndex(pd.to_datetime(df[frekvens].str.replace(
            frek_no, freq_en), errors='coerce'), freq='Q-DEC')
    elif frekvens in ['uke', 'week']:
        df.index = pd.PeriodIndex(pd.to_datetime(df[frekvens].str.replace(
            frek_no, freq_en).add('-0'), format=fmt, errors='coerce'), freq='W-MON')
    else:
        df.index = pd.PeriodIndex(pd.to_datetime(
            df[frekvens], format=fmt, errors='coerce'), freq=freq_en)
    return frekvens

### slutt funksjoner ###

# URL til tabellenes metadata i PxWebApi, som vi skal poste spørringene mot


URL1 = 'https://data.ssb.no/api/v0/no/table/05327'  # KPI-jae
URL2 = 'https://data.ssb.no/api/v0/no/table/03013'  # KPI total

# API-query i JSON mot tabell 05327 - siste 5 år

sp1 = {
    "query": [
      {
          "code": "Konsumgrp",
          "selection": {
              "filter": "item",
              "values": ['JA_TOTAL', 'JAE_TOTAL', 'JE_TOTAL', 'JEL_TOTAL']
          }
      },
        {
          "code": "ContentsCode",
          "selection": {
              "filter": "item",
              "values": ["KPIJustIndMnd"]
          }
      },
        {
          "code": "Tid",
          "selection": {
              "filter": "top",
              "values": ["60"]
          }
      }
    ],
    "response": {
        "format": "json-stat2"
    }
}

# JSON-spørring mot tabell 03013 siste 5 år

sp2 = {
    "query": [
      {
          "code": "Konsumgrp",
          "selection": {
              "filter": "item",
              "values": ["TOTAL"]
          }
      },
        {
          "code": "ContentsCode",
          "selection": {
              "filter": "item",
              "values": ["KpiIndMnd"]
          }
      },
        {
          "code": "Tid",
          "selection": {
              "filter": "top",
              "values": ["60"]
          }
      }
    ],
    "response": {
        "format": "json-stat2"
    }
}


# Poster spørringene sp1 og sp2 mot metadatas url'er. Resultatene lagres som res1 og res2
res1 = requests.post(URL1, json=sp1)
res2 = requests.post(URL2, json=sp2)

# Leser resultatet med JSON-stat biblioteket pyjstat
ds1 = pyjstat.Dataset.read(res1.text)
ds2 = pyjstat.Dataset.read(res2.text)

# Skriver dette til to Pandas dataframes, df1 og df2.
df1 = ds1.write('dataframe')
df2 = ds2.write('dataframe')

df1.head(7)

df1.tail()  # slutten av datasettet

# Kaller funksjonen for datokonvertering for df1. *Kan sløyfes*.
dateConv(df1)

df1.index

df1.info()

df1.tail(15)

dateConv(df2)  # kan sløyfes eller kommenteres ut.

# Plot av df2 blir riktig, for her er det bare en serie
df2.plot()


# Standard plot av df1 gir alle 4 intervallene. Resultat er avhengig av om det er dato eller kategori på x-aksen.
df1.plot()  # standard plot gir alle 4 intervallene og resultat er avhengig av om det er dato eller kategori på x-aksen

# ### slår sammen de to "dataframene"  df1 og df2 med en enkel concat til datasettet "sammen"
sammen = pd.concat([df1, df2])

# Viser topp og bunn for det sammeslåtte datasettet
sammen.head()
sammen.tail()

# ### Omstrukturerer (pivoterer) tabellen for å få en bedre visning

df3 = sammen.pivot(columns='konsumgruppe', values='value')


# uten kall til dateconv() bruk i stedet måned som index slik:
# df3 = sammen.pivot(index='måned', columns='konsumgruppe', values='value')

df3.head(3)
df3.index
df3.tail(3)

# ### Figur med Pandas innebygde plot-funksjon
df3.plot()

# Plot med flere parametre
df3.plot(marker="o", markersize=3, figsize=(12, 8))

# Lagrer figurvisningen som en funksjon. Her er også SSBfarger definert.
# Du kan gi høyde og bredde som parametre. Her bruker vi Matplotlib og ikke Pandas plot.


def visfigur(bredde=12, hoyde=6):
    fig, ax = plt.subplots(figsize=(bredde, hoyde))
    #definerer ssb farger på figurene
    ssbCol = ['#1a9d49', '#075745', '#1d9de2', '#0f2080', '#c78800',
              '#471f00', '#c775a7', '#a3136c', '#909090', '#000000']
    plt.xlabel('måned')
    plt.ylabel('index')
    ax.set_title('Figur som viser KPI total og undeliggende KPI serier')
    df3.plot(ax=ax, color=ssbCol)
    plt.show()


visfigur()

# ### Plot med ulike stiler
# I Matplotlib kan du prøve ut ulike ferdige stiler. Vi kan evt. lage vår egen etter SSBs designmal.
#
# Prøv ut: 'Solarize_Light2',  'bmh', 'classic', 'dark_background' 'fivethirtyeight', 'seaborn-talk'
with plt.style.context('Solarize_Light2'):
    visfigur()

with plt.style.context('fivethirtyeight'):
    visfigur(16, 8)

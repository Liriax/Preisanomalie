import pandas as pd
import tsod
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("orders_price.csv", parse_dates=[0],index_col=0,header=None,names=['ArtNr','RC','Unit','Unit Price'])
df_art=df.groupby(by='ArtNr').agg({"Unit":'count'}).reset_index()
artnr=df_art.sort_values('Unit',ascending=False)['ArtNr'].to_list()
artnr=[a for a in artnr if a[0] not in ['V','S']][0:10]
fig=go.Figure()
for art in artnr:
    df_item = df[df['ArtNr']==art]
    series = df_item["Unit Price"]
    detector = tsod.RangeDetector(quantiles=[0.05,0.95])
    detector.fit(series)
    res = detector.detect(series)
    # print(series[res])
    fig.add_trace(go.Scatter(x=series.index,y=series.values,mode='lines',name=art))
    fig.add_trace(go.Scatter(x=series[res].index,y=series[res].values,mode='markers',name=art+" anomalie"))
fig.show()
    
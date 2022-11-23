import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import model
import numpy as np
from datetime import date
from statsmodels.tsa.stattools import acf, pacf

def trend_plot(past_data):
   fig = go.Figure()
   fig.add_scatter(x= past_data['date'], y= past_data['close'], name= "actual")
   fig.add_scatter(x = past_data['date'], y= past_data['close'].rolling(30).mean(), name= "trend")
   fig.update_layout(title= "Trend of prices", height= 400, template='ggplot2', xaxis_title= "Day", yaxis_title= "Price", paper_bgcolor="LightSteelBlue")
   return fig

def box_plot(past_data):
   past_data['date'] = pd.to_datetime(past_data['date'])
   past_data['month'] = past_data['date'].dt.strftime('%m')
   today = str(date.today())
   last_year = str(int(today[:4]) - 1)
   past_data = past_data.drop(past_data[past_data['date'].dt.strftime('%Y') == last_year].index).reset_index(drop= True)
   fig = px.box(past_data, x='month', y= 'close')
   fig.update_layout(title= 'Comparison between months',height= 400, template= 'ggplot2', xaxis_title= "Month", yaxis_title= "Price", paper_bgcolor="LightSteelBlue")
   return fig   

def acf_pacf_plot(past_data, plot_pacf):
   corr_array = pacf(past_data['date'].dropna(), alpha=0.05) if plot_pacf else acf(past_data['date'].dropna(), alpha=0.05)
   lower_y = corr_array[1][:,0] - corr_array[0]
   upper_y = corr_array[1][:,1] - corr_array[0]
   fig = go.Figure()
   [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='#3f3f3f') 
    for x in range(len(corr_array[0]))]
   fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                  marker_size=12)
   fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
   fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
                  fill='tonexty', line_color='rgba(255,255,255,0)')
   fig.update_traces(showlegend=False)
   title='Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
   fig.update_layout(title=title, paper_bgcolor= "LightSteelBlue")
   
   return fig

def prediction_plot(time_step, num_day_shown, data):
   if num_day_shown != 89 and num_day_shown != 14:
      num_day_shown = 365 + 14
   modeled_data = model.my_model(data= data, num_day_shown=num_day_shown, time_step= time_step)
   trace = go.Figure()
   trace.add_scatter(x= modeled_data['date'], y= modeled_data['close'], name= 'actual')
   trace.add_scatter(x= modeled_data['date'], y= modeled_data['valid_pred'], name= 'valid prediction')
   trace.add_scatter(x= modeled_data['date'], y= modeled_data['future_pred'], name= 'prediction for 14 days next')
   trace.update_layout(title= 'Prediction for next 2 weeks', height= 400, template='ggplot2', xaxis_title= "Day", yaxis_title= "Price", paper_bgcolor="LightSteelBlue")
   return [go.Figure(data= trace)]
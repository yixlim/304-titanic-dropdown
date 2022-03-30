######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/plotly-dash-apps/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Female']=df['Sex'].map({'male':0, 'female':1})
df['Embarked'].map({'Southampton':'Southampton', 'Cherbourg': 'Cherbourg', 'Queenstown':'Queenstown'})
df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list=['Survived', 'Female', 'Fare', 'Age']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_count=pd.DataFrame(df.groupby(['Embarked','Pclass'])[continuous_var].count())
results=pd.DataFrame(grouped_count)
    # Create a grouped bar chart
    
mydata1 = go.Bar(
    x=results.loc['Cherbourg'].index,
    y=results.loc['Cherbourg'][continuous_var],
    name='Cherbourg',
    marker=dict(color='darkgreen')
    )
mydata2 = go.Bar(
        x=results.loc['Queenstown'].index,
        y=results.loc['Queenstown'][continuous_var],
        name='Queenstown',
        marker=dict(color='lightblue')
    )
mydata3 = go.Bar(
        x=results.loc['Southampton'].index,
        y=results.loc['Southampton'][continuous_var],
        name='Southampton',
        marker=dict(color='orange')
    )

mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Class'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)

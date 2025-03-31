import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Загрузка данных (пример - можно заменить на ваш источник)
data = {
    "Countries": ["India", "China", "United States", "Turkey", "Russia"],
    "Q1'20": [101.9, 106.5, 37.7, 31.9, 10.8],
    "Q2'20": [63.7, 137.0, 32.8, 23.9, 4.9]
    # ... (остальные кварталы из ваших данных)
}

df = pd.DataFrame(data)

# Создаем список всех кварталов для удобства
quarters = [col for col in df.columns if col != 'Countries']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Квартальные экономические показатели стран (2020-2023)"),
    
    html.Div([
        html.Label("Выберите страну:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Countries']],
            value='India',
            clearable=False
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.Label("Выберите показатель для сравнения:"),
        dcc.Dropdown(
            id='compare-dropdown',
            options=[{'label': 'Без сравнения', 'value': 'none'}] + 
                   [{'label': country, 'value': country} for country in df['Countries']],
            value='none'
        )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    
    dcc.Graph(id='quarterly-plot'),
    
    html.Div([
        html.H3("Статистика по выбранной стране:"),
        html.Div(id='country-stats')
    ])
])

@app.callback(
    [Output('quarterly-plot', 'figure'),
     Output('country-stats', 'children')],
    [Input('country-dropdown', 'value'),
     Input('compare-dropdown', 'value')]
)
def update_graph(selected_country, compare_country):
    # Основной график
    fig = px.line(
        title=f"Динамика показателей: {selected_country}" + 
              (f" vs {compare_country}" if compare_country != 'none' else "")
    )
    
    # Добавляем основную страну
    country_data = df[df['Countries'] == selected_country].iloc[0]
    fig.add_scatter(
        x=quarters, 
        y=country_data[quarters],
        name=selected_country,
        line=dict(width=4)
    )
    
    # Добавляем страну для сравнения (если выбрана)
    if compare_country != 'none':
        compare_data = df[df['Countries'] == compare_country].iloc[0]
        fig.add_scatter(
            x=quarters, 
            y=compare_data[quarters],
            name=compare_country,
            line=dict(dash='dot')
        )
    
    # Статистика
    stats = [
        html.P(f"Среднее значение: {country_data[quarters].mean():.1f}"),
        html.P(f"Максимальное значение: {country_data[quarters].max():.1f} (в {country_data[quarters].idxmax()})"),
        html.P(f"Минимальное значение: {country_data[quarters].min():.1f} (в {country_data[quarters].idxmin()})"),
        html.P(f"Последний квартал: {country_data[quarters[-1]]:.1f} ({quarters[-1]})")
    ]
    
    return fig, stats

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
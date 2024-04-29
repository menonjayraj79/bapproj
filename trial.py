import dash
from dash import dcc
from dash import html
import pandas as pd 
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
import sqlite3

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df = pd.read_excel('Acomplete.xlsx')

# Connect to the SQLite database
conn = sqlite3.connect('marks.db')  # Replace 'your_database_name.db' with your actual database name
df.to_sql("marks", conn, index=False)  # 'projects' is the table name
# Read data from the SQLite database into a DataFrame
query = "SELECT * FROM marks"  # Replace 'your_table_name' with your actual table name
marks = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Now you have your data in the 'marks' DataFrame
print(marks.head())  # Check the first few rows to verify

# Define dropdown options
dropdown_options = [
    {'label': 'sub 1', 'value': 'Bcomplete.xlsx'},
    {'label': 'sub 2', 'value': 'Ccomplete.xlsx'},
    {'label': 'sub 3', 'value': 'Acomplete.xlsx'}
]

# Create dropdown component
dropdown = dcc.Dropdown(
    id='file-dropdown',
    options=dropdown_options,
    value='Acomplete.xlsx',
    style={'margin-bottom': '5px'}
)

# Read data from selected Excel file
marks = pd.read_excel(dropdown.value)


@app.callback(
    dash.dependencies.Output('marks', 'children'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_marks(selected_file):
    marks = pd.read_excel(selected_file)
    return html.Table([
        # html.Thead(
        #     html.Tr([html.Th(col) for col in marks.columns])
        # ),
        # html.Tbody([
        #     html.Tr([
        #         html.Td(marks.iloc[i][col]) for col in marks.columns
        #     ]) for i in range(len(marks))
        # ])
    ])


# Calculate the proportion of students who achieved different ranges of lab scores
@app.callback(
    dash.dependencies.Output('pie', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_pie_chart(selected_file):
    marks = pd.read_excel(selected_file)
    lab_scores_ranges = pd.cut(marks['labConverted40'], bins=[
                               0, 10, 20, 30, 40], labels=['0-10', '10-20', '20-30', '30-40'])
    lab_scores_proportions = lab_scores_ranges.value_counts(normalize=True)

    pie_chart = {
        'data': [
            {
                'values': lab_scores_proportions.values,
                'labels': lab_scores_proportions.index,
                'type': 'pie',
                'name': 'Lab Scores',
                'hoverinfo': 'label+percent+name',
                'hole': .3,
                'marker': {
                    'colors': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA'],
                    'line': {'color': 'white', 'width': 2}

                },
                'textfont': {'color': 'white'},
                'textposition': 'inside',
                'textinfo': 'percent'
            }
        ],
        'layout': {
            'title': 'Lab Performance Analysis',
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }

    return pie_chart


# Calculate average marks for each year
yearly_average_marks = marks.groupby('year')['total100'].mean()

# Create line graph for performance over time
performance_line_graph = dcc.Graph(
    id='performance_line',
    figure={
        'data': [
            {
                'x': yearly_average_marks.index,
                'y': yearly_average_marks.values,
                'mode': 'lines',
                'name': 'Avg Marks'
            }
        ],
        'layout': {
            'title': 'Performance Over Time',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Average Marks'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the graph based on dropdown selection


@app.callback(
    dash.dependencies.Output('performance_line', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_performance_line(selected_file):
    marks = pd.read_excel(selected_file)
    yearly_average_marks = marks.groupby('year')['total100'].mean()

    line_graph = {
        'data': [
            {
                'x': yearly_average_marks.index,
                'y': yearly_average_marks.values,
                'mode': 'lines',
                'name': 'Avg Marks'
            }
        ],
        'layout': {
            'title': 'Performance Over Time',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Average Marks'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }

    return line_graph


# Create histogram for Credit and Pointer Distribution
histogram = dcc.Graph(
    id='histogram',
    figure={
        'data': [
            {
                'x': marks['creditObt40'],
                'name': 'Credits Obtained',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#636EFA'
                }
            },
            {
                'x': marks['pointer10'],
                'name': 'Pointers',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#EF553B'
                }
            }
        ],
        'layout': {
            'title': 'Credit and Pointer Distribution',
            'xaxis': {'title': 'Value', 'color': 'white'},
            'yaxis': {'title': 'Number of Students', 'color': 'white'},
            'barmode': 'overlay',
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the histogram based on dropdown selection


@app.callback(
    dash.dependencies.Output('histogram', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_histogram(selected_file):
    marks = pd.read_excel(selected_file)
    histogram_figure = {
        'data': [
            {
                'x': marks['creditObt40'],
                'name': 'Credits Obtained',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#636EFA'
                }
            },
            {
                'x': marks['pointer10'],
                'name': 'Pointers',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#EF553B'
                }
            }
        ],
        'layout': {
            'title': 'Credit and Pointer Distribution',
            'xaxis': {'title': 'Value', 'color': 'white'},
            'yaxis': {'title': 'Number of Students', 'color': 'white'},
            'barmode': 'overlay',
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return histogram_figure


# Group data by teacher and get marks
teacher_marks = marks.groupby('teacher')['total100']

# Create box plot
box_plot = dcc.Graph(
    id='box',
    figure={
        'data': [
            {
                'y': teacher_marks.get_group(x),
                'type': 'box',
                'name': x,
                'marker': {
                    'color': '#00CC96'
                },
                'boxpoints': 'all',
                'jitter': 0.3,
                'pointpos': -1.8
            } for x in teacher_marks.groups
        ],
        'layout': {
            'title': 'Teacher-wise Performance Comparison',
            'yaxis': {'title': 'Marks', 'color': 'white'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the box plot based on dropdown selection


@app.callback(
    dash.dependencies.Output('box', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_box_plot(selected_file):
    marks = pd.read_excel(selected_file)
    teacher_marks = marks.groupby('teacher')['total100']
    box_plot_figure = {
        'data': [
            {
                'y': teacher_marks.get_group(x),
                'type': 'box',
                'name': x,
                'marker': {
                    'color': '#00CC96'
                },
                'boxpoints': 'all',
                'jitter': 0.3,
                'pointpos': -1.8
            } for x in teacher_marks.groups
        ],
        'layout': {
            'title': 'Teacher-wise Performance Comparison',
            'yaxis': {'title': 'Marks', 'color': 'white'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return box_plot_figure


# Calculate average grades for each attendance percentage
attendance_grades = marks.groupby('lecAttendance100')[
    'theoryConverted60'].mean()

# Create line graph
line_graph = dcc.Graph(
    id='line',
    figure={
        'data': [
            {
                'x': attendance_grades.index,
                'y': attendance_grades.values,
                'mode': 'lines',
                'name': 'Avg Grade',
                'line': {'color': '#AB63FA'}
            }
        ],
        'layout': {
            'title': 'Attendance Impact on Grades',
            'xaxis': {'title': 'Attendance Percentage', 'color': 'white'},
            'yaxis': {'title': 'Average Grade', 'color': 'white'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the line graph based on dropdown selection


@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_line_graph(selected_file):
    marks = pd.read_excel(selected_file)
    attendance_grades = marks.groupby('lecAttendance100')[
        'theoryConverted60'].mean()
    line_graph_figure = {
        'data': [
            {
                'x': attendance_grades.index,
                'y': attendance_grades.values,
                'mode': 'lines',
                'name': 'Avg Grade',
                'line': {'color': '#AB63FA'}
            }
        ],
        'layout': {
            'title': 'Attendance Impact on Grades',
            'xaxis': {'title': 'Attendance Percentage', 'color': 'white'},
            'yaxis': {'title': 'Average Grade', 'color': 'white'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return line_graph_figure


# Update the callback function to update the scatter plot based on dropdown selection


@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_scatter_plot(selected_file):
    marks = pd.read_excel(selected_file)
    scatter_plot_figure = {
        'data': [
            {
                'x': marks['theoryConverted60'],
                'y': marks['labConverted40'],
                'mode': 'markers',
                'name': 'Students',
                'marker': {
                    'color': '#AB63FA',
                    'size': 8,
                    'line': {'color': 'black    ', 'width': 0.5}
                }
            }
        ],
        'layout': {
            'title': 'Correlation between Theory and Lab Scores',
            'xaxis': {'title': 'Theory Scores', 'color': 'white'},
            'yaxis': {'title': 'Lab Scores', 'color': 'white'},
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black  ',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return scatter_plot_figure


# Update the callback function to update the bar chart based on dropdown selection
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_bar_chart(selected_file):
    marks = pd.read_excel(selected_file)
    average_ise = marks['iseA20'].mean()
    average_mse = marks['mse30'].mean()
    average_ese = marks['ese100'].mean()

    return {
        'data': [
            {'x': ['ISE', 'MSE', 'ESE'], 'y': [average_ise, average_mse,
                                               average_ese], 'type': 'bar', 'name': 'Avg Score',
             'marker': {'color': ['#636EFA', '#EF553B', '#00CC96']},
             'textfont': {'color': 'white'},
             'textposition': 'auto',
             'text': [f'{avg:.2f}' for avg in [average_ise, average_mse, average_ese]]
             }
        ],
        'layout': {
            'title': 'Performance Distribution by Exam Type',
            'paper_bgcolor': 'black ',
            'plot_bgcolor': 'black',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }


tab1_content = html.Div([
    html.Div(id='marks'),
    html.H1(children='Performance Distribution by Exam Type',
            style={'color': 'white'}),
    dcc.Graph(
        id='graph',
        style={'paper_bgcolor': 'black  ', 'plot_bgcolor': 'black '},

    )],
    className="mt-1 mb-3",
)

tab2_content = html.Div([
    html.H1(children='Correlation between Theory and Lab Scores',
            style={'color': 'white'}),
    dcc.Graph(
        id='scatter',
        style={'paper_bgcolor': 'black  ', 'plot_bgcolor': 'black '},

    ),],
    className="mt-1 mb-3",
)
tab3_content = html.Div([
    html.H1(children='Attendance Impact on Grades',
            style={'color': 'white'}),
    line_graph,],
    className="mt-1 mb-3",
)
tab4_content = html.Div([
    html.H1(children='Teacher-wise Performance Comparison',
            style={'color': 'white'}),
    box_plot,],
    className="mt-1 mb-3",
)
tab5_content = html.Div([
    html.H1(children='Credit and Pointer Distribution',
            style={'color': 'white'}),
    histogram,],
    className="mt-1 mb-3",
)
tab6_content = html.Div([
    html.H1(children='Performance Over Time', style={'color': 'white'}),
    performance_line_graph,],
    className="mt-1 mb-3",
)
tab7_content = html.Div([
    html.H1(children='Lab Performance Analysis', style={'color': 'white'}),
    dcc.Graph(
        id='pie',
        style={'paper_bgcolor': 'black  ', 'plot_bgcolor': 'black '},

    ),],
    className="mt-1 mb-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(tab3_content, label="Tab 3"),
        dbc.Tab(tab4_content, label="Tab 4"),
        dbc.Tab(tab5_content, label="Tab 5"),
        dbc.Tab(tab6_content, label="Tab 6"),
        dbc.Tab(tab7_content, label="Tab 7"),
    ]
)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="black",
    dark=True,
    className=" mb-3",  # Add bottom margin
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.layout = dbc.Container(dbc.Container(html.Div(
    children=[
        navbar,
        dropdown,
        # accordion,
        tabs
    ],
    style={'background': 'black',
           'color': 'white', 'font-family': 'Arial'}
)))

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)  

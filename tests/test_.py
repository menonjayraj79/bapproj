import pandas as pd
from dash.testing.application_runners import import_app
from dash.dependencies import Input, Output
from dash import html

# Import the callback function you want to test
from test import update_pie_chart, update_performance_line, update_histogram, toggle_navbar_collapse
# from test2 import update_bar_chart

# Define the test function
def test_update_pie_chart():
    # Load the Dash app 
    
    # Define the test input value
    selected_file = "Acomplete.xlsx"  # Assuming you have a test Excel file
    
    response = update_pie_chart(selected_file)
    print(response)

    
    # Assert the output
    expected_output = {
        'data': [
            {
                'values': [47,53,45,67],  # Example values
                'labels': ['0-10','10-20','20-30','30-40'],  # Example labels
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
    
    print(expected_output)
    assert response == expected_output

def test_update_performance_line():
    # Load the Dash app
    selected_file = "Acomplete.xlsx"
    # Define the test input value
    # Assuming you have a test Excel file
    
    # Simulate the callback
    response = update_performance_line(selected_file)

    # Assert the output
    expected_output = {
        'data': [
            {
                'x': [2018, 2019, 2020],  # Example years
                'y': [85, 88, 90],  # Example average marks
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
    
    assert response == expected_output

def test_update_histogram():
    # Load the Dash app

    # Define the test input value
    selected_file = "Acomplete.xlsx"  # Assuming you have a test Excel file
    
    # Simulate the callback
    response = update_histogram(selected_file)

    # Assert the output
    expected_output = {
        'data': [
            {
                'x': [40, 35, 30, 25, 20],  # Example data for 'creditObt40'
                'name': 'Credits Obtained',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#636EFA'
                }
            },
            {
                'x': [9.5, 9, 8.5, 8, 7.5],  # Example data for 'pointer10'
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
    
    assert response == expected_output

# Define the test function
def test_toggle_navbar_collapse():

    # Simulate the initial state of the navbar collapse component
    initial_is_open = False

    # Simulate clicking the navbar toggler button
    n_clicks = 1

    # Simulate the callback
    response = toggle_navbar_collapse(n_clicks, initial_is_open)

    # Assert the output
    expected_output = not initial_is_open
    assert response == expected_output



# Define the test function
# def test_update_bar_chart():

#     # Simulate the UID value entered by the user
#     uid_value = '2010300032'

#     # Simulate clicking the submit button
#     n_clicks = 1

#     # Simulate the callback
#     response = update_bar_chart(n_clicks, uid_value)

#     # Assert the output figure
#     expected_data = [
#         go.Bar(
#             x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
#             y=[10,20,30,40,50],  # Example scores
#             name='ISE',
#             marker=dict(color='rgb(255, 0, 0)')
#         ),
#         go.Bar(
#             x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
#             y=[10,20,30,40,50],  # Example scores
#             name='MSE',
#             marker=dict(color='rgb(0, 255, 0)')
#         ),
#         go.Bar(
#             x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
#             y=[10,20,30,40,50],  # Example scores
#             name='ESE',
#             marker=dict(color='rgb(0, 0, 255)')
#         )
#     ]
#     expected_layout = go.Layout(
#         title='Exam Type Performance Across Courses',
#         xaxis=dict(title='Courses'),
#         yaxis=dict(title='Scores'),
#         barmode='group',
#         plot_bgcolor='rgb(17, 17, 17)',
#         paper_bgcolor='rgb(17, 17, 17)',
#         font=dict(color='rgb(255, 255, 255)')
#     )
#     expected_figure = go.Figure(data=expected_data, layout=expected_layout)

#     assert response == expected_figure        
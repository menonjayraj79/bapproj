import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(
    [
        # html.Label('Dropdown to choose from the choices'),
        # dcc.Dropdown(
        #     id='dropdown',
        #     options=[
        #         {'label': 'Option 1', 'value': 'option1'},
        #         {'label': 'Option 2', 'value': 'option2'},
        #         {'label': 'Option 3', 'value': 'option3', 'disabled': True},
        #     ],
        #     # value='option1',
        #     multi=True,
        #     placeholder='Please select...',
        #     # disabled=False,
        # ),

        # dcc.Slider(
        #     id='slider',
        #     min=0,
        #     max=10,
        #     step=0.5,
        #     value=5,
        #     marks={str(i): str(i) for i in range(11)},
        #     tooltip={'placement': 'bottom'}
        # ),

        # dcc.RangeSlider(
        #     id='range_slider',
        #     min=0,
        #     max=10,
        #     step=0.5,
        #     value=[3, 7],
        #     marks={str(i): str(i) for i in range(11)},
        #     tooltip={'placement': 'bottom'}
        # ),

        # dcc.Input(
        #     id='input',
        #     type='text',
        #     # value='input',
        #     placeholder='Type something...',
        #     debounce=True,
        #     # disabled=False,
        #     maxLength=10,
        #     minLength=5,
        #     # required=True
        # ),

        # dcc.Textarea(
        #     id='textarea',
        #     placeholder='Enter a value...',
        #     value='This is a TextArea component',
        #     style={'width': '100%'}
        # ),
        # html.Button('Submit', id='button', n_clicks=0),

        # dcc.Checklist(
        #     id='checklist',
        #     options=[
        #         {'label': 'Option 1', 'value': 'option1'},
        #         {'label': 'Option 2', 'value': 'option2'},
        #         {'label': 'Option 3', 'value': 'option3', 'disabled': True},
        #     ],
        #     value=['option1', 'option2'],
        #     inline=True,
        #     # switch=True,
        # ),

        # dcc.RadioItems(
        #     id='radio',
        #     options=[
        #         {'label': 'Option 1', 'value': 'option1'},
        #         {'label': 'Option 2', 'value': 'option2'},
        #         {'label': 'Option 3', 'value': 'option3', 'disabled': True},
        #     ],
        #     value='option1',
        #     inline=True,
        #     # switch=True,
        # ),



        # dcc.DatePickerSingle(
        #     id='date_picker_single',
        #     date='2021-06-01',
        #     display_format='YYYY-MM-DD',
        #     # with_portal=True,
        #     # number_of_months_shown=1,
        #     # placeholder='Select a date',
        #     # initial_visible_month='2021-06-01',
        #     # day_size=50,
        #     # is_RTL=True,
        #     # show_outside_days=True,
        #     # with_full_screen_portal=True,
        #     # month_format='MMMM, YYYY',
        #     # first_day_of_week=1,
        #     # reopen_calendar_on_clear=True,
        #     # clearable=True,
        #     # # disabled=True,
        #     # min_date_allowed='2021-06-01',
        #     # max_date_allowed='2021-06-30',
        # )


        dcc.DatePickerRange(
            id='date_picker_range',
            start_date='2021-06-01',
            end_date='2021-06-30',
            display_format='YYYY-MM-DD',
            # with_portal=True,
            # number_of_months_shown=1,
            # placeholder='Select a date',
            # initial_visible_month='2021-06-01',
            # day_size=50,
            # is_RTL=True,
            # show_outside_days=True,
            # with_full_screen_portal=True,
            # month_format='MMMM, YYYY',
            # first_day_of_week=1,
            # reopen_calendar_on_clear=True,
            # clearable=True,
            # # disabled=True,
            # min_date_allowed='2021-06-01',
            # max_date_allowed='2021-06-30',

        ),

        dcc.Markdown('''
                     **Markdown** is a way to style text on the web. You control the display of the document;
                        formatting words as bold or italic, adding images, and creating lists are just a few of the things we can do with Markdown.
                        '''),
    ]

)

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, ALL, MATCH
from dash_iconify import DashIconify
from flask import Flask

from phone import PhoneColorPalette, Phone

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)


phones = [Phone("blue", height="65vh", number="+1 719 212 2797", id=0),
          Phone("green", height="65vh", id=1),
          Phone("pink", height="65vh", id=2),
          Phone("white", height="65vh", id=3)]

app.layout = dbc.Container(
    [html.H1("Your virtual phones : "), html.Div([html.Div([phone, html.P(phone.number)],
                                                           className="d-flex flex-column justify-content-center align-items-center")
                                                  for phone in phones],
                                                 className="d-flex flex-row"),
     ],
    className="p-5 d-flex flex-column")


# [phone, html.P(phone.number)]
def get_phone_by_number(number):
    for phone in phones:
        if phone.number == number:
            return phone
    return None


@app.callback(
    Output({'label': 'phone-text', 'index': MATCH}, "children"),
    [Input({'label': 'send-message-phone', 'index': MATCH}, "n_clicks")],
    State({'label': 'phone-text-area', 'index': MATCH}, "value"),
    prevent_initial_call=True
)
def send_input(n_clicks, value):
    phone = get_phone_by_number("+1 719 212 2797")
    if n_clicks is None:
        return "Please enter a number"
    else:
        phone.messages_list.append(value)
        children = [html.Div(
            f"{message}",
            style={"color": "black", "background-color": "white", "border-radius": "10px", "padding": "5px",
                   "border": "1px solid gray", "font-size": "0.8rem", "margin": "0.5rem"}) for message in
            phone.messages_list]

        print("Sending message: " + value + " to +33637890663 from " + phone.number)
        phone.send_sms(value, "+33637890663")
        return children


palette = PhoneColorPalette("blue")


@app.callback(
    Output({'label': 'phone-container', 'index': MATCH}, "children"),
    Input({'label': 'phone-go-contact', 'index': MATCH}, "n_clicks"),
    State({'label': 'phone-container', 'index': MATCH}, "children"),
    prevent_initial_call=True
)
def go_contact(n_clicks, children):
    if n_clicks is None:
        return children
    else:
        id = 5000
        header = html.Div(
            [
                html.Div(
                    [html.Div(
                        DashIconify(icon="openmoji:anger-symbol", width=30, color=f"{palette.high_contrast}")),
                        html.H6("Absolute 0", style={"color": "black"})],
                    className="d-flex flex-row justify-content-center align-items-center p-2 gap-2"),
            ],

            id={'label': 'phone-top', 'index': id},
            style={"width": "100%",
                   "min-height": "10%",
                   "position": "relative",
                   "height": "10%", "background-color": f"{palette.top}",
                   "borderRadius": "10px 10px 0px 0px",
                   "border-bottom": f"3px ridge {palette.buttons}"},
            className="d-flex flex-row justify-content-center align-items-center p-2")

        children = [html.Div([  # Equivalent to `html.Div([...])`
            # Header
            header,

            # Messages
            html.Div(),

            # Footer
        ], style={"position": "absolute", "top": "0px", "left": "0px", "bottom": "0px", "right": "0px",
                  "overflow": "auto"}),
            html.Div(),

        ]
        return children


if __name__ == "__main__":
    app.run_server()

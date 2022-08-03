import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, ALL, MATCH
from dash_iconify import DashIconify
from flask import Flask

from phone import PhoneColorPalette, Phone

# https://hackersandslackers.com/plotly-dash-with-flask/
# server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

phones = [Phone("blue", height="65vh", number="+1 719 212 2797", id=0),
          Phone("green", height="65vh", width="45vw", id=1),
          Phone("pink", height="40vh", id=2),
          Phone("white", height="65vh", id=3)]

app.layout = html.Div([dbc.Container(
    [html.H1("Your virtual phones : "), html.Div([html.Div([phone, html.P(phone.number)],
                                                           className="d-flex flex-column justify-content-center align-items-center")
                                                  for phone in phones],
                                                 className="d-flex flex-row"),
     ],
    className="p-5 d-flex flex-column",
    )],
    style={"background": "linear-gradient(#FFF59D, #B2EBF2)", "position": "absolute", "top": "0", "left": "0",
           "bottom": "0", "right": "0"}
)


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
    Input({'label': 'phone-go-to-mail', 'index': MATCH}, "n_clicks"),
    State({'label': 'phone-container', 'index': MATCH}, "children"),
    prevent_initial_call=True
)
def go_contact(n_clicks, n_clicks_, children):
    label, index = dash.ctx.triggered_id["label"], dash.ctx.triggered_id["index"]
    print(label, index)
    phone = get_phone_by_number("+1 719 212 2797")
    if label == "phone-go-contact":
        return [phone.messaging_screen("none"), phone.main_screen("block")]
    elif label == "phone-go-to-mail":
        return [phone.messaging_screen("block"), phone.main_screen("none")]


"""@app.callback(
    Output({'label': 'phone-container', 'index': MATCH}, "children")),
    Input({'label': 'phone-go-to-contact-list', 'index': MATCH}, "n_clicks"),"""
if __name__ == "__main__":
    app.run_server(host="localhost", port=8080, debug=True)

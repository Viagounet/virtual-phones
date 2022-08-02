import re
from cgitb import html
import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify

from send_sms import send_sms_to


class PhoneColorPalette:
    def __init__(self, color):
        self.colors = {
            'blue': ["#BBDEFB", "#EEFFFF", "#8AACC8", "#293137"],
            'green': ["#C8E6C9", "#FBFFFC", "#97B498", "#353D35"],
            'pink': ["#F8BBD0", "#FFFFFF", "#C9B2BA", "#423238"],
            'white': ["#FAFAFA", "#FFFFFF", "#C7C7C7", "#1A1A1A"], }

        self.top = self.colors[color][0]
        self.bg = self.colors[color][1]
        self.buttons = self.colors[color][2]
        self.high_contrast = self.colors[color][3]


class Phone(html.Div):
    def __init__(self, color, id, number="None", height="auto", width="auto", **kwargs):
        self.number = number
        self.recipient = "TDK"
        self.messages_list = ["Yes this is a test", "and another test"]
        if self.number == "None":
            self.number = "No number set"
            self.recipient = ""
            self.messages_list = []

        self.messages = html.Div([html.Div(
            f"{message}",
            style={"color": "black", "background-color": "white", "border-radius": "10px", "padding": "5px",
                   "border": "1px solid gray", "font-size": "0.8rem", "margin": "0.5rem"}) for message in
            self.messages_list],
        id={'label': 'phone-text', 'index': id})

        if height != "auto" and width == "auto":
            value = float(re.sub("[^0-9]", "", height))
            measure = re.sub('[^a-zA-Z]+', '', height)
            width = str(value / 2) + measure
        elif height == "auto" and width != "auto":
            value = float(re.sub("[^0-9]", "", width))
            measure = re.sub('[^a-zA-Z]+', '', width)
            height = str(value * 2) + measure

        palette = PhoneColorPalette(color)
        self.footer = html.Div([
            html.Div([
                dbc.Input(placeholder="Your text message", id={'label': 'phone-text-area', 'index': id}),
                html.Div(DashIconify(icon="material-symbols:send-rounded", width=30, color=f"{palette.buttons}",
                                     ), id={'label': 'send-message-phone', 'index': id}, className="send-button")
            ], className="d-flex flex-row justify-content-center align-items-center p-2 gap-2")
        ],
            style={"width": "100%", "position": "absolute", "bottom": "0%", "background-color": f"{palette.bg}",
                   "borderRadius": "0px 0px 10px 10px"})

        self.header = html.Div(
            [
                html.Div(
                    [html.Div(
                        DashIconify(icon="material-symbols:contact-page", width=30, color=f"{palette.high_contrast}"),
                        className="send-button", id={'label': 'phone-go-contact', 'index': id}),
                        html.H6(self.recipient, style={"color": "black"})],
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

        super().__init__(
            [html.Div([  # Equivalent to `html.Div([...])`
                # Header
                self.header,

                # Messages
                self.messages,

                # Footer
            ], style={"position": "absolute", "top": "0px", "left": "0px", "bottom": "0px", "right": "0px",
                      "overflow": "auto"}),
                self.footer,

            ],

            style={'color': 'white', 'backgroundColor': f"{palette.bg}",
                   "width": width, "height": height, "border": "7px gray ridge",
                   "borderRadius": "20px", "margin": "10px", "position": "relative"},
            className="phone",
            id={'label': 'phone-container', 'index': id},
        )

    def send_sms(self, content, recipient):
        send_sms_to(content, recipient, self.number)


"""{'color': 'white', 'backgroundColor': f"{palette.bg}",
                       "width": width, "height": height, "border": "7px gray ridge",
                       "borderRadius": "20px", "margin": "10px"}"""

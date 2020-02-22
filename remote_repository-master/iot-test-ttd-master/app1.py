import os
import pathlib

import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, request,render_template
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq

import pandas as pd
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
LOGO = "https://www.tirumala.org/NewImages/TTD-Logo.png"
LOGO1= "https://www.tirumala.org/NewImages/HD-TXT.png"


server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = 'smarttrak'
api = Api(server)
db = SQLAlchemy()

db.init_app(server)

@server.before_first_request
def create_tables():
    db.create_all()

class DeviceModel(db.Model):
    __tablename__ = 'devices'

    devId = db.Column(db.String(20), primary_key=True)
    tstamp =db.Column(db.Float(precision=2))
    rphvol = db.Column(db.Float(precision=2))
    yphvol = db.Column(db.Float(precision=2))
    bphvol = db.Column(db.Float(precision=2))
    rphcu = db.Column(db.Float(precision=2))
    yphcu = db.Column(db.Float(precision=2))
    bphcu = db.Column(db.Float(precision=2))
    necu = db.Column(db.Float(precision=2))
    phrpwr = db.Column(db.Float(precision=2))
    phrpwrfun = db.Column(db.Float(precision=2))
    phrepwr = db.Column(db.Float(precision=2))
    ph3pwr = db.Column(db.Float(precision=2))
    freq = db.Column(db.Float(precision=2))
    rphpf = db.Column(db.Float(precision=2))
    yphpf = db.Column(db.Float(precision=2))
    bphpf = db.Column(db.Float(precision=2))
    avgpf = db.Column(db.Float(precision=2))
    rphang = db.Column(db.Float(precision=2))
    yphang = db.Column(db.Float(precision=2))
    bphang = db.Column(db.Float(precision=2))
    avgvol = db.Column(db.Float(precision=2))
    actfwdABS= db.Column(db.Float(precision=2))
    apfwdABS = db.Column(db.Float(precision=2))
    relagfwdABS= db.Column(db.Float(precision=2))
    releadfwdABS = db.Column(db.Float(precision=2))


    def __init__(self, devId,tstamp,rphvol,yphvol,bphvol,rphcu,
                    yphcu,bphcu,necu,phrpwr,phrpwrfun,phrepwr,
                    ph3pwr,freq,rphpf,yphpf,bphpf,avgpf,rphang,yphang,
                    bphang,avgvol,actfwdABS,apfwdABS,relagfwdABS,releadfwdABS):
        self.devId = devId
        self.tstamp= tstamp
        self.rphvol = rphvol
        self.yphvol = yphvol
        self.bphvol = bphvol
        self.rphcu = rphcu
        self.yphcu = yphcu
        self.bphcu = bphcu
        self.necu = necu
        self.phrpwr = phrpwr
        self.phrpwrfun = phrpwrfun
        self.phrepwr = phrepwr
        self.ph3pwr = ph3pwr
        self.freq = freq
        self.rphpf = rphpf
        self.yphpf = yphpf
        self.bphpf = bphpf
        self.avgpf = avgpf
        self.rphang = rphang
        self.yphang = yphang
        self.bphang = bphang
        self.avgvol = avgvol
        self.actfwdABS = actfwdABS
        self.apfwdABS = apfwdABS
        self.relagfwdABS = relagfwdABS
        self.releadfwdABS = releadfwdABS

    def json(self):
        return {'devId': self.devId,'tstamp':self.tstamp,'rphvol': self.rphvol,'yphvol': self.yphvol,'bphvol': self.bphvol,'rphcu': self.rphcu,'yphcu': self.yphcu,'bphcu': self.bphcu,'necu': self.necu,'phrpwr': self.phrpwr,'phrpwrfun': self.phrpwrfun,'phrepwr': self.phrepwr,'ph3pwr': self.ph3pwr,'freq': self.freq,'rphpf': self.rphpf,'yphpf': self.yphpf,'bphpf': self.bphpf,'avgpf': self.avgpf,'rphang': self.rphang,'yphang': self.yphang,'bphang': self.bphang,'avgvol': self.avgvol,'actfwdABS': self.actfwdABS,'apfwdABS': self.apfwdABS,'relagfwdABS': self.relagfwdABS,'releadfwdABS': self.releadfwdABS}

    @classmethod
    def find_by_name(cls, devId):
        return cls.query.filter_by(devId=devId).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Device(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tstamp',type=float)
    parser.add_argument('rphvol',
        type=float
    )
    parser.add_argument('yphvol',
        type=float
    )
    parser.add_argument('bphvol',
        type=float
    )
    parser.add_argument('rphcu',
            type=float
    )
    parser.add_argument('yphcu',
            type=float
    )
    parser.add_argument('bphcu',
            type=float
    )
    parser.add_argument('necu',
        type=float
    )
    parser.add_argument('phrpwr',
        type=float
    )
    parser.add_argument('phrpwrfun',
        type=float
    )
    parser.add_argument('phrepwr',
        type=float
    )
    parser.add_argument('ph3pwr',
        type=float
    )
    parser.add_argument('freq',
        type=float
    )
    parser.add_argument('rphpf',
        type=float
    )
    parser.add_argument('yphpf',
            type=float
    )
    parser.add_argument('bphpf',
            type=float
    )
    parser.add_argument('avgpf',
            type=float
    )
    parser.add_argument('rphang',
        type=float
    )
    parser.add_argument('yphang',
        type=float
    )
    parser.add_argument('bphang',
        type=float
    )
    parser.add_argument('avgvol',
            type=float
    )
    parser.add_argument('actfwdABS',
            type=float
    )
    parser.add_argument('apfwdABS',
            type=float
    )
    parser.add_argument('relagfwdABS',
        type=float
    )
    parser.add_argument('releadfwdABS',
        type=float
    )


    def get(self, devId):
        device = DeviceModel.find_by_name(devId)
        if device:
            return device.json()
        return {'message': 'Device not found'}, 404

    def post(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is None:
            device = DeviceModel(devId,data['tstamp'], data['rphvol'],data['yphvol'],data['bphvol'],data['rphcu'],data['yphcu'],
                                        data['bphcu'],data['necu'],data['freq'],data['phrpwr'],data['phrpwrfun'],data['phrepwr'],data['ph3pwr'],
                                        data['rphpf'],
                                        data['yphpf'],data['bphpf'],data['avgpf'],data['rphang'],data['yphang'],
                                        data['bphang'],data['avgvol'],data['actfwdABS'],data['apfwdABS'],data['relagfwdABS'],
                                        data['releadfwdABS'])
        else:
            device.tstamp = data['tstamp']
            device.rphvol = data['rphvol']
            device.yphvol = data['yphvol']
            device.bphvol = data['bphvol']
            device.rphcu = data['rphcu']
            device.yphcu = data['yphcu']
            device.bphcu = data['bphcu']
            device.necu = data['necu']
            device.freq = data['freq']
            device.phrpwr = data['phrpwr']
            device.phrpwrfun = data['phrpwrfun']
            device.phrepwr = data['phrepwr']
            device.ph3pwr = data['ph3pwr']
            device.rphpf = data['rphpf']
            device.yphpf = data['yphpf']
            device.bphpf = data['bphpf']
            device.avgpf = data['avgpf']
            device.rphang = data['rphang']
            device.yphang = data['yphang']
            device.bphang = data['bphang']
            device.avgvol = data['avgvol']
            device.actfwdABS = data['actfwdABS']
            device.apfwdABS = data['apfwdABS']
            device.relagfwdABS = data['relagfwdABS']
            device.releadfwdABS = data['releadfwdABS']

        #data = Device.parser.parse_args()

        #device = DeviceModel(devId, data['rphvol'],data['yphvol'],data['bphvol'],data['rphcu'],data['yphcu'],
        #                            data['bphcu'],data['necu'],data['freq'],data['phrpwr'],data['phrpwrfun'],data['phrepwr'],data['ph3pwr'],
        #                            data['rphpf'],
        #                            data['yphpf'],data['bphpf'],data['avgpf'],data['rphang'],data['yphang'],
        #                            data['bphang'],data['avgvol'],data['actfwdABS'],data['apfwdABS'],data['relagfwdABS'],
        #                            data['releadfwdABS'])


        try:
            device.save_to_db()
        except:
            return {"message": "An error occurred inserting the device data."}, 500

        return device.json(), 201


    def put(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is True:
            

            device = DeviceModel(devId,data['tstamp'], data['rphvol'],data['yphvol'],data['bphvol'],data['rphcu'],data['yphcu'],
                                        data['bphcu'],data['necu'],data['freq'],data['phrpwr'],data['phrpwrfun'],data['phrepwr'],data['ph3pwr'],
                                        data['rphpf'],
                                        data['yphpf'],data['bphpf'],data['avgpf'],data['rphang'],data['yphang'],
                                        data['bphang'],data['avgvol'],data['actfwdABS'],data['apfwdABS'],data['relagfwdABS'],
                                        data['releadfwdABS'])
        else:
            device.tstamp = data['tstamp']
            device.rphvol = data['rphvol']
            device.yphvol = data['yphvol']
            device.bphvol = data['bphvol']
            device.rphcu = data['rphcu']
            device.yphcu = data['yphcu']
            device.bphcu = data['bphcu']
            device.necu = data['necu']
            device.freq = data['freq']
            device.phrpwr = data['phrpwr']
            device.phrpwrfun = data['phrpwrfun']
            device.phrepwr = data['phrepwr']
            device.ph3pwr = data['ph3pwr']
            device.rphpf = data['rphpf']
            device.yphpf = data['yphpf']
            device.bphpf = data['bphpf']
            device.avgpf = data['avgpf']
            device.rphang = data['rphang']
            device.yphang = data['yphang']
            device.bphang = data['bphang']
            device.avgvol = data['avgvol']
            device.actfwdABS = data['actfwdABS']
            device.apfwdABS = data['apfwdABS']
            device.relagfwdABS = data['relagfwdABS']
            device.releadfwdABS = data['releadfwdABS']

        device.save_to_db()

        return device.json()


class DeviceList(Resource):
    def get(self):
        return {'devices': [x.json() for x in DeviceModel.query.all()]}



#@server.route('/')
#def index():
    #devices = DeviceModel.query.all()
    #return render_template('index.html',devices=devices)

api.add_resource(Device, '/device/<string:devId>')
api.add_resource(DeviceList, '/devices')

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

params = [
    'DeviceID','tstamp','rphvol','yphvol','bphvol','rphcu',
                    'yphcu','bphcu','necu','freq','phrpwr','phrpwrfun','phrepwr',
                    'ph3pwr','rphpf','yphpf','bphpf','avgpf','rphang','yphang',
                    'bphang','avgvol','actfwdABS','apfwdABS','relagfwdABS','releadfwdABS'
]

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "15rem",
    "padding": "2rem 2rem",
    "fontSize":"30rem"
}
collapse = html.Div(
    [
        dbc.Button("Menu",id="collapse-button",className="mb-4",color="primary"),
        dbc.Container(dbc.Collapse(
            children=[dbc.DropdownMenu(nav=True,in_navbar=True,label="Substations",
            children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Dev 1",href="/Dev-1",id="dev-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("Dev 2",href="/Dev-2",id="dev-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("Dev 3",href="/Dev-3",id="dev-3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVM 1",href="/SVM-1",id="svm-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVM 2",href="/SVM 2",id="svm-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("SVM 3",href="/SVM-3",id="svm-3"))])]),
                    dbc.DropdownMenu(nav=True,in_navbar=True,label="Streetlights",
                        children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("JEO 1",href="/jeo-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("JEO 2",href="/jeo 2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("JEO 3",href="/jeo 3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVSD 1",href="/SVSD-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVSD 2",href="/SVSD 2")),dbc.DropdownMenuItem(divider=True)])])],                                                                  
                                
    id="collapse"),style={"backgroundColor":"grey","width":"auto"})])     

sidebar = html.Div(
        [
       dbc.Row(
            html.Img(src=LOGO,height="100px",width="auto"),style={"padding-left":0}),
                
            dbc.Nav(collapse, vertical=True)
  ] ,
style={
    "position": "absolute",
    "top": 0,
    "left":"2rem",
    "bottom": 0,
    "width": "12rem",
    "padding": "1rem 0rem",
    "backgroundColor":"light"},
     id="sidebar",
)
button =html.Div(
           dbc.Row(
              [
                  dbc.Col(dbc.Button("Login",color="primary",className="mb-3",href="#"),style={"padding-left":"20rem","width":"5rem"})]))
navbar = dbc.Navbar(
           html.Div(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                html.H2((html.Img(src=LOGO1,height="60px",width="auto"))),style={"fontSize":"50px","padding-left":"25rem"})),
                        dbc.NavbarToggler(id="navbar-toggler"),
                         dbc.Collapse(sidebar,id="sidebar-collapse",navbar=True),
                         dbc.Collapse(button,id="button-collapse",navbar=True)
                        ],

                    align="center",
                    no_gutters=True,
                ),
             ),
          )
content = html.Div(id="page-content", style=CONTENT_STYLE)

data1= html.Div([
        html.H4('Substation Data Live Feed'),
        html.Table(id="live-update-text"),],style={"overflowX":"scroll"}) 

app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.config['suppress_callback_exceptions']=True

def table(devices):
    table_header=[
        html.Thead(html.Tr([html.Th('Dev') ,html.Th('tstamp'), html.Th('rphV') ,
            html.Th('yphV') , html.Th('bphV') ,html.Th('rphI') ,
            html.Th('yphI') , html.Th('bphI'),html.Th('neI') ,
            html.Th('freq') , html.Th('phrP') , html.Th('phrPfn') ,
            html.Th('phrepwr') , html.Th('ph3P') , html.Th('rphpf') ,
            html.Th('yphpf') , html.Th('bphpf') , html.Th('Apf') ,
            html.Th('rphAn') , html.Th('yphAn') , html.Th('bphAn') ,
            html.Th('AvgV'), html.Th('|actfwd|'), html.Th('|apfwd|'),
            html.Th('|rg|'), html.Th('|rd|')]))]
    table_body=[
        html.Tbody(html.Tr([html.Td(dev.devId),html.Td(dev.tstamp), html.Td(dev.rphvol) ,
            html.Td(dev.yphvol) , html.Td(dev.bphvol) ,html.Td(dev.rphcu),
            html.Td(dev.yphcu) , html.Td(dev.bphcu),html.Td(dev.necu),
            html.Td(dev.freq) , html.Td(dev.phrpwr) ,html.Td(dev.phrpwrfun),
            html.Td(dev.phrepwr), html.Td(dev.ph3pwr), html.Td(dev.rphpf),
            html.Td(dev.yphpf),html.Td(dev.bphpf) ,html.Td(dev.avgpf),
            html.Td(dev.rphang),html.Td(dev.yphang),html.Td(dev.bphang),
            html.Td(dev.avgvol),html.Td(dev.actfwdABS),html.Td(dev.apfwdABS),
            html.Td(dev.relagfwdABS),html.Td(dev.releadfwdABS)]))for dev in devices]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table

app.layout = html.Div([navbar,content,data1,dcc.Location(id="url",refresh=False)])

@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className")])
                            

def update_output_div(input_value):
    devices = DeviceModel.query.all()

    return [html.Table(table(devices)
        )]
    
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
for i in range(1,4):
    @app.callback(
         Output("dev-{%d}"%i, "active"),
         [Input("url", "pathname")],
         )
    def toggle_active_links(pathname):
        if pathname == "/":
        # Treat page 1 as the homepage / index
            return True, False, False
        return [pathname == "/Dev-{%d}"%i]

@app.callback([Output("page-content", "children")],
        [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/Dev-1"]:

        return [
                html.H4("Displays Device 1 Graph")]
    elif pathname in ["/", "/Dev-2"]:

        return [
                html.H4("Displays Device 2 Graph")]
    elif pathname in ["/", "/Dev-3"]:

        return [
                html.H4("Displays Device 3 Graph")]
    
   # If the user tries to reach a different page, return a 404 message
    return [404]





if __name__ == '__main__':
    app.run_server(debug=True)

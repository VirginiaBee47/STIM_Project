
__all__ = ["api_funcs", "API_KEY", "data_processing", "dummy_matplot", "game", "summoner", "user"]


import PySimpleGUI as sg

def hello_world():
    sg.Window(title="Hello world", layout=[[]], margins=(100, 50)).read()
    
def hello_homeD():
    print("Hi Home D! It's ME! YAK!")
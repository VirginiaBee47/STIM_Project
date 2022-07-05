import PySimpleGUI as sg

def hello_world():
    sg.Window(title="Hello world", layout=[[]], margins=(100, 50)).read()
    
def main():
    print("Hi Home D! It's ME! YAK!")
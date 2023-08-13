import streamlit.components.v1 as components

def webcam():
    _webcam = components.html(open("webcam.html").read(), width=640, height=520)
    return _webcam

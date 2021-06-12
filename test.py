#!/usr/bin/env python3

import threading

from client import Client
from server import Server


def c_thread():
    print("c thread")
    c = Client()
    c.run()

def s_thread():
    print("s thread")
    s = Server()
    s.run()



st = threading.Thread(target=s_thread)
ct = threading.Thread(target=c_thread)

st.start()
ct.start()

st.join()
ct.join()



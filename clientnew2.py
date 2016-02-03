import matplotlib.pyplot as plt
import websocket
import thread
import time
import json
import random
import numpy as np
from scipy.fftpack import fft
#print len(dt)
def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        ip=0;
        while True:
            pt=time.time()
            #Fs = 8000
            #f = 1
            #sample = 10000
            #x = np.arange(sample)
            #y = np.sin(2 * np.pi * f *random.randrange(0, 100)* x / Fs)
            #yy = np.sin(2 * np.pi * f*random.randrange(0, 20) * x / Fs)
            #yyy = np.sin(2 * np.pi * f*random.randrange(0, 50) * x / Fs)
            N = 600
            T = 1.0 / 800.0
            x = np.linspace(0.0, N*T, N)
            y = np.sin(random.randrange(0, 100) * 2.0*np.pi*x) + 0.5*np.sin(random.randrange(0, 150) * 2.0*np.pi*x)+0.5*np.sin(random.randrange(0, 100) * 2.0*np.pi*x)
            #print(dt)
            #dt=[]
            #for i in range(0,10000):
             #   dt.append({"unit" : i, "value" : random.randrange(1, 250)});
            data={
                "data": y.tolist(),
                "time":time.time(),
                "T":T,
                "N":N
                }
            time.sleep(1)
            if(ip<2):
                ws.send("Login B")
            else:
                ws.send("A "+json.dumps(data))
            ip=ip+1
            print time.time()-pt
        time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://localhost:9000",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()

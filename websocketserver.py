from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import json
from scipy.fftpack import fft
import numpy as np
a={}
import json
#Login a
class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        #a.append(self);
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            msg=payload.decode('utf8');
            #print("Text message received: {0}".format(payload.decode('utf8')))
            data=msg.split(" ",1)
            if(data[0]=="Login"):
                a[data[1]]=self
            elif(data[0] in a):
                jasdata=json.loads(data[1])
                yf = fft(np.array(jasdata["data"]))
                xf = np.linspace(0.0, 1.0/(2.0*jasdata["T"]), jasdata["N"]/2)
                yf=2.0/jasdata["N"] * np.abs(yf[0:jasdata["N"]/2])
                datapkt={
                    "ydata":yf.tolist()[1:50],
                    "xdata":xf.tolist()[1:50],
                    #"ydata":jasdata["data"],
                    #"xdata":np.linspace(0.0, 1, len(jasdata["data"])).tolist(),
                    "time":jasdata["time"]
                    }
                datastr=json.dumps(datapkt)
                encstr= datastr.encode('utf8')
                a[data[0]].sendMessage(encstr, False)
                print ("sending........."+str(len(yf)))
                
        print(a)
        # echo back message verbatim
        #self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        #a.remove(self)

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    #log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()

import socket
import cv2
import numpy as np

from BillReader import BillReader
from CurrencyRecognizer import CurrencyRecognizer
from Summarizer import OurSummarizer
from TextRecognizer import TextRecognizer
from Bot import Bot
from DetectObject import DetectObject
from maskDetec import DetectMask

# first time use
#import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
global flag
flag = 0

totCash = []

def totAmt():
    sum =0
    for i in totCash:
        sum = sum + i
    print(totCash)
    totCash.clear()
    print(totCash)
    return sum

class Server():
    def __init__(self, portNo):
        self.host = socket.gethostname()
        print("host ",self.host)
        self.port = portNo
        print("port ", self.port)
        self.size = 4096
        self.sock=socket.socket()
        print("sock 1",self.sock)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("sock 2", self.sock)
        self.sock.bind((self.host,self.port))
        print("sock 3",self.sock)
        self.sock.listen(1)
        print("sock 4", self.sock)
        self.conn, self.addr = self.sock.accept()
        print("sock 5", self.sock)
        print("Client connected")

        self.billReader = BillReader()
        self.currencyRecognizer = CurrencyRecognizer()
        # self.currencyRecognizer.configure("D:\\TP_PROGS\\Projects\\TeProjSahara\\progs\\Sahara-System-For-Aiding-Visually-Impaired-master\\Sahara-System-For-Aiding-Visually-Impaired-master\\Server_side\\DataFiles\\yolov3.weights",\
        #      "D:\\TP_PROGS\\Projects\\TeProjSahara\\progs\\Sahara-System-For-Aiding-Visually-Impaired-master\\Sahara-System-For-Aiding-Visually-Impaired-master\\Server_side\\DataFiles\\yolov3-tiny.cfg", \
        #          ('10','20','50','100','200','500','2000'))
        self.ourSummarizer = OurSummarizer()
        self.textRecognizer = TextRecognizer()
        self.bot = Bot()
        self.objectDet = DetectObject()
        self.maskDet = DetectMask()


    def fetchData(self):
        data = b""
        try:
            while True:
                dataChunk = self.conn.recv(self.size)
                data+=dataChunk   
                if dataChunk.endswith(b"eof"):
                    data = data[:-3]
                    imgString, command = data.split(b"mof")
                    nparr = np.frombuffer(imgString, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                    break
        
            return image, command

        except ValueError:
            return None, ""


    def selectModule(self, image, command):
        msg=""
        intent, _ = self.bot.getIntent(command.decode("utf-8"))
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print(intent)
        global flag

        if flag == 1:
            if intent == "Next":
                msg, temp = self.currencyRecognizer.readCurr(image)
                if temp == 0:
                    pass
                else:
                    totCash.append(temp)
                    msg = msg + " say NEXT to continue, STOP for final amount"

            elif intent=="Stop":
                finalAmt = totAmt()
                msg = "Total amount of cash in your hand is equal to " + str(finalAmt)
                flag = 0
            else:
                msg = "I didnt catch what you said, Please repeat"

        else:
            if intent=="CurrencyRecognition":
                msg, _ = self.currencyRecognizer.readCurr(image)
            elif intent=="BillReading":
                msg = self.billReader.readBill(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            elif intent=="TextSummarization":
                text = self.textRecognizer.ocr(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                print("TEXTTTTT", text)
                msg = self.ourSummarizer.genSummary(text)
            elif intent=="BasicTextReading":
                msg = self.textRecognizer.ocr(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            elif intent == "Object":
                msg = self.objectDet.objDetect(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            elif intent == "Mask":
                msg = self.maskDet.masKDetect(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

            elif intent=="TotalCash":
                msg, temp = self.currencyRecognizer.readCurr(image)
                totCash.append(temp)
                if temp == 0:
                    pass
                else:
                    msg = msg + " To continue totalling say the word NEXT. To get the final total say STOP"
                    flag = 1
            else:
                msg = "I didnt catch what you said. Please repeat"

        print(msg)
        return msg


    def sendReply(self, msg):
        msg = ".".join(msg.splitlines())
        msg+='\n'
        self.conn.send(msg.encode())


    def keepListening(self):
        print("on")
        while True:
            image, command = self.fetchData()
            print("image", command)
            if len(command)!=0:
                msgFromModule = self.selectModule(image, command)
                self.sendReply(msgFromModule)
            else:
                self.sendReply("Something went wrong. Please click the picture again.")


    def restartServer(self):
        self.conn.close()
        self.sock.bind((self.host,self.port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()


    def closeConnection(self):
        self.conn.close()


    def __del__(self):
        self.conn.close()

print("hello")
server = Server(7100)

server.keepListening()


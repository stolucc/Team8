#!/usr/bin/env python3

from socket import *
import time
from tkinter import *

class Client(object):

    def __init__(self):
        """Initialises the client."""
        self._addr = gethostbyname(gethostname())
        self._hostAddr = None
        self._hostPort = None
        self._pnts = []
        self._fundsAvailable = 500
        self._fundsBetted = 10
        self._fundsInsured = 0
        self._sock = None

    def _open(self, name, hostAddr, hostPort):
        self._hostAddr = hostAddr
        self._hostPort = hostPort
        """Sets up the client and establishes a connection with the host."""
        self._sock = socket(AF_INET, SOCK_STREAM) #Creates a socket that uses TCP
        try:
            self._connection = self._sock.connect((self._hostAddr, self._hostPort)) #Creates a connection with the host's IP address and port number
            info = (name, self._pnts, self._fundsAvailable - self._fundsBetted, self._fundsBetted, self._fundsInsured)
            self.transmit("ctrl", info)
            time.sleep(1)
            self.transmit("ctrl", "start")
        except:
            self._close()
        finally:
            return

    def message(self, message):
        """Sends 'message' to the host to be broadcated."""
        self.transmit("chat", message)
        messageText.delete("1.0", END)
        return

    def hit(self):
        """Requests the dealer for a card."""
        self.transmit("cmmd", "hit")
        return

    def stick(self):
        """Requests the dealer to end the turn."""
        self.transmit("cmmd", "stick")
        return

    def doubleDown(self):
        """Requests the dealer for a card to increase the bet and to end the turn."""
        self.transmit("cmmd", "double_down")
        return
    
    def takeOutInsurance(self):
        """Requests the dealer for insurance."""
        self.transmit("cmmd", "take_out_insurance")
        return

    def surrender(self):
        """Requests the dealer to be allowed to surrender and to receive half of the bet back."""
        self.transmit("cmmd", "surrender")
        return
    
    def transmit(self, mssgType, mssg):
        """Creates a standardised message and sends it over the established connection."""
        mssgStr = str(mssg)
        message = str((self._addr, mssgType, mssgStr))
        self._sock.sendall(message.encode())

    def _close(self):
        """Closes the established connection."""
        self._sock.close()

def validator(event):
    """Limits the user to only entering 1000 characters into 'messageText' and updates 'messageLabel' to accurately keep track of the number of characters entered."""
    text = messageText.get("1.0", END)
    if event.keysym_num == 65293:
        messageText.delete("end-2c", END)
    if len(text) - 1 > 1000:
        messageText.delete("1.1000", END)
        print(text)
    messageLabel["text"] = "%s/1000" %(len(text)-1)



"""Creates the client and the GUI to use interact with it."""
client = Client()
root = Tk()
root.title("Blackjack")
root.configure(bg="green")
root.minsize(width=900, height=300)
root.maxsize(width=900, height=300)

overAllFrame = Frame(root, bg="green")
overAllFrame.pack(fill="both", expand=True, pady=12)
frame1 = Frame(overAllFrame, bg="green")
frame1.pack(side=TOP, expand=True, pady=12)
frame2 = Frame(overAllFrame, bg="green")
frame2.pack(side=TOP, expand=True, pady=12)
chatFrame = Frame(frame2, bg="green")
chatFrame.pack(side=LEFT, expand=True)
mssgFrame = Frame(frame2, bg="green")
mssgFrame.pack(side=RIGHT, expand=True)
frame3 = Frame(overAllFrame, bg="green")
frame3.pack(side=TOP, expand=True, pady=12)

nameLabel = Label(frame1, width=12, bg="gold", text="Name:")
nameLabel.grid(row=1, column=1, padx=3, pady=3)
nameEntry = Entry(frame1, width=15)
nameEntry.grid(row=1, column=2, padx=3, pady=3)
addrLabel = Label(frame1, width=15, bg="gold", text="Host Addr:")
addrLabel.grid(row=1, column=3, padx=3, pady=3)
addrEntry = Entry(frame1, width=15)
addrEntry.grid(row=1, column=4, padx=3, pady=3)
portLabel = Label(frame1, width=15, bg="gold", text="Host Port:")
portLabel.grid(row=1, column=5, padx=3, pady=3)
portEntry = Entry(frame1, width=15)
portEntry.grid(row=1, column=6, padx=3, pady=3)
connectButton = Button(frame1, text="Connect", command=(lambda:client._open(nameEntry.get(), addrEntry.get(), int(portEntry.get()))), width=9)
connectButton.grid(row=1, column=7, padx=3, pady=3)

messageScrollbar = Scrollbar(chatFrame)
messageScrollbar.pack(side=RIGHT, fill=Y)
messageText = Text(chatFrame, height=6, width=50)
messageText.bind("<KeyRelease>", validator)
messageText.pack(side=LEFT)
messageScrollbar.config(command=messageText.yview)
messageText.config(yscrollcommand=messageScrollbar.set)
messageLabel = Label(mssgFrame, text= "0/1000", width=9)
messageLabel.pack(padx=12, pady=12)
messageButton = Button(mssgFrame, text="Send", command=(lambda:client.message(messageText.get("1.0", END))), width=9)
messageButton.pack(padx=12, pady=12)

hitButton = Button(frame3, text="Hit", command=(lambda:client.hit()), width=15)
hitButton.grid(row=1, column=1, padx=3, pady=3)
stickButton = Button(frame3, text="Stick", command=(lambda:client.stick()), width=15)
stickButton.grid(row=1, column=2, padx=3, pady=3)
dobuleDownButton = Button(frame3, text="Double Down", command=(lambda:client.doubleDown()), width=15)
dobuleDownButton.grid(row=1, column=3, padx=3, pady=3)
takeOutInsuranceButton = Button(frame3, text="Take Out Insurance", command=(lambda:client.takeOutInsurance()), width=15)
takeOutInsuranceButton.grid(row=1, column=4, padx=3, pady=3)
surrenderButton = Button(frame3, text="Surrender", command=(lambda:client.surrender()), width=15)
surrenderButton.grid(row=1, column=5, padx=3, pady=3)
root.mainloop()

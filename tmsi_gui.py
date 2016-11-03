from time import sleep
from tkinter import *
from tkinter.ttk import *
import tmcontroller
from datetime import datetime
from tmcontroller import TinymeshController

import logging

#logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
logging.info('Started')
logging.warning('%s before you %s', 'Look', 'leap!')
logging.error('I am an error')


root = Tk()
root.wm_title("Tinymesh network manager")
numberOfRadios = 3


tree = Treeview(root,height=numberOfRadios)

tree["columns"] = ("rssi", "age","temp","latency")
tree.column("rssi", width=100)
tree.heading("rssi", text="Signal strength")

tree.column("age", width=200)
tree.heading("age", text="Seconds since last contact")

tree.column("temp", width=150)
tree.heading("temp", text="Module temperature")

tree.heading("latency", text="LatencyCounter")

# radioRows = []
# for i in range(numberOfRadios):
#     id=tree.insert("", 0, text="Radio "+str(i), values=("50%", "7"))
#     radioRows.append(id)

tm=TinymeshController()
def update():
    # read new radio status from tmcontroller
    radioStates=tm.process_new_data()
    for radioId, status in radioStates.items():
        valuesFormatted = ["{0:.0f}%".format((255 - status["OriginRssi"]) / 2.55),
                           (datetime.now() - status["ReceivedTime"]).seconds,
                            status.get("ModuleTemperature"),
                           status.get("LatencyCounter")]

        if tree.exists(radioId):
            tree.item(radioId,values=valuesFormatted)
        else:
            tree.insert("",0,iid=radioId,text=radioId, values=valuesFormatted)

    #shoow any new serial data
    s=tm.get_serial_data()
    if s:
        text.insert(END, "\n" + str(s))
        text.see(END)
    root.after(100,update)




tree.pack()

textScroller = Scrollbar(root)
text = Text(root)
textScroller.pack(side=RIGHT, fill=Y)
text.pack(side=LEFT, fill=Y)
textScroller.config(command=text.yview)
text.config(yscrollcommand=textScroller.set)

text.insert(INSERT, 'Sportident punches:\n')



update()
root.mainloop()
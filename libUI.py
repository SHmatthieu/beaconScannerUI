import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image
import threading
import time


# Beacon container class, add an attribute to this class (with a defaut value)
# and it will be shown on the UI.
class Beacon:
    def __init__(self, name="", dist=0, info=""):
        self.name = name
        self.dist = dist
        self.info = info


# UI class
# after creating an instance use startUI to start the main loop 
# use addBeacon and removeBeacon inside an other thread to add and remove beacons.
class BtscannerUI:

    def __init__(self):
        print("BtscannerUI")
        
        self.onOff = False
        self.font = "Arial"
        self.bgMainColor = "#141c1c"
        self.bgSecColor = "#242c34"
        self.textColor = "white"
        self.beacons = {}
        self.infoLabels = {}
        self.keys = []
        self.graphValues = []
        self.totalBeacons = 0
        self.s = 20
        self.t = [i for i in range(self.s)]
        self.d = [0 for _ in range(self.s)]
        self.root = tk.Tk()
        self.root.title("Bluetooth scanner")
        self.root.configure( bg=self.bgSecColor)
        self.root.geometry("900x400")



        stylebt = ttk.Style()
        stylebt.configure("TButton",
            foreground=self.textColor,       
            background=self.bgSecColor,   
            font=(self.font, 15),       
            padding=(10, 5)          
        )

        main_frame = tk.Frame(self.root,borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        main_frame.configure( bg=self.bgSecColor)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        frame1 = tk.Frame(main_frame, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1,bg=self.bgMainColor)
        frame22 = tk.Frame(main_frame, bg=self.bgSecColor)
        frame22.grid(row=1, column=0)
        frame2 = tk.Frame(frame22, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1,bg=self.bgMainColor)
        frame3 = tk.Frame(frame22, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1,bg=self.bgMainColor)

        frame1.grid(row=0, column=0, padx=10, pady=10)
        frame2.grid(row=0, column=0, padx=10, pady=10)
        frame3.grid(row=0, column=1, padx=10, pady=10)


        self.startButton(frame1,0,0)
        self.statText(frame1, 0,1)
        self.graph(frame1,0,2)


        self.raspLogo(frame2, 0, 0)
        n1 = self.distCell(frame2, 1, "#0c68c9", 0, 1)
        n2 = self.distCell(frame2, 2, "#0d549b", 0, 2)
        n3 = self.distCell(frame2, 3, "#144c83", 0, 3)
        n4 = self.distCell(frame2, 4, "#143657", 0, 4)
        n5 = self.distCell(frame2, 5, "#142025", 0, 5)
        def updateCells(event):
            totals = [0,0,0,0,0]
            for _,i in self.beacons.items():
                if i.dist < 1:
                    totals[0]+=1
                    next
                elif i.dist < 2:
                    totals[1]+=1
                elif i.dist < 3:
                    totals[2]+=1
                elif i.dist < 4:
                    totals[3]+=1
                else:
                    totals[4]+=1
            n1["text"] = str(totals[0])
            n2["text"] = str(totals[1])
            n3["text"] = str(totals[2])
            n4["text"] = str(totals[3])
            n5["text"] = str(totals[4])
            

        self.root.bind("<<updateCells>>", updateCells)

        self.deviceList(frame3, 0, 0)

    # start/stop widget
    def startButton(self, parent, row, column):
        frame = tk.Frame(parent, bg=self.bgMainColor)
        def buttonClick():
            self.onOff = not self.onOff
            if b["text"] == "Start":
                b["text"] = " Stop"
                canvas.itemconfig(circle, fill="green")
            else:
                b["text"] = "Start"
                canvas.itemconfig(circle, fill="red")

        b=ttk.Button(frame, text="Start",command=buttonClick)
        b["style"] = "TButton"
        b.grid(row=0, column=0)
        canvas = tk.Canvas(frame, width=40, height=40, bg=self.bgMainColor,highlightthickness=0)
        canvas.grid(row=0, column=1)
        x, y, radius = 20, 20, 10
        circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red")
        frame.grid(row=row, column=column) 

    # scanner info widget
    def statText(self, parent, row, column):
        textFont = (self.font, 16)
        frame = tk.Frame(parent, bg=self.bgMainColor)

        label1 = tk.Label(frame, text="Currently : ", bg=self.bgMainColor, fg=self.textColor, font=textFont)
        label1.grid(row=0, column=0)
        label2 = tk.Label(frame, text="Total : ", bg=self.bgMainColor, fg=self.textColor, font=textFont)
        label2.grid(row=1, column=0)
        score1 = tk.Label(frame, text="0", bg=self.bgMainColor, fg=self.textColor, font=textFont)
        score1.grid(row=0, column=1)
        score2 = tk.Label(frame, text="0", bg=self.bgMainColor, fg=self.textColor, font=textFont)
        score2.grid(row=1, column=1)
        frame.grid(row=row, column=column, padx=10) 
        def updateCount(event):
            if self.onOff:
                score1["text"] = str(len(self.beacons))
                score2["text"] = str(self.totalBeacons)
        self.root.bind("<<updateCount>>", updateCount)

    # graph widget
    def graph(self,parent, row, column):
        fig = Figure(figsize=(6, 2),facecolor=self.bgMainColor,edgecolor=self.textColor)
        ax = fig.add_subplot(facecolor=self.bgMainColor)
        line, = ax.plot(self.t, self.d)
        ax.set_title("number of detected devices",fontsize=14, color=self.textColor)
        ax.xaxis.label.set_color(self.textColor)  
        ax.yaxis.label.set_color(self.textColor)  
        ax.tick_params(axis="x", colors=self.textColor)  
        ax.tick_params(axis="y", colors=self.textColor)
        ax.spines["bottom"].set_color(self.textColor)
        ax.spines["left"].set_color(self.textColor)
        ax.spines["top"].set_color(self.textColor)
        ax.spines["right"].set_color(self.textColor)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column)
        def updateGraph(event):
            if self.onOff:
                self.d.append(len(self.beacons))
                self.d = self.d[1:]
                ax.set_xlim(0, self.s)
                ax.set_ylim(min(self.d)-3, max(self.d)+3)
                line.set_data(self.t, self.d)
                canvas.draw()
        self.root.bind("<<updateGraph>>", updateGraph)
    
    # device list widget
    def deviceList(self, parent, row, column):
        textFont = (self.font, 16)
        Listdata = tk.StringVar(value=[])
        l = tk.Listbox(parent, height=5, listvariable=Listdata, bg=self.bgMainColor, font=(self.font, 15), fg=self.textColor)
        l.grid(column=column, row=row)
        s = ttk.Scrollbar(parent, orient="vertical", command=l.yview)
        s.grid(column=column+1, row=0,sticky="NS")
        l['yscrollcommand'] = s.set

        def updateList(event):
            self.keys = [k for k,_ in self.beacons.items()]
            Listdata.set(self.keys)
        self.root.bind("<<updateList>>", updateList)

        def updateDetails(selection):
            beacon = self.beacons[self.keys[selection[0]]]
            for k, lab in self.infoLabels.items():
                lab["text"] = getattr(beacon, k)
        l.bind("<<ListboxSelect>>", lambda e: updateDetails(l.curselection()))

        frame = tk.Frame(parent, bg=self.bgMainColor)
        i = 0
        for k, _ in Beacon().__dict__.items():
            label1 = tk.Label(frame, text=k + " : ", bg=self.bgMainColor, fg=self.textColor, font=textFont)
            label1.grid(row=i, column=0)
            score1 = tk.Label(frame, text="0", bg=self.bgMainColor, fg=self.textColor, font=textFont)
            score1.grid(row=i, column=1)
            i+=1
            self.infoLabels[k] = score1
        frame.grid(column=column+2, row=row)


    def distCell(self,parent, dist, color, row, column, max=False):
        frame = tk.Frame(parent, bg=color)
        distLabel = tk.Label(frame, text="<{}m".format(dist), bg=color, fg=self.textColor, font=(self.font, 15))
        numLabel = tk.Label(frame, text="0", bg=color,fg=self.textColor, font=(self.font, 25))
        distLabel.grid(column=0, row=0)
        numLabel.grid(column=0, row=1)
        frame.grid(column=column, row=row)
        return numLabel


    def raspLogo(self, parent, row, column):
        img = Image.open("raspLogo.png")
        myimg = ImageTk.PhotoImage(img.resize((70,70)))
        frame = tk.Label(parent, image=myimg, bg=self.bgMainColor)
        frame.photo = myimg
        frame.grid(row=row, column=column)

    # start the main loop
    def startUI(self):
        def freqUpdate():
            while True:
                time.sleep(0.5)
                self.graphValues.append(len(self.beacons))
                self.root.event_generate("<<updateGraph>>")
        threading.Thread(target=freqUpdate).start()
        self.root.mainloop()

    def addBeacon(self, beacon):
        self.totalBeacons+=1
        self.beacons[beacon.name] = beacon
        self.root.event_generate("<<updateCount>>")
        self.root.event_generate("<<updateList>>")
        self.root.event_generate("<<updateCells>>")
        
    def removeBeacon(self, beacon):
        try:
            del self.beacons[beacon.name]
            self.root.event_generate("<<updateCount>>")
            self.root.event_generate("<<updateList>>")
            self.root.event_generate("<<updateCells>>")
        except:
            pass



if __name__ == "__main__":
    bt = BtscannerUI()
    bt.startUI()
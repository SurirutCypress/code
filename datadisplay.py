import tkinter as tk
import data_reader
import data_class
import graphs

class SensorGUI(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.data = data_class.SensorData()
        tk.Label(self, text='Data Logger').pack(side='top')
        self.graph = graphs.PyplotEmbed(self, self.data)
        self.graph.pack()
        self.initialized = False
        self.power = False

        button_frame = tk.Frame(self)
        button_frame.pack(side='bottom')
        self.reading = False
        self.read_button = tk.Button(button_frame, text="Read",command=self.toggle_read)
        self.read_button.pack(side='left')

        #light_button = tk.Button(button_frame, text="Power", command=lambda: data_reader.usb_write('E'))
        self.light_button = tk.Button(button_frame, text="Turn On Lights", command=self.toggle_power)
        self.light_button.pack(side='left')

    def toggle_power(self):
        if self.power:
            self.power = False
            self.light_button.config(text="Turn On Lights")
            data_reader.usb_write('F')

        else:
            self.power = True
            data_reader.usb_write('N')
            self.light_button.config(text="Turn Off Lights")

    def toggle_read(self):
        if self.reading:
            self.after_cancel(self.reading)
            self.reading = False
            self.read_button.config(text="Read")
            data_reader.usb_write('S')
        else:
            data_reader.usb_write('R')
            self.read_button.config(text="Stop Read")
            self.read_data()


    def read_data(self):
        self.reading = self.after(1000, self.read_data)
        packet_data = data_reader.usb_read_data()
        print(packet_data)
        if packet_data:
            print(packet_data)
            self.data.add_data(packet_data)
            if not self.initialized:
                self.initialized = True
                self.graph.init_data()
            else:
                self.graph.updata_data()


if __name__ == '__main__':
    app=SensorGUI()
    app.title("")

    app.geometry("1000x550")



    app.mainloop()



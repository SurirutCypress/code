import tkinter as tk
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FRAME_COLOR = 'pink'
GRAPH_COLOR = 'black'

class PyplotEmbed(tk.Frame):
    """
    Class that will make a tkinter frame with a matplotlib plot area embedded in the frame
    """

    def __init__(self, master, data):
        tk.Frame.__init__(self, master=master)
        self.data = data  # alias data into class
        print(plt.subplots(2, 3))

        # self.figure_bed.set_facecolor(FRAME_COLOR)
        # self.top_axes[0].set_facecolor(GRAPH_COLOR)
        # self.top_axes[1].set_facecolor(GRAPH_COLOR)
        # self.bottom_axes[0].set_facecolor(GRAPH_COLOR)
        # self.bottom_axes[1].set_facecolor(GRAPH_COLOR)

        self.figure_bed, (self.top_axes, self.bottom_axes) = plt.subplots(2, 3)
        self.power_axis = self.top_axes[2].twinx()
        self.dity_axis = self.bottom_axes[2].twinx()
        self.figure_bed.set_facecolor('white')
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.figure_bed, master=self)
        self.canvas._tkcanvas.config(highlightthickness=0)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.l = None

    def init_data(self):
        self.LPG_line, = self.top_axes[0].plot(self.data.time, self.data.LPG)
        #self.Dust_line, = self.top_axes[0].plot(self.data.time, self.data.Dust)
        self.top_axes[0].set_ylim(0, 1000)
        self.top_axes[0].set_title('Air quality ', fontsize=10)
        self.top_axes[0].set_ylabel('[ppm]')
        self.top_axes[0].set_xlabel('t(s)')

        self.Dust_line, = self.top_axes[1].plot(self.data.time, self.data.Dust)
        self.top_axes[1].set_ylim(0, 1.5)
        self.top_axes[1].set_title('Particle', fontsize=10)
        self.top_axes[1].set_ylabel('[mg/m3]')
        self.top_axes[1].set_xlabel('t(s)')

        #self.Current_line, = self.top_axes[1].plot(self.data.time, self.data.Current)
        # self.top_axes[1].set_ylim(0, 5)
        # self.top_axes[1].set_title('Current', fontsize=10)
        # self.top_axes[1].set_ylabel('[A]')
        # self.top_axes[1].set_xlabel('t(s)')



        self.ElectricPower_line, = self.power_axis.plot(self.data.time, self.data.ElectricPower,'r')
        self.Current_line, = self.top_axes[2].plot(self.data.time, self.data.Current,'b')
        self.top_axes[2].set_title('Current & ElectricPower', fontsize=10)
        self.top_axes[2].set_ylim(0, 5)
        self.top_axes[2].set_ylabel('[A]')
        self.power_axis.set_ylim(0, 1000)
        self.power_axis.set_ylabel('[W]')
        self.top_axes[2].set_xlabel('t(s)')

        self.lux_line, = self.bottom_axes[0].plot(self.data.time, self.data.lux)
        self.bottom_axes[0].set_ylim(0, 1000)
        self.bottom_axes[0].set_title('Occupancy condition', fontsize=10)
        self.bottom_axes[0].set_ylabel('[Lux]')
        self.bottom_axes[0].set_xlabel('t(s)')

        self.motion_line, = self.bottom_axes[1].plot(self.data.time, self.data.motion)
        self.bottom_axes[1].set_ylim(-1, 2)
        self.bottom_axes[1].set_title('PIR motion', fontsize=10)
        self.bottom_axes[1].set_ylabel('Movement')
        self.bottom_axes[1].set_xlabel('t(s)')

        self.hum_line, = self.dity_axis.plot(self.data.time, self.data.humidity, color="green")
        self.temp_line, = self.bottom_axes[2].plot(self.data.time, self.data.temperature,color="blue")
        self.heatindex_line, = self.bottom_axes[2].plot(self.data.time, self.data.HI,'.r')
        self.bottom_axes[2].set_title('Temperature & Humidity', fontsize=10)
        self.bottom_axes[2].set_ylim(0, 100)
        self.bottom_axes[2].set_ylabel('[°C]')
        self.dity_axis.set_ylim(0, 100)
        self.dity_axis.set_ylabel('[%]')
        self.bottom_axes[2].set_xlabel('t(s)')

    def updata_data(self):
        print('time:', self.data.time)
        self.LPG_line.set_ydata(self.data.LPG)
        self.LPG_line.set_xdata(self.data.time)
        self.top_axes[0].set_xlim(0, self.data.time[-1])

        self.Dust_line.set_ydata(self.data.Dust)
        self.Dust_line.set_xdata(self.data.time)
        self.top_axes[1].set_xlim(0, self.data.time[-1])

        self.Current_line.set_ydata(self.data.Current)
        self.ElectricPower_line.set_ydata(self.data.ElectricPower)
        self.Current_line.set_xdata(self.data.time)
        self.ElectricPower_line.set_xdata(self.data.time)
        self.top_axes[2].set_xlim(0, self.data.time[-1])

        self.lux_line.set_ydata(self.data.lux)
        self.lux_line.set_xdata(self.data.time)
        self.bottom_axes[0].set_xlim(0, self.data.time[-1])

        self.motion_line.set_ydata(self.data.motion)
        self.motion_line.set_xdata(self.data.time)
        self.bottom_axes[1].set_xlim(0, self.data.time[-1])

        self.hum_line.set_ydata(self.data.humidity)
        self.temp_line.set_ydata(self.data.temperature)
        self.heatindex_line.set_ydata(self.data.HI)
        self.hum_line.set_xdata(self.data.time)
        self.temp_line.set_xdata(self.data.time)
        self.heatindex_line.set_xdata(self.data.time)
        self.bottom_axes[2].set_xlim(0, self.data.time[-1])


        # self.motion_line.set_ydata(self.data.motion)
        # self.motion_line.set_xdata(self.data.time)
        # self.bottom_axes[3].set_xlim(0, self.data.time[-1])

        #print(self.data.time)
        plt.tight_layout()
        self.canvas.draw()




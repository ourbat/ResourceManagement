from tkinter import *
from HardwareMonitoring import HardwareMonitoring
import tkinter as tk


class CpuTemperatureMonitor:
    def __init__(self,window):
        self.window = window
        self.hw_monitor = HardwareMonitoring()

        """
        设置窗口大小和初始位置
        """
        window_width = 250
        window_height = 60
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coord = (screen_width - window_width) - 605  # Y轴默认显示位置
        y_coord = (screen_height - window_height) - 810  # X轴默认显示位置
        self.window.geometry(f'{window_width}x{window_height}+{x_coord}+{y_coord}')

        """
        窗口样式
        """
        self.window.wm_attributes('-topmost', True)  # 窗口总是置于顶层
        self.window.overrideredirect(1)  # 去标题
        self.window.wm_attributes('-transparentcolor', 'white')
        self.window.wm_attributes('-alpha', 0.9)  # 整体透明度
        self.window.wm_attributes("-toolwindow", True)
        self.window.config(bg="#22222e")
        font_style = ("黑体", 10)  # 设置黑体字体样式

        """
        加载监控参数
        """
        # 显示CPU负载
        self.cpu_load_label = Label(self.window, text="", font=font_style,height=2)
        self.cpu_load_label.pack(padx=10, pady=0)
        # 显示GPU负载
        self.gpu_load_label = Label(self.window, text="", font=font_style,height=2)
        self.gpu_load_label.pack(padx=10, pady=0)
        self.update_data()

        """
        右键退出
        """
        def on_button_click():
            self.window.destroy()
        self.popup_menu = Menu(self.window, tearoff=0)
        self.popup_menu.add_command(label="退出", command=on_button_click)

        def show_popup(event):
            if event.num == 3:
                self.popup_menu.post(event.x_root, event.y_root)
        self.window.bind("<Button-3>", show_popup)

        """
        鼠标左键按下后跟随移动、鼠标左键松开后停止移动的示例程序。在这个示例中，我们使用了bind()方法和unbind()方法来绑定和取消事件处理函数。
        """
        self.window.resizable(False, False)

        # 添加鼠标事件以移动窗口。
        self.window.bind("<Button-1>", self.on_left_button_down)
        self.window.bind("<B1-Motion>", self.on_mouse_left_drag)
        self.window.bind("<ButtonRelease-1>", self.on_left_button_up)

        # 启动Tkinter的事件循环。
        self.window.mainloop()

    def on_left_button_down(self, event):
        """
        开始移动窗口。
        :param event:
        :return:
        """
        self.move = True
        self.last_x, self.last_y = event.x_root, event.y_root

    def on_mouse_left_drag(self, event):
        """
        将窗口拖动到当前鼠标点。
        :param event:
        :return:
        """
        if self.move:
            dx, dy = event.x_root - self.last_x, event.y_root - self.last_y
            x, y = self.window.winfo_geometry().split("+")[1:]
            new_x, new_y = int(x) + dx, int(y) + dy
            self.window.geometry(f"+{new_x}+{new_y}")
            self.last_x, self.last_y = event.x_root, event.y_root

    def on_left_button_up(self, event):
        """
        停止车窗移动。
        :param event:
        :return:
        """
        self.move = False

    def stop(self):
        """
        停止CPU温度监视器。
        :return:
        """
        self.window.quit()

    def update_data(self):
        """
        刷新窗口中的数据，并显示相对应的内容
        :return:
        """
        cpu_load_label_temp = self.hw_monitor.get_cpu_load()
        cpu_temperature_label_temp = self.hw_monitor.get_cpu_temperature()
        gpu_load_label_temp = self.hw_monitor.get_gpu_load()
        gpu_temperature_label_temp = self.hw_monitor.get_gpu_temperature()

        # 根据温度设定标签字体颜色
        if cpu_temperature_label_temp > 80:
            cpu_color = "red"
        else:
            cpu_color = "#EDEDED"

        if gpu_temperature_label_temp > 80:
            gpu_color = "red"
        else:
            gpu_color = "#EDEDED"

        self.cpu_load_label.config(text=f"CPU负载: {cpu_load_label_temp}% 温度: {cpu_temperature_label_temp}°C", fg=cpu_color, bg="#22222e")
        self.gpu_load_label.config(text=f"GPU负载: {gpu_load_label_temp}% 温度: {gpu_temperature_label_temp}°C", fg=gpu_color, bg="#22222e")
        self.window.after(1000, self.update_data)


if __name__ == '__main__':
    root = tk.Tk()
    monitor = CpuTemperatureMonitor(root)
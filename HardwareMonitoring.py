import clr
import os
import time

# 添加对OpenHardwareMonitorLib.dll的引用
clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '\OpenHardwareMonitorLib.dll')
# clr.AddReference(r'./OpenHardwareMonitorLib.dll')
from OpenHardwareMonitor.Hardware import *


class HardwareMonitoring:
    def __init__(self):
        # 创建Computer对象，并设置启用CPU和GPU的传感器
        self.computer = Computer()
        self.computer.CPUEnabled = True
        self.computer.GPUEnabled = True
        self.computer.RAMEnabled = True
        self.computer.Open()

    def get_sensor_value(self, sensor_type, hardware_type, name_contains):
        """
        获取特定传感器类型、硬件类型和命名规则的传感器的值

        :param sensor_type: 传感器类型（如SensorType.Temperature）
        :param hardware_type: 硬件类型（如HardwareType.CPU）
        :param name_contains: 传感器名称包含的内容（如'Core'）
        :return: 返回传感器值，保留一位小数
        """
        for hardware in self.computer.Hardware:
            if hardware.HardwareType == hardware_type:
                hardware.Update()
                for sensor in hardware.Sensors:
                    if sensor.SensorType == sensor_type and name_contains in sensor.Name:
                        return round(sensor.Value, 1)

    def get_cpu_temperature(self):
        """
        获取CPU温度值
        """
        return self.get_sensor_value(SensorType.Temperature, HardwareType.CPU, 'Package')

    def get_cpu_load(self):
        """
        获取CPU负载值
        """
        return self.get_sensor_value(SensorType.Load, HardwareType.CPU, 'Total')

    def get_cpu_clocks(self):
        """
        获取CPU时钟频率值
        """
        return self.get_sensor_value(SensorType.Clock, HardwareType.CPU, 'Core')

    def get_gpu_temperature(self):
        """
        获取GPU温度值
        """
        return self.get_sensor_value(SensorType.Temperature, HardwareType.GpuNvidia, 'Core')

    def get_gpu_load(self):
        """
        获取GPU负载值
        """
        return self.get_sensor_value(SensorType.Load, HardwareType.GpuNvidia, 'Core')

    def get_gpu_clocks(self):
        """
        获取GPU时钟频率值
        """
        return self.get_sensor_value(SensorType.Clock, HardwareType.GpuNvidia, 'Core')

    def get_memory_usage(self):
        """
        获取内存使用百分比
        """
        return self.get_sensor_value(SensorType.Load, HardwareType.RAM, 'Memory')

    def close(self):
        """
        关闭Computer对象，释放资源
        """
        if self.computer is not None:
            self.computer.Close()


if __name__ == '__main__':
    monitor = HardwareMonitoring()
    while True:
        print(f"当前CPU温度为：{monitor.get_cpu_temperature()}℃")
        print(f"当前CPU使用率：{monitor.get_cpu_load()}%")
        time.sleep(1)
    monitor.close()

import serial
import time
import binascii
import numpy as np
import matplotlib.pyplot as plt

# 定义相机的分辨率
CAMERA_WIDTH = 176
CAMERA_HEIGHT = 144

def open_serial_port(port, baudrate, timeout):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def read_image(ser):
    if ser is None:
        return None

    frame_data = []
    reading = False

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "Reading frame":
            reading = True
            continue
        if reading:
            if line == "":
                break
            frame_data.append(line)

    if len(frame_data) == 0:
        print("No data received.")
        return None

    # 调试：打印接收到的数据
    print(f"Frame data length: {len(frame_data)}")
    print(f"First 100 characters: {frame_data[:100]}")

    hex_data = ''.join(frame_data)

    try:
        byte_data = binascii.unhexlify(hex_data)
    except binascii.Error as e:
        print(f"Error converting hex data: {e}")
        return None

    pixel_values = np.frombuffer(byte_data, dtype=np.uint16)

    if pixel_values.size != CAMERA_WIDTH * CAMERA_HEIGHT:
        print(f"Unexpected number of pixels: {pixel_values.size}, expected: {CAMERA_WIDTH * CAMERA_HEIGHT}")
        return None

    image = pixel_values.reshape((CAMERA_HEIGHT, CAMERA_WIDTH))
    return image

def main():
    port = '/dev/tty.usbmodem1101'  # 请根据实际情况修改
    baudrate = 9600
    timeout = 1

    while True:
        ser = open_serial_port(port, baudrate, timeout)
        if ser:
            image = read_image(ser)
            if image is not None:
                plt.imshow(image, cmap='gray')
                plt.show()
            ser.close()
        time.sleep(1)

if __name__ == '__main__':
    main()

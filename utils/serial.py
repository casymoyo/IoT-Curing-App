import serial

def read_serial_data(port='COM5', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
  
        line = ser.readline().decode('utf-8').strip()

        ser.close()

        return line
    except serial.SerialException as e:
        return f"Error: {e}"

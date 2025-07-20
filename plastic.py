import serial
import time

try:
    ser = serial.Serial('COM7', 9600, timeout=1)  # Open COM7 at 9600 baud
    time.sleep(2)  # Wait for Arduino to reset after connection

    ser.write(b'paper\n')  # Send the string "plastic" followed by newline
    print("Sent 'plastic' to COM7")

    ser.close()  # Close the port
except Exception as e:
    print(f"Serial error: {e}")

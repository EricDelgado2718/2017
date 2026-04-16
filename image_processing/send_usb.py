
import serial
import time


def send_message(port, baud = 9600, timeout = 1)
    ser = serial.Serial(port, baud, timeout = timeout)
    ser.reset_input_buffer() 

    try:
        while True:
            ser.write(b"1") 
            print("Sent: 1")
            time.sleep(1)
            ser.write(b"0")
            print("Sent: 0")
            time.sleep(1)
    except KeyboardInterrupt:
        ser.close()

if __name__ == "__main__":
    send_message();
     

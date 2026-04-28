import serial
import argparse

def send_message(port = "COM3", baud = 9600, timeout = 1):
    ser = serial.Serial(port, baud, timeout = timeout)
    ser.reset_input_buffer()
    print("Enter 1 or 0")
    try:
        while True:
            user_input = input("> ").strip()
            if user_input.lower() == "q":
                break
            if user_input == "1":
                ser.write(b"1")
            elif user_input == "0":
                ser.write(b"0")
            else:
                print("Invalid Input - Enter 1 or 0")
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("Serial port closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Send USB message")
    parser.add_argument("-p", "--port", default = "COM3")
    parser.add_argument("-b", "--baud", default = "9600", type=int)
    args = parser.parse_args()
    send_message(port = args.port, baud = args.baud)

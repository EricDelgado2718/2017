import argparse
from smbus2 import SMBus

def send_message(bus_num = 1, address = 0x08):
    with SMBus(bus_num) as bus:
        print("Enter 1 or 0")
        try:
            while True:
                user_input = input("> ").strip().lower()
                if user_input == "q":
                    break
                elif user_input == "1":
                    bus.write_byte(address, 1)
                elif user_input == "0":
                    bus.write_byte(address, 0)
                elif user_input == "r":
                    state = bus.read_byte(address)
                else:
                    print("Invalid input - 1 or 0")
        except KeyboardInterrupt:
            pass
        except OSError as e:
            print(f"I2C error: {e}")
        finally:
            print("Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Teensy I2C")
    parser.add_argument("-b", "--bus", default=1, type=int, help= "I2C bus number")
    parser.add_argument("-a", "--address", default="0x08", help= "Teensy slave address in hex")
    args = parser.parse_args()
    send_message(bus_num = args.bus, address = int(args.address, 16))

import pigpio
import time
import argparse

def run_slave(address = 0x08):
    pi = pigpio.pi()
    if not pi.connected:
        raise RuntimeError("pigpio not running")

    pi.bsc_i2c(address)

    current_value = 0
    print(f"I2C slave running at: {address}. Current value: {current_value}")
    print("Enter 1 or 0 to update Teensy output")
    try:
        while True:
            user_input = input("> ").strip().lower()
            if user_input == "q":
                break
            elif user_input in ("1", "0"):
                current_value = int(user_input)
                pi.bsc_i2c(address, bytes([current_value]))
                print(f"Value set to {current_value}")
            else:
                print("Enter 1, 0")


            status, count, data = pi.bsc_i2c(address, bytes([current_value]))
            if count > 0:
                print(f"Master wrote {count} bytes: {list(data)}")

    except KeyboardInterrupt:
        pass
    finally:
        pi.bsc_i2c(0)
        pi.stop()
        print("Slave closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Teensy I2C")
    parser.add_argument("-a", "--address", default="0x08", help= "Teensy slave address in hex")
    args = parser.parse_args()
    run_slave(address = int(args.address, 16))

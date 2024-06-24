import argparse
import os
import time
import serial
from github import Github
from github import Auth


def main():
    auth = Auth.Token(os.environ.get("GH_TOKEN"))
    wait = 300

    parser = argparse.ArgumentParser(description="Serial port writer")
    parser.add_argument("port", type=str, help="Serial port")
    parser.add_argument("baudrate", type=int, help="Baudrate")
    args = parser.parse_args()

    with Github(auth=auth) as g, serial.Serial(baudrate=args.baudrate) as ser:
        while not ser.is_open:
            try:
                ser.port = args.port
                ser.open()
                print(f"Serial port {ser.name} opened")
                initString = ser.readline()
                if initString == b"<ready>\n":
                    print("Arduino ready to receive data")
                    while True:
                        notifications = g.get_user().get_notifications()
                        print(f"Notification count: {notifications.totalCount}")
                        ser.write(bytes(str(notifications.totalCount), "utf-8"))
                        print(f"Sleeping for {wait} seconds")
                        time.sleep(int(wait))
            except serial.SerialException as e:
                if e.errno == 16:
                    print("Serial port already in use, trying again in 10 seconds")
                    time.sleep(10)
                else:
                    raise


if __name__ == "__main__":
    try:
      main()
    except KeyboardInterrupt:
      print("Exiting")

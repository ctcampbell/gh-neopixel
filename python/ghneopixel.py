# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pygithub>=2.3.0",
#   "pyserial>=3.5",
# ]
# ///

import argparse
import os
import time
from serial import Serial, SerialException
from github import Github
from github import Auth


def main():
    auth = Auth.Token(os.environ.get("GH_TOKEN"))
    wait = 300

    parser = argparse.ArgumentParser(description="Serial port writer")
    parser.add_argument("port", type=str, help="Serial port")
    parser.add_argument("baudrate", type=int, help="Baudrate")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    with Github(auth=auth) as g, Serial(baudrate=args.baudrate) as ser:
        while not ser.is_open:
            try:
                ser.port = args.port
                ser.open()
                print(f"Serial port {ser.name} opened")
                initString = ser.readline()
                if initString.startswith(b"<ready>"):
                    print("Arduino ready to receive data")
                    print("Polling for issues")
                    while True:
                        issues = g.get_repo(
                            "github/advanced-security-field"
                        ).get_issues(
                            state="open",
                            labels=["region-corporate-emea", "pending_ase_approval"],
                        )
                        if args.debug:
                            print(f"Issue count: {issues.totalCount}")
                        ser.write(bytes(str(issues.totalCount), "utf-8"))
                        if args.debug:
                            print(f"Sleeping for {wait} seconds")
                        time.sleep(int(wait))
            except SerialException as e:
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

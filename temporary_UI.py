import serial
import time

def initialize():
    ser = serial.Serial('COM3', 115200, timeout=1)        #serial port at /dev/ttyACM0, baud rate of 115200,
    print("\nInitializing...")
                                                                    # one second timeout before initializing
    ser.dtr = False                                           #Prevents reset of the arduino upon receiving the message,
                                                                    # which would normally block transmission
    time.sleep(1)                                                #set the timeout
    return ser                                                     #Allows you to use it like a regular serial port

# It is one line for now. My diagnostic version will be more. This is used in place of ser.write(str.encode())


def send_command(ser, message):
    if isinstance(message, str):
        ser.write(message.encode())
    else:
        raise ValueError("The message must be a string")
        return

# Do not use directly unless for testing purposes

def makeDrink(ser, ingredients):
    if len(ingredients.split(';')) <= 5:
        if ingredients.find(';') == -1 and len(ingredients.split(',')) == 2 or ingredients.find(';') != -1:
            message = "pour:" + ingredients + "\n"
            print('Sent: ' + message)
            send_command(ser, message)
            return
    print("Invalid Command, try again")


if __name__ == "__main__":
    ser = initialize()
    time.sleep(1)
    print("Welcome to the sloshinator!")
    while True:
        command = input("Enter a command: ").lower()
        command = command.replace(" ", "")
        if command[0:6] == 'prime:':
            if command[6:] == "all":
                message = command + '\n'
                send_command(ser, message)
                print('Sent: ' + message)
            else:
                try:
                    int(command[6:])
                    message = command + '\n'
                    send_command(ser, message)
                    print('Sent: ' + message)
                except:
                    print("Invalid Command, try again")
        elif command[0:5] == 'pour:':
            message = command[5:]
            makeDrink(ser, message)
        else:
            print("Invalid Command, try again")
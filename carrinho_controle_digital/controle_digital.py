import keyboard
import serial
from time import sleep


import pygame
from pygame.locals import *

potencia = 0
direcao = 0.5


# Example usage
serial_port = '/dev/ttyACM0' 
baud_rate = 9600  # Replace with your baud rate


def read_serial_data(serial_port, baud_rate, timeout=1):
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    
    while ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print("Received data:", data)

    ser.close()
            

def send_message(serial_port, message):
    ser = serial.Serial(serial_port, 9600)  # Open the serial port
    ser.write(message.encode())  # Send the message
    ser.close()  # Close the serial port


def get_arrow_key():
    global potencia 
    global direcao
    global serial_port
    global baud_rate

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    potencia = 255
                elif event.key == K_DOWN:
                    potencia = 0
                elif event.key == K_LEFT:
                    direcao += 0.5
                elif event.key == K_RIGHT:
                    direcao -= 0.5

                if direcao > 1:
                    direcao = 1
                if direcao < 0:
                    direcao = 0

                potencia_roda_esquerda = int(potencia * (1 - direcao))
                potencia_roda_direita = int(potencia * (direcao))
                send_message(serial_port, f"01 {potencia_roda_direita} \n")
                sleep(0.3)
#    read_serial_data(serial_port, baud_rate)
                send_message(serial_port, f"02 {potencia_roda_esquerda} \n")
                sleep(0.3)
#    read_serial_data(serial_port, baud_rate)


    

    #print(f"01 {potencia_roda_direita}\n")
    #print(f"02 {potencia_roda_esquerda}\n")




pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Arrow Key Input')

while True:
    get_arrow_key()
    

    pass
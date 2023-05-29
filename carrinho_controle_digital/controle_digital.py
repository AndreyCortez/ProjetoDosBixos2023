import keyboard
import serial
from time import sleep
import math as m


import pygame
from pygame.locals import *

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

"""

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
                    potencia += 50
                elif event.key == K_DOWN:
                    potencia -= 50
                elif event.key == K_LEFT:
                    direcao += 0.5
                elif event.key == K_RIGHT:
                    direcao -= 0.5

                if direcao > 3.1415 / 2:
                    direcao = 3.1415 / 2
                if direcao < 0:
                    direcao = 0

                if potencia > 0:
                    potencia_roda_esquerda = int(m.fabs(potencia * m.cos(direcao)))
                    potencia_roda_direita = int(m.fabs(potencia *  (1 - m.cos(direcao))))
        
                    print(f"{potencia_roda_esquerda} 1 0 {potencia_roda_direita} 1 0 \n")
                    send_message(serial_port, f"{potencia_roda_esquerda} 1 0 {potencia_roda_direita} 1 0 \n")
    
                else:
                    potencia_roda_esquerda = int(m.fabs(potencia * m.cos(direcao)))
                    potencia_roda_direita = int(m.fabs(potencia *  (1 - m.cos(direcao))))
        
                    print(f"{potencia_roda_esquerda} 0 1 {potencia_roda_direita} 0 1 \n")
                    send_message(serial_port, f"{potencia_roda_esquerda} 0 1 {potencia_roda_direita} 1 0 \n")

    #print(f"01 {potencia_roda_direita}\n")
    #print(f"02 {potencia_roda_esquerda}\n")




pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Arrow Key Input')


while True:
    get_arrow_key()
    

    pass

"""

import tkinter as tk

def saturar(val, max, min):
    if (val > max):
        return int(max)
    elif(val < min):
        return int(min)
    return int(val)


def update_label():
    # Your function logic here    
    potencia_bruto = slider1.get()
    volante_bruto = slider2.get()
    freio_bruto = slider3.get()
    
    potencia = float(potencia_bruto) / 1023.0
    direcao = (float(volante_bruto) / 511.5) - 1

    diametro_da_roda = 1
    distancia_entre_eixos = 2
    pi = 3.1415
    range_volante = 90 * (pi / 180)

    torque_adicionado = diametro_da_roda * m.tan((direcao * range_volante)) / (2 * distancia_entre_eixos)
    motor_esquerdo_potencia = potencia_bruto * (1 - torque_adicionado) / 4
    motor_direito_potencia = potencia_bruto * (1 + torque_adicionado) / 4
    motor_esquerdo_potencia = saturar(motor_esquerdo_potencia, 255, 0)
    motor_direito_potencia = saturar(motor_direito_potencia, 255, 0)


    label.config(text = f"{motor_esquerdo_potencia} 0 1 {motor_direito_potencia} 0 1 \n")
    send_message(serial_port, f"{motor_esquerdo_potencia} 0 1 {motor_direito_potencia} 1 0 \n")

    # Schedule the function to be called again after 1 second
    root.after(500, update_label)


def increase_slider_value(event):
    if event.keysym == 'Up':
        slider1.set(slider1.get() + 64)
    elif event.keysym == 'Down':
        slider1.set(slider1.get() - 64)
    if event.keysym == 'Right':
        slider2.set(slider2.get() - 64)
    elif event.keysym == 'Left':
        slider2.set(slider2.get() + 64)
root = tk.Tk()
root.title("Slider App")

# Slider 1
slider1 = tk.Scale(root, from_=0, to=1023, orient=tk.HORIZONTAL, label="Trhotle")
slider1.pack()

# Slider 2
slider2 = tk.Scale(root, from_=0, to=1023, orient=tk.HORIZONTAL, label="Steer")
slider2.set(512)
slider2.pack()

# Slider 3
slider3 = tk.Scale(root, from_=0, to=1023, orient=tk.HORIZONTAL, label="Brake")
slider3.pack()

# Label to display slider values
label = tk.Label(root, text="")
label.pack()

# Bind key events to the root window
root.bind('<KeyPress>', increase_slider_value)

update_label()

root.mainloop()

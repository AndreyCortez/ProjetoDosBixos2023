#include <SPI.h>
#include <LoRa.h>
#include <string.h>
#include <stdlib.h>

#define motor_esquerdo 5
#define motor_direito 3

char comando_bruto[100];
int comando_index = 0;

int fila_comandos[100][100];

char serial_string[100];

void executar_comando()
{
    //Serial.println(comando[0]);
    //Serial.println(comando[1]);

    switch (comando[0])
    {
    case 01:
        analogWrite(motor_direito, comando[1]);
        break;

    case 02: analogWrite(motor_esquerdo, comando[1]);
    
    default:
        break;
    }

    memset(comando,0,100);
}



void setup()
{
    Serial.begin(9600);
    while (!Serial)
        ;

    Serial.println("LoRa Receiver");

    if (!LoRa.begin(433E6))
    {
        Serial.println("Starting LoRa failed!");
        while (1)
            ;
    }

    //attachInterrupt(2, executar_comando, )
    

    pinMode(motor_direito, OUTPUT);
    pinMode(motor_esquerdo, OUTPUT);
}

void loop()
{
    // try to parse packet
    int packetSize = LoRa.parsePacket();
    if (packetSize)
    {
        // received a packet
        // Serial.println("Received packet '");

        // read packet
        while (LoRa.available())
        {
            comando_bruto[comando_index] = (char)LoRa.read();
            comando_index += 1;
        }

        //Serial.println(comando_bruto);
        char * pch = strtok(comando_bruto, " \n");
        comando_index = 0;


        while (pch != NULL)
        {
            //sprintf(serial_string,"%s\n", pch);
            //Serial.print(serial_string);
            
            comando[comando_index] = atoi(pch);

            pch = strtok(NULL, " \n");
            comando_index++;
        }


        executar_comando();
        memset(comando_bruto,0,100);
        
    }
}

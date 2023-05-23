#include <SPI.h>
#include <LoRa.h>
#include <string.h>
#include <stdlib.h>

#define motor_esquerdo_pwm 6
#define motor_esquerdo_in1 A0
#define motor_esquerdo_in2 A1

#define motor_direito_pwm 5
#define motor_direito_in3 A2
#define motor_direito_in4 A3

char comando_bruto[100];
int fila_comandos[100];

void pacote_recebido();
void executar_comando(int *comando);
void checar_conexao();

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

    // attachInterrupt(2, executar_comando, )

    /* Aqui definimos os pinos que serão utilizados */
    pinMode(motor_esquerdo_pwm, OUTPUT);
    pinMode(motor_esquerdo_in1, OUTPUT);
    pinMode(motor_esquerdo_in2, OUTPUT);
    pinMode(motor_direito_pwm, OUTPUT);
    pinMode(motor_direito_in3, OUTPUT);
    pinMode(motor_direito_in4, OUTPUT);

    digitalWrite(motor_esquerdo_in1, LOW);
    digitalWrite(motor_esquerdo_in2, LOW);
    digitalWrite(motor_direito_in3, LOW);
    digitalWrite(motor_direito_in4, LOW);
}

void loop()
{
    // try to parse packet
    int packetSize = LoRa.parsePacket();
    if (packetSize)
    {
        // received a packet
        //Serial.println("Received packet '");

        // read packet
        int comando_index = 0;


        while (LoRa.available())
        {
            comando_bruto[comando_index] = (char)LoRa.read();
            comando_index += 1;
        }

        //Serial.println(comando_bruto);
        char *pch = strtok(comando_bruto, " \n");
        comando_index = 0;

        while (pch != NULL)
        {
            // sprintf(serial_string,"%s\n", pch);
            // Serial.print(serial_string);

            fila_comandos[comando_index] = atoi(pch);

            pch = strtok(NULL, " \n");
            comando_index++;
        }

        executar_comando(fila_comandos);
        memset(fila_comandos, 0, 100);
        memset(comando_bruto, 0, 100);
    }
}

void executar_comando(int *comando)
{
    for (int i = 0; i < 6; i++)
    {
        Serial.print(i);
        Serial.print(" : ");
        Serial.println(comando[i]);
    }

    analogWrite(motor_esquerdo_pwm, comando[0]);
    digitalWrite(motor_esquerdo_in1, comando[1]);
    digitalWrite(motor_esquerdo_in2, comando[2]);

    analogWrite(motor_direito_pwm, comando[3]);
    digitalWrite(motor_direito_in3, comando[4]);
    digitalWrite(motor_direito_in4, comando[5]);
}

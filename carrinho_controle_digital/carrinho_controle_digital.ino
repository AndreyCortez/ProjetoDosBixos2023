#include <SPI.h>
#include <LoRa.h>

int counter = 0;

void setup()
{
    Serial.begin(9600);
    while (!Serial)
        ;

    Serial.println("LoRa Sender");

    if (!LoRa.begin(433E6))
    {
        Serial.println("Starting LoRa failed!");
        while (1)
            ;
    }
}

char comando_bruto[100];
int comando_index = 0;
String receivedData;

void loop()
{

    while (Serial.available())
    {
        receivedData = Serial.readStringUntil('\n'); // Read the incoming data until a newline character is received
        receivedData.trim();                         // Remove leading and trailing whitespace characters
    }

    if (receivedData != "")
    {
        // send packet
        LoRa.beginPacket();
        Serial.print(receivedData.c_str());
        LoRa.print(receivedData.c_str());
        LoRa.endPacket();
    }
    receivedData = "";
}

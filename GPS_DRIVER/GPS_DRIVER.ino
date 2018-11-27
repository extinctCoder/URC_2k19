#include <TinyGPS++.h>
#include <SoftwareSerial.h>

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

int updateRate = 6;

TinyGPSPlus gps;

SoftwareSerial ss(RXPin, TXPin);

void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud); 
}

void loop()
{
  if(gps.location.isValid()){
    if(gps.location.isUpdated()){
      Serial.println (String(gps.location.lat(),updateRate)+","+String(gps.location.lng(),updateRate));
    }}
    smartDelay(0);
}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}

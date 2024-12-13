/**
#NOTE: I left a strange ordering that needs to be accounted for when dealing with errors
since we may have succeeded in commanding the IO expander but fail to disconnect from the bus. 

Dec 12 2024
The previous version of the amp board does not use I2C repeaters while the updated one at ASU does. We still want to use the up to date primecamfe python library
while putting in the least work. Simplist method is probably to fake the connect/disconnect comand and alter the addressing of the expanders since we are addressing them instead.
**/
#define _CLEARBUFF  while(Serial.available()>0){Serial.read();}

#include <Wire.h>

#define __I2C_REPEATER_I2C_ADDR 0b1100000
#define __IO_EXPANDER_I2C_ADDR 0b0100000
#define __LTC4302_CMD_CONNECT_CARD 0b11100000
#define __LTC4302_CMD_DISCONNECT_CARD 0b01100000

// send the 'connect bus' command to the register.
int connect_i2c_bus(uint8_t address)
{
    return 0;
}

// send the 'disconnect bus' command to the repeater
int disconnect_i2c_bus(uint8_t address)
{
    return 0;
}

void setup(){
    Serial.begin(115200);
    Wire.begin();    
}

void loop(){
    char data[2];

    while(Serial.available() < 2);

    String str = Serial.readStringUntil('\n');
    if (str.equals("get_id")){
        //ensure empty input
        _CLEARBUFF
        Serial.println("primecam_amp_frontend");
    }
    else if (str.equals("set_atten"))
    {
        Serial.readBytes(data, 2);
        _CLEARBUFF
        if (data[0] > 7){
            Serial.println("FAIL, BAD ADDRESS NOT BETWEEN 0 THROUGH 7");
            return;
        }
        if (data[1] > 127){
            Serial.println("FAIL, ATTENUATION VALUE MUST BE BETWEEN 0 AND 31.75");
            return;
        }
        //ensure empty input
      

      if (connect_i2c_bus(data[0])!=0){
        Serial.println(("FAIL, NO-ACKNOWLEDGE FROM I2C REPEATER ON CONNECT()"));
        return;
      }
      Wire.beginTransmission(0b0100000+data[0]);
      Wire.write(data[1]);
      int status = Wire.endTransmission();
      if (disconnect_i2c_bus(data[0])!=0){
          Serial.println("FAIL, NO-ACKNOWLEDGE FROM I2C REPEATER ON DISCONNECT()");
          return;
      }
      if (status == 0){
          Serial.println("OK");
      } else {
          Serial.println("FAIL, NO-ACKNOWLEDGE FROM IO EXPANDER");
      }
    } else if(str.equals("get_atten")){
        Serial.readBytes(data, 1);
        _CLEARBUFF
        if (data[0] > 7){
            Serial.println("FAIL, BAD ADDRESS NOT BETWEEN 0 THROUGH 7");
            return;
        }
        if (connect_i2c_bus(data[0])!=0){
            Serial.println(("FAIL, NO-ACKNOWLEDGE FROM I2C REPEATER ON CONNECT()"));
            return;
        }
        data[1] = 0;
        Wire.requestFrom(0b0100000+data[0], 1);
        data[1] = Wire.read();
        int status = Wire.endTransmission();
        if (disconnect_i2c_bus(data[0])!=0){
            Serial.println("FAIL, NO-ACKNOWLEDGE FROM I2C REPEATER ON DISCONNECT()");
            return;
        }
        Serial.println(data[1], DEC);

    } 
    else {
        Serial.println("BAD COMMAND");
    }

}
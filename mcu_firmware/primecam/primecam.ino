/**
#NOTE: I left a strange ordering that needs to be accounted for when dealing with errors
since we may have succeeded in commanding the IO expander but fail to disconnect from the bus. 
**/
#include <Wire.h>

#define __I2C_REPEATER_I2C_ADDR 0b1100000
#define __IO_EXPANDER_I2C_ADDR 0b0100000
#define __LTC4302_CMD_CONNECT_CARD 0b11100000
#define __LTC4302_CMD_DISCONNECT_CARD 0b01100000

// send the 'connect bus' command to the register.
int connect_i2c_bus(uint8_t address)
{
  Wire.beginTransmission(__I2C_REPEATER_I2C_ADDR + address);
  Wire.write(__LTC4302_CMD_CONNECT_CARD); // Connect IIC Bus
  return Wire.endTransmission();
}

// send the 'disconnect bus' command to the repeater
int disconnect_i2c_bus(uint8_t address)
{
  Wire.beginTransmission(__I2C_REPEATER_I2C_ADDR + address);
  Wire.write(__LTC4302_CMD_DISCONNECT_CARD);
  return Wire.endTransmission();
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
        while(Serial.available()>0){
            Serial.read();
        }
        Serial.println("primecam_amp_frontend");
    }
    else if (str.equals("set_atten"))
    {
        Serial.readBytes(data, 2);

        if (data[0] == 0 || data[0] > 8){
            Serial.println("FAIL, BAD ADDRESS NOT BETWEEN 1 THROUGH 8");
            return;
        }
        if (data[1] > 127){
            Serial.println("FAIL, ATTENUATION VALUE IS TOO LARGE");
            return;
        }
        //ensure empty input
        while(Serial.available()>0){
            Serial.read();
        }

      if (connect_i2c_bus(data[0])!=0){
        Serial.println(("FAIL, NO-ACKNOWLEDGE FROM I2C REPEATER ON CONNECT()"));
        return;
      }
      Wire.beginTransmission(0b0100000);
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
    } else {
        Serial.println("BAD COMMAND");
    }

}
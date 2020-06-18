#include <SPI.h> 
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN   9
#define CSN_PIN 10
#define x_axis A0 // x axis
#define y_axis A1 //y axis
#define button1 8 // joystick button
#define button2 2 // A button
#define button3 3 // B button
#define button4 4 // C button
#define button5 5 // D button
#define button6 6 // E button
#define button7 7 // F button

const uint64_t pipe = 0xF0F0F0F0E1LL;//0xE8E8F0F0E1LL 
RF24 radio(CE_PIN, CSN_PIN); 
byte radioData[4];  
int throttle = 1000;
boolean incrementFlag = false;
boolean decrementFlag = false;
boolean autonomous = false;
void setup() 
{
  Serial.begin(9600);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
  pinMode(button4, INPUT);
  pinMode(button5, INPUT);
  pinMode(button6, INPUT);
  pinMode(button7, INPUT);
}
void loop()   
{
  //radioData[0] = 0x25;//map(analogRead(x_axis),0,1023,0,200);
  radioData[0] = (char)(map(analogRead(x_axis),0,1023,0,200));
  if (digitalRead(button4)== 0 && incrementFlag == false){
    if(throttle < 1300){
      throttle += 300;
    }
    else if (throttle < 2000) {
      throttle += 100;
    }
    incrementFlag = true;
  }
  else if (digitalRead(button4)== 1){
    incrementFlag = false;
  }
  if (digitalRead(button2)== 0 && decrementFlag == false){
    if(throttle > 1300){
      throttle -= 100;
    }
    else if (throttle > 1000) {
      throttle -= 300;
    }
    decrementFlag = true;
  }
  else if (digitalRead(button2)== 1){
    decrementFlag = false;
  }
  //radioData[1] = 0x20;//throttle/10;
  //radioData[2] = 0x01;//digitalRead(button3);
  radioData[1] = (char)(throttle/10);
  radioData[2] = (char)(digitalRead(button3));
  if (!digitalRead(button6)){
    autonomous = true;
  }
  else if (!digitalRead(button7)){
    autonomous = false;
  }
  radioData[3] = (char)(autonomous);
  radio.write(&radioData, sizeof(radioData)); 
 //Serial.print(radioData[0]);
 //Serial.print('\t');
 //Serial.println(radioData[1]);
 //delay(50);
}

 #define THROTTLE A0
#define TEMP A4
float tempOffset = 22.3;
unsigned long start = millis();
float speed = 0.0;
float fuel = 100;
unsigned long updateFuel = millis();
unsigned long sendData = millis();
unsigned long seq = 0;
float calculateThrottle() {
  int raw = analogRead(THROTTLE);
  float throttle = raw * (100.0/1023.0);
  return throttle;
}
float calculateSpeed(float throttle) {
  float v = throttle * 2.2;
  speed += (v - speed) * 0.08;
  if (speed < 0.1) speed = 0.0;
  if (speed > 220.0) speed = 220.0;
  return speed;
}
float calculateRPM(float Speed){
  float rpm = 800.0 + (Speed * (5200.0/220.0));
  if (rpm >= 6000.0) rpm = 6000.0;
  return rpm;
}
float calculateTemp() {
  float raw = analogRead(TEMP);
  float voltage = raw * (5.0/1023.0);
  float temp = voltage * 100.0;
  temp -= tempOffset;
  return temp;
}
float calculateFuel() {
  unsigned long fuelNow = millis();
  if((fuelNow - updateFuel) >= 10000){
    updateFuel = fuelNow;
    if(speed > 1.0){
      fuel -= 0.02;
      if(fuel < 0.0) fuel = 0.0;
    }
  }
  return fuel;
}
void setup() {
  pinMode(THROTTLE, INPUT);
  pinMode(TEMP, INPUT);
  Serial.begin(115200);
}
void loop() {
  float throttle = calculateThrottle();
  speed = calculateSpeed(throttle);
  float rpm = calculateRPM(speed);
  float temp = calculateTemp();
  fuel = calculateFuel();
  unsigned long now = millis();
  if ((now - sendData) >= 500) {
    sendData = now;
    seq++;
    Serial.print("{\"seq\":");
    Serial.print(seq);
    Serial.print(",\"throttle\":");
    Serial.print(throttle, 1);
    Serial.print(",\"speed\":");
    Serial.print(speed, 1);
    Serial.print(",\"rpm\":");
    Serial.print(rpm, 0);
    Serial.print(",\"temp\":");
    Serial.print(temp, 1);
    Serial.print(",\"fuel\":");
    Serial.print(fuel, 1);
    Serial.println("}");
  }
}

#include <Wire.h>

const int MPU_ADDR = 0x68;  // Adresse I2C du MPU6050

float accX_offset = 0.0f;
float accY_offset = 0.0f;
float accZ_offset = 0.0f;

void setup() {
  Serial.begin(9600);
  delay(1000); // Donne le temps au moniteur série de se connecter

  Wire.begin();

  // Réveil du MPU6050
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); // registre power management
  Wire.write(0x00); // wake up
  Wire.endTransmission(true);

  Serial.println("== Calibration de l'accéléromètre ==");

  calibrateAccelerometer();

  Serial.println("== Offsets mesurés (bruts et en g) ==");
  Serial.print("AccX offset (brut) = "); Serial.println(accX_offset);
  Serial.print("AccY offset (brut) = "); Serial.println(accY_offset);
  Serial.print("AccZ offset (brut) = "); Serial.println(accZ_offset);
  Serial.println();
  
  Serial.print("AccX offset (g) = "); Serial.println(accX_offset / 16384.0f, 6);
  Serial.print("AccY offset (g) = "); Serial.println(accY_offset / 16384.0f, 6);
  Serial.print("AccZ offset (g) = "); Serial.println(accZ_offset / 16384.0f, 6);
}

void loop() {
  // Ne rien faire ici
}

void readRawAccel(int16_t &ax, int16_t &ay, int16_t &az) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // Adresse du registre AccX
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);

  if (Wire.available() >= 6) {
    ax = Wire.read() << 8 | Wire.read();
    ay = Wire.read() << 8 | Wire.read();
    az = Wire.read() << 8 | Wire.read();
  }
}

void calibrateAccelerometer() {
  long sumX = 0, sumY = 0, sumZ = 0;
  int16_t ax, ay, az;
  const int N = 1000;

  for (int i = 0; i < N; i++) {
    readRawAccel(ax, ay, az);
    sumX += ay;
    sumY += -ax;
    sumZ += az;
    delay(2);
  }

  accX_offset = (float)sumX / N;
  accY_offset = (float)sumY / N;
  accZ_offset = (float)sumZ / N - 16384.0f; // on enlève 1g de gravité
}

#include <Wire.h>

const int MPU_ADDR = 0x68;  // Adresse I2C du MPU6050

float gyroX_offset = 0.0f;
float gyroY_offset = 0.0f;
float gyroZ_offset = 0.0f;

void setup() {
  Serial.begin(9600);
  delay(1000); // Laisse le temps au moniteur série de se connecter

  Wire.begin();

  // Réveil du MPU6050
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); // registre power management
  Wire.write(0x00); // wake up
  Wire.endTransmission(true);

  Serial.println("== Calibration du gyroscope ==");

  calibrateGyroscope();

  Serial.println("== Offsets mesurés (bruts et en °/s) ==");

  Serial.print("GyroX offset (brut) = "); Serial.println(gyroX_offset);
  Serial.print("GyroY offset (brut) = "); Serial.println(gyroY_offset);
  Serial.print("GyroZ offset (brut) = "); Serial.println(gyroZ_offset);
  Serial.println();

  Serial.print("GyroX offset (°/s) = "); Serial.println(gyroX_offset / 131.0f, 6);
  Serial.print("GyroY offset (°/s) = "); Serial.println(gyroY_offset / 131.0f, 6);
  Serial.print("GyroZ offset (°/s) = "); Serial.println(gyroZ_offset / 131.0f, 6);
}

void loop() {
  // Ne rien faire ici
}

void readRawGyro(int16_t &gx, int16_t &gy, int16_t &gz) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x43); // Adresse du registre GyroX
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);

  if (Wire.available() >= 6) {
    gx = Wire.read() << 8 | Wire.read();
    gy = Wire.read() << 8 | Wire.read();
    gz = Wire.read() << 8 | Wire.read();
  }
}

void calibrateGyroscope() {
  long sumX = 0, sumY = 0, sumZ = 0;
  int16_t gx, gy, gz;
  const int N = 1000;

  for (int i = 0; i < N; i++) {
    readRawGyro(gx, gy, gz);
    sumX += gy;
    sumY += -gx;
    sumZ += gz;
    delay(2); // petit délai pour stabiliser les lectures
  }

  gyroX_offset = (float)sumX / N;
  gyroY_offset = (float)sumY / N;
  gyroZ_offset = (float)sumZ / N;
}

#include <Wire.h>
#include "Kalman.h"
#include <MPU6050.h>
#include <QMC5883LCompass.h>

MPU6050 mpu;
QMC5883LCompass mag;
Kalman kalmanX, kalmanY;

float accX, accY, accZ;
float gyroX, gyroY, gyroZ;
float magX, magY, magZ;
float roll, pitch, yaw;

unsigned long timer;
float dt;

// Calibration offsets
float magX_offset = 0, magY_offset = 0;

void calibrateMagnetometer() {
  long xMin = 32767, xMax = -32768, yMin = 32767, yMax = -32768;
  Serial.println("Move the sensor in all directions to calibrate the magnetometer...");
  for (int i = 0; i < 500; i++) {
    mag.read();
    int x = mag.getX();
    int y = mag.getY();
    if (x < xMin) xMin = x;
    if (x > xMax) xMax = x;
    if (y < yMin) yMin = y;
    if (y > yMax) yMax = y;
    delay(20);
  }
  magX_offset = (xMax + xMin) / 2.0;
  magY_offset = (yMax + yMin) / 2.0;
  Serial.println("Calibration done.");
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
  mag.init();
  mag.setCalibrationOffsets(0, 0, 0); // default

  calibrateMagnetometer();

  timer = micros();
}

void loop() {
  // Compute dt
  unsigned long now = micros();
  dt = (now - timer) / 1000000.0;
  timer = now;

  // Read MPU6050
  accX = mpu.getAccelerationX() / 16384.0;
  accY = mpu.getAccelerationY() / 16384.0;
  accZ = mpu.getAccelerationZ() / 16384.0;
  gyroX = mpu.getRotationX() / 131.0;
  gyroY = mpu.getRotationY() / 131.0;
  gyroZ = mpu.getRotationZ() / 131.0;

  // Compute pitch and roll from acc
  float rollAcc = atan2(accY, accZ) * RAD_TO_DEG;
  float pitchAcc = atan2(-accX, sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;

  // Kalman filter update
  roll = kalmanX.getAngle(rollAcc, gyroX, dt);
  pitch = kalmanY.getAngle(pitchAcc, gyroY, dt);

  // Read magnetometer
  mag.read();
  magX = mag.getX() - magX_offset;
  magY = mag.getY() - magY_offset;
  yaw = atan2(magY * cos(roll * DEG_TO_RAD) + magZ * sin(roll * DEG_TO_RAD),
              magX * cos(pitch * DEG_TO_RAD) +
              magY * sin(pitch * DEG_TO_RAD) * sin(roll * DEG_TO_RAD) -
              magZ * sin(pitch * DEG_TO_RAD) * cos(roll * DEG_TO_RAD));
  yaw *= RAD_TO_DEG;
  if (yaw < 0) yaw += 360;

  // Display
  Serial.print("Roll: ");
  Serial.print(roll);
  Serial.print(" Pitch: ");
  Serial.print(pitch);
  Serial.print(" Yaw: ");
  Serial.println(yaw);

  delay(20);
}

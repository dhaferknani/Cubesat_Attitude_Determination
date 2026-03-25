# Cubesat_Attitude_Determination
Focusing on estimating spacecraft orientation using MEMS sensors and algorithms such Kalman filters for precise pointing control.  Key Features Processes inertial and reference data (e.g., angular rates, magnetic fields, sun vectors) to output quaternions and attitude estimates. 
# CubeSat Attitude Determination using MEMS Sensor Data Fusion

**Final Year Degree Project**  
Attitude determination of a CubeSat by fusing data from MEMS sensors (Gyroscope, Accelerometer, Magnetometer) using complementary filter / Kalman filter / Madgwick filter (choose what you used).

![Project Overview](results/simulation_screenshot.png)  
*(Add one or two key screenshots or plots here - e.g. estimated vs real attitude quaternion or Euler angles)*
dynamic Test of the cubesat with 0° angle
<img width="1543" height="2153" alt="image" src="https://github.com/user-attachments/assets/ec1df288-0c30-4403-bd02-3a014e3caafd" />
dynamic Test of the cubesat with 180° angle
<img width="1543" height="2153" alt="image" src="https://github.com/user-attachments/assets/cb9925fa-c54b-45e7-835a-91b95a5deac1" />

## 🎯 Project Overview
This project implements **sensor data fusion algorithms** to estimate the orientation (attitude) of a 1U/3U CubeSat in orbit or in a simulation/test environment.  
The system processes raw MEMS IMU/MAG data and outputs quaternion or Euler angles.

### Key Features
- Real-time or offline sensor data processing
- Implementation of **data fusion** (e.g., Complementary filter, Extended Kalman Filter, Madgwick)
- Simulation of CubeSat dynamics (or hardware-in-the-loop)
- Comparison between different fusion methods
- Python for high-level simulation & visualization
- C/C++ for embedded/real-time performance

## 🛠️ Technologies
- **Python** – Data processing, simulation, plotting (NumPy, SciPy, Matplotlib)
- **C / C++** – Optimized algorithms for embedded systems
- MEMS Sensors: Gyroscope, Accelerometer, Magnetometer
- Tools: CMake / GCC (for C++), Jupyter Notebooks (optional)

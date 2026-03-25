import pandas as pd
import serial
import time
import numpy as np
import csv
# Read CSV
data = pd.read_csv(
    "C:\\Users\\knani\\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\\document stage\\donnée.csv",
    encoding='latin1',
    sep=';',
    skiprows=12
)

# Configure serial port
ser = serial.Serial('COM5', 115200)  # Replace with your ESP32's COM port
time.sleep(2)  # Wait for serial connection to initialize

# Lists to store RMSE values for each line
rmse_roll = []
rmse_pitch = []
rmse_yaw = []

output_filename = "arduino_results.csv"
output_file = open(output_filename, mode='w', newline='')
csv_writer = csv.writer(output_file)
# Write header
csv_writer.writerow([
    "Line", "Roll_Arduino", "Pitch_Arduino", "Yaw_Arduino",
    "Roll_CSV", "Pitch_CSV", "Yaw_CSV",
    "RMSE_Roll", "RMSE_Pitch", "RMSE_Yaw"
])
# Send data line by line and calculate RMSE
for index, row in data.iterrows():
    # Format sensor data with newline terminator
    line = f"{row['Ax(g)']},{row['Ay(g)']},{row['Az(g)']},"
    line += f"{row['Gx(r/s)']},{row['Gy(r/s)']},{row['Gz(r/s)']},"
    line += f"{row['Mx(uT)']},{row['My(uT)']},{row['Mz(uT)']}\n"
    
    try:
        # Send data to ESP32
        ser.write(line.encode())
        #print("Sent:", line.strip())
        
        # Read response from ESP32
        response = ser.readline().decode('utf-8').strip()
        #print("Received:", response)
        
        # Parse Arduino output (roll,pitch,yaw)
        try:
            roll_arduino, pitch_arduino, yaw_arduino = map(float, response.split(','))
        except ValueError:
            print(f"Error parsing Arduino response at line {index}: {response}")
            continue
        
        # Get CSV estimated Euler angles
        roll_csv = row['r_est(d)']
        pitch_csv = row['p_est(d)']
        yaw_csv = row['y_est(d)']
        def angle_diff(yaw_arduino, yaw_csv):
         #calculate the minimum difference between two angles
         # Normalize yaw_arduino to [0, 360)
         d = yaw_arduino - yaw_csv
         # Normalize to [-180, 180]
         return (d + 180) % 360 - 180
        # Calculate errors
        error_roll = roll_arduino - roll_csv
        error_pitch = pitch_arduino - pitch_csv
        #error_yaw = yaw_arduino - yaw_csv
        error_yaw = angle_diff(yaw_arduino, yaw_csv)
        # Calculate RMSE for this line (single point, so RMSE = absolute error)
        rmse_roll.append(error_roll ** 2)
        rmse_pitch.append(error_pitch ** 2)
        rmse_yaw.append(error_yaw ** 2)
        
        #print(f"Line {index},Rx:{response}, RMSE - Roll: {np.sqrt(error_roll ** 2):.2f}, Pitch: {np.sqrt(error_pitch ** 2):.2f}, Yaw: {np.sqrt(error_yaw ** 2):.2f}")
        csv_writer.writerow([
        index,
        roll_arduino, pitch_arduino, yaw_arduino,
        roll_csv, pitch_csv, yaw_csv,
        np.sqrt(error_roll ** 2),
        np.sqrt(error_pitch ** 2),
        np.sqrt(error_yaw ** 2)
    ])
    except serial.SerialException as e:
        print(f"Serial error at line {index}: {e}")
        break
    except Exception as e:
        print(f"Error at line {index}: {e}")
        continue
    
    time.sleep(0.05)  # Delay to prevent overwhelming the ESP32

# Close serial connection
#ser.close()
print(f"\nSaved all results to {output_filename}")
# Calculate average RMSE across all lines
if rmse_roll and rmse_pitch and rmse_yaw:
    avg_rmse_roll = np.sqrt(np.mean(rmse_roll))
    avg_rmse_pitch = np.sqrt(np.mean(rmse_pitch))
    avg_rmse_yaw = np.sqrt(np.mean(rmse_yaw))
    print("\nAverage RMSE:")
    print(f"Roll: {avg_rmse_roll:.2f} degrees")
    print(f"Pitch: {avg_rmse_pitch:.2f} degrees")
    print(f"Yaw: {avg_rmse_yaw:.2f} degrees")
else:
    print("\nNo valid RMSE data calculated.")
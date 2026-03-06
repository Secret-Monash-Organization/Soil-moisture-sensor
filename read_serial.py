import serial
import time
import csv

# Setup serial connection
ser = serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)


with open('DataLog.csv','r',newline='') as file:
    reader = csv.reader(file)

    csv_data = []
    row_idx = 0

    for row in reader:
        if row_idx != 0:   #skip first row
            csv_data.append(row)
        row_idx += 1


mass_input = int(input("Choose a mass to log [0,25,50,75,100]: \n"))
while mass_input not in [0,25,50,75,100]:
    mass_input = int(input("Choose a mass to log [0,25,50,75,100]: \n"))


time.sleep(2) #wait for connection

write_buffer = [mass_input]

if ser.is_open():
    print("Serial port connected successfully!")
    for _ in range(3):
        msg_adc = ser.readline().decode().strip() #convert serial bytes to float
        write_buffer.append(float(msg_adc))

else: print("Failed to connect port")

#modify row
for i,row in enumerate(csv_data):
    if int(row[0]) == mass_input: csv_data[i] = write_buffer

with open('DataLog.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)
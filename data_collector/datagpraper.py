import serial
import time

# 시리얼 포트 설정
ser = serial.Serial('COM3', 9600, timeout=1)

# 파일 열기
file_path = 'rail_30_data_1.txt'
file = open(file_path, 'w')

iter = 0
start_time = time.time() 

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        try:
            iter += 1
            parts = line.split(',')  # 데이터 파싱
            if len(parts) >= 4:
                # 현재 시간에서 시작 시간을 빼서 상대 시간 계산
                current_time = time.time() - start_time

                ax_val = float(parts[4])  # X 축 가속도
                ay_val = float(parts[5])  # Y 축 가속도
                az_val = float(parts[6])  # Z 축 가속도
                
                print(f'{iter} : x 축 가속도 {ax_val}, y축 가속도 {ay_val}, z축 가속도 {az_val}')

                file.write(f"{ax_val},{ay_val},{az_val}\n")
        except ValueError:
            print("데이터 파싱 실패:", line)
    time.sleep(0.01)  


import serial
import matplotlib.pyplot as plt
import time

ser = serial.Serial('COM3', 9600, timeout=1)

# 파일 열기
file_path = 'bearing_15_data_2].txt'
file = open(file_path, 'w')

iter = 0
# 초기 그래프 및 데이터 리스트 설정
plt.ion()
fig, ax = plt.subplots()
times = []  # 시간축 데이터 저장 리스트
ydata_x, ydata_y, ydata_z = [], [], []  # X, Y, Z 축 가속도 데이터 리스트
line_x, = ax.plot(times, ydata_x, 'r-', label='X axis')
line_y, = ax.plot(times, ydata_y, 'g-', label='Y axis')
line_z, = ax.plot(times, ydata_z, 'b-', label='Z axis')
ax.legend()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration')
start_time = time.time()  # 시작 시간 기록

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        try:
            iter += 1
            parts = line.split(',')  # 데이터 파싱
            if len(parts) >= 4:
                # 현재 시간에서 시작 시간을 빼서 상대 시간 계산
                current_time = time.time() - start_time
                times.append(current_time)
                
                ax_val = float(parts[4])  # X 축 가속도
                ay_val = float(parts[5])  #s Y 축 가속도
                az_val = float(parts[6])  # Z 축 가속도
                
                ydata_x.append(ax_val)
                ydata_y.append(ay_val)
                ydata_z.append(az_val)

                print(f'{iter} : x 축 가속도 {ax_val}, y축 가속도 {ay_val}, z축 가속도 {az_val}')

                # 데이터를 파일에 저장
                file.write(f"{ax_val},{ay_val},{az_val}\n")

                # # 그래프 업데이트
                line_x.set_data(times, ydata_x)
                line_y.set_data(times, ydata_y)
                line_z.set_data(times, ydata_z)

                ax.relim()  # 데이터 한계 업데이트
                ax.autoscale_view()  # 축 스케일 자동 조정

                fig.canvas.draw()
                fig.canvas.flush_events()
        except ValueError:
            print("데이터 파싱 실패:", line)
    plt.pause(0.01)

# 프로그램이 종료될 때 파일을 닫기 위한 코드
file.close()

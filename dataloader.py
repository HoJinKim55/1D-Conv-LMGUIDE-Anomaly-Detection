import numpy as np
import glob
import pandas as pd

"""
original = 센서 30개
"""
step_max = 5
min_time = 0
max_time = 20000
gap_time = 10
win_size = [10, 30, 60]

train_start = 0
train_end = 8000


def generate_signature_matrix_node(data):
	sensor_n = data.shape[0]
	# min-max normalization
	max_value = np.max(data, axis=1)
	min_value = np.min(data, axis=1)
	data = (np.transpose(data) - min_value)/(max_value - min_value + 1e-6)
	data = np.transpose(data)

	#multi-scale signature matix generation
	for w in range(len(win_size)):
		matrix_all = []
		win = win_size[w]
		print ("generating signature with window " + str(win) + "...")
		for t in range(min_time, max_time, gap_time):
			#print t
			matrix_t = np.zeros((sensor_n, sensor_n))
			if t >= 60:
				for i in range(sensor_n): #30x30
					for j in range(i, sensor_n):
						#if np.var(data[i, t - win:t]) and np.var(data[j, t - win:t]):
						matrix_t[i][j] = np.inner(data[i, t - win:t], data[j, t - win:t])/(win) # rescale by win
						matrix_t[j][i] = matrix_t[i][j]
			matrix_all.append(matrix_t)
		return matrix_all
	

def generate_train_test_data(matrix_all):
	data_all = matrix_all
	
	train_test_time = [[train_start, train_end]]
	for i in range(len(train_test_time)):
		step_multi_matrix = []
		for data_id in range(int(train_test_time[i][0]/gap_time)):
			
			for step_id in range(step_max, 0, -1):
				multi_matrix = []
				# for k in range(len(value_colnames)):
				for i in range(len(win_size)):
					multi_matrix.append(data_all[i][data_id - step_id])
				step_multi_matrix.append(multi_matrix)
		return step_multi_matrix







if __name__ == '__main__':
	csv_path = glob.glob("C:/Users/oltea/Desktop/kinhojin/졸업작품/코드/code/challenge_data/train/*.csv")
	vib_arr = []
	vib2_arr = []
	for i in csv_path:
		cs = pd.read_csv(i)
		x = cs['bearingB_x'].values
		y = cs['bearingB_y'].values
		vib_arr.append([x,y])
	vib_arr = np.array(vib_arr)

	vib_arr = np.reshape(vib_arr, (2,-1))
	a = generate_signature_matrix_node(vib_arr)
	b = generate_train_test_data(a)
	print(1)





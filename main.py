from kalman_filter import KalmanFilter
import ngsim_data_loader as data_loader
import sys
import numpy as np
import matplotlib.pyplot as plt



if __name__ == "__main__":
	tracked_objects = {}

	if len(sys.argv) < 2:
		print("Usage: python main.py <data_path>")
		sys.exit(1)
	file_path = sys.argv[1]
	labeled_objects = data_loader.load_data(file_path)

	for labeled_object in labeled_objects:
		if labeled_object.vehicle_id not in tracked_objects:
			tracked_objects[labeled_object.vehicle_id] = []
		else:
			tracked_objects[labeled_object.vehicle_id].append(labeled_object)

	filter = KalmanFilter()

	for idx, vehicle_id in enumerate(tracked_objects):
		if idx <= 4:
			continue
		gt_points_x = []
		gt_points_y = []
		kalman_points_x = []
		kalman_points_y = []
		#for labeled_object in tracked_objects[vehicle_id]:
			#print(labeled_object)
		#	print(str(labeled_object.local_x) + " " +str(labeled_object.local_y))
		#sys.exit(1)
		for labeled_object in tracked_objects[vehicle_id]:

			measurements = np.zeros((2, 1))
			measurements[0] = labeled_object.local_x
			measurements[1] = labeled_object.local_y

			print("measurements:")
			print(measurements)
			x, P = filter.predict()
			gt_points_x.append(measurements[0].item(0))
			gt_points_y.append(measurements[1].item(0))
			kalman_points_x.append(x[0].item(0))
			kalman_points_y.append(x[1].item(0))
			print("x:")
			print(x)
			#print("cov:")
			#print(filter.P)
			filter.update(measurements)
		temp1 = np.array(kalman_points_x)
		#print(np.array(kalman_points_x))
		print("GROUND TRUTH------------------")
		temp2 = np.array(gt_points_x)
		#for idx, elem in enumerate(gt_points_x):
		#	if idx == 0:
		#		continue
		#	else:
		#		print(gt_points_x[idx] - gt_points_x[idx-1])

		plt.plot(gt_points_x, gt_points_y)
		plt.plot(kalman_points_x, gt_points_y)
		plt.show()
		break

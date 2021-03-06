from kalman_filter import KalmanFilter
import data_loader
import sys
import numpy as np
import matplotlib.pyplot as plt



if __name__ == "__main__":
	tracked_objects = {}

	if len(sys.argv) < 2:
		print("Usage: python main.py <file_name>")
		sys.exit(1)
	file_path = sys.argv[1]
	labeled_objects = data_loader.load_data(file_path)

	for labeled_object in labeled_objects:
		if labeled_object.track_id not in tracked_objects:
			tracked_objects[labeled_object.track_id] = []
		else:
			tracked_objects[labeled_object.track_id].append(labeled_object)
		# print(labeled_object.track_id)


	filter = KalmanFilter()

	for track_id in tracked_objects:
		if track_id == -1:
			continue
		gt_points_x = []
		gt_points_y = []
		kalman_points_x = []
		kalman_points_y = []
		for labeled_object in tracked_objects[track_id]:
			z = labeled_object.bbox
			print("z:")
			print(z)
			top_left_x = float(z[0])
			top_left_y = float(z[1])

			bottom_right_x = float(z[2])
			bottom_right_y = float(z[3])

			centre_x = (top_left_x + bottom_right_x) / 2
			centre_y = (top_left_y + bottom_right_y) / 2
			measurements = np.zeros((2, 1))
			measurements[0] = centre_x
			measurements[1] = centre_y

			print("measurements:")
			print(z)
			x, P = filter.predict()
			gt_points_x.append(measurements[0])
			gt_points_y.append(measurements[1])
			kalman_points_x.append(x[0])
			kalman_points_y.append(x[1])
			#print("x:")
			print(labeled_object.bbox)
			filter.update(measurements)
		plt.scatter(gt_points_x, gt_points_y)
		plt.scatter(kalman_points_x, kalman_points_y)
		plt.show()
		break

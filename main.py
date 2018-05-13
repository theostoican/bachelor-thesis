from kalman_filter import KalmanFilter
import data_loader
import sys
import numpy as np


if __name__ == "__main__":
	tracked_objects = {}

	if len(sys.argv) < 2:
		print("Usage: python data_loader.py <file_name>")
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
		for labeled_object in tracked_objects[track_id]:
			z = labeled_object.location
			measurements = np.zeros((2, 1))
			measurements[0] = z[0]
			measurements[1] = z[2]

			print("measurements:")
			print(z)
			x, P = filter.predict()
			#print("x:")
			print(x)
			filter.update(measurements)
		break
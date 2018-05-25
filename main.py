from kalman_filter import KalmanFilter
import ngsim_data_loader as data_loader
import sys
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser


if __name__ == "__main__":
	tracked_objects = {}
	parser = ArgumentParser()



	# Various parameters for running the program
	parser.add_argument("--eval_every", type = int, default = 50,
            help = "Evaluate policy every ... epochs.")
	parser.add_argument("--predict_steps", type = int, default = 5,
            help = "Evaluate policy every ... epochs.")
	parser.add_argument('--data_file', action = 'store', type = str, help="Path to the dataset.");
	args = parser.parse_args()

	# The data file is mandatory, so exit the program if it is not provided
	if not args.data_file:
		print("Usage: python main.py <data_path>")
		sys.exit(1)

	file_path = args.data_file
	labeled_objects = data_loader.load_data(file_path)

	for labeled_object in labeled_objects:
		if labeled_object.vehicle_id not in tracked_objects:
			tracked_objects[labeled_object.vehicle_id] = []
		else:
			tracked_objects[labeled_object.vehicle_id].append(labeled_object)

	filter = KalmanFilter()

	for idx, vehicle_id in enumerate(tracked_objects):
		if idx <= 6:
			continue
		gt_points_x = []
		gt_points_y = []
		kalman_points_x = []
		kalman_points_y = []
		kalman_tracking_x = []
		kalman_tracking_y = []
		#for labeled_object in tracked_objects[vehicle_id]:
			#print(labeled_object)
		#	print(str(labeled_object.local_x) + " " +str(labeled_object.local_y))
		#sys.exit(1)
		for frame_num, labeled_object in enumerate(tracked_objects[vehicle_id]):

			measurements = np.zeros((2, 1))
			measurements[0] = labeled_object.local_x
			measurements[1] = labeled_object.local_y

			#print("measurements:")
			#print(measurements)
			if frame_num % args.eval_every == 0:
				print("frame_num: " + str(frame_num))
				#for i in range(10):
				predicted_x_vals = filter.multi_step_predict(args.predict_steps)
				print(len(predicted_x_vals))
				for x_val in predicted_x_vals:
					kalman_points_x.append(x_val[0].item(0))
					kalman_points_y.append(x_val[1].item(0))

			x, P = filter.predict()
			kalman_tracking_x.append(x[0].item(0))
			kalman_tracking_y.append(x[1].item(0))
			gt_points_x.append(measurements[0].item(0))
			gt_points_y.append(measurements[1].item(0))

			#x, P = filter.predict()
			#kalman_points_x.append(x[0].item(0))
			#kalman_points_y.append(x[1].item(0))

			#print("x:")
			#print(x)
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
		plt.plot(kalman_tracking_x, kalman_tracking_y)
		plt.scatter(kalman_points_x, kalman_points_y)
		plt.show()
		break

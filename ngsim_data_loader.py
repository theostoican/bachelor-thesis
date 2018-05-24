import csv

class LabelObject:
	def __init__(self, vehicle_id, frame_id, global_time, local_x, local_y, global_x, global_y):
		self.vehicle_id = vehicle_id
		self.frame_id = frame_id
		self.local_x = local_x
		self.local_y = local_y
		self.global_x = global_x
		self.global_time = global_time

def load_data(data_path):
	labeled_objects = []

	with open(data_path) as csvfile:
		reader = csv.DictReader(csvfile)
		count = -1
		for row in reader:
			count += 1
			# Ignore the header of the CSV file
			if count == 0:
				continue
			#print(row)
			labeled_objects.append(LabelObject(row['Vehicle_ID'], row['Frame_ID'], row['Global_Time'], row['Local_X'], row['Local_Y'],
						row['Global_X'], row['Global_Y']))
			print(row['Local_X'])
	return labeled_objects


if __name__ == "__main__":
	objs = load_data('./ngsim_trunc.csv')
	#print(objs)

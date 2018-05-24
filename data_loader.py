import math

class LabelObject:
	def __init__(self, frame, track_id, class_type, truncated, occluded, alpha,
		bbox, dimensions, location, rotation_y):
		self.frame = frame
		self.track_id = track_id
		self.type = class_type
		self.truncated = truncated
		self.occluded = occluded
		self.alpha = alpha
		self.bbox = bbox
		self.dimensions = dimensions
		self.location = location
		self.rotation_y = rotation_y

def convertFromGeoToCart(init_lon, init_lat, lon, lat):
	dx = (lon - init_lon)*40000*math.cos((init_lat + lat)*math.pi/360)/360
	dy = (lat - init_lat)*40000/360

	return dx, dy

class EgoCoordinates:
	def __init__(self, x, y):
		self.x = x
		self.y = y



def load_data(data_path, imu_path):
	labeled_objects = []
	imu_data = []
	init_lon = None
	init_lat = None

	with open(data_path) as fin:
		lines = fin.readlines()

		#Interpret the file line by line
		for line in lines:
			label_elems = line.split()

			frame = label_elems[0]
			track_id = int(label_elems[1])
			class_type = label_elems[2]
			truncated = label_elems[3]
			occluded = label_elems[4]
			alpha = label_elems[5]
			bbox = label_elems[6:10]
			dimensions = label_elems[10:13]
			location = [float(i) for i in label_elems[13:16]]
			rotation_y = label_elems[16]

			labeled_objects.append(LabelObject(frame, track_id, class_type,
				truncated, occluded, alpha, bbox, dimensions, location, rotation_y))

	with open(imu_path) as fin:
		lines = fin.readlines()
		for line in lines:
			data = line.split()
			curr_lat = float(data[0])
			curr_lon = float(data[1])
			if len(imu_data) == 0:
				init_lon = curr_lon
				init_lat = curr_lat
			x, y = convertFromGeoToCart(init_lon, init_lat, curr_lon, curr_lat)
			imu_data.append(EgoCoordinates(x, y))

	return labeled_objects, imu_data


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

def load_data(path):
	labeled_objects = []
	with open(path) as fin:
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



	return labeled_objects





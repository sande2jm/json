import mpu.io 
import json

size = 4
json_dic = json.load(open('test.json'))

def split_json(data):
	splits = []
	for i in range(size):
		transform = {}
		n = int(len(data['images'])/size)
		if i == size - 1:
			transform.update({'images':data['images'][i*n:]})
		else:
			transform.update({'images':data['images'][i*n:(i*n)+n]})
		splits.append(transform)
	return splits

splits = split_json(json_dic)

for i,x in enumerate(splits):
	mpu.io.write("split_" + str(i) + ".json", x)
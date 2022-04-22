import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
import boto3

def main():
	s3_client = boto3.client('s3')
	ssm_client = boto3.client('ssm')

	#s3 img object name
	s3_img = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
	
	#s3 bucket
	s3_bucket = urllib.parse.unquote_plus(event['Records'][0]['s3']['bucket']['name'], encoding='utf-8')
		
	# s3 model object 
	s3_model_path = ssm_client.get_parameters(
		Names=['model_path'], WithDecryption=True
		)

	# s3 bucket object 
	s3_bucket_path = ssm_client.get_parameters(
		Names=['model_bucket'], WithDecryption=True
		)

	
	with open('./tmp/image.jpg', 'wb') as f: 
		s3_client.download_fileobj(s3_model_bucket, s3_model_path,f)

	with open('./tmp/model.h5', 'wb') as f: 
		s3_client.download_fileobj(image_path, model_path,f)



	predict_saved_model(image_path, model_path)
	return {
		"statusCode": 200, 
		"headers": {
			"Content-Type": "application/json"
		}, 
		"body": json.dumps({
			"Region": json_region
		})
	}

def predict_saved_model(img_path): 
	model = tf.keras.models.load_model('models/save_at_50.h5')
	image_size = (180, 180)
	img = keras.preprocessing.image.load_img(
		img_path, target_size=image_size
		)
	img_array = keras.preprocessing.image.img_to_array(img)
	img_array = tf.expand_dims(img_array, 0)

	predictions = model.predict(img_array)
	score = predictions[0]
	return {str(score)} 



main()
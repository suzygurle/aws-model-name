import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import src.data.load_data as loader
import src.models.categorization_model as model_loader
import boto3
import mlflow


remote_url = 'https://aws-model-lab.s3.eu-west-3.amazonaws.com/kagglecatsanddogs_3367a.zip'
file_dir = '/data/raw'
file_name = '/data/raw/kagglecatsanddogs_3367a.zip'
TRACKING_URI = ''

loader.get_data(remote_url, file_dir, file_name)

num_skipped = 0
for folder_name in ("Cat", "Dog"):
    folder_path = os.path.join("/data/raw/PetImages", folder_name)
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        try:
            fobj = open(fpath, "rb")
            is_jfif = tf.compat.as_bytes("JFIF") in fobj.peek(10)
        finally:
            fobj.close()

        if not is_jfif:
            num_skipped += 1
            # Delete corrupted image
            os.remove(fpath)

print("Deleted %d images" % num_skipped)

image_size = (180, 180)
batch_size = 32

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "/data/raw/PetImages",
    validation_split=0.2,
    subset="training",
    seed=1337, #important to set seed
    image_size=image_size,
    batch_size=batch_size,
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "/data/raw/PetImages",
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

# performance
train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

#create model
image_size = (180, 180)
model = model_loader.make_model(input_shape=image_size + (3,), num_classes=2)

# train 
epochs = 1

callbacks = [
    keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
]
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
model.fit(
    train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
)

## mlflow
run_name = 'Default'
metric_name = 'accuracy'
mlflow.tracking.set_tracking_uri(TRACKING_URI)

with mlflow.start_run(run_name = run_name) as run: 
    mlflow.log_metric(metric_name, value)

## SNS 

client = boto3.client('sns')

response = client.publish(
    TopicArn='arn:aws:sns:eu-west-3:124716560638:AlertExample',
    Message='completed the task',
    Subject='AWS Notification',
)

print(response)


result = model.save()



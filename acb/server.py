from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import os
import keras
import base64
import io
from PIL import Image

os.environ["KERAS_BACKEND"] = "tensorflow"
from keras import layers, ops

app = Flask(__name__)

prediction_model = tf.keras.models.load_model('my_model.keras')
img_height = 200
img_width = 35
characters = ['1','2','3','4','5','6','7','8','9','A','B','D','E','F','G','H','J','M','N','R','T','Y','a','b','d','e','f','g','h','j','m','n','q','r','t','y']
max_length = 6

char_to_num = layers.StringLookup(vocabulary=list(characters), mask_token=None)
num_to_char = layers.StringLookup(vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True)

def preprocess_image(image):
    image = np.expand_dims(image, axis=0)
    return image

def encode_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.io.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    print(img.shape)
    img = ops.image.resize(img, [img_width, img_height])
    img = ops.transpose(img, axes=[1, 0, 2])
    return img

def ctc_decode(y_pred, input_length, greedy=True, beam_width=100, top_paths=1):
    input_shape = ops.shape(y_pred)
    num_samples, num_steps = input_shape[0], input_shape[1]
    y_pred = ops.log(ops.transpose(y_pred, axes=[1, 0, 2]) + keras.backend.epsilon())
    input_length = ops.cast(input_length, dtype="int32")

    if greedy:
        (decoded, log_prob) = tf.nn.ctc_greedy_decoder(
            inputs=y_pred, sequence_length=input_length
        )
    else:
        (decoded, log_prob) = tf.compat.v1.nn.ctc_beam_search_decoder(
            inputs=y_pred,
            sequence_length=input_length,
            beam_width=beam_width,
            top_paths=top_paths,
        )
    decoded_dense = []
    for st in decoded:
        st = tf.SparseTensor(st.indices, st.values, (num_samples, num_steps))
        decoded_dense.append(tf.sparse.to_dense(sp_input=st, default_value=-1))
    return (decoded_dense, log_prob)

def decode_prediction(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    results = ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :max_length]
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text[0]

def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text

def decode_base64_image(base64_string):
    if base64_string.startswith("data:image/png;base64,"):
        base64_string = base64_string.replace("data:image/png;base64,", "")
    
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image_path = 'temp.png'
    image.save(image_path)
    
    return image_path

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        image_file = request.files['image']
        image_path = 'temp.png'
        image_file.save(image_path)
    elif 'image_base64' in request.json:
        base64_string = request.json['image_base64']
        image_path = decode_base64_image(base64_string)
    else:
        return jsonify({"error": "No image provided."})

    try:
        encoded_image = encode_image(image_path)
        preprocessed_image = preprocess_image(encoded_image)
        pred = prediction_model.predict(preprocessed_image)
        pred_text = decode_batch_predictions(pred)
        return jsonify({'prediction': pred_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8001, debug=False)
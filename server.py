from cloth_mask import ClothMask
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from base64 import b64decode, b64encode

app = Flask(__name__)
cloth_mask = ClothMask()


@app.route('/infer', methods=['POST'])
def infer():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    input_image = data["input_image"]
    # 从 base64 解码出图片
    images = [Image.open(BytesIO(b64decode(input_image)))]
    output_images = cloth_mask(images)
    buffered = BytesIO()
    output_images[0].save(buffered, format='JPEG')
    output_image = b64encode(buffered.getvalue()).decode('utf-8')
    result = {'result': {'output_image': output_image}}
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

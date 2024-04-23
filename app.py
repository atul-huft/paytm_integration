from flask import Flask, render_template, request, jsonify
from PaytmChecksum import generateSignature, verifySignature, encrypt, decrypt
# from createQR import
import webbrowser
import json
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr_code():
    # data = request.form
    orderId = request.form.get('orderId')
    amount = request.form.get('amount')

    create_qr_code(orderId, amount)  # Call your create_qr_code function here

    return jsonify({'message': 'QR Code generation request sent'})

def create_qr_code(orderId, amount):
    # Your code to generate the QR code and open the URL goes here
    # Example code:
    paytm_params = {
        "mid": "test5P07128923987041",
        "orderId": orderId,
        "amount": amount,
        "businessType": "UPI_QR_CODE",
        "posId": "S12_123",
    }

    try:
        checksum = generateSignature(json.dumps(paytm_params), "nXuJnxiYoHRe&&2J")
        paytm_request = {
            "body": paytm_params,
            "head": {
                "clientId": "C11",
                "version": "v1",
                "signature": checksum
            }
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post('https://securegw.paytm.in/paymentservices/qr/create', json=paytm_request, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        extract_and_use_qr_code_details(json_response, orderId, amount)
    except Exception as e:
        print(f"Error: {e}")


def extract_and_use_qr_code_details(response, orderId, amount):
    body = response.get("body", {})
    qr_code_id = body.get("qrCodeId")
    qr_data = body.get("qrData")
    image = body.get("image")  # Assuming this is a URL or base64 encoded image data
    port = "COM3"

    print({"qrCodeId": qr_code_id, "qrData": qr_data, "image": image, "port": port, "orderId": orderId, "amount": amount})

    url = f"PaytmPayments:?requestId=123;method=displayTxnQr;mid=test5P07128923987041;portName={port};baudRate=115200;parity=0;dataBits=8;stopBits=1;order_id={orderId};order_amount={amount};qrcode_id={qr_data};currencySign=null;debugMode=1;posid=POS-1"

    print(url)
    try:
        webbrowser.open(url)
        print('Successfully opened the deep link URL in the default web browser.')
    except Exception as e:
        print(f'Failed to open the deep link URL: {e}')


if __name__ == '__main__':
    app.run(debug=True)

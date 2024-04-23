import requests
import json
from PaytmChecksum import generateSignature, verifySignature, encrypt, decrypt
import webbrowser

orderId = "order125"
amount = "100"


def create_qr_code(orderId, amount):
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
    port = "COM4"

    print({"qrCodeId": qr_code_id, "qrData": qr_data, "image": image, "port": port, "orderId": orderId, "amount": amount})

    url = f"PaytmPayments:?requestId=123;method=displayTxnQr;mid=test5P07128923987041;portName={port};baudRate=115200;parity=0;dataBits=8;stopBits=1;order_id={orderId};order_amount={amount};qrcode_id={qr_data};currencySign=null;debugMode=1;posid=POS-1"

    print(url)
    try:
        webbrowser.open(url)
        print('Successfully opened the deep link URL in the default web browser.')
    except Exception as e:
        print(f'Failed to open the deep link URL: {e}')


create_qr_code(orderId, amount)

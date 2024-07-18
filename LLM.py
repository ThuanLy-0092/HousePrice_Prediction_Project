import os
import requests
import json
import pandas as pd

s = requests.Session()

def Create_More_Vars(text):
    api_base = "https://api.endpoints.anyscale.com/v1"
    token = "esecret_pctmwgldbhm1548psxgi8sdnky"
    url = f"{api_base}/chat/completions"
    body = {
        "model": "meta-llama/Meta-Llama-3-70B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": "hãy trả kết quả ra dưới dạng JSON: {\"DiaChi\": \"...\",\"TienIch\" :\"True or False\", \"SoTang\": \"number\",\"NearSchool\": \"True or False\",\"NearHospital\" :\"True or False\",\"Security\":\"0 or 1 or 2\",\"LegalClarity\":\"0 or 1\" }"
            },
            {
                "role": "assistant",
                "content": "Here is the response in JSON format:\n\n```\n{\n  \"DiaChi\": \"Ngõ 11, Khuất Duy Tiến, Thanh Xuân, Hà Nội\",\n  \"TienIch\": true,\n  \"SoTang\": 3\n,\"NearSchool\": \"False\",\"NearHospital\" :\"True\",\"Security\":\"2\",\"LegalClarity\" :\"0 or 1\"}\n```\n\nLet me know if you need anything else!"
            },
            {"role": "user", "content": text}
        ],
        "temperature": 1,
        "max_tokens": 256,
        "top_p": 1,
        "frequency_penalty": 0
    }

    json_data = None
    max_retries = 5  # Số lần thử lại tối đa
    retries = 0

    while json_data is None and retries < max_retries:
        response = s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body)
        response_json = response.json()
        assistant_message = response_json['choices'][0]['message']['content']

        start_index = assistant_message.find('```') + 3
        end_index = assistant_message.rfind('```')
        json_str = assistant_message[start_index:end_index]

        try:
            json_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}. Retrying...")
            retries += 1

    if json_data is None:
        print("Failed to get a valid JSON response after maximum retries.")
        return None

    # Extract additional information
    security = json_data.get('Security', 0)
    near_school = json_data.get('NearSchool', 0)
    near_hospital = json_data.get('NearHospital', 0)
    legalclarity= json_data.get('LegalClarity',0)

    return {
        'DiaChi': json_data.get('DiaChi', 'Unknown'),
        'TienIch': json_data.get('TienIch', False),
        'SoTang': json_data.get('SoTang', 0),
        'Security': security,
        'NearSchool': near_school,
        'NearHospital': near_hospital,
        'LegalClarity': legalclarity
    }


def Predict_SellHouse(text):
    api_base = "https://api.endpoints.anyscale.com/v1"  
    token = "esecret_pctmwgldbhm1548psxgi8sdnky"
    url = f"{api_base}/chat/completions"

    body = {
        "model": "meta-llama/Meta-Llama-3-70B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": "hãy trả kết quả ra dưới dạng JSON như: {\"SellHouse\": true or false}"
            },
            {
                "role": "assistant",
                "content": "Here is the revised response:\n\n`{\"SellHouse\": true,}`"
            },
            {
                "role": "user",
                "content": "Có tin được không Liền kề Hud Sơn Tây, vị trí đẹp, tăng giá tốt, giá không tưởng !!\nHUD Sơn Tây, Sơn Tây, Hà Nội\n5 tỷ"
            },
            {
                "role": "assistant",
                "content": "`{\"SellHouse\": true}`"
            },
            {
                "role": "user",
                "content": "The power of online advertising facebook ads\nChâu Đốc, An Giang\n12 triệu"
            },
            {
                "role": "assistant",
                "content": "`{\"SellHouse\": false}`"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 1,
        "max_tokens": 256,
        "top_p": 1,
        "frequency_penalty": 0
    }
    headers = {"Authorization": f"Bearer {token}"}

    json_data = None
    max_retries = 5
    retries = 0

    while json_data is None and retries < max_retries:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        response_json = response.json()
        assistant_message = response_json['choices'][0]['message']['content']
        start_index = assistant_message.find('`') + 1
        end_index = assistant_message.rfind('`')
        json_str = assistant_message[start_index:end_index]
        
                
        try:
            json_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}. Retrying...")
            retries += 1

    if json_data is None:
        print("Failed to get a valid JSON response after maximum retries.")
        return False
    
    sellhouse = json_data.get('SellHouse', False)
    return sellhouse
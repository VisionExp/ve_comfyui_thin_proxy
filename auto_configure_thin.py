import json
import os
import subprocess
import requests


def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False


def get_text_from_file(url, as_array):
    response = requests.get(url)
    if response.status_code == 200:
        response_string = response.content.decode('utf-8')
        if as_array:
            items = [item.strip() for item in response_string.split(',')]
            return items
        else:
            if is_valid_json(response_string):
                return json.loads(response_string)
            else:
                print(f'JSON in this url: {url} is not valid')

    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def create_empty_file(name):
    if os.path.exists(name):
        print(f"File '{name}' already exists. Skipping download.")
    else:
        with open(name, 'w') as file:
            pass
        print(f"File {name} successfully created ")


nodes_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/nodes_list.txt"
controlnet_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/controlnet_list_thin.txt"
clip_vision_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/clip_vision_list.txt"
loras_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/loras_list.txt"
models_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/models_list.txt"
upscale_models_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/upscale_models_list.txt"
ip_adapter_url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/ip_adapter.txt"

custom_nodes_list = get_text_from_file(nodes_url, as_array=True)
controlnet_list = get_text_from_file(controlnet_url, as_array=False)
clip_vision_list = get_text_from_file(clip_vision_url, as_array=False)
loras_list = get_text_from_file(loras_url, as_array=False)
models_list = get_text_from_file(models_url, as_array=False)
upscale_models_list = get_text_from_file(upscale_models_url, as_array=False)
ip_adapter_list = get_text_from_file(ip_adapter_url, as_array=True)

script_root = os.path.dirname(os.path.abspath(__file__))

print(':::Loading custom nodes')
os.chdir(script_root)
os.chdir("custom_nodes")
for repo_url in custom_nodes_list:
    subprocess.run(['git', 'clone', repo_url])

print(':::Loading controlnet models')
os.chdir(script_root)
os.chdir("models/controlnet")

for folder_name, files in controlnet_list:
    os.mkdir(folder_name)
    os.chdir(folder_name)
    for filename in files:
        create_empty_file(filename)


print(':::Loading models')
os.chdir(script_root)
os.chdir("models/checkpoints")
for url, filename in models_list.items():
    create_empty_file(filename)

print(':::Loading loras')
os.chdir(script_root)
os.chdir("models/loras")
for url, filename in loras_list.items():
    create_empty_file(filename)

print(':::Loading upscale models')
os.chdir(script_root)
os.chdir("models/upscale_models")
for url, filename in upscale_models_list.items():
    create_empty_file(filename)

print(':::Loading IPAdapter model')
os.chdir(script_root)
os.chdir('models')
os.mkdir("ipadapter")
os.chdir("models/ipadapter")
for repo_url in ip_adapter_list:
    subprocess.run(['git', 'clone', repo_url])

print(':::Loading CLIP Vision')
os.chdir(script_root)
os.chdir("models/clip_vision")
for url, filename in clip_vision_list.items():
    create_empty_file(filename)

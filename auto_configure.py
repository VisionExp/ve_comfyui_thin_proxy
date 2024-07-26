
import os
import subprocess
import requests


def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        response_string = response.content.decode('utf-8')
        array = [item.strip() for item in response_string.split(',')]
        return array
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


url = "https://raw.githubusercontent.com/VisionExp/ve_comfy_custom_nodes_list/main/nodes_list.txt"
custom_extensions = download_file(url)
print(custom_extensions)
subprocess.run(['git', 'lfs', 'install'])

script_root = os.path.dirname(os.path.abspath(__file__))

os.chdir("custom_nodes")


for repo_url in custom_extensions:
    subprocess.run(['git', 'clone', repo_url])

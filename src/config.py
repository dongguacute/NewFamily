import json
import os
import requests
CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        self.openapiurl = ""
        self.apikey = ""
        self.modelname = ""
        # 个人资料
        self.username = "User"
        # 界面设置
        self.dark_mode = False
        self.show_avatar = True
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.openapiurl = data.get("openapiurl", "")
                    self.apikey = data.get("apikey", "")
                    self.modelname = data.get("modelname", "")
                    self.username = data.get("username", "User")
                    self.dark_mode = data.get("dark_mode", False)
                    self.show_avatar = data.get("show_avatar", True)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    "openapiurl": self.openapiurl,
                    "apikey": self.apikey,
                    "modelname": self.modelname,
                    "username": self.username,
                    "dark_mode": self.dark_mode,
                    "show_avatar": self.show_avatar,
                }, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

# 单例模式，方便全局访问
config = Config()

def get_config(openapiurl: str = None, apikey: str = None, modelname: str = None):
    # 如果传入参数，则更新单例并返回
    if openapiurl is not None: config.openapiurl = openapiurl
    if apikey is not None: config.apikey = apikey
    if modelname is not None: config.modelname = modelname
    
    return {
        "openapiurl": config.openapiurl,
        "apikey": config.apikey,
        "modelname": config.modelname,
    }

def testapi(openapiurl: str, apikey: str, modelname: str):
    config.openapiurl = openapiurl
    config.apikey = apikey
    config.modelname = modelname
    config.save()
    
    # 测试 API 调用
    try:
        response = requests.post(
            f"{openapiurl}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {apikey}",
                "Content-Type": "application/json",
            },
            json={
                "model": modelname,
                "messages": [{"role": "user", "content": "你好"}]
            }
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"API 测试失败: {e}")
        return False

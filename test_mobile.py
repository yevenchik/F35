import subprocess
import time
import json
import urllib.request
import base64
import os
import websocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. Test Landscape Phone (844 x 390)
cmd_landscape = [
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9223",
    "--remote-allow-origins=*",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=844,390",
    "http://127.0.0.1:8088/index.html"
]

proc = subprocess.Popen(cmd_landscape, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9223/json")
    targets = json.loads(req.read().decode('utf-8'))
    ws_url = [t['webSocketDebuggerUrl'] for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(ws_url)

    msg_id = 1
    def send_cdp(method, params=None):
        global msg_id
        payload = {"id": msg_id, "method": method, "params": params or {}}
        msg_id += 1
        ws.send(json.dumps(payload))
        while True:
            res = json.loads(ws.recv())
            if res.get('id') == payload['id']:
                return res

    send_cdp("Runtime.enable")
    send_cdp("Page.enable")
    time.sleep(1.0)

    # Capture Landscape Phone
    res = send_cdp("Page.captureScreenshot", {"format": "png"})
    with open(r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\shot_phone_landscape.png", "wb") as f:
        f.write(base64.b64decode(res['result']['data']))
    print("Captured shot_phone_landscape.png")
    ws.close()
finally:
    proc.terminate()

# 2. Test Portrait Phone (390 x 844)
cmd_portrait = [
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9224",
    "--remote-allow-origins=*",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=390,844",
    "http://127.0.0.1:8088/index.html"
]

proc2 = subprocess.Popen(cmd_portrait, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9224/json")
    targets = json.loads(req.read().decode('utf-8'))
    ws_url = [t['webSocketDebuggerUrl'] for t in targets if t.get('type') == 'page'][0]
    ws = websocket.create_connection(ws_url)

    send_cdp("Runtime.enable")
    send_cdp("Page.enable")
    time.sleep(1.0)

    # Capture Portrait Phone
    res = send_cdp("Page.captureScreenshot", {"format": "png"})
    with open(r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\shot_phone_portrait.png", "wb") as f:
        f.write(base64.b64decode(res['result']['data']))
    print("Captured shot_phone_portrait.png")
    ws.close()
finally:
    proc2.terminate()

print("Mobile test complete.")


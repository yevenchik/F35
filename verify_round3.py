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

print(f"Using browser: {chrome_path}")

cmd = [
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9230",
    "--remote-allow-origins=*",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=1280,720",
    "http://127.0.0.1:8088/index.html"
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9230/json")
    targets = json.loads(req.read().decode('utf-8'))
    page_target = None
    for t in targets:
        if t.get('type') == 'page' and 'F-35' in t.get('title', ''):
            page_target = t
            break

    if not page_target:
        for t in targets:
            if t.get('type') == 'page':
                page_target = t
                break

    ws_url = page_target['webSocketDebuggerUrl']
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

    def capture(name):
        res = send_cdp("Page.captureScreenshot", {"format": "png"})
        if 'result' in res and 'data' in res['result']:
            data = base64.b64decode(res['result']['data'])
            path = os.path.join(r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation", name)
            with open(path, "wb") as f:
                f.write(data)
            print(f"Captured {name} ({len(data)} bytes)")

    # 1. Sunset View
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.toggleTimeOfDay();"})
    time.sleep(0.5)
    capture("shot_sunset.png")

    # 2. Night Stealth View with Slime Lights and Airfield Illumination
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.toggleTimeOfDay();"})
    time.sleep(0.5)
    capture("shot_night.png")

    # 3. Night View Orbit around F-35 showing glowing green formation slime lights
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.setCamera(3); window.simulationApp.orbitAngleY = 0.3; window.simulationApp.orbitAngleX = 0.7; window.simulationApp.orbitDistance = 18;"})
    time.sleep(0.5)
    capture("shot_night_slime_lights.png")

    # 4. Cockpit Free-Look View
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.setCamera(1); window.simulationApp.cockpitLookYaw = 0.65; window.simulationApp.cockpitLookPitch = -0.25;"})
    time.sleep(0.5)
    capture("shot_cockpit_look.png")

    # 5. Reset to Day and Chase Cam
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.toggleTimeOfDay(); window.simulationApp.setCamera(0); window.simulationApp.cockpitLookYaw = 0; window.simulationApp.cockpitLookPitch = 0;"})
    time.sleep(0.5)
    capture("shot_round3_day.png")

    ws.close()

finally:
    proc.terminate()
    print("Round 3 verification complete.")

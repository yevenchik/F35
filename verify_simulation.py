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
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=1280,720",
    "http://127.0.0.1:8088/index.html"
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
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

    time.sleep(1.5)

    def capture(name):
        res = send_cdp("Page.captureScreenshot", {"format": "png"})
        if 'result' in res and 'data' in res['result']:
            data = base64.b64decode(res['result']['data'])
            path = os.path.join(r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation", name)
            with open(path, "wb") as f:
                f.write(data)
            print(f"Captured {name} ({len(data)} bytes)")

    # 1. Chase View
    capture("shot_chase.png")

    # 2. Cockpit HUD View (Mode 1)
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.setCamera(1)"})
    time.sleep(0.8)
    capture("shot_cockpit.png")

    # 3. Orbit View (Mode 3)
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.setCamera(3);"})
    time.sleep(0.8)
    capture("shot_orbit.png")

    # 4. Action Mode: Bay open, Gear down, Afterburner boost
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.setCamera(0); window.simulationApp.toggleBay(); window.simulationApp.toggleGear(); window.simulationApp.physics.throttle = 1.25;"})
    time.sleep(1.0)
    capture("shot_action.png")

    # 5. Offshore Carrier Strike Group View
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.cameraMode = -1; window.simulationApp.camera.position.set(6350, 160, 8350); window.simulationApp.camera.lookAt(6500, 45, 7500);"})
    time.sleep(0.5)
    capture("shot_fleet.png")

    # 6. Active Gun Firing View in Chase Cam
    send_cdp("Runtime.evaluate", {"expression": "window.simulationApp.setCamera(0); for (let i = 0; i < 8; i++) { window.simulationApp.fireGun(); window.simulationApp.gunCooldown = 0; }"})
    time.sleep(0.03)
    capture("shot_firing.png")

    ws.close()

finally:
    proc.terminate()
    print("Browser test complete.")

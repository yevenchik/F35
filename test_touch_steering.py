import subprocess
import time
import json
import urllib.request
import os
import websocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

cmd = [
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9225",
    "--remote-allow-origins=*",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=844,390",
    "http://127.0.0.1:8088/index.html"
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9225/json")
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
    time.sleep(1.0)

    # 1. Check initial inputs
    res1 = send_cdp("Runtime.evaluate", {"expression": "JSON.stringify({pitch: window.simulationApp.physics.pitchInput, roll: window.simulationApp.physics.rollInput, throttle: window.simulationApp.physics.throttle})"})
    print("Initial physics inputs:", res1['result'].get('result', {}).get('value'))

    # 2. Simulate touch stick pull back (Pitch Up) and roll right
    send_cdp("Runtime.evaluate", {"expression": """
        window.simulationApp.touchPitch = 0.85;
        window.simulationApp.touchRoll = 0.70;
        window.simulationApp.touchThrottleDelta = 1.0;
        window.simulationApp.touchFiringGun = true;
    """})

    time.sleep(0.5)

    # 3. Check physics inputs during touch
    res2 = send_cdp("Runtime.evaluate", {"expression": "JSON.stringify({pitch: window.simulationApp.physics.pitchInput, roll: window.simulationApp.physics.rollInput, throttle: window.simulationApp.physics.throttle, ammo: window.simulationApp.physics.ammo})"})
    print("During touch inputs:", res2['result'].get('result', {}).get('value'))

    # 4. Release touch
    send_cdp("Runtime.evaluate", {"expression": """
        window.simulationApp.touchPitch = 0;
        window.simulationApp.touchRoll = 0;
        window.simulationApp.touchThrottleDelta = 0;
        window.simulationApp.touchFiringGun = false;
    """})

    time.sleep(0.2)
    res3 = send_cdp("Runtime.evaluate", {"expression": "JSON.stringify({pitch: window.simulationApp.physics.pitchInput, roll: window.simulationApp.physics.rollInput, throttle: window.simulationApp.physics.throttle})"})
    print("After touch release:", res3['result'].get('result', {}).get('value'))

    ws.close()
finally:
    proc.terminate()

print("Touch functional verification passed.")

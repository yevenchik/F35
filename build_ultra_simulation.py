import os

# Create the full ultra-high-fidelity simulation build script
script_content = r'''# =============================================================================
# ULTRA HIGH-FIDELITY BUILD SCRIPT FOR F-35 LIGHTNING II 3D FLIGHT SIMULATION
# Full PBR IBL + Post-Processing HDR Bloom + Gerstner Ocean + Plane Overhaul + Beast Mode
# =============================================================================

import os

output_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\index.html"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>F-35 Lightning II - 3D Flight Simulation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  
  <!-- Three.js Core & Controls -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  
  <!-- Three.js Post-Processing Shaders & Passes -->
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>

  <style>
    :root {
      --hud-green: #00ff77;
      --hud-glow: rgba(0, 255, 119, 0.45);
      --hud-amber: #ffaa00;
      --hud-red: #ff3344;
      --hud-cyan: #00e5ff;
      --panel-bg: rgba(6, 12, 18, 0.88);
      --panel-border: rgba(0, 255, 119, 0.35);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
      touch-action: none;
      -webkit-touch-callout: none;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #010408;
      font-family: 'Rajdhani', sans-serif;
      color: #e0f0ea;
      touch-action: none;
      overscroll-behavior: none;
    }

    #webgl-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      display: block;
    }

    #hud-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 2;
      pointer-events: none;
    }

    #g-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 3;
      pointer-events: none;
      transition: background 0.15s ease-out;
    }

    #ui-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 16px 20px;
    }

    .interactive {
      pointer-events: auto;
    }

    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      background: var(--panel-bg);
      border: 1px solid var(--panel-border);
      border-radius: 8px;
      padding: 8px 18px;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
    }

    .top-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .aircraft-badge {
      font-size: 19px;
      font-weight: 700;
      letter-spacing: 2px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .badge-tag {
      background: rgba(0, 255, 119, 0.15);
      border: 1px solid var(--hud-green);
      color: var(--hud-green);
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'Share Tech Mono', monospace;
    }

    .flight-status {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: 'Share Tech Mono', monospace;
      font-size: 12px;
      color: #79a896;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--hud-green);
      box-shadow: 0 0 8px var(--hud-green);
      animation: pulseDot 2s infinite;
    }

    @keyframes pulseDot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .top-controls {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .hud-btn {
      background: rgba(14, 25, 34, 0.85);
      border: 1px solid rgba(0, 255, 119, 0.4);
      color: #c0ded2;
      font-family: 'Rajdhani', sans-serif;
      font-size: 13px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      letter-spacing: 1px;
    }

    .hud-btn:hover {
      background: rgba(0, 255, 119, 0.2);
      border-color: var(--hud-green);
      color: #fff;
      box-shadow: 0 0 12px rgba(0, 255, 119, 0.35);
    }

    .hud-btn.active {
      background: rgba(0, 255, 119, 0.28);
      border-color: var(--hud-green);
      color: var(--hud-green);
      box-shadow: 0 0 14px rgba(0, 255, 119, 0.5);
    }

    .hud-btn.beast-active {
      background: rgba(255, 170, 0, 0.28);
      border-color: var(--hud-amber);
      color: var(--hud-amber);
      box-shadow: 0 0 14px rgba(255, 170, 0, 0.5);
    }

    .middle-section {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      margin: auto 0;
    }

    .side-gauge-cluster {
      background: var(--panel-bg);
      border: 1px solid var(--panel-border);
      border-radius: 8px;
      padding: 14px 18px;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
      display: flex;
      flex-direction: column;
      gap: 12px;
      min-width: 170px;
    }

    .gauge-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .gauge-label {
      font-family: 'Share Tech Mono', monospace;
      font-size: 11px;
      color: #79a896;
      letter-spacing: 1px;
    }

    .gauge-value {
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      font-family: 'Rajdhani', sans-serif;
    }

    .gauge-unit {
      font-size: 12px;
      color: #79a896;
      margin-left: 2px;
    }

    .bar-container {
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
      margin-top: 4px;
    }

    .bar-fill {
      height: 100%;
      background: var(--hud-green);
      box-shadow: 0 0 8px var(--hud-green);
      transition: width 0.1s linear;
    }

    .bottom-bar {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      width: 100%;
    }

    .camera-switcher, .action-panel {
      background: var(--panel-bg);
      border: 1px solid var(--panel-border);
      border-radius: 8px;
      padding: 8px 12px;
      backdrop-filter: blur(12px);
      display: flex;
      gap: 8px;
    }

    /* Mobile Controls */
    .mobile-controls {
      display: none;
      position: absolute;
      bottom: 12px;
      left: 14px;
      right: 14px;
      justify-content: space-between;
      align-items: flex-end;
      pointer-events: none;
      z-index: 30;
    }

    .mobile-stick-cluster {
      display: flex;
      align-items: flex-end;
      gap: 12px;
      pointer-events: auto;
    }

    .touch-stick-zone {
      width: 110px;
      height: 110px;
      background: radial-gradient(circle, rgba(0, 255, 119, 0.08) 0%, rgba(4, 12, 18, 0.6) 80%);
      border: 2px solid rgba(0, 255, 119, 0.5);
      border-radius: 50%;
      pointer-events: auto;
      position: relative;
      box-shadow: 0 0 15px rgba(0, 255, 119, 0.25), inset 0 0 10px rgba(0, 255, 119, 0.15);
      touch-action: none;
    }

    .touch-stick-zone::after {
      content: 'FLIGHT STICK';
      position: absolute;
      bottom: -18px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 9px;
      font-family: 'Share Tech Mono', monospace;
      color: rgba(0, 255, 119, 0.7);
      letter-spacing: 1px;
      white-space: nowrap;
    }

    .touch-knob {
      width: 44px;
      height: 44px;
      background: radial-gradient(circle, #55ffaa 0%, #00bb55 100%);
      border: 2px solid #ffffff;
      border-radius: 50%;
      position: absolute;
      top: calc(50% - 22px);
      left: calc(50% - 22px);
      box-shadow: 0 0 14px rgba(0, 255, 119, 0.8);
      pointer-events: none;
    }

    .mobile-throttle-cluster {
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: auto;
    }

    .touch-throttle-btn {
      width: 46px;
      height: 46px;
      border-radius: 8px;
      background: rgba(14, 25, 34, 0.88);
      border: 1.5px solid var(--hud-green);
      color: #fff;
      font-family: 'Share Tech Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 10px rgba(0, 255, 119, 0.25);
      touch-action: none;
    }

    .touch-throttle-btn:active {
      background: rgba(0, 255, 119, 0.3);
      transform: scale(0.94);
    }

    .mobile-action-buttons {
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: auto;
    }

    .mobile-btn-row {
      display: flex;
      gap: 8px;
      justify-content: flex-end;
    }

    .touch-round-btn {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: rgba(14, 25, 34, 0.9);
      border: 2px solid var(--hud-green);
      color: #fff;
      font-family: 'Share Tech Mono', monospace;
      font-weight: 700;
      font-size: 11px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 10px rgba(0, 255, 119, 0.3);
      touch-action: none;
    }

    .touch-round-btn.primary-gun {
      width: 58px;
      height: 58px;
      background: rgba(45, 18, 12, 0.92);
      border-color: #ffaa00;
      color: #ffeedd;
      box-shadow: 0 0 14px rgba(255, 170, 0, 0.5);
      font-size: 13px;
    }

    .touch-round-btn.primary-gun:active {
      background: rgba(255, 170, 0, 0.4);
      transform: scale(0.93);
    }

    .touch-round-btn.primary-msl {
      width: 54px;
      height: 54px;
      background: rgba(10, 36, 44, 0.9);
      border-color: #00e5ff;
      box-shadow: 0 0 12px rgba(0, 229, 255, 0.4);
    }

    .touch-round-btn.secondary {
      width: 44px;
      height: 44px;
      background: rgba(14, 25, 34, 0.85);
      font-size: 10px;
    }

    .landscape-hint {
      display: none;
      position: absolute;
      top: 48px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 229, 255, 0.92);
      color: #03121a;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
      box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
      z-index: 60;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }

    .landscape-hint button {
      background: transparent;
      border: none;
      color: #03121a;
      font-weight: 900;
      font-size: 16px;
      cursor: pointer;
    }

    #master-warning {
      position: absolute;
      top: 15%;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(255, 34, 51, 0.88);
      border: 2px solid #ff3344;
      color: #fff;
      font-family: 'Share Tech Mono', monospace;
      font-size: 22px;
      font-weight: 700;
      letter-spacing: 4px;
      padding: 8px 30px;
      border-radius: 6px;
      box-shadow: 0 0 30px rgba(255, 34, 51, 0.8);
      z-index: 50;
      display: none;
      animation: alertBlink 0.5s infinite alternate ease-in-out;
    }

    #target-destroyed-banner {
      position: absolute;
      top: 24%;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 255, 119, 0.92);
      border: 2px solid #00ff77;
      color: #031208;
      font-family: 'Share Tech Mono', monospace;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 3px;
      padding: 8px 24px;
      border-radius: 6px;
      box-shadow: 0 0 35px rgba(0, 255, 119, 0.8);
      z-index: 50;
      display: none;
    }

    @keyframes alertBlink {
      from { opacity: 0.3; transform: translateX(-50%) scale(0.96); }
      to { opacity: 1; transform: translateX(-50%) scale(1.04); }
    }

    .modal-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(2, 6, 12, 0.85);
      backdrop-filter: blur(10px);
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }

    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-box {
      background: #09121a;
      border: 1px solid var(--hud-green);
      box-shadow: 0 0 35px rgba(0, 255, 119, 0.25), 0 20px 50px rgba(0, 0, 0, 0.8);
      border-radius: 10px;
      width: 90%;
      max-width: 680px;
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(0, 255, 119, 0.3);
      padding-bottom: 12px;
    }

    .modal-title {
      font-size: 22px;
      font-weight: 700;
      color: #fff;
      letter-spacing: 2px;
    }

    .close-btn {
      background: transparent;
      border: none;
      color: #99aabb;
      font-size: 24px;
      cursor: pointer;
    }

    .help-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .help-group-title {
      color: var(--hud-green);
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      margin-bottom: 8px;
      text-transform: uppercase;
    }

    .help-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      padding: 4px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .key-badge {
      background: rgba(0, 255, 119, 0.15);
      border: 1px solid rgba(0, 255, 119, 0.4);
      color: var(--hud-green);
      font-family: 'Share Tech Mono', monospace;
      font-size: 12px;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 700;
    }

    @media (orientation: portrait) and (max-width: 900px) {
      .landscape-hint { display: flex; }
    }

    @media (max-width: 900px), (max-height: 520px) {
      .bottom-bar { display: none !important; }
      .side-gauge-cluster { display: none !important; }
      .mobile-controls { display: flex !important; }
      .top-bar { padding: 4px 8px; gap: 6px; }
      .aircraft-badge { font-size: 13px; }
      .badge-tag, .flight-status { display: none !important; }
      .top-controls { gap: 4px; }
      .hud-btn { padding: 4px 7px; font-size: 11px; }
    }
  </style>
</head>
<body>
  <canvas id="webgl-canvas"></canvas>
  <canvas id="hud-canvas"></canvas>
  <div id="g-overlay"></div>
  <div id="master-warning">WARNING: PULL UP</div>
  <div id="target-destroyed-banner">TARGET DESTROYED +100 PTS</div>

  <div id="landscape-hint" class="landscape-hint">
    <span>&#128260; ROTATE PHONE TO LANDSCAPE FOR BEST FLIGHT CONTROLS</span>
    <button id="close-hint-btn">&times;</button>
  </div>

  <div id="ui-container">
    <div class="top-bar interactive">
      <div class="top-left">
        <div class="aircraft-badge">
          <span>F-35A LIGHTNING II</span>
          <span class="badge-tag">5th GEN STEALTH</span>
        </div>
        <div class="flight-status">
          <span class="status-dot"></span>
          <span id="flight-state-text">AIRBORNE // FBW ACTIVE</span>
        </div>
      </div>
      <div class="top-controls">
        <button class="hud-btn" id="audio-toggle-btn" title="Toggle Sound Engine (M)">
          <span id="audio-icon">&#128263;</span> SOUND: OFF
        </button>
        <button class="hud-btn" id="beast-toggle-btn" title="Toggle Beast Mode External Pylons (P)">
          BEAST: OFF
        </button>
        <button class="hud-btn" id="bay-toggle-btn" title="Toggle Internal Weapons Bay (B)">
          BAY: CLOSED
        </button>
        <button class="hud-btn" id="gear-toggle-btn" title="Toggle Landing Gear (G)">
          GEAR: UP
        </button>
        <button class="hud-btn" id="gfx-toggle-btn" title="Toggle Ultra Post-Processing Graphics">
          GFX: ULTRA
        </button>
        <button class="hud-btn" id="respawn-btn" title="Reset Flight Position (R)">
          RESET (R)
        </button>
        <button class="hud-btn" id="help-btn" title="Open Flight Handbook & Controls (H)">
          HELP (?)
        </button>
      </div>
    </div>

    <div class="middle-section">
      <div class="side-gauge-cluster interactive">
        <div class="gauge-item">
          <div class="gauge-label">AIRSPEED</div>
          <div class="gauge-value" id="val-airspeed">425 <span class="gauge-unit">KTS</span></div>
        </div>
        <div class="gauge-item">
          <div class="gauge-label">MACH NUMBER</div>
          <div class="gauge-value" id="val-mach">M 0.65</div>
        </div>
        <div class="gauge-item">
          <div class="gauge-label">THROTTLE POWER</div>
          <div class="gauge-value" id="val-throttle">85 <span class="gauge-unit">%</span></div>
          <div class="bar-container">
            <div class="bar-fill" id="throttle-bar" style="width: 85%;"></div>
          </div>
        </div>
        <div class="gauge-item">
          <div class="gauge-label">LOAD FACTOR</div>
          <div class="gauge-value" id="val-gforce">+1.0 <span class="gauge-unit">G</span></div>
        </div>
      </div>

      <div class="side-gauge-cluster interactive">
        <div class="gauge-item">
          <div class="gauge-label">ALTITUDE (MSL)</div>
          <div class="gauge-value" id="val-altitude">5,280 <span class="gauge-unit">FT</span></div>
        </div>
        <div class="gauge-item">
          <div class="gauge-label">VERTICAL VELOCITY</div>
          <div class="gauge-value" id="val-vvi">+0 <span class="gauge-unit">FPM</span></div>
        </div>
        <div class="gauge-item">
          <div class="gauge-label">ANGLE OF ATTACK</div>
          <div class="gauge-value" id="val-aoa">+2.1 <span class="gauge-unit">DEG</span></div>
        </div>
        <div class="gauge-item">
          <div class="gauge-label">INTERNAL STORES</div>
          <div class="weap-status">
            <div class="weap-row"><span class="weap-name">GAU-22/A 25MM</span><span class="weap-count" id="val-ammo">180</span></div>
            <div class="weap-row"><span class="weap-name">AIM-120D AMRAAM</span><span class="weap-count" id="val-missiles">4</span></div>
            <div class="weap-row"><span class="weap-name">AIM-9X SIDEWINDER</span><span class="weap-count">2</span></div>
            <div class="weap-row"><span class="weap-name">FLARES (IRCM)</span><span class="weap-count" id="val-flares">24</span></div>
            <div class="weap-row"><span class="weap-name">TARGETS DESTROYED</span><span class="weap-count" id="val-score" style="color:var(--hud-green)">0 / 5</span></div>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-bar">
      <div class="camera-switcher interactive">
        <button class="hud-btn active" id="cam-chase" data-cam="0">1: CHASE CAM</button>
        <button class="hud-btn" id="cam-cockpit" data-cam="1">2: COCKPIT HUD</button>
        <button class="hud-btn" id="cam-flyby" data-cam="2">3: FLYBY CAM</button>
        <button class="hud-btn" id="cam-orbit" data-cam="3">4: 360° ORBIT</button>
      </div>

      <div class="action-panel interactive">
        <button class="hud-btn" id="btn-fire-gun" title="Fire 25mm Gatling Gun (F or Left Click)">GUN (F)</button>
        <button class="hud-btn" id="btn-launch-missile" title="Launch AIM-120 Missile (Space)">MISSILE (SPC)</button>
        <button class="hud-btn" id="btn-dispense-flare" title="Dispense Countermeasure Flares (C)">FLARES (C)</button>
        <button class="hud-btn" id="btn-afterburner" title="Toggle Afterburner Boost (Shift)">AB BOOST</button>
      </div>
    </div>
  </div>

  <div class="mobile-controls">
    <div class="mobile-stick-cluster">
      <div class="touch-stick-zone" id="touch-stick">
        <div class="touch-knob" id="touch-knob"></div>
      </div>
      <div class="mobile-throttle-cluster">
        <button class="touch-throttle-btn" id="touch-btn-throttle-up">THR+<br><span style="color:#00ff77;font-size:9px">AB</span></button>
        <button class="touch-throttle-btn" id="touch-btn-throttle-dn">THR-<br><span style="color:#ffaa00;font-size:9px">BRK</span></button>
      </div>
    </div>

    <div class="mobile-action-buttons">
      <div class="mobile-btn-row">
        <button class="touch-round-btn secondary" id="touch-btn-cam">CAM</button>
        <button class="touch-round-btn secondary" id="touch-btn-flare">FLR</button>
      </div>
      <div class="mobile-btn-row">
        <button class="touch-round-btn primary-msl" id="touch-btn-missile">MSL</button>
        <button class="touch-round-btn primary-gun" id="touch-btn-gun">GUN</button>
      </div>
    </div>
  </div>

  <div class="modal-overlay" id="help-modal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title">
          <span>F-35 LIGHTNING II FLIGHT MANUAL</span>
        </div>
        <button class="close-btn" id="close-help-btn">&times;</button>
      </div>
      <div class="help-grid">
        <div class="help-column">
          <div class="help-group-title">Flight Controls (Fly-By-Wire)</div>
          <div class="help-row"><span>Pitch Up (Stick Back)</span><span class="key-badge">S / Down</span></div>
          <div class="help-row"><span>Pitch Down (Stick Fwd)</span><span class="key-badge">W / Up</span></div>
          <div class="help-row"><span>Roll Left / Right</span><span class="key-badge">A / D / Left / Right</span></div>
          <div class="help-row"><span>Rudder Yaw</span><span class="key-badge">Q / E</span></div>
          <div class="help-row"><span>Throttle Increase / AB</span><span class="key-badge">Shift</span></div>
          <div class="help-row"><span>Throttle Decrease / Idle</span><span class="key-badge">Ctrl / Z</span></div>
        </div>
        <div class="help-column">
          <div class="help-group-title">Weapons & Systems</div>
          <div class="help-row"><span>Fire 25mm GAU-22/A Cannon</span><span class="key-badge">F / Click</span></div>
          <div class="help-row"><span>Launch AIM-120D AMRAAM</span><span class="key-badge">Spacebar</span></div>
          <div class="help-row"><span>Deploy Decoy Flares</span><span class="key-badge">C</span></div>
          <div class="help-row"><span>Toggle Beast Mode Pylons</span><span class="key-badge">P</span></div>
          <div class="help-row"><span>Toggle Internal Weapons Bay</span><span class="key-badge">B</span></div>
          <div class="help-row"><span>Toggle Landing Gear</span><span class="key-badge">G</span></div>
          <div class="help-row"><span>Cycle Camera Views</span><span class="key-badge">V / 1-4</span></div>
          <div class="help-row"><span>Toggle Sound Synthesizer</span><span class="key-badge">M</span></div>
          <div class="help-row"><span>Respawn Aircraft</span><span class="key-badge">R</span></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    // =========================================================================
    // 1. PROCEDURAL 2048x2048 HAVE GLASS V PBR TEXTURE GENERATOR
    // =========================================================================
    function generateHighResStealthTexture() {
      const canvas = document.createElement('canvas');
      canvas.width = 2048;
      canvas.height = 2048;
      const ctx = canvas.getContext('2d');

      // Base Have Glass V dark radar-absorbent ferrite coating
      ctx.fillStyle = '#444a51';
      ctx.fillRect(0, 0, 2048, 2048);

      // Subtle composite panels
      const cols = 16;
      const rows = 16;
      const cw = 2048 / cols;
      const ch = 2048 / rows;

      for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
          const shade = 64 + Math.floor((Math.sin(i * 1.7) * Math.cos(j * 2.3) + 1) * 7);
          ctx.fillStyle = `rgb(${shade}, ${shade + 4}, ${shade + 8})`;
          ctx.fillRect(i * cw + 2, j * ch + 2, cw - 4, ch - 4);
        }
      }

      // Panel seam lines
      ctx.strokeStyle = '#272b30';
      ctx.lineWidth = 3;
      for (let i = 0; i <= cols; i++) {
        ctx.beginPath(); ctx.moveTo(i * cw, 0); ctx.lineTo(i * cw, 2048); ctx.stroke();
      }
      for (let j = 0; j <= rows; j++) {
        ctx.beginPath(); ctx.moveTo(0, j * ch); ctx.lineTo(2048, j * ch); ctx.stroke();
      }

      // Subdued USAF Star-and-Bar National Insignia
      const drawRoundel = (cx, cy, radius) => {
        ctx.save();
        ctx.translate(cx, cy);
        ctx.fillStyle = '#555d66';
        ctx.fillRect(-radius * 1.5, -radius * 0.24, radius * 3.0, radius * 0.48);
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, Math.PI * 2);
        ctx.fillStyle = '#4b525a';
        ctx.fill();
        ctx.strokeStyle = '#636c76';
        ctx.lineWidth = 4;
        ctx.stroke();

        ctx.fillStyle = '#7a8591';
        ctx.beginPath();
        for (let k = 0; k < 5; k++) {
          const a1 = (k * 4 * Math.PI) / 5 - Math.PI / 2;
          const r1 = radius * 0.85;
          const x1 = Math.cos(a1) * r1;
          const y1 = Math.sin(a1) * r1;
          if (k === 0) ctx.moveTo(x1, y1);
          else ctx.lineTo(x1, y1);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      };

      drawRoundel(512, 1024, 130);
      drawRoundel(1536, 1024, 130);

      // Stencils and maintenance markings
      ctx.fillStyle = '#79838d';
      ctx.font = 'bold 22px "Share Tech Mono", monospace';
      ctx.fillText('NO STEP', 400, 780);
      ctx.fillText('NO STEP', 1560, 780);
      ctx.fillText('RESCUE ->', 740, 480);
      ctx.fillText('DANGER - JET INTAKE', 720, 1350);
      ctx.fillText('FF 08-0747', 1024 - 80, 1820);

      const tex = new THREE.CanvasTexture(canvas);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(1, 1);
      return tex;
    }

    // Procedural HDR Sky Texture for Image-Based Lighting (IBL)
    function generateHDRSkyTexture() {
      const canvas = document.createElement('canvas');
      canvas.width = 2048;
      canvas.height = 1024;
      const ctx = canvas.getContext('2d');

      const grad = ctx.createLinearGradient(0, 0, 0, 1024);
      grad.addColorStop(0.0, '#061c36');
      grad.addColorStop(0.35, '#15487a');
      grad.addColorStop(0.48, '#5999cf');
      grad.addColorStop(0.50, '#d2e7f7'); // Horizon haze line
      grad.addColorStop(0.52, '#0c2e4e'); // Ocean horizon line
      grad.addColorStop(0.75, '#071f36');
      grad.addColorStop(1.0, '#030f1c');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 2048, 1024);

      // Intense Sun Disc with corona glow
      const sunX = 1400;
      const sunY = 320;
      const sunGrad = ctx.createRadialGradient(sunX, sunY, 5, sunX, sunY, 180);
      sunGrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
      sunGrad.addColorStop(0.15, 'rgba(255, 250, 220, 0.9)');
      sunGrad.addColorStop(0.4, 'rgba(255, 220, 160, 0.4)');
      sunGrad.addColorStop(1.0, 'rgba(255, 200, 120, 0.0)');
      ctx.fillStyle = sunGrad;
      ctx.beginPath();
      ctx.arc(sunX, sunY, 180, 0, Math.PI * 2);
      ctx.fill();

      // Specular ocean reflection of sun
      const oceanRefl = ctx.createRadialGradient(sunX, 700, 10, sunX, 700, 240);
      oceanRefl.addColorStop(0.0, 'rgba(255, 240, 200, 0.55)');
      oceanRefl.addColorStop(0.3, 'rgba(200, 220, 255, 0.2)');
      oceanRefl.addColorStop(1.0, 'rgba(10, 40, 70, 0.0)');
      ctx.fillStyle = oceanRefl;
      ctx.fillRect(sunX - 240, 512, 480, 380);

      const tex = new THREE.CanvasTexture(canvas);
      tex.mapping = THREE.EquirectangularReflectionMapping;
      return tex;
    }

    // =========================================================================
    // 2. PROCEDURAL SOUND ENGINE WITH COCKPIT ACOUSTIC DAMPENING & VOICE ALERTS
    // =========================================================================
    class SoundEngine {
      constructor() {
        this.ctx = null;
        this.engineGain = null;
        this.whineOsc = null;
        this.rumbleGain = null;
        this.afterburnerGain = null;
        this.cockpitFilter = null;
        this.isMuffled = false;
        this.hasSonicBoomed = false;
      }

      init() {
        if (this.ctx) return;
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();

        // Master output & Cockpit Low-Pass Filter
        this.cockpitFilter = this.ctx.createBiquadFilter();
        this.cockpitFilter.type = 'lowpass';
        this.cockpitFilter.frequency.value = 18000; // Unmuffled default
        this.cockpitFilter.connect(this.ctx.destination);

        // 1. Turbofan Whine Oscillator
        this.whineOsc = this.ctx.createOscillator();
        this.whineOsc.type = 'sawtooth';
        const whineFilter = this.ctx.createBiquadFilter();
        whineFilter.type = 'bandpass';
        whineFilter.frequency.value = 850;
        whineFilter.Q.value = 3.5;

        this.engineGain = this.ctx.createGain();
        this.engineGain.gain.value = 0.04;

        this.whineOsc.connect(whineFilter);
        whineFilter.connect(this.engineGain);
        this.engineGain.connect(this.cockpitFilter);
        this.whineOsc.start();

        // 2. Jet Blast Noise (Brownian Roar)
        const bufferSize = this.ctx.sampleRate * 2;
        const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = noiseBuffer.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
          const white = Math.random() * 2 - 1;
          data[i] = (lastOut + (0.02 * white)) / 1.02;
          lastOut = data[i];
          data[i] *= 3.5;
        }

        const roarNoise = this.ctx.createBufferSource();
        roarNoise.buffer = noiseBuffer;
        roarNoise.loop = true;

        const roarFilter = this.ctx.createBiquadFilter();
        roarFilter.type = 'lowpass';
        roarFilter.frequency.value = 420;

        this.rumbleGain = this.ctx.createGain();
        this.rumbleGain.gain.value = 0.08;

        roarNoise.connect(roarFilter);
        roarFilter.connect(this.rumbleGain);
        this.rumbleGain.connect(this.cockpitFilter);
        roarNoise.start();

        // 3. Afterburner Sub-Bass Rumble
        this.abOsc = this.ctx.createOscillator();
        this.abOsc.type = 'triangle';
        this.abOsc.frequency.value = 55;
        this.afterburnerGain = this.ctx.createGain();
        this.afterburnerGain.gain.value = 0.0;
        this.abOsc.connect(this.afterburnerGain);
        this.afterburnerGain.connect(this.cockpitFilter);
        this.abOsc.start();
      }

      setCockpitMuffled(muffled) {
        if (!this.ctx || !this.cockpitFilter) return;
        this.isMuffled = muffled;
        const targetFreq = muffled ? 650 : 18000;
        this.cockpitFilter.frequency.setTargetAtTime(targetFreq, this.ctx.currentTime, 0.15);
      }

      speakAlert(phrase) {
        if (!('speechSynthesis' in window)) return;
        try {
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(phrase);
          utterance.rate = 1.15;
          utterance.pitch = 0.95;
          utterance.volume = 0.9;
          window.speechSynthesis.speak(utterance);
        } catch (e) {}
      }

      update(throttle, speedKnots) {
        if (!this.ctx) return;
        const t = Math.max(0, Math.min(1.3, throttle));
        const freq = 320 + t * 900 + (speedKnots / 700) * 400;
        this.whineOsc.frequency.setTargetAtTime(freq, this.ctx.currentTime, 0.08);

        const targetGain = 0.03 + t * 0.08;
        this.engineGain.gain.setTargetAtTime(targetGain, this.ctx.currentTime, 0.08);

        const roarTarget = 0.05 + t * 0.14 + (speedKnots / 800) * 0.08;
        this.rumbleGain.gain.setTargetAtTime(roarTarget, this.ctx.currentTime, 0.08);

        const abVal = (t > 1.0) ? (t - 1.0) * 0.6 : 0.0;
        this.afterburnerGain.gain.setTargetAtTime(abVal, this.ctx.currentTime, 0.05);

        if (speedKnots > 661 && !this.hasSonicBoomed) {
          this.playSonicBoom();
          this.hasSonicBoomed = true;
        } else if (speedKnots < 640) {
          this.hasSonicBoomed = false;
        }
      }

      playGunfire() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(35, this.ctx.currentTime + 0.05);
        gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);
        osc.connect(gain);
        gain.connect(this.cockpitFilter);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.05);
      }

      playMissileLaunch() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(380, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(120, this.ctx.currentTime + 0.7);
        gain.gain.setValueAtTime(0.25, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.7);
        osc.connect(gain);
        gain.connect(this.cockpitFilter);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.7);
      }

      playFlare() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(180, this.ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.12);
        osc.connect(gain);
        gain.connect(this.cockpitFilter);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.12);
      }

      playSonicBoom() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(80, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(20, this.ctx.currentTime + 0.9);
        gain.gain.setValueAtTime(0.7, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.9);
        osc.connect(gain);
        gain.connect(this.cockpitFilter);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.9);
      }

      playTargetExplosion() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(110, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(25, this.ctx.currentTime + 1.2);
        gain.gain.setValueAtTime(0.45, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.2);
        osc.connect(gain);
        gain.connect(this.cockpitFilter);
        osc.start();
        osc.stop(this.ctx.currentTime + 1.2);
      }
    }

    const sound = new SoundEngine();

    // =========================================================================
    // 3. PANORAMIC COCKPIT DISPLAY (PCD) AVIONICS ENGINE
    // =========================================================================
    class CockpitPCDDisplay {
      constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.width = 512;
        this.canvas.height = 256;
        this.ctx = this.canvas.getContext('2d');
        this.texture = new THREE.CanvasTexture(this.canvas);
        this.radarSweep = 0;
      }

      update(state, targets, beastMode) {
        const ctx = this.ctx;
        ctx.fillStyle = '#040b10';
        ctx.fillRect(0, 0, 512, 256);

        // Frame dividers
        ctx.strokeStyle = '#0e2a22';
        ctx.lineWidth = 2;
        ctx.strokeRect(4, 4, 164, 248);
        ctx.strokeRect(172, 4, 168, 248);
        ctx.strokeRect(344, 4, 164, 248);

        // 1. Left Telemetry & Stores
        ctx.fillStyle = '#00ff77';
        ctx.font = '11px "Share Tech Mono", monospace';
        ctx.fillText('SYS / STORES', 14, 22);
        ctx.fillText(`ENG RPM: ${Math.round(state.throttle * 100)}%`, 14, 46);
        ctx.fillText(`CORE TEMP: ${Math.round(480 + state.throttle * 320)}C`, 14, 66);
        ctx.fillText(`FUEL: 12,450 LBS`, 14, 86);
        ctx.fillText(`GUN: ${state.ammo} RDS`, 14, 116);
        ctx.fillText(`AMRAAM: ${state.missilesLeft} / 4`, 14, 136);
        ctx.fillText(`SIDEWINDER: 2 / 2`, 14, 156);
        ctx.fillText(`FLARES: ${state.flaresLeft}`, 14, 176);
        ctx.fillText(`GEAR: ${state.gearDown ? 'DOWN' : 'UP'}`, 14, 206);
        ctx.fillText(`BEAST: ${beastMode ? 'ACTIVE' : 'STEALTH'}`, 14, 226);

        // 2. Center Synthetic ADI
        ctx.save();
        ctx.translate(256, 128);
        ctx.beginPath();
        ctx.arc(0, 0, 68, 0, Math.PI * 2);
        ctx.clip();

        const euler = new THREE.Euler().setFromQuaternion(state.quaternion, 'YXZ');
        ctx.rotate(-euler.z);
        const pitchY = euler.x * 120;

        ctx.fillStyle = '#0c3866';
        ctx.fillRect(-120, pitchY - 240, 240, 240);
        ctx.fillStyle = '#443216';
        ctx.fillRect(-120, pitchY, 240, 240);

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-70, pitchY);
        ctx.lineTo(70, pitchY);
        ctx.stroke();
        ctx.restore();

        // ADI center reticle
        ctx.strokeStyle = '#00ffaa';
        ctx.lineWidth = 2;
        ctx.strokeRect(252, 124, 8, 8);

        // 3. Right Tactical Radar
        ctx.fillStyle = '#00ff77';
        ctx.fillText('TAC RADAR 30NM', 354, 22);

        const rx = 426;
        const ry = 138;
        const rRadius = 80;

        ctx.strokeStyle = '#0e4430';
        ctx.beginPath(); ctx.arc(rx, ry, rRadius, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.arc(rx, ry, rRadius * 0.6, 0, Math.PI * 2); ctx.stroke();

        this.radarSweep = (this.radarSweep + 0.05) % (Math.PI * 2);
        ctx.strokeStyle = 'rgba(0, 255, 119, 0.7)';
        ctx.beginPath();
        ctx.moveTo(rx, ry);
        ctx.lineTo(rx + Math.cos(this.radarSweep) * rRadius, ry + Math.sin(this.radarSweep) * rRadius);
        ctx.stroke();

        // Ownship symbol
        ctx.fillStyle = '#00ff77';
        ctx.beginPath();
        ctx.moveTo(rx, ry - 6); ctx.lineTo(rx - 5, ry + 5); ctx.lineTo(rx + 5, ry + 5);
        ctx.closePath();
        ctx.fill();

        if (targets && targets.length) {
          const jetPos = state.position;
          for (const tgt of targets) {
            if (tgt.destroyed) continue;
            const dx = (tgt.mesh.position.x - jetPos.x) / 350;
            const dz = (tgt.mesh.position.z - jetPos.z) / 350;
            if (Math.hypot(dx, dz) < rRadius - 4) {
              ctx.fillStyle = tgt.isHostile ? '#ff3344' : '#00e5ff';
              ctx.fillRect(rx + dx - 3, ry + dz - 3, 6, 6);
            }
          }
        }

        this.texture.needsUpdate = true;
      }
    }

    // =========================================================================
    // 4. HIGH-FIDELITY F-35 LIGHTNING II 3D AIRCRAFT MODEL & SYSTEMS
    // =========================================================================
    class F35Aircraft {
      constructor() {
        this.group = new THREE.Group();
        this.innerModel = new THREE.Group();
        this.innerModel.rotation.y = Math.PI; // Nose points to -Z forward in world
        this.group.add(this.innerModel);

        this.stealthTex = generateHighResStealthTexture();
        this.pcd = new CockpitPCDDisplay();

        // Have Glass V radar-absorbent ferrite RAM material
        this.bodyMaterial = new THREE.MeshStandardMaterial({
          map: this.stealthTex,
          color: 0x5a636c,
          roughness: 0.38,
          metalness: 0.40,
          flatShading: false
        });

        this.darkAccentMaterial = new THREE.MeshStandardMaterial({
          color: 0x1f2327,
          roughness: 0.55,
          metalness: 0.45
        });

        // Polycarbonate gold radar-reflective canopy
        this.canopyMaterial = new THREE.MeshPhysicalMaterial({
          color: 0xdfa634,
          metalness: 0.25,
          roughness: 0.08,
          transmission: 0.72,
          transparent: true,
          opacity: 0.85,
          reflectivity: 0.95,
          clearcoat: 1.0,
          clearcoatRoughness: 0.05
        });

        // Heat-scorched titanium nozzle petals
        this.nozzleMaterial = new THREE.MeshStandardMaterial({
          color: 0x22272c,
          roughness: 0.35,
          metalness: 0.85
        });

        // Moving Control Surfaces & Interactive Cockpit
        this.leftLEF = null;
        this.rightLEF = null;
        this.leftFlaperon = null;
        this.rightFlaperon = null;
        this.leftStabilator = null;
        this.rightStabilator = null;
        this.leftRudder = null;
        this.rightRudder = null;
        this.leftBayDoor = null;
        this.rightBayDoor = null;
        this.landingGearGroup = new THREE.Group();
        this.pylonsGroup = new THREE.Group();
        this.nozzlePetals = [];
        this.afterburnerPlume = null;
        this.shockDiamonds = [];
        this.vaporCone = null;
        this.leftWingVortex = null;
        this.rightWingVortex = null;
        this.heatShimmerGroup = new THREE.Group();
        this.hotasStick = null;
        this.hotasThrottle = null;
        this.canopy = null;
        this.pilotMesh = null;
        this.beastMode = false;

        this.buildModel();
      }

      buildModel() {
        const m = this.innerModel;

        // 1. Nose Radome & Continuous Forebody Chine
        const noseGeo = new THREE.ConeGeometry(0.9, 3.8, 8);
        noseGeo.rotateX(Math.PI / 2); // Point sharp apex forward along +Z
        noseGeo.scale(1.15, 0.65, 1.0);
        const nose = new THREE.Mesh(noseGeo, this.bodyMaterial);
        nose.position.set(0, 0.1, 6.2);
        m.add(nose);

        // Pitot boom protruding from sharp radome apex
        const pitot = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.03, 0.8, 6), this.darkAccentMaterial);
        pitot.rotation.x = Math.PI / 2;
        pitot.position.set(0, 0.1, 8.4);
        m.add(pitot);

        // Electro-Optical Targeting System (EOTS) Sapphire Prism Window
        const eotsPrismGeo = new THREE.ConeGeometry(0.35, 0.85, 4);
        eotsPrismGeo.rotateX(-Math.PI / 2);
        const eotsPrism = new THREE.Mesh(eotsPrismGeo, new THREE.MeshPhysicalMaterial({
          color: 0x00e5ff,
          transmission: 0.85,
          roughness: 0.05,
          metalness: 0.1,
          clearcoat: 1.0
        }));
        eotsPrism.position.set(0, -0.42, 5.8);
        m.add(eotsPrism);

        // Internal EOTS Sensor Optics
        const eotsOptic = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), new THREE.MeshBasicMaterial({ color: 0x00ff88 }));
        eotsOptic.position.set(0, -0.42, 5.8);
        m.add(eotsOptic);

        // 6x Distributed Aperture System (DAS) Optical Sensors
        const dasMat = new THREE.MeshStandardMaterial({ color: 0x112233, roughness: 0.1, metalness: 0.9 });
        const dasGeo = new THREE.BoxGeometry(0.12, 0.12, 0.04);
        const dasOffsets = [
          [-0.75, 0.25, 4.8], [0.75, 0.25, 4.8],   // Nose sides
          [-0.45, 1.02, -0.8], [0.45, 1.02, -0.8], // Upper dorsal spine
          [-0.55, -0.52, 0.5], [0.55, -0.52, 0.5]  // Underbelly
        ];
        dasOffsets.forEach(pos => {
          const das = new THREE.Mesh(dasGeo, dasMat);
          das.position.set(pos[0], pos[1], pos[2]);
          m.add(das);
        });

        // Forward chines & cockpit glare shield
        const fwdChine = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.8, 4.2), this.bodyMaterial);
        fwdChine.position.set(0, 0.15, 2.8);
        m.add(fwdChine);

        // Main Blended Fuselage & Dorsal Spine
        const midFuselage = new THREE.Mesh(new THREE.BoxGeometry(3.3, 1.25, 6.5), this.bodyMaterial);
        midFuselage.position.set(0, 0.25, -1.8);
        m.add(midFuselage);

        const spineGeo = new THREE.ConeGeometry(0.75, 5.5, 4);
        spineGeo.rotateX(Math.PI / 2);
        spineGeo.scale(1.2, 0.6, 1.0);
        const spine = new THREE.Mesh(spineGeo, this.bodyMaterial);
        spine.position.set(0, 0.95, -1.5);
        m.add(spine);

        // 2. DSI Intakes with 3D Compression Bumps
        const leftIntake = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.95, 3.2), this.bodyMaterial);
        leftIntake.position.set(-1.65, -0.05, 1.2);
        leftIntake.rotation.set(-0.15, 0.08, -0.15);
        m.add(leftIntake);

        const leftBump = new THREE.Mesh(new THREE.SphereGeometry(0.35, 10, 8), this.bodyMaterial);
        leftBump.scale.set(0.6, 0.9, 1.8);
        leftBump.position.set(-1.3, -0.05, 2.2);
        m.add(leftBump);

        const rightIntake = leftIntake.clone();
        rightIntake.position.x = 1.65;
        rightIntake.rotation.set(-0.15, -0.08, 0.15);
        m.add(rightIntake);

        const rightBump = leftBump.clone();
        rightBump.position.x = 1.3;
        m.add(rightBump);

        // 3. Cockpit, Martin-Baker US16E Ejection Seat & Interactive HOTAS
        const seatGroup = new THREE.Group();
        const seatBack = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.75, 0.15), this.darkAccentMaterial);
        seatBack.position.set(0, 0.65, 2.6);
        seatBack.rotation.x = -0.2;
        seatGroup.add(seatBack);

        // Seat Guide Rails
        const railMat = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.8 });
        const leftGuideRail = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.2, 6), railMat);
        leftGuideRail.position.set(-0.24, 0.65, 2.55);
        leftGuideRail.rotation.x = -0.2;
        seatGroup.add(leftGuideRail);

        const rightGuideRail = leftGuideRail.clone();
        rightGuideRail.position.x = 0.24;
        seatGroup.add(rightGuideRail);

        // Primary Ejection Pull Ring (Yellow & Black striped loop)
        const pullRing = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.012, 6, 12, Math.PI), new THREE.MeshBasicMaterial({ color: 0xffcc00 }));
        pullRing.rotation.x = Math.PI / 2;
        pullRing.position.set(0, 0.38, 2.85);
        seatGroup.add(pullRing);

        // Pilot Helmet with Gen III HMDS visor
        const helmet = new THREE.Mesh(new THREE.SphereGeometry(0.14, 12, 12), new THREE.MeshStandardMaterial({ color: 0x222629, roughness: 0.5 }));
        helmet.position.set(0, 0.90, 2.70);
        seatGroup.add(helmet);

        const visor = new THREE.Mesh(new THREE.SphereGeometry(0.11, 8, 8, 0, Math.PI), new THREE.MeshBasicMaterial({ color: 0x00ff88 }));
        visor.rotation.set(-0.15, Math.PI / 2, 0);
        visor.position.set(0, 0.90, 2.80);
        seatGroup.add(visor);

        // Moving HOTAS Side-Stick Controller (Right Console)
        const stickHolder = new THREE.Group();
        stickHolder.position.set(0.35, 0.50, 3.05);
        const stickGrip = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.025, 0.22, 6), this.darkAccentMaterial);
        stickGrip.position.y = 0.11;
        stickHolder.add(stickGrip);
        seatGroup.add(stickHolder);
        this.hotasStick = stickHolder;

        // Moving HOTAS Throttle Lever (Left Console)
        const throttleHolder = new THREE.Group();
        throttleHolder.position.set(-0.35, 0.52, 3.05);
        const throttleGrip = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.06, 0.12), this.darkAccentMaterial);
        throttleGrip.position.y = 0.04;
        throttleHolder.add(throttleGrip);
        seatGroup.add(throttleHolder);
        this.hotasThrottle = throttleHolder;

        this.pilotMesh = seatGroup;
        m.add(seatGroup);

        // Panoramic Cockpit Display (PCD) screen
        const pcdMat = new THREE.MeshBasicMaterial({ map: this.pcd.texture });
        const pcdScreen = new THREE.Mesh(new THREE.PlaneGeometry(0.68, 0.24), pcdMat);
        pcdScreen.position.set(0, 0.58, 3.6);
        pcdScreen.rotation.x = -0.65;
        m.add(pcdScreen);

        // Gold Polycarbonate Canopy
        const canopyCurve = new THREE.CylinderGeometry(0.52, 0.65, 2.8, 12);
        canopyCurve.rotateX(Math.PI / 2);
        canopyCurve.scale(0.85, 0.55, 1.0);
        const canopy = new THREE.Mesh(canopyCurve, this.canopyMaterial);
        canopy.position.set(0, 0.78, 3.1);
        m.add(canopy);
        this.canopy = canopy;

        // Canopy Bow Rearview Mirrors
        const mirrorGeo = new THREE.PlaneGeometry(0.09, 0.05);
        const mirrorMat = new THREE.MeshStandardMaterial({ color: 0xccddee, metalness: 0.95, roughness: 0.1 });
        const leftMirror = new THREE.Mesh(mirrorGeo, mirrorMat);
        leftMirror.position.set(-0.32, 0.92, 3.3);
        leftMirror.rotation.set(-0.2, 0.4, 0);
        m.add(leftMirror);

        const rightMirror = leftMirror.clone();
        rightMirror.position.x = 0.32;
        rightMirror.rotation.y = -0.4;
        m.add(rightMirror);

        // 4. Main Wings, Drooping Slats (LEF) & Flaperons
        const wingShape = new THREE.Shape();
        wingShape.moveTo(0, 0);
        wingShape.lineTo(-5.2, -2.4);
        wingShape.lineTo(-5.0, -3.4);
        wingShape.lineTo(0, -3.2);
        wingShape.closePath();

        const wingGeo = new THREE.ExtrudeGeometry(wingShape, { depth: 0.15, bevelEnabled: true, bevelSize: 0.04, bevelThickness: 0.04 });
        wingGeo.rotateX(Math.PI / 2);

        const leftWing = new THREE.Mesh(wingGeo, this.bodyMaterial);
        leftWing.position.set(-1.3, 0.15, 0.8);
        m.add(leftWing);

        const rightWing = new THREE.Mesh(wingGeo, this.bodyMaterial);
        rightWing.position.set(1.3, 0.15, 0.8);
        rightWing.scale.set(-1, 1, 1);
        m.add(rightWing);

        // Leading-Edge Slats (LEF)
        const lefGeo = new THREE.BoxGeometry(3.6, 0.06, 0.35);
        this.leftLEF = new THREE.Mesh(lefGeo, this.bodyMaterial);
        this.leftLEF.position.set(-3.2, 0.14, -0.6);
        this.leftLEF.rotation.y = -0.42;
        m.add(this.leftLEF);

        this.rightLEF = new THREE.Mesh(lefGeo, this.bodyMaterial);
        this.rightLEF.position.set(3.2, 0.14, -0.6);
        this.rightLEF.rotation.y = 0.42;
        m.add(this.rightLEF);

        // Trailing-Edge Flaperons
        const flaperonGeo = new THREE.BoxGeometry(2.3, 0.08, 0.75);
        this.leftFlaperon = new THREE.Mesh(flaperonGeo, this.bodyMaterial);
        this.leftFlaperon.position.set(-3.4, 0.15, -2.2);
        m.add(this.leftFlaperon);

        this.rightFlaperon = new THREE.Mesh(flaperonGeo, this.bodyMaterial);
        this.rightFlaperon.position.set(3.4, 0.15, -2.2);
        m.add(this.rightFlaperon);

        // Wingtip Sidewinder Rails
        const railGeo = new THREE.BoxGeometry(0.12, 0.12, 2.2);
        const leftRail = new THREE.Mesh(railGeo, this.darkAccentMaterial);
        leftRail.position.set(-5.15, 0.15, -1.9);
        m.add(leftRail);

        const leftSidewinder = this.createAIM9XMesh();
        leftSidewinder.position.set(-5.15, 0.05, -1.9);
        m.add(leftSidewinder);

        const rightRail = leftRail.clone();
        rightRail.position.x = 5.15;
        m.add(rightRail);

        const rightSidewinder = this.createAIM9XMesh();
        rightSidewinder.position.set(5.15, 0.05, -1.9);
        m.add(rightSidewinder);

        // External Weapons Pylons ("Beast Mode" - 2x GBU-31 JDAM bombs)
        this.buildBeastModePylons();
        m.add(this.pylonsGroup);

        // 5. Twin Canted Vertical Tails (~20° Outward)
        const vertTailShape = new THREE.Shape();
        vertTailShape.moveTo(0, 0);
        vertTailShape.lineTo(-0.85, 2.6);
        vertTailShape.lineTo(-1.85, 2.5);
        vertTailShape.lineTo(-1.85, 0);
        vertTailShape.closePath();

        const leftTailGeo = new THREE.ExtrudeGeometry(vertTailShape, { depth: 0.1, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02 });
        const leftTailMesh = new THREE.Mesh(leftTailGeo, this.bodyMaterial);
        leftTailMesh.position.set(-1.15, 0.6, -3.2);
        leftTailMesh.rotation.set(0, 0.05, 0.35);
        m.add(leftTailMesh);

        this.leftRudder = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.8, 0.55), this.bodyMaterial);
        this.leftRudder.position.set(-1.8, 1.7, -4.6);
        this.leftRudder.rotation.z = 0.35;
        m.add(this.leftRudder);

        const rightTailMesh = new THREE.Mesh(leftTailGeo, this.bodyMaterial);
        rightTailMesh.position.set(1.15, 0.6, -3.2);
        rightTailMesh.rotation.set(0, -0.05, -0.35);
        rightTailMesh.scale.set(-1, 1, 1);
        m.add(rightTailMesh);

        this.rightRudder = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.8, 0.55), this.bodyMaterial);
        this.rightRudder.position.set(1.8, 1.7, -4.6);
        this.rightRudder.rotation.z = -0.35;
        m.add(this.rightRudder);

        // 6. All-Moving Horizontal Tail Stabilators
        const stabShape = new THREE.Shape();
        stabShape.moveTo(0, 0);
        stabShape.lineTo(-2.2, -0.9);
        stabShape.lineTo(-1.9, -2.1);
        stabShape.lineTo(0, -1.6);
        stabShape.closePath();

        const stabGeo = new THREE.ExtrudeGeometry(stabShape, { depth: 0.08, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02 });
        stabGeo.rotateX(Math.PI / 2);

        this.leftStabilator = new THREE.Mesh(stabGeo, this.bodyMaterial);
        this.leftStabilator.position.set(-1.25, 0.25, -4.6);
        m.add(this.leftStabilator);

        this.rightStabilator = new THREE.Mesh(stabGeo, this.bodyMaterial);
        this.rightStabilator.position.set(1.25, 0.25, -4.6);
        this.rightStabilator.scale.set(-1, 1, 1);
        m.add(this.rightStabilator);

        // 7. Engine & 15 Articulated Serrated Titanium Nozzle Petals
        const shroud = new THREE.Mesh(new THREE.CylinderGeometry(0.82, 0.78, 2.2, 16), this.bodyMaterial);
        shroud.rotation.x = Math.PI / 2;
        shroud.position.set(0, 0.35, -4.5);
        m.add(shroud);

        // Internal Turbine Augmentor Flame-Gutter Ring
        this.augmentorGlow = new THREE.Mesh(
          new THREE.TorusGeometry(0.55, 0.06, 8, 16),
          new THREE.MeshBasicMaterial({ color: 0xff3300 })
        );
        this.augmentorGlow.rotation.x = Math.PI / 2;
        this.augmentorGlow.position.set(0, 0.35, -5.3);
        m.add(this.augmentorGlow);

        const petalGroup = new THREE.Group();
        petalGroup.position.set(0, 0.35, -5.55);
        const petalGeo = new THREE.BoxGeometry(0.20, 0.035, 0.85);
        petalGeo.translate(0, 0, -0.425); // Forward pivot

        for (let i = 0; i < 15; i++) {
          const angle = (i * Math.PI * 2) / 15;
          const petalHolder = new THREE.Group();
          petalHolder.rotation.z = angle;
          const petal = new THREE.Mesh(petalGeo, this.nozzleMaterial);
          petal.position.y = 0.62;
          petalHolder.add(petal);
          petalGroup.add(petalHolder);
          this.nozzlePetals.push(petal);
        }
        m.add(petalGroup);

        // Multi-Layer Afterburner Plume
        const plumeGroup = new THREE.Group();
        plumeGroup.position.set(0, 0.35, -5.9);

        const flameOuterGeo = new THREE.ConeGeometry(0.58, 4.8, 16, 1, true);
        flameOuterGeo.rotateX(Math.PI / 2);
        const flameOuter = new THREE.Mesh(flameOuterGeo, new THREE.MeshBasicMaterial({
          color: 0xff7700,
          transparent: true,
          opacity: 0.8,
          blending: THREE.AdditiveBlending,
          side: THREE.DoubleSide
        }));
        flameOuter.position.z = -2.4;
        plumeGroup.add(flameOuter);

        const flameCoreGeo = new THREE.ConeGeometry(0.34, 3.4, 16, 1, true);
        flameCoreGeo.rotateX(Math.PI / 2);
        const flameCore = new THREE.Mesh(flameCoreGeo, new THREE.MeshBasicMaterial({
          color: 0x00d5ff,
          transparent: true,
          opacity: 0.9,
          blending: THREE.AdditiveBlending,
          side: THREE.DoubleSide
        }));
        flameCore.position.z = -1.7;
        plumeGroup.add(flameCore);

        for (let i = 0; i < 4; i++) {
          const diamond = new THREE.Mesh(
            new THREE.OctahedronGeometry(0.20 - i * 0.03, 0),
            new THREE.MeshBasicMaterial({ color: 0xffffff, blending: THREE.AdditiveBlending })
          );
          diamond.position.z = -1.0 - i * 0.9;
          diamond.scale.set(0.7, 0.7, 2.2);
          plumeGroup.add(diamond);
          this.shockDiamonds.push(diamond);
        }

        this.afterburnerPlume = plumeGroup;
        this.afterburnerPlume.visible = false;
        m.add(plumeGroup);

        // Transonic Prandtl-Glauert Vapor Shock Collar (Mach ~ 1.0)
        const vaporGeo = new THREE.CylinderGeometry(2.4, 3.8, 1.2, 16, 1, true);
        vaporGeo.rotateX(Math.PI / 2);
        this.vaporCone = new THREE.Mesh(vaporGeo, new THREE.MeshBasicMaterial({
          color: 0xffffff,
          transparent: true,
          opacity: 0.0,
          side: THREE.DoubleSide,
          blending: THREE.AdditiveBlending
        }));
        this.vaporCone.position.set(0, 0.25, -0.6);
        m.add(this.vaporCone);

        // Wingtip Vortex Ribbons (High-G Turns)
        const vortexGeo = new THREE.CylinderGeometry(0.04, 0.12, 18, 6);
        vortexGeo.rotateX(Math.PI / 2);
        const vortexMat = new THREE.MeshBasicMaterial({ color: 0xddeeff, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending });
        this.leftWingVortex = new THREE.Mesh(vortexGeo, vortexMat);
        this.leftWingVortex.position.set(-5.15, 0.15, -11.0);
        m.add(this.leftWingVortex);

        this.rightWingVortex = new THREE.Mesh(vortexGeo, vortexMat);
        this.rightWingVortex.position.set(5.15, 0.15, -11.0);
        m.add(this.rightWingVortex);

        // 8. Tricycle Retractable Landing Gear with Oleo Struts
        this.buildLandingGear();
        m.add(this.landingGearGroup);
      }

      buildBeastModePylons() {
        this.pylonsGroup.visible = false;

        const pylonGeo = new THREE.BoxGeometry(0.18, 0.35, 2.4);
        const pylonMat = this.darkAccentMaterial;

        // Inboard Left Pylon + GBU-31 JDAM bomb
        const leftPylon = new THREE.Mesh(pylonGeo, pylonMat);
        leftPylon.position.set(-2.5, -0.15, -1.2);
        const leftJdam = this.createGBU31Mesh();
        leftJdam.position.set(0, -0.32, 0);
        leftPylon.add(leftJdam);
        this.pylonsGroup.add(leftPylon);

        // Inboard Right Pylon + GBU-31 JDAM bomb
        const rightPylon = new THREE.Mesh(pylonGeo, pylonMat);
        rightPylon.position.set(2.5, -0.15, -1.2);
        const rightJdam = this.createGBU31Mesh();
        rightJdam.position.set(0, -0.32, 0);
        rightPylon.add(rightJdam);
        this.pylonsGroup.add(rightPylon);
      }

      createGBU31Mesh() {
        const jdam = new THREE.Group();
        // Bomb Body
        const bodyGeo = new THREE.CylinderGeometry(0.24, 0.24, 2.6, 12);
        bodyGeo.rotateX(Math.PI / 2);
        const body = new THREE.Mesh(bodyGeo, new THREE.MeshStandardMaterial({ color: 0x485244, roughness: 0.6 }));
        jdam.add(body);

        // Steel Penetrator Ogive Nose
        const noseGeo = new THREE.ConeGeometry(0.24, 0.7, 12);
        noseGeo.rotateX(Math.PI / 2);
        const nose = new THREE.Mesh(noseGeo, new THREE.MeshStandardMaterial({ color: 0x778274, metalness: 0.6 }));
        nose.position.z = 1.65;
        jdam.add(nose);

        // Yellow Explosive Hazard Stripe
        const stripe = new THREE.Mesh(new THREE.CylinderGeometry(0.242, 0.242, 0.15, 12).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xffcc00 }));
        stripe.position.z = 1.15;
        jdam.add(stripe);

        // Tail Guidance Kit & Grid Fins
        const tail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.22, 0.8), this.darkAccentMaterial);
        tail.position.z = -1.6;
        jdam.add(tail);

        for (let i = 0; i < 4; i++) {
          const fin = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.5, 0.35), this.darkAccentMaterial);
          fin.rotation.z = (i * Math.PI) / 2;
          fin.position.z = -1.75;
          jdam.add(fin);
        }
        return jdam;
      }

      createAIM9XMesh() {
        const missile = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 2.4, 8).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xb5bcc4, roughness: 0.4 }));
        missile.add(body);
        const seeker = new THREE.Mesh(new THREE.SphereGeometry(0.065, 8, 8), new THREE.MeshStandardMaterial({ color: 0x112233, metalness: 0.9 }));
        seeker.position.z = 1.2;
        missile.add(seeker);

        for (let i = 0; i < 4; i++) {
          const fin = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.32, 0.22), this.darkAccentMaterial);
          fin.rotation.z = (i * Math.PI) / 2;
          fin.position.z = -1.0;
          missile.add(fin);
        }
        return missile;
      }

      createAIM120Mesh() {
        const missile = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 3.2, 8).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xd8dde4, roughness: 0.5 }));
        missile.add(body);
        const nose = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.6, 8).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x88929e, roughness: 0.3 }));
        nose.position.z = 1.9;
        missile.add(nose);

        for (let i = 0; i < 4; i++) {
          const wing = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.55, 0.45), this.darkAccentMaterial);
          wing.rotation.z = (i * Math.PI) / 2;
          wing.position.z = 0.2;
          missile.add(wing);

          const tailFin = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.42, 0.35), this.darkAccentMaterial);
          tailFin.rotation.z = (i * Math.PI) / 2;
          tailFin.position.z = -1.4;
          missile.add(tailFin);
        }
        return missile;
      }

      buildLandingGear() {
        const gearMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.3, roughness: 0.4 });
        const tireMat = new THREE.MeshStandardMaterial({ color: 0x181a1c, roughness: 0.9 });

        // Nose Gear with Twin Tires & Catapult Launch Bar
        const noseGear = new THREE.Group();
        noseGear.position.set(0, 0, 4.3);
        const noseStrut = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.4, 8), gearMat);
        noseStrut.position.y = -0.7;
        noseGear.add(noseStrut);

        // Twin Nose Tires
        const tireGeo = new THREE.CylinderGeometry(0.24, 0.24, 0.12, 12).rotateZ(Math.PI / 2);
        const noseTireL = new THREE.Mesh(tireGeo, tireMat);
        noseTireL.position.set(-0.11, -1.35, 0);
        noseGear.add(noseTireL);

        const noseTireR = new THREE.Mesh(tireGeo, tireMat);
        noseTireR.position.set(0.11, -1.35, 0);
        noseGear.add(noseTireR);

        // Catapult Tow Launch Bar
        const launchBar = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.45, 0.05), gearMat);
        launchBar.position.set(0, -1.1, 0.25);
        launchBar.rotation.x = -0.6;
        noseGear.add(launchBar);

        this.landingGearGroup.add(noseGear);

        // Main Left Gear
        const mainGearL = new THREE.Group();
        mainGearL.position.set(-1.25, 0, -1.2);
        const mainStrutL = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.5, 8), gearMat);
        mainStrutL.position.set(0, -0.75, 0);
        mainStrutL.rotation.z = 0.15;
        mainGearL.add(mainStrutL);

        const mainTireL = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.24, 14).rotateZ(Math.PI / 2), tireMat);
        mainTireL.position.set(-0.18, -1.45, 0);
        mainGearL.add(mainTireL);
        this.landingGearGroup.add(mainGearL);

        // Main Right Gear
        const mainGearR = new THREE.Group();
        mainGearR.position.set(1.25, 0, -1.2);
        const mainStrutR = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.5, 8), gearMat);
        mainStrutR.position.set(0, -0.75, 0);
        mainStrutR.rotation.z = -0.15;
        mainGearR.add(mainStrutR);

        const mainTireR = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.24, 14).rotateZ(Math.PI / 2), tireMat);
        mainTireR.position.set(0.18, -1.45, 0);
        mainGearR.add(mainTireR);
        this.landingGearGroup.add(mainGearR);

        this.landingGearGroup.visible = false;
      }

      toggleBeastMode() {
        this.beastMode = !this.beastMode;
        this.pylonsGroup.visible = this.beastMode;
        return this.beastMode;
      }

      updateVisuals(physics, dt) {
        // Control Surfaces Deflection
        const pitch = physics.pitchInput;
        const roll = physics.rollInput;
        const yaw = physics.yawInput;

        // Differential Stabilators
        if (this.leftStabilator) this.leftStabilator.rotation.x = pitch * 0.42 - roll * 0.22;
        if (this.rightStabilator) this.rightStabilator.rotation.x = pitch * 0.42 + roll * 0.22;

        // Flaperons (with STOL flap extension when gear is down)
        const stolFlap = physics.gearDown ? 0.45 : 0.0;
        if (this.leftFlaperon) this.leftFlaperon.rotation.x = -pitch * 0.35 + roll * 0.45 + stolFlap;
        if (this.rightFlaperon) this.rightFlaperon.rotation.x = -pitch * 0.35 - roll * 0.45 + stolFlap;

        // Rudders (with automatic toe-in airbrake during ground roll)
        const groundAirbrake = (physics.onGround && physics.speedKnots > 30) ? 0.35 : 0.0;
        if (this.leftRudder) this.leftRudder.rotation.y = yaw * 0.40 - groundAirbrake;
        if (this.rightRudder) this.rightRudder.rotation.y = yaw * 0.40 + groundAirbrake;

        // Drooping Slats (LEF) at high AoA
        const slatDroop = (physics.aoaDeg > 8.0) ? Math.min(0.5, (physics.aoaDeg - 8.0) * 0.04) : 0.0;
        if (this.leftLEF) this.leftLEF.rotation.x = slatDroop;
        if (this.rightLEF) this.rightLEF.rotation.x = slatDroop;

        // Interactive HOTAS flight controls in cockpit
        if (this.hotasStick) {
          this.hotasStick.rotation.x = -pitch * 0.25;
          this.hotasStick.rotation.z = -roll * 0.25;
        }
        if (this.hotasThrottle) {
          this.hotasThrottle.position.z = 3.05 + (physics.throttle - 0.5) * 0.22;
        }

        // Dilating Nozzle Petals
        const dilation = (physics.throttle > 1.0) ? (physics.throttle - 1.0) * 0.75 : 0.0;
        for (let i = 0; i < this.nozzlePetals.length; i++) {
          this.nozzlePetals[i].rotation.x = -dilation;
        }

        // Afterburner Plume & Shock Diamonds
        const isAB = physics.throttle > 1.0;
        if (this.afterburnerPlume) {
          this.afterburnerPlume.visible = isAB;
          if (isAB) {
            const scale = 0.85 + (physics.throttle - 1.0) * 1.8 + Math.random() * 0.15;
            this.afterburnerPlume.scale.set(scale, scale, scale * 1.3);
            for (let i = 0; i < this.shockDiamonds.length; i++) {
              this.shockDiamonds[i].rotation.z += 0.2;
              this.shockDiamonds[i].scale.setScalar(0.8 + Math.random() * 0.4);
            }
          }
        }

        // Transonic Prandtl-Glauert Vapor Shock Collar
        if (this.vaporCone) {
          const m = physics.mach;
          if (m >= 0.94 && m <= 1.06) {
            const intensity = 1.0 - Math.abs(m - 1.0) / 0.06;
            this.vaporCone.material.opacity = intensity * 0.65 * (0.85 + Math.random() * 0.3);
            this.vaporCone.scale.setScalar(1.0 + (m - 0.94) * 0.8);
          } else {
            this.vaporCone.material.opacity = 0.0;
          }
        }

        // Wingtip Vortex Ribbons
        const g = Math.abs(physics.gForce);
        if (this.leftWingVortex && this.rightWingVortex) {
          if (g > 4.2 && physics.speedKnots > 200) {
            const vortexAlpha = Math.min(0.7, (g - 4.2) / 4.0);
            this.leftWingVortex.material.opacity = vortexAlpha;
            this.rightWingVortex.material.opacity = vortexAlpha;
          } else {
            this.leftWingVortex.material.opacity = 0.0;
            this.rightWingVortex.material.opacity = 0.0;
          }
        }

        // Landing gear deployment
        this.landingGearGroup.visible = physics.gearDown;
      }
    }

    // =========================================================================
    // 5. WORLD ENVIRONMENT: GERSTNER OCEAN, 2500+ TREES, AIRBASE & CARRIER FLEET
    // =========================================================================
    class WorldEnvironment {
      constructor(scene, renderer) {
        this.scene = scene;
        this.renderer = renderer;
        this.papiLights = [];
        this.targets = [];
        this.time = 0;

        this.buildLightingAndSky();
        this.buildGerstnerOcean();
        this.buildArchipelagoTerrain();
        this.buildInstancedForests();
        this.buildMilitaryAirbase();
        this.buildCarrierStrikeGroup();
        this.buildDestructibleTargets();
        this.buildAtmosphericClouds();
      }

      buildLightingAndSky() {
        // Procedural IBL Environment
        const pmrem = new THREE.PMREMGenerator(this.renderer);
        pmrem.compileEquirectangularShader();
        this.hdrSkyTex = generateHDRSkyTexture();
        this.envMap = pmrem.fromEquirectangular(this.hdrSkyTex).texture;
        this.scene.environment = this.envMap;

        // Sky Dome Sphere
        const skyGeo = new THREE.SphereGeometry(38000, 32, 16);
        const skyMat = new THREE.MeshBasicMaterial({
          map: this.hdrSkyTex,
          side: THREE.BackSide,
          depthWrite: false
        });
        this.sky = new THREE.Mesh(skyGeo, skyMat);
        this.scene.add(this.sky);

        // Sunlight
        this.sunLight = new THREE.DirectionalLight(0xfffaee, 2.6);
        this.sunLight.position.set(4000, 6000, 3000);
        this.scene.add(this.sunLight);

        // Ambient Hemisphere
        const hemiLight = new THREE.HemisphereLight(0x8cbef8, 0x182c40, 1.1);
        this.scene.add(hemiLight);

        // Atmospheric Fog
        this.scene.fog = new THREE.FogExp2(0x8cbfe8, 0.000025);
      }

      buildGerstnerOcean() {
        // Custom Trochoidal Gerstner Wave Shader
        const oceanVertexShader = `
          uniform float time;
          varying vec3 vWorldPosition;
          varying vec3 vNormal;

          vec3 gerstnerWave(vec4 wave, vec3 p, inout vec3 tangent, inout vec3 binormal) {
            float steepness = wave.z;
            float wavelength = wave.w;
            float k = 2.0 * 3.14159265 / wavelength;
            float c = sqrt(9.8 / k);
            vec2 d = normalize(wave.xy);
            float f = k * (dot(d, p.xz) - c * time);
            float a = steepness / k;

            tangent += vec3(
              -d.x * d.x * (steepness * sin(f)),
              d.x * (steepness * cos(f)),
              -d.x * d.y * (steepness * sin(f))
            );
            binormal += vec3(
              -d.x * d.y * (steepness * sin(f)),
              d.y * (steepness * cos(f)),
              -d.y * d.y * (steepness * sin(f))
            );
            return vec3(
              d.x * (a * cos(f)),
              a * sin(f),
              d.y * (a * cos(f))
            );
          }

          void main() {
            vec3 p = position;
            vec3 tangent = vec3(1.0, 0.0, 0.0);
            vec3 binormal = vec3(0.0, 0.0, 1.0);

            vec4 w1 = vec4(1.0, 0.6, 0.16, 220.0);
            vec4 w2 = vec4(-0.6, 0.8, 0.12, 110.0);
            vec4 w3 = vec4(0.4, -0.9, 0.08, 55.0);
            vec4 w4 = vec4(-0.7, -0.4, 0.05, 25.0);

            p += gerstnerWave(w1, position, tangent, binormal);
            p += gerstnerWave(w2, position, tangent, binormal);
            p += gerstnerWave(w3, position, tangent, binormal);
            p += gerstnerWave(w4, position, tangent, binormal);

            vNormal = normalize(cross(binormal, tangent));
            vec4 worldPos = modelMatrix * vec4(p, 1.0);
            vWorldPosition = worldPos.xyz;
            gl_Position = projectionMatrix * viewMatrix * worldPos;
          }
        `;

        const oceanFragmentShader = `
          uniform vec3 sunDirection;
          uniform vec3 deepColor;
          uniform vec3 shallowColor;
          uniform vec3 sunColor;
          varying vec3 vWorldPosition;
          varying vec3 vNormal;

          void main() {
            vec3 viewDir = normalize(cameraPosition - vWorldPosition);
            vec3 normal = normalize(vNormal);

            float fresnel = 0.02 + 0.98 * pow(1.0 - max(0.0, dot(viewDir, normal)), 5.0);

            vec3 halfVec = normalize(sunDirection + viewDir);
            float spec = pow(max(0.0, dot(normal, halfVec)), 260.0) * 3.8;

            vec3 waterColor = mix(deepColor, shallowColor, fresnel * 0.65);
            vec3 skyReflection = vec3(0.42, 0.68, 0.94);

            vec3 finalColor = mix(waterColor, skyReflection, fresnel) + sunColor * spec;
            gl_FragColor = vec4(finalColor, 0.94);
          }
        `;

        const oceanGeo = new THREE.PlaneGeometry(85000, 85000, 140, 140);
        oceanGeo.rotateX(-Math.PI / 2);

        this.oceanUniforms = {
          time: { value: 0.0 },
          sunDirection: { value: new THREE.Vector3(4000, 6000, 3000).normalize() },
          deepColor: { value: new THREE.Color(0x061c33) },
          shallowColor: { value: new THREE.Color(0x0a3c66) },
          sunColor: { value: new THREE.Color(0xfffae0) }
        };

        const oceanMat = new THREE.ShaderMaterial({
          vertexShader: oceanVertexShader,
          fragmentShader: oceanFragmentShader,
          uniforms: this.oceanUniforms,
          transparent: true
        });

        this.ocean = new THREE.Mesh(oceanGeo, oceanMat);
        this.ocean.position.y = 0;
        this.scene.add(this.ocean);
      }

      buildArchipelagoTerrain() {
        const segs = 110;
        const terrainGeo = new THREE.PlaneGeometry(13000, 13000, segs, segs);
        terrainGeo.rotateX(-Math.PI / 2);

        const pos = terrainGeo.attributes.position;
        const colors = [];
        const color = new THREE.Color();

        for (let i = 0; i < pos.count; i++) {
          const x = pos.getX(i);
          const z = pos.getZ(i);

          const d = Math.hypot(x, z + 2000);
          const islandMask = Math.max(0, 1.0 - Math.pow(Math.min(1.0, d / 4800), 2));

          const n1 = Math.sin(x * 0.0008) * Math.cos(z * 0.0008) * 160;
          const n2 = Math.sin(x * 0.0022 + 1.2) * Math.cos(z * 0.0022 + 0.8) * 70;
          const n3 = Math.sin(x * 0.005) * Math.cos(z * 0.005) * 25;

          const landBase = (islandMask > 0.08) ? (160 * Math.pow(islandMask, 0.75)) : -55;
          let elev = landBase + (n1 + n2 + n3) * islandMask;

          // Flatten runway airbase area
          if (Math.abs(x) < 280 && Math.abs(z + 2000) < 1850) {
            elev = 35.8;
          } else if (islandMask <= 0.08) {
            elev = -65.0; // Deep ocean seabed
          } else if (elev < 1.0) {
            elev = -35.0 * (1.0 - Math.max(0, elev / 1.0));
          }

          pos.setY(i, elev);

          if (elev < 0.5) {
            color.setHex(0x0c2540); // Seabed
          } else if (elev < 12) {
            color.setHex(0xdcc79c); // Golden sand beach
          } else if (elev < 170) {
            color.setHex(0x2d5a28); // Lush green valley
          } else if (elev < 330) {
            color.setHex(0x454e47); // Rocky granite slopes
          } else {
            color.setHex(0xf0f5fa); // Snow dusting on mountain peaks
          }
          colors.push(color.r, color.g, color.b);
        }

        terrainGeo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        terrainGeo.computeVertexNormals();

        const terrainMat = new THREE.MeshStandardMaterial({
          vertexColors: true,
          roughness: 0.90,
          metalness: 0.1
        });

        this.terrain = new THREE.Mesh(terrainGeo, terrainMat);
        this.scene.add(this.terrain);
      }

      buildInstancedForests() {
        // 2,500 Instanced 3D Trees across island valleys
        const treeCount = 2200;
        const trunkGeo = new THREE.CylinderGeometry(0.8, 1.5, 10, 5);
        trunkGeo.translate(0, 5, 0);
        const trunkMat = new THREE.MeshStandardMaterial({ color: 0x3d2716, roughness: 0.9 });

        const leavesGeo = new THREE.ConeGeometry(5.5, 16, 5);
        leavesGeo.translate(0, 16, 0);
        const leavesMat = new THREE.MeshStandardMaterial({ color: 0x1e4620, roughness: 0.8 });

        const trunkMesh = new THREE.InstancedMesh(trunkGeo, trunkMat, treeCount);
        const leavesMesh = new THREE.InstancedMesh(leavesGeo, leavesMat, treeCount);

        const dummy = new THREE.Object3D();
        let placed = 0;

        for (let i = 0; i < treeCount; i++) {
          const angle = Math.random() * Math.PI * 2;
          const r = 400 + Math.random() * 3200;
          const tx = Math.cos(angle) * r;
          const tz = -2000 + Math.sin(angle) * r;

          // Don't place on runway or taxiways
          if (Math.abs(tx) < 220 && Math.abs(tz + 2000) < 1750) continue;

          // Determine elevation
          const d = Math.hypot(tx, tz + 2000);
          const islandMask = Math.max(0, 1.0 - Math.pow(Math.min(1.0, d / 4800), 2));
          const elev = (160 * Math.pow(islandMask, 0.75)) + (Math.sin(tx * 0.001) + Math.cos(tz * 0.001)) * 30;

          if (elev > 14 && elev < 175) {
            dummy.position.set(tx, elev, tz);
            const scale = 0.8 + Math.random() * 0.5;
            dummy.scale.set(scale, scale, scale);
            dummy.rotation.y = Math.random() * Math.PI * 2;
            dummy.updateMatrix();

            trunkMesh.setMatrixAt(placed, dummy.matrix);
            leavesMesh.setMatrixAt(placed, dummy.matrix);
            placed++;
          }
        }

        trunkMesh.count = placed;
        leavesMesh.count = placed;
        trunkMesh.instanceMatrix.needsUpdate = true;
        leavesMesh.instanceMatrix.needsUpdate = true;

        this.scene.add(trunkMesh);
        this.scene.add(leavesMesh);
      }

      buildMilitaryAirbase() {
        const airbase = new THREE.Group();
        airbase.position.set(0, 36, -2000);

        // Concrete Runway (Runway 36L / 18R)
        const runway = new THREE.Mesh(
          new THREE.PlaneGeometry(160, 3200).rotateX(-Math.PI / 2),
          new THREE.MeshStandardMaterial({ color: 0x22272c, roughness: 0.75 })
        );
        airbase.add(runway);

        // Centerline stripes
        const stripeGeo = new THREE.PlaneGeometry(4, 50).rotateX(-Math.PI / 2);
        const stripeMat = new THREE.MeshBasicMaterial({ color: 0xffffff, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
        for (let z = -1400; z <= 1400; z += 90) {
          const s = new THREE.Mesh(stripeGeo, stripeMat);
          s.position.set(0, 0.15, z);
          airbase.add(s);
        }

        // Threshold Piano Keys
        const keyGeo = new THREE.PlaneGeometry(5, 75).rotateX(-Math.PI / 2);
        for (let x = -60; x <= 60; x += 15) {
          const kS = new THREE.Mesh(keyGeo, stripeMat);
          kS.position.set(x, 0.15, 1480);
          airbase.add(kS);
          const kN = new THREE.Mesh(keyGeo, stripeMat);
          kN.position.set(x, 0.15, -1480);
          airbase.add(kN);
        }

        // 4-Light Dynamic PAPI Glide Slope Indicators
        this.papiLights = [];
        for (let i = 0; i < 4; i++) {
          const pLight = new THREE.Mesh(new THREE.SphereGeometry(1.4, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
          pLight.position.set(-105 - i * 8, 2, 1450);
          airbase.add(pLight);
          this.papiLights.push(pLight);
        }

        // Taxiways and Tarmac
        const taxiway = new THREE.Mesh(
          new THREE.PlaneGeometry(70, 2600).rotateX(-Math.PI / 2),
          new THREE.MeshStandardMaterial({ color: 0x1a1e22, roughness: 0.85 })
        );
        taxiway.position.set(-135, 0.05, 0);
        airbase.add(taxiway);

        // Blue Taxiway Edge Lights
        const blueLightMat = new THREE.MeshBasicMaterial({ color: 0x0088ff });
        const blueLightGeo = new THREE.SphereGeometry(0.5, 6, 6);
        for (let z = -1200; z <= 1200; z += 120) {
          const bL = new THREE.Mesh(blueLightGeo, blueLightMat);
          bL.position.set(-175, 1, z);
          airbase.add(bL);
        }

        // Hardened Aircraft Shelters (HAS)
        const hangarMat = new THREE.MeshStandardMaterial({ color: 0x363d44, roughness: 0.7 });
        for (let h = -2; h <= 2; h++) {
          const hangar = new THREE.Mesh(new THREE.CylinderGeometry(28, 28, 65, 16, 1, false, 0, Math.PI), hangarMat);
          hangar.rotation.set(0, Math.PI / 2, Math.PI / 2);
          hangar.position.set(-220, 14, h * 180);
          airbase.add(hangar);
        }

        // Control Tower with Rotating Airport Beacon
        const tower = new THREE.Group();
        tower.position.set(150, 0, -400);
        const towerBase = new THREE.Mesh(new THREE.CylinderGeometry(14, 18, 70, 8), new THREE.MeshStandardMaterial({ color: 0xdddddd }));
        towerBase.position.y = 35;
        tower.add(towerBase);

        const cab = new THREE.Mesh(new THREE.CylinderGeometry(22, 16, 14, 8), new THREE.MeshStandardMaterial({ color: 0x223344, roughness: 0.2 }));
        cab.position.y = 74;
        tower.add(cab);

        this.beaconLight = new THREE.Mesh(new THREE.SphereGeometry(2.5, 8, 8), new THREE.MeshBasicMaterial({ color: 0x00ff88 }));
        this.beaconLight.position.set(0, 84, 0);
        tower.add(this.beaconLight);
        airbase.add(tower);

        // Long-range Air Surveillance Radar Station
        const radarStation = new THREE.Group();
        radarStation.position.set(220, 0, 300);
        const domeBase = new THREE.Mesh(new THREE.CylinderGeometry(20, 24, 25, 8), new THREE.MeshStandardMaterial({ color: 0x555e66 }));
        domeBase.position.y = 12.5;
        radarStation.add(domeBase);

        this.radarDish = new THREE.Mesh(new THREE.BoxGeometry(40, 12, 4), new THREE.MeshStandardMaterial({ color: 0xffaa00 }));
        this.radarDish.position.y = 30;
        radarStation.add(this.radarDish);
        airbase.add(radarStation);

        // Jet Fuel Storage Tanks
        const tankMat = new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.4 });
        for (let k = 0; k < 3; k++) {
          const tank = new THREE.Mesh(new THREE.CylinderGeometry(22, 22, 24, 16), tankMat);
          tank.position.set(-260, 12, -700 + k * 65);
          airbase.add(tank);
        }

        this.scene.add(airbase);
      }

      buildCarrierStrikeGroup() {
        const fleetGroup = new THREE.Group();
        fleetGroup.position.set(6500, 5, 7500); // 6 miles offshore
        fleetGroup.rotation.y = 0.55;

        // 1. CVN Supercarrier (Nimitz/Ford scale)
        const cvn = new THREE.Group();
        const hullMat = new THREE.MeshStandardMaterial({ color: 0x2b3137, roughness: 0.65 });
        const cvnHull = new THREE.Mesh(new THREE.BoxGeometry(110, 48, 760), hullMat);
        cvnHull.position.y = 22;
        cvn.add(cvnHull);

        const deckMat = new THREE.MeshStandardMaterial({ color: 0x181c20, roughness: 0.9 });
        const cvnDeck = new THREE.Mesh(new THREE.PlaneGeometry(165, 800).rotateX(-Math.PI / 2), deckMat);
        cvnDeck.position.y = 46.2;
        cvn.add(cvnDeck);

        // Angled landing strip
        const stripeMat = new THREE.MeshBasicMaterial({ color: 0xffea00 });
        const angledStripe = new THREE.Mesh(new THREE.PlaneGeometry(6, 420).rotateX(-Math.PI / 2), stripeMat);
        angledStripe.rotation.y = -0.16;
        angledStripe.position.set(-18, 46.4, 40);
        cvn.add(angledStripe);

        // 4 Arresting Gear Wires
        const wireMat = new THREE.MeshBasicMaterial({ color: 0x222222 });
        for (let w = 0; w < 4; w++) {
          const wire = new THREE.Mesh(new THREE.BoxGeometry(80, 0.4, 0.4), wireMat);
          wire.rotation.y = -0.16;
          wire.position.set(-16, 46.5, 140 + w * 28);
          cvn.add(wire);
        }

        // Catapult Tracks & Jet Blast Deflectors (JBD)
        const jbdMat = new THREE.MeshStandardMaterial({ color: 0x3a424a, roughness: 0.7 });
        const jbd1 = new THREE.Mesh(new THREE.BoxGeometry(22, 10, 2), jbdMat);
        jbd1.position.set(22, 51.0, -110);
        jbd1.rotation.x = -0.7; // Raised blast deflector
        cvn.add(jbd1);

        // Island Superstructure & Radar Mast
        const island = new THREE.Mesh(new THREE.BoxGeometry(22, 55, 120), hullMat);
        island.position.set(65, 73, 10);
        cvn.add(island);

        const mast = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 3.5, 70, 6), new THREE.MeshStandardMaterial({ color: 0x1a1e22 }));
        mast.position.set(65, 130, 10);
        cvn.add(mast);

        // Phalanx CIWS Mounts
        const ciwsMat = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
        const ciws = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 7, 8), ciwsMat);
        ciws.position.set(-70, 50, 320);
        cvn.add(ciws);

        fleetGroup.add(cvn);

        // 2. Two Arleigh Burke-Class Aegis Destroyers in Escort Formation
        const buildDDG = (x, z) => {
          const ddg = new THREE.Group();
          ddg.position.set(x, 14, z);

          const ddgHull = new THREE.Mesh(new THREE.BoxGeometry(45, 28, 380), new THREE.MeshStandardMaterial({ color: 0x384048, roughness: 0.6 }));
          ddg.add(ddgHull);

          const superstructure = new THREE.Mesh(new THREE.BoxGeometry(32, 26, 140), new THREE.MeshStandardMaterial({ color: 0x48525b }));
          superstructure.position.set(0, 20, 20);
          ddg.add(superstructure);

          // Phased Array SPY-1 Radar Face
          const radarFace = new THREE.Mesh(new THREE.BoxGeometry(16, 16, 2), new THREE.MeshStandardMaterial({ color: 0x1f2428 }));
          radarFace.rotation.x = -0.3;
          radarFace.position.set(0, 30, -50);
          ddg.add(radarFace);

          // 5-Inch Deck Gun
          const gunTurret = new THREE.Mesh(new THREE.BoxGeometry(14, 10, 18), new THREE.MeshStandardMaterial({ color: 0x22262a }));
          gunTurret.position.set(0, 18, 120);
          const gunBarrel = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 28, 8).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x111111 }));
          gunBarrel.position.set(0, 3, 16);
          gunTurret.add(gunBarrel);
          ddg.add(gunTurret);

          return ddg;
        };

        fleetGroup.add(buildDDG(-550, -400));
        fleetGroup.add(buildDDG(600, 450));

        this.scene.add(fleetGroup);
      }

      buildDestructibleTargets() {
        this.targets = [];

        // 2 Offshore Naval Drone Ships
        const dronePositions = [
          new THREE.Vector3(-3200, 6, 2800),
          new THREE.Vector3(-4200, 6, -1500)
        ];

        dronePositions.forEach((pos, idx) => {
          const droneGroup = new THREE.Group();
          droneGroup.position.copy(pos);

          const droneHull = new THREE.Mesh(new THREE.BoxGeometry(28, 14, 120), new THREE.MeshStandardMaterial({ color: 0xcc2233 }));
          droneHull.position.y = 6;
          droneGroup.add(droneHull);

          const tower = new THREE.Mesh(new THREE.BoxGeometry(18, 22, 30), new THREE.MeshStandardMaterial({ color: 0xffffff }));
          tower.position.set(0, 20, 0);
          droneGroup.add(tower);

          this.scene.add(droneGroup);
          this.targets.push({
            name: `TGT ${idx + 1}: NAVAL DRONE SHIP`,
            mesh: droneGroup,
            radius: 45,
            isHostile: true,
            destroyed: false
          });
        });

        // 3 Mountain Radar Installation Bunkers
        const bunkerPositions = [
          new THREE.Vector3(1200, 220, -3200),
          new THREE.Vector3(-1400, 240, -3400),
          new THREE.Vector3(1800, 190, -1200)
        ];

        bunkerPositions.forEach((pos, idx) => {
          const bunkerGroup = new THREE.Group();
          bunkerGroup.position.copy(pos);

          const dome = new THREE.Mesh(new THREE.SphereGeometry(30, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xeeeeee }));
          bunkerGroup.add(dome);

          const bunkerBase = new THREE.Mesh(new THREE.BoxGeometry(70, 20, 70), new THREE.MeshStandardMaterial({ color: 0x333b42 }));
          bunkerBase.position.y = -10;
          bunkerGroup.add(bunkerBase);

          this.scene.add(bunkerGroup);
          this.targets.push({
            name: `TGT ${idx + 3}: RADAR BUNKER`,
            mesh: bunkerGroup,
            radius: 42,
            isHostile: true,
            destroyed: false
          });
        });
      }

      buildAtmosphericClouds() {
        const cloudMat = new THREE.MeshStandardMaterial({
          color: 0xffffff,
          roughness: 0.95,
          metalness: 0.05
        });

        const cloudPuffGeo = new THREE.SphereGeometry(180, 8, 8);
        for (let i = 0; i < 45; i++) {
          const cloud = new THREE.Group();
          const cx = (Math.random() - 0.5) * 45000;
          const cy = 2800 + Math.random() * 3500;
          const cz = (Math.random() - 0.5) * 45000;
          cloud.position.set(cx, cy, cz);

          for (let p = 0; p < 7; p++) {
            const puff = new THREE.Mesh(cloudPuffGeo, cloudMat);
            puff.position.set(
              (Math.random() - 0.5) * 420,
              (Math.random() - 0.5) * 120,
              (Math.random() - 0.5) * 420
            );
            const s = 0.6 + Math.random() * 0.8;
            puff.scale.set(s, s * 0.6, s);
            cloud.add(puff);
          }
          this.scene.add(cloud);
        }
      }

      update(dt) {
        this.time += dt;
        if (this.oceanUniforms) {
          this.oceanUniforms.time.value = this.time;
        }

        if (this.radarDish) {
          this.radarDish.rotation.y += 0.8 * dt;
        }
        if (this.beaconLight) {
          this.beaconLight.rotation.y += 3.5 * dt;
        }
      }
    }

    // =========================================================================
    // 6. COMBAT SYSTEM: MULTI-STAGE EXPLOSIONS, WATER GEYSERS & BRASS CASINGS
    // =========================================================================
    class CombatSystem {
      constructor(scene, aircraft, world) {
        this.scene = scene;
        this.aircraft = aircraft;
        this.world = world;
        this.tracers = [];
        this.missiles = [];
        this.flares = [];
        this.explosions = [];
        this.waterGeysers = [];
        this.brassCasings = [];
        this.score = 0;

        // Composite Glowing Tracer Meshes
        this.tracerOuterGeo = new THREE.CylinderGeometry(0.32, 0.32, 16.0, 8).rotateX(Math.PI / 2);
        this.tracerOuterMat = new THREE.MeshBasicMaterial({ color: 0xff6600, transparent: true, opacity: 0.95 });
        this.tracerCoreGeo = new THREE.CylinderGeometry(0.14, 0.14, 16.4, 6).rotateX(Math.PI / 2);
        this.tracerCoreMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        this.tracerHeadGeo = new THREE.SphereGeometry(0.65, 8, 8);
        this.tracerHeadMat = new THREE.MeshBasicMaterial({ color: 0xffdd33 });

        // Spent 25mm Brass Casings
        this.brassGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.28, 6);
        this.brassMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.9, roughness: 0.2 });

        // Muzzle Flash
        this.muzzleFlash = new THREE.Mesh(
          new THREE.SphereGeometry(0.65, 8, 8),
          new THREE.MeshBasicMaterial({ color: 0xffe066, transparent: true, opacity: 0.95 })
        );
        this.muzzleFlash.visible = false;
        this.scene.add(this.muzzleFlash);
        this.muzzleFlashTimer = 0;
        this.isFiringGun = false;
        this.gunFiringTimer = 0;
        this.lastHitTime = 0;

        this.flareGeo = new THREE.SphereGeometry(0.40, 8, 8);
        this.flareMat = new THREE.MeshBasicMaterial({ color: 0xffbb22 });
      }

      fireGun() {
        sound.playGunfire();
        this.isFiringGun = true;
        this.gunFiringTimer = 0.09;

        const jetPos = this.aircraft.group.position;
        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.aircraft.group.quaternion);
        const up = new THREE.Vector3(0, 1, 0).applyQuaternion(this.aircraft.group.quaternion);
        const right = new THREE.Vector3(1, 0, 0).applyQuaternion(this.aircraft.group.quaternion);

        const gunPos = jetPos.clone()
          .add(right.clone().multiplyScalar(-1.1))
          .add(up.clone().multiplyScalar(0.48))
          .add(forward.clone().multiplyScalar(3.2));

        // Muzzle flash trigger
        this.muzzleFlash.position.copy(gunPos);
        this.muzzleFlash.visible = true;
        this.muzzleFlashTimer = 0.05;

        // Composite Incendiary Tracer Round
        const tracerGroup = new THREE.Group();
        tracerGroup.position.copy(gunPos);
        tracerGroup.add(new THREE.Mesh(this.tracerOuterGeo, this.tracerOuterMat));
        tracerGroup.add(new THREE.Mesh(this.tracerCoreGeo, this.tracerCoreMat));
        tracerGroup.add(new THREE.Mesh(this.tracerHeadGeo, this.tracerHeadMat));

        const velocity = forward.clone().multiplyScalar(1250).add(new THREE.Vector3(
          (Math.random() - 0.5) * 6,
          (Math.random() - 0.5) * 6,
          (Math.random() - 0.5) * 6
        ));

        tracerGroup.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, -1), velocity.clone().normalize());
        this.tracers.push({ mesh: tracerGroup, velocity: velocity, life: 2.5 });
        this.scene.add(tracerGroup);

        // Eject 25mm Brass Shell Casing into slipstream
        const brass = new THREE.Mesh(this.brassGeo, this.brassMat);
        brass.position.copy(gunPos).add(new THREE.Vector3(0, -0.4, -0.2));
        const brassVel = new THREE.Vector3(
          -4 - Math.random() * 3,
          -6 - Math.random() * 4,
          (Math.random() - 0.5) * 4
        ).applyQuaternion(this.aircraft.group.quaternion);

        this.brassCasings.push({ mesh: brass, velocity: brassVel, life: 1.2 });
        this.scene.add(brass);
      }

      launchMissile() {
        sound.playMissileLaunch();
        const jetPos = this.aircraft.group.position;
        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.aircraft.group.quaternion);
        const down = new THREE.Vector3(0, -1, 0).applyQuaternion(this.aircraft.group.quaternion);

        const missileMesh = this.aircraft.createAIM120Mesh();
        missileMesh.rotation.y = Math.PI;
        missileMesh.position.copy(jetPos).add(down.multiplyScalar(0.8));
        missileMesh.quaternion.copy(this.aircraft.group.quaternion);

        this.missiles.push({
          mesh: missileMesh,
          velocity: forward.clone().multiplyScalar(400),
          forward: forward,
          life: 8.0,
          ignited: false,
          ignitionTimer: 0.2
        });
        this.scene.add(missileMesh);
      }

      dispenseFlares() {
        sound.playFlare();
        const jetPos = this.aircraft.group.position;
        const backward = new THREE.Vector3(0, 0, 1).applyQuaternion(this.aircraft.group.quaternion);
        const down = new THREE.Vector3(0, -1, 0).applyQuaternion(this.aircraft.group.quaternion);

        for (let i = 0; i < 2; i++) {
          const flare = new THREE.Mesh(this.flareGeo, this.flareMat);
          const side = (i === 0) ? -1 : 1;
          const right = new THREE.Vector3(side, 0, 0).applyQuaternion(this.aircraft.group.quaternion);

          flare.position.copy(jetPos).add(down.clone().multiplyScalar(0.6)).add(right.clone().multiplyScalar(0.8));
          const vel = backward.clone().multiplyScalar(40 + Math.random() * 20)
            .add(down.clone().multiplyScalar(25 + Math.random() * 15))
            .add(right.clone().multiplyScalar(side * 20));

          this.flares.push({ mesh: flare, velocity: vel, life: 2.8 });
          this.scene.add(flare);
        }
      }

      createMultiStageExplosion(position) {
        sound.playTargetExplosion();
        const expGroup = new THREE.Group();
        expGroup.position.copy(position);

        // Flash Core
        const flash = new THREE.Mesh(
          new THREE.SphereGeometry(22, 12, 12),
          new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 1.0 })
        );
        expGroup.add(flash);

        // Turbulent Fireball Lobes
        const lobes = [];
        for (let i = 0; i < 5; i++) {
          const lobe = new THREE.Mesh(
            new THREE.SphereGeometry(14 + i * 2, 8, 8),
            new THREE.MeshBasicMaterial({ color: (i % 2 === 0) ? 0xff5500 : 0xffaa00, transparent: true, opacity: 0.9 })
          );
          lobe.position.set((Math.random() - 0.5) * 12, (Math.random() - 0.5) * 12, (Math.random() - 0.5) * 12);
          expGroup.add(lobe);
          lobes.push(lobe);
        }

        // Billowing Smoke Column
        const smoke = new THREE.Mesh(
          new THREE.SphereGeometry(16, 8, 8),
          new THREE.MeshStandardMaterial({ color: 0x181818, roughness: 0.9, transparent: true, opacity: 0.85 })
        );
        smoke.position.y = 8;
        expGroup.add(smoke);

        this.scene.add(expGroup);
        this.explosions.push({ group: expGroup, flash, lobes, smoke, age: 0, maxAge: 2.4 });
      }

      createWaterGeyser(position) {
        const geyser = new THREE.Mesh(
          new THREE.CylinderGeometry(4, 18, 55, 10),
          new THREE.MeshBasicMaterial({ color: 0xddf0ff, transparent: true, opacity: 0.85 })
        );
        geyser.position.set(position.x, 27.5, position.z);
        this.scene.add(geyser);
        this.waterGeysers.push({ mesh: geyser, age: 0, maxAge: 1.5 });
      }

      checkTargetHit(pos) {
        if (!this.world || !this.world.targets) return false;
        for (const tgt of this.world.targets) {
          if (tgt.destroyed) continue;
          if (tgt.mesh.position.distanceTo(pos) < tgt.radius) {
            tgt.destroyed = true;
            this.lastHitTime = performance.now();
            this.createMultiStageExplosion(tgt.mesh.position);
            tgt.mesh.scale.set(0.001, 0.001, 0.001);

            this.score++;
            sound.speakAlert('TARGET DESTROYED');
            const scoreEl = document.getElementById('val-score');
            if (scoreEl) scoreEl.innerText = `${this.score} / ${this.world.targets.length}`;

            const banner = document.getElementById('target-destroyed-banner');
            if (banner) {
              banner.innerText = `${tgt.name} DESTROYED! +100 PTS`;
              banner.style.display = 'block';
              setTimeout(() => { banner.style.display = 'none'; }, 2500);
            }
            return true;
          }
        }
        return false;
      }

      update(dt) {
        // Muzzle flash timer
        if (this.muzzleFlashTimer > 0) {
          this.muzzleFlashTimer -= dt;
          if (this.muzzleFlashTimer <= 0) this.muzzleFlash.visible = false;
        }
        if (this.gunFiringTimer > 0) {
          this.gunFiringTimer -= dt;
          if (this.gunFiringTimer <= 0) this.isFiringGun = false;
        }

        // Tracers update
        for (let i = this.tracers.length - 1; i >= 0; i--) {
          const tr = this.tracers[i];
          tr.life -= dt;
          tr.mesh.position.addScaledVector(tr.velocity, dt);
          tr.velocity.y -= 9.8 * dt;
          tr.mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, -1), tr.velocity.clone().normalize());

          if (this.checkTargetHit(tr.mesh.position)) {
            this.scene.remove(tr.mesh);
            this.tracers.splice(i, 1);
          } else if (tr.mesh.position.y <= 0) {
            this.createWaterGeyser(tr.mesh.position);
            this.scene.remove(tr.mesh);
            this.tracers.splice(i, 1);
          } else if (tr.life <= 0) {
            this.scene.remove(tr.mesh);
            this.tracers.splice(i, 1);
          }
        }

        // Brass casings update
        for (let i = this.brassCasings.length - 1; i >= 0; i--) {
          const b = this.brassCasings[i];
          b.life -= dt;
          b.velocity.y -= 9.8 * dt;
          b.mesh.position.addScaledVector(b.velocity, dt);
          b.mesh.rotation.x += 12 * dt;
          b.mesh.rotation.y += 8 * dt;

          if (b.life <= 0 || b.mesh.position.y <= 0) {
            this.scene.remove(b.mesh);
            this.brassCasings.splice(i, 1);
          }
        }

        // Missiles update
        for (let i = this.missiles.length - 1; i >= 0; i--) {
          const m = this.missiles[i];
          m.life -= dt;
          m.ignitionTimer -= dt;
          if (m.ignitionTimer <= 0 && !m.ignited) m.ignited = true;

          if (m.ignited) {
            m.velocity.addScaledVector(m.forward, 880 * dt);
          }
          m.mesh.position.addScaledVector(m.velocity, dt);

          if (this.checkTargetHit(m.mesh.position) || m.mesh.position.y <= 0 || m.life <= 0) {
            if (m.mesh.position.y <= 0) this.createWaterGeyser(m.mesh.position);
            this.createMultiStageExplosion(m.mesh.position);
            this.scene.remove(m.mesh);
            this.missiles.splice(i, 1);
          }
        }

        // Flares update
        for (let i = this.flares.length - 1; i >= 0; i--) {
          const fl = this.flares[i];
          fl.life -= dt;
          fl.velocity.y -= 18 * dt;
          fl.velocity.multiplyScalar(0.97);
          fl.mesh.position.addScaledVector(fl.velocity, dt);
          fl.mesh.scale.setScalar(0.8 + Math.random() * 0.7);

          if (fl.mesh.position.y <= 0 || fl.life <= 0) {
            this.scene.remove(fl.mesh);
            this.flares.splice(i, 1);
          }
        }

        // Multi-stage explosions animation
        for (let i = this.explosions.length - 1; i >= 0; i--) {
          const exp = this.explosions[i];
          exp.age += dt;
          const progress = exp.age / exp.maxAge;

          // Flash fades quickly
          exp.flash.material.opacity = Math.max(0, 1.0 - exp.age * 8.0);
          exp.flash.scale.addScalar(18 * dt);

          // Fireball expands and fades to dark smoke
          for (const lobe of exp.lobes) {
            lobe.scale.addScalar(14 * dt);
            lobe.position.y += 12 * dt;
            lobe.material.opacity = Math.max(0, 0.9 - progress * 1.1);
          }

          // Smoke pillar rises and expands
          exp.smoke.position.y += 28 * dt;
          exp.smoke.scale.addScalar(22 * dt);
          exp.smoke.material.opacity = Math.max(0, 0.85 - progress * 0.9);

          if (exp.age >= exp.maxAge) {
            this.scene.remove(exp.group);
            this.explosions.splice(i, 1);
          }
        }

        // Water geysers animation
        for (let i = this.waterGeysers.length - 1; i >= 0; i--) {
          const wg = this.waterGeysers[i];
          wg.age += dt;
          wg.mesh.scale.x += 1.8 * dt;
          wg.mesh.scale.z += 1.8 * dt;
          wg.mesh.material.opacity = Math.max(0, 0.85 - (wg.age / wg.maxAge));

          if (wg.age >= wg.maxAge) {
            this.scene.remove(wg.mesh);
            this.waterGeysers.splice(i, 1);
          }
        }
      }
    }

    // =========================================================================
    // 7. FLIGHT DYNAMICS: AERODYNAMICS, LOADS, GEAR STOL PHYSICS & VOICE CUES
    // =========================================================================
    class FlightPhysics {
      constructor(aircraft) {
        this.aircraft = aircraft;
        this.position = new THREE.Vector3(0, 1600, 2800); // 5,200 ft over runway approach
        this.quaternion = new THREE.Quaternion();
        this.velocity = new THREE.Vector3(0, 0, -235); // 457 knots forward cruise

        this.throttle = 0.85;
        this.gearDown = false;
        this.bayOpen = false;
        this.onGround = false;

        this.ammo = 180;
        this.missilesLeft = 4;
        this.flaresLeft = 24;

        this.pitchInput = 0;
        this.rollInput = 0;
        this.yawInput = 0;

        this.speedKnots = 457;
        this.mach = 0.69;
        this.altitudeFt = 5250;
        this.climbRateFpm = 0;
        this.gForce = 1.0;
        this.aoaDeg = 2.0;
        this.headingDeg = 0;
        this.yawRate = 0;

        this.alertTimer = 0;
      }

      reset() {
        this.position.set(0, 1600, 2800);
        this.quaternion.set(0, 0, 0, 1);
        this.velocity.set(0, 0, -235);
        this.throttle = 0.85;
        this.gearDown = false;
        this.bayOpen = false;
        this.onGround = false;
        this.ammo = 180;
        this.missilesLeft = 4;
        this.flaresLeft = 24;
      }

      update(dt) {
        const speed = this.velocity.length();
        this.speedKnots = speed * 1.94384;
        this.mach = this.speedKnots / 661.47;
        this.altitudeFt = this.position.y * 3.28084;
        this.climbRateFpm = this.velocity.y * 196.85;

        // Heading angle
        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.quaternion);
        let hDeg = Math.atan2(forward.x, -forward.z) * (180 / Math.PI);
        this.headingDeg = (hDeg + 360) % 360;

        // Angle of Attack (AoA)
        const localVel = this.velocity.clone().applyQuaternion(this.quaternion.clone().invert());
        this.aoaDeg = (speed > 10) ? Math.atan2(-localVel.y, -localVel.z) * (180 / Math.PI) : 0;

        // Flight surface control authority
        const dynamicPres = Math.min(1.0, speed / 120);
        const pitchRate = this.pitchInput * 1.65 * dynamicPres;
        const rollRate = this.rollInput * 2.85 * dynamicPres;
        const yawRate = this.yawInput * 0.85 * dynamicPres;
        this.yawRate = yawRate;

        // Rotational Integration
        const deltaQuat = new THREE.Quaternion();
        const euler = new THREE.Euler(pitchRate * dt, yawRate * dt, -rollRate * dt, 'YXZ');
        deltaQuat.setFromEuler(euler);
        this.quaternion.multiply(deltaQuat);

        // Forces: Thrust, Lift, Drag, Gravity
        const up = new THREE.Vector3(0, 1, 0).applyQuaternion(this.quaternion);
        const maxThrust = (this.throttle > 1.0) ? 225000 : 145000;
        const thrustForce = forward.clone().multiplyScalar(this.throttle * maxThrust);

        // Lift curve with STOL flap droop bonus
        const flapLiftBonus = this.gearDown ? 0.35 : 0.0;
        const liftCoeff = Math.sin(this.aoaDeg * Math.PI / 180) * 4.2 + 0.18 + flapLiftBonus;
        const liftMagnitude = 0.5 * 1.225 * Math.pow(speed, 2) * 42.7 * liftCoeff;
        const liftForce = up.clone().multiplyScalar(Math.max(-200000, Math.min(420000, liftMagnitude)));

        // Drag (Parasitic + Transonic wave drag + Induced drag)
        const waveDrag = (this.mach > 0.95 && this.mach < 1.15) ? 0.045 : 0.018;
        const gearDrag = this.gearDown ? 0.035 : 0.0;
        const bayDrag = this.bayOpen ? 0.025 : 0.0;
        const dragCoeff = 0.022 + waveDrag + gearDrag + bayDrag + Math.pow(liftCoeff, 2) / (Math.PI * 2.4);
        const dragForce = this.velocity.clone().normalize().multiplyScalar(-0.5 * 1.225 * Math.pow(speed, 2) * 42.7 * dragCoeff);

        const mass = 19500;
        const gravityForce = new THREE.Vector3(0, -9.81 * mass, 0);

        const totalForce = new THREE.Vector3()
          .add(thrustForce)
          .add(liftForce)
          .add(dragForce)
          .add(gravityForce);

        const accel = totalForce.clone().divideScalar(mass);
        this.velocity.addScaledVector(accel, dt);
        this.position.addScaledVector(this.velocity, dt);

        // Load factor (G-Force)
        const aeroNormal = liftForce.clone().add(thrustForce).dot(up) / (mass * 9.81);
        this.gForce = (speed > 30) ? aeroNormal : 1.0;

        // Ground collision & Runway Roll-Out
        this.onGround = false;
        if (this.position.y < 36.5) {
          if (this.gearDown && Math.abs(this.position.x) < 90 && Math.abs(this.position.z + 2000) < 1650) {
            // Safe runway landing
            this.position.y = 36.5;
            this.velocity.y = 0;
            this.velocity.multiplyScalar(0.985); // Brake friction
            this.onGround = true;
          } else {
            // Crash into terrain / water
            this.position.y = 36.0;
            this.velocity.set(0, 0, 0);
            document.getElementById('master-warning').innerText = "CRASH - PRESS (R) TO RESPAWN";
            document.getElementById('master-warning').style.display = "block";
          }
        }

        // Periodic Voice Caution Callouts
        this.alertTimer += dt;
        if (this.alertTimer > 2.8) {
          this.alertTimer = 0;
          if (this.altitudeFt < 550 && !this.onGround) {
            sound.speakAlert('ALTITUDE');
          } else if (this.gForce > 8.5) {
            sound.speakAlert('OVER G');
          }
        }

        sound.update(this.throttle, this.speedKnots);
        this.aircraft.group.position.copy(this.position);
        this.aircraft.group.quaternion.copy(this.quaternion);
        this.aircraft.updateVisuals(this, dt);
      }
    }

    // =========================================================================
    // 8. COLLIMATED HUD DISPLAY & GAU-22/A BALLISTIC GUN PIPPER
    // =========================================================================
    class HUDDisplay {
      constructor(canvasId, physics, world, combat) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.physics = physics;
        this.world = world;
        this.combat = combat;
        this.resize();
        window.addEventListener('resize', () => this.resize());
      }

      resize() {
        this.dpr = Math.min(window.devicePixelRatio || 1, 2);
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width * this.dpr;
        this.canvas.height = this.height * this.dpr;
        this.canvas.style.width = this.width + 'px';
        this.canvas.style.height = this.height + 'px';
        this.cx = this.width / 2;
        this.cy = this.height / 2;
      }

      render(cameraMode, camera) {
        const ctx = this.ctx;
        ctx.save();
        ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
        ctx.clearRect(0, 0, this.width, this.height);

        if (cameraMode === 3) {
          ctx.restore();
          return;
        }

        const isMobile = (this.width < 800 || this.height < 520);
        const hudCenterY = (cameraMode === 0) ? (isMobile ? this.cy - 20 : this.cy - 40) : this.cy;

        ctx.strokeStyle = '#00ff77';
        ctx.fillStyle = '#00ff77';
        ctx.shadowColor = 'rgba(0, 255, 119, 0.65)';
        ctx.shadowBlur = 6;
        ctx.lineWidth = 2;
        ctx.font = '14px "Share Tech Mono", monospace';

        // 1. Waterline Crosshair
        const wlWidth = isMobile ? 26 : 40;
        ctx.beginPath();
        ctx.moveTo(this.cx - wlWidth, hudCenterY);
        ctx.lineTo(this.cx - 12, hudCenterY);
        ctx.lineTo(this.cx - 12, hudCenterY + 6);
        ctx.moveTo(this.cx + 2, hudCenterY);
        ctx.arc(this.cx, hudCenterY, 2, 0, Math.PI * 2);
        ctx.moveTo(this.cx + 12, hudCenterY + 6);
        ctx.lineTo(this.cx + 12, hudCenterY);
        ctx.lineTo(this.cx + wlWidth, hudCenterY);
        ctx.stroke();

        // 2. Flight Path Marker (FPM)
        const fpmX = this.cx - this.physics.yawRate * (isMobile ? 30 : 45);
        const fpmY = hudCenterY + this.physics.aoaDeg * (isMobile ? 6 : 9);
        ctx.beginPath();
        ctx.arc(fpmX, fpmY, 8, 0, Math.PI * 2);
        ctx.moveTo(fpmX, fpmY - 8); ctx.lineTo(fpmX, fpmY - 16);
        ctx.moveTo(fpmX - 8, fpmY); ctx.lineTo(fpmX - 18, fpmY);
        ctx.moveTo(fpmX + 8, fpmY); ctx.lineTo(fpmX + 18, fpmY);
        ctx.stroke();

        // 3. Conformal Pitch Ladder
        ctx.save();
        ctx.translate(this.cx, hudCenterY);
        const euler = new THREE.Euler().setFromQuaternion(this.physics.quaternion, 'YXZ');
        const pitchDeg = euler.x * (180 / Math.PI);
        ctx.rotate(-euler.z);

        const pixelsPerDeg = isMobile ? 7.0 : 9.0;
        const horizonY = pitchDeg * pixelsPerDeg;

        for (let p = -80; p <= 80; p += 10) {
          const y = horizonY - p * pixelsPerDeg;
          if (Math.abs(y) < this.height * 0.42) {
            if (p === 0) {
              ctx.setLineDash([12, 8]);
              ctx.beginPath(); ctx.moveTo(-160, y); ctx.lineTo(160, y); ctx.stroke();
              ctx.setLineDash([]);
            } else {
              const isPos = p > 0;
              if (!isPos) ctx.setLineDash([6, 5]);
              const lw = isMobile ? 55 : 85;
              ctx.beginPath();
              ctx.moveTo(-lw, y); ctx.lineTo(-25, y); ctx.lineTo(-25, y + (isPos ? 8 : -8));
              ctx.moveTo(25, y + (isPos ? 8 : -8)); ctx.lineTo(25, y); ctx.lineTo(lw, y);
              ctx.stroke();
              ctx.setLineDash([]);
              ctx.fillText(Math.abs(p), -lw - 30, y + 5);
              ctx.fillText(Math.abs(p), lw + 10, y + 5);
            }
          }
        }
        ctx.restore();

        // 4. Heading Tape
        const tapeY = isMobile ? 45 : 65;
        const curHead = this.physics.headingDeg;
        ctx.strokeRect(this.cx - 140, tapeY - 20, 280, 28);
        ctx.beginPath();
        ctx.moveTo(this.cx, tapeY + 12); ctx.lineTo(this.cx - 5, tapeY + 19); ctx.lineTo(this.cx + 5, tapeY + 19);
        ctx.closePath();
        ctx.fill();

        for (let h = -40; h <= 40; h += 5) {
          const markH = (Math.round(curHead / 5) * 5 + h + 360) % 360;
          const delta = (markH - curHead + 540) % 360 - 180;
          const x = this.cx + delta * 9.0;
          if (x > this.cx - 135 && x < this.cx + 135) {
            const isMajor = markH % 10 === 0;
            ctx.beginPath();
            ctx.moveTo(x, tapeY - 20); ctx.lineTo(x, tapeY - (isMajor ? 8 : 13)); ctx.stroke();
            if (isMajor) {
              let t = (markH / 10).toString().padStart(2, '0');
              if (markH === 0) t = 'N';
              if (markH === 90) t = 'E';
              if (markH === 180) t = 'S';
              if (markH === 270) t = 'W';
              ctx.fillText(t, x - 6, tapeY + 2);
            }
          }
        }

        // 5. Airspeed and Altitude Boxes
        const boxOffset = isMobile ? Math.min(135, this.width * 0.32) : 240;
        const spdX = this.cx - boxOffset;
        ctx.strokeRect(spdX - 70, hudCenterY - 20, 75, 38);
        ctx.fillText(`${Math.round(this.physics.speedKnots)}`, spdX - 60, hudCenterY + 5);
        ctx.fillText(`M ${this.physics.mach.toFixed(2)}`, spdX - 60, hudCenterY + 32);

        const altX = this.cx + boxOffset;
        ctx.strokeRect(altX - 5, hudCenterY - 20, 85, 38);
        ctx.fillText(`${Math.round(this.physics.altitudeFt)}`, altX + 5, hudCenterY + 5);
        ctx.fillText(`${(this.physics.climbRateFpm > 0 ? '+' : '')}${Math.round(this.physics.climbRateFpm)}`, altX + 5, hudCenterY + 32);

        ctx.fillText(`G: ${this.physics.gForce.toFixed(1)}`, spdX - 70, hudCenterY + 70);
        ctx.fillText(`AoA: ${this.physics.aoaDeg.toFixed(1)}°`, spdX - 70, hudCenterY + 92);

        // 6. Tactical Target Boxes
        if (this.world && this.world.targets && camera) {
          const tempV = new THREE.Vector3();
          for (const tgt of this.world.targets) {
            if (tgt.destroyed) continue;
            tempV.copy(tgt.mesh.position);
            tempV.project(camera);

            if (tempV.z < 1.0) {
              const tx = (tempV.x * 0.5 + 0.5) * this.width;
              const ty = (-tempV.y * 0.5 + 0.5) * this.height;

              if (tx > 60 && tx < this.width - 60 && ty > 60 && ty < this.height - 60) {
                const distNm = (this.physics.position.distanceTo(tgt.mesh.position) / 1852).toFixed(1);
                ctx.strokeStyle = '#ff3344';
                ctx.strokeRect(tx - 18, ty - 18, 36, 36);
                ctx.fillStyle = '#ff3344';
                ctx.font = '11px "Share Tech Mono", monospace';
                ctx.fillText(`${tgt.name}`, tx - 40, ty - 24);
                ctx.fillText(`${distNm} NM`, tx - 20, ty + 30);
              }
            }
          }
        }

        // 7. Dynamic GAU-22/A Ballistic Gun Pipper
        if (camera) {
          const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.physics.quaternion);
          const gunRange = 850;
          const dropY = -0.5 * 9.8 * Math.pow(gunRange / 1250, 2);
          const gunBoreWorld = this.physics.position.clone()
            .add(forward.clone().multiplyScalar(gunRange))
            .add(new THREE.Vector3(0, dropY, 0));

          const proj = gunBoreWorld.clone().project(camera);
          if (proj.z < 1.0) {
            const gx = (proj.x * 0.5 + 0.5) * this.width;
            const gy = (-proj.y * 0.5 + 0.5) * this.height;

            const isFiring = this.combat && this.combat.isFiringGun;

            let targetLock = false;
            if (this.world && this.world.targets) {
              for (const tgt of this.world.targets) {
                if (tgt.destroyed) continue;
                const tp = tgt.mesh.position.clone().project(camera);
                if (tp.z < 1.0) {
                  const tx = (tp.x * 0.5 + 0.5) * this.width;
                  const ty = (-tp.y * 0.5 + 0.5) * this.height;
                  if (Math.hypot(tx - gx, ty - gy) < 48) {
                    targetLock = true;
                    break;
                  }
                }
              }
            }

            ctx.save();
            ctx.translate(gx, gy);

            const reticleColor = targetLock ? '#ff2222' : (isFiring ? '#ffaa00' : '#00ff88');
            ctx.strokeStyle = reticleColor;
            ctx.fillStyle = reticleColor;
            ctx.lineWidth = targetLock ? 2.8 : 2;

            const kickX = isFiring ? (Math.random() - 0.5) * 3 : 0;
            const kickY = isFiring ? (Math.random() - 0.5) * 3 : 0;
            const reticleRadius = isFiring ? 22 : 18;

            ctx.beginPath(); ctx.arc(kickX, kickY, reticleRadius, 0, Math.PI * 2); ctx.stroke();
            ctx.beginPath(); ctx.arc(kickX, kickY, 2.5, 0, Math.PI * 2); ctx.fill();

            ctx.beginPath();
            ctx.moveTo(kickX - reticleRadius - 8, kickY); ctx.lineTo(kickX - reticleRadius + 4, kickY);
            ctx.moveTo(kickX + reticleRadius - 4, kickY); ctx.lineTo(kickX + reticleRadius + 8, kickY);
            ctx.moveTo(kickX, kickY - reticleRadius - 8); ctx.lineTo(kickX, kickY - reticleRadius + 4);
            ctx.moveTo(kickX, kickY + reticleRadius - 4); ctx.lineTo(kickX, kickY + reticleRadius + 8);
            ctx.stroke();

            ctx.font = '10px "Share Tech Mono", monospace';
            const statusText = isFiring ? 'FIRING 25MM' : (targetLock ? 'SHOOT!' : 'GAU-22 RDY');
            ctx.fillText(statusText, -28, reticleRadius + 14);

            ctx.strokeStyle = 'rgba(0, 255, 119, 0.25)';
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.moveTo(0, -reticleRadius);
            ctx.lineTo(this.cx - gx, hudCenterY - gy);
            ctx.stroke();
            ctx.setLineDash([]);

            // Hitmarker confirmation
            if (this.combat && (performance.now() - this.combat.lastHitTime < 240)) {
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 3;
              ctx.beginPath();
              ctx.moveTo(-12, -12); ctx.lineTo(12, 12);
              ctx.moveTo(12, -12); ctx.lineTo(-12, 12);
              ctx.stroke();
              ctx.font = 'bold 13px "Share Tech Mono", monospace';
              ctx.fillStyle = '#ff2233';
              ctx.fillText('HIT!', 16, -6);
            }

            ctx.restore();
          }
        }

        ctx.restore();
      }
    }

    // =========================================================================
    // 9. MAIN SIMULATION CONTROLLER WITH POST-PROCESSING COMPOSER
    // =========================================================================
    class App {
      constructor() {
        this.canvas = document.getElementById('webgl-canvas');
        this.renderer = new THREE.WebGLRenderer({
          canvas: this.canvas,
          antialias: true,
          powerPreference: 'high-performance',
          logarithmicDepthBuffer: true
        });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.15;

        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.5, 50000);

        // Three.js Post-Processing EffectComposer
        this.ultraGraphics = true;
        this.composer = null;
        this.bloomPass = null;
        this.initPostProcessing();

        this.orbitControls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.orbitControls.enabled = false;
        this.orbitControls.enableDamping = true;

        this.cameraMode = 0; // 0: Chase, 1: Cockpit, 2: Flyby, 3: Orbit
        this.flybyPos = new THREE.Vector3();

        this.aircraft = new F35Aircraft();
        this.scene.add(this.aircraft.group);

        this.environment = new WorldEnvironment(this.scene, this.renderer);
        this.physics = new FlightPhysics(this.aircraft);
        this.combat = new CombatSystem(this.scene, this.aircraft, this.environment);
        this.hud = new HUDDisplay('hud-canvas', this.physics, this.environment, this.combat);

        this.keys = {};
        this.touchRoll = 0;
        this.touchPitch = 0;
        this.touchYaw = 0;
        this.touchThrottleDelta = 0;
        this.touchFiringGun = false;
        this.stickTouchId = null;

        this.gunCooldown = 0;
        this.isLaunchingMissile = false;
        this.lastTime = performance.now();
        this.frameCount = 0;

        this.domAirspeed = document.getElementById('val-airspeed');
        this.domMach = document.getElementById('val-mach');
        this.domThrottle = document.getElementById('val-throttle');
        this.domThrottleBar = document.getElementById('throttle-bar');
        this.domGForce = document.getElementById('val-gforce');
        this.domAltitude = document.getElementById('val-altitude');
        this.domVVI = document.getElementById('val-vvi');
        this.domAoA = document.getElementById('val-aoa');
        this.domAmmo = document.getElementById('val-ammo');
        this.domMissiles = document.getElementById('val-missiles');
        this.domFlares = document.getElementById('val-flares');
        this.domAudioBtn = document.getElementById('audio-toggle-btn');
        this.domBeastBtn = document.getElementById('beast-toggle-btn');
        this.domGfxBtn = document.getElementById('gfx-toggle-btn');
        this.domGearBtn = document.getElementById('gear-toggle-btn');
        this.domBayBtn = document.getElementById('bay-toggle-btn');

        this.setupEventListeners();
        this.setupUI();
        this.animate();
      }

      initPostProcessing() {
        if (typeof THREE.EffectComposer !== 'undefined' && typeof THREE.UnrealBloomPass !== 'undefined') {
          this.composer = new THREE.EffectComposer(this.renderer);
          const renderPass = new THREE.RenderPass(this.scene, this.camera);
          this.composer.addPass(renderPass);

          this.bloomPass = new THREE.UnrealBloomPass(
            new THREE.Vector2(window.innerWidth, window.innerHeight),
            1.0, // strength
            0.55, // radius
            0.82  // threshold
          );
          this.composer.addPass(this.bloomPass);
        }
      }

      setupEventListeners() {
        window.addEventListener('resize', () => {
          this.camera.aspect = window.innerWidth / window.innerHeight;
          this.camera.updateProjectionMatrix();
          this.renderer.setSize(window.innerWidth, window.innerHeight);
          if (this.composer) {
            this.composer.setSize(window.innerWidth, window.innerHeight);
            if (this.bloomPass) this.bloomPass.resolution.set(window.innerWidth, window.innerHeight);
          }
        });

        const unlockAudio = () => {
          if (!sound.ctx) {
            sound.init();
            this.domAudioBtn.innerHTML = '<span>&#128266;</span> SOUND: ON';
            this.domAudioBtn.classList.add('active');
          } else if (sound.ctx.state === 'suspended') {
            sound.ctx.resume();
          }
        };
        ['click', 'touchstart', 'touchend', 'keydown'].forEach((evt) => {
          window.addEventListener(evt, unlockAudio, { once: true, passive: true });
        });

        window.addEventListener('keydown', (e) => {
          if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {
            e.preventDefault();
          }

          this.keys[e.code] = true;

          if (!sound.ctx) {
            sound.init();
            this.domAudioBtn.innerHTML = '<span>&#128266;</span> SOUND: ON';
            this.domAudioBtn.classList.add('active');
          }

          if (e.code === 'KeyG') this.toggleGear();
          if (e.code === 'KeyB') this.toggleBay();
          if (e.code === 'KeyP') this.toggleBeastMode();
          if (e.code === 'KeyC') this.deployFlares();
          if (e.code === 'Space') this.launchMissile();
          if (e.code === 'KeyR') this.resetAircraft();
          if (e.code === 'KeyH') this.toggleHelp();
          if (e.code === 'KeyM') this.toggleAudio();
          if (e.code === 'KeyV') this.cycleCamera();
          if (e.code === 'Digit1') this.setCamera(0);
          if (e.code === 'Digit2') this.setCamera(1);
          if (e.code === 'Digit3') this.setCamera(2);
          if (e.code === 'Digit4') this.setCamera(3);
        });

        window.addEventListener('keyup', (e) => {
          this.keys[e.code] = false;
        });

        window.addEventListener('mousedown', (e) => {
          if (e.target.tagName !== 'BUTTON' && e.button === 0 && this.cameraMode !== 3) {
            this.fireGun();
          }
        });
      }

      setupUI() {
        this.domAudioBtn.addEventListener('click', () => this.toggleAudio());
        this.domBeastBtn.addEventListener('click', () => this.toggleBeastMode());
        this.domGfxBtn.addEventListener('click', () => this.toggleGraphics());
        this.domBayBtn.addEventListener('click', () => this.toggleBay());
        this.domGearBtn.addEventListener('click', () => this.toggleGear());
        document.getElementById('respawn-btn').addEventListener('click', () => this.resetAircraft());
        document.getElementById('help-btn').addEventListener('click', () => this.toggleHelp());
        document.getElementById('close-help-btn').addEventListener('click', () => this.toggleHelp());

        const camBtns = document.querySelectorAll('.camera-switcher button');
        camBtns.forEach((btn) => {
          btn.addEventListener('click', (e) => {
            const mode = parseInt(e.target.dataset.cam);
            this.setCamera(mode);
          });
        });

        document.getElementById('btn-fire-gun').addEventListener('click', () => this.fireGun());
        document.getElementById('btn-launch-missile').addEventListener('click', () => this.launchMissile());
        document.getElementById('btn-dispense-flare').addEventListener('click', () => this.deployFlares());
        document.getElementById('btn-afterburner').addEventListener('click', () => {
          this.physics.throttle = (this.physics.throttle > 1.0) ? 1.0 : 1.3;
        });

        // Virtual Flight Stick (Multi-touch with identifier)
        const stickZone = document.getElementById('touch-stick');
        const knob = document.getElementById('touch-knob');

        const updateStick = (touch) => {
          const rect = stickZone.getBoundingClientRect();
          const centerX = rect.left + rect.width / 2;
          const centerY = rect.top + rect.height / 2;
          let dx = touch.clientX - centerX;
          let dy = touch.clientY - centerY;
          const maxDist = rect.width / 2;
          const dist = Math.hypot(dx, dy);
          if (dist > maxDist) {
            dx = (dx / dist) * maxDist;
            dy = (dy / dist) * maxDist;
          }
          knob.style.transform = `translate(${dx}px, ${dy}px)`;
          this.touchRoll = dx / maxDist;
          this.touchPitch = dy / maxDist; // Pull down = pitch up
        };

        stickZone.addEventListener('touchstart', (e) => {
          e.preventDefault();
          for (let i = 0; i < e.changedTouches.length; i++) {
            if (this.stickTouchId === null) {
              this.stickTouchId = e.changedTouches[i].identifier;
              updateStick(e.changedTouches[i]);
              break;
            }
          }
        }, { passive: false });

        window.addEventListener('touchmove', (e) => {
          if (this.stickTouchId !== null) {
            for (let i = 0; i < e.changedTouches.length; i++) {
              if (e.changedTouches[i].identifier === this.stickTouchId) {
                updateStick(e.changedTouches[i]);
                break;
              }
            }
          }
        }, { passive: false });

        const releaseStick = (e) => {
          if (this.stickTouchId !== null) {
            for (let i = 0; i < e.changedTouches.length; i++) {
              if (e.changedTouches[i].identifier === this.stickTouchId) {
                this.stickTouchId = null;
                this.touchRoll = 0;
                this.touchPitch = 0;
                knob.style.transform = 'translate(0, 0)';
                break;
              }
            }
          }
        };

        window.addEventListener('touchend', releaseStick);
        window.addEventListener('touchcancel', releaseStick);

        // Throttle Buttons
        const btnThUp = document.getElementById('touch-btn-throttle-up');
        const btnThDn = document.getElementById('touch-btn-throttle-dn');

        if (btnThUp) {
          const startThUp = (e) => { e.preventDefault(); this.touchThrottleDelta = 1.0; };
          const endThUp = (e) => { e.preventDefault(); if (this.touchThrottleDelta > 0) this.touchThrottleDelta = 0; };
          btnThUp.addEventListener('touchstart', startThUp, { passive: false });
          btnThUp.addEventListener('touchend', endThUp, { passive: false });
          btnThUp.addEventListener('touchcancel', endThUp, { passive: false });
          btnThUp.addEventListener('mousedown', startThUp);
          btnThUp.addEventListener('mouseup', endThUp);
        }

        if (btnThDn) {
          const startThDn = (e) => { e.preventDefault(); this.touchThrottleDelta = -1.0; };
          const endThDn = (e) => { e.preventDefault(); if (this.touchThrottleDelta < 0) this.touchThrottleDelta = 0; };
          btnThDn.addEventListener('touchstart', startThDn, { passive: false });
          btnThDn.addEventListener('touchend', endThDn, { passive: false });
          btnThDn.addEventListener('touchcancel', endThDn, { passive: false });
          btnThDn.addEventListener('mousedown', startThDn);
          btnThDn.addEventListener('mouseup', endThDn);
        }

        // Gun Button (Continuous firing while held)
        const btnGun = document.getElementById('touch-btn-gun');
        if (btnGun) {
          const startGun = (e) => {
            e.preventDefault();
            this.touchFiringGun = true;
            this.fireGun();
          };
          const endGun = (e) => {
            e.preventDefault();
            this.touchFiringGun = false;
          };
          btnGun.addEventListener('touchstart', startGun, { passive: false });
          btnGun.addEventListener('touchend', endGun, { passive: false });
          btnGun.addEventListener('touchcancel', endGun, { passive: false });
          btnGun.addEventListener('mousedown', startGun);
          btnGun.addEventListener('mouseup', endGun);
        }

        // Missile Button
        const btnMsl = document.getElementById('touch-btn-missile');
        if (btnMsl) {
          btnMsl.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.launchMissile();
          }, { passive: false });
          btnMsl.addEventListener('click', () => this.launchMissile());
        }

        // Flare Button
        const btnFlr = document.getElementById('touch-btn-flare');
        if (btnFlr) {
          btnFlr.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.deployFlares();
          }, { passive: false });
          btnFlr.addEventListener('click', () => this.deployFlares());
        }

        // Camera Cycle Button
        const btnCam = document.getElementById('touch-btn-cam');
        if (btnCam) {
          btnCam.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.cycleCamera();
          }, { passive: false });
          btnCam.addEventListener('click', () => this.cycleCamera());
        }

        // Dismiss landscape hint
        const hintBtn = document.getElementById('close-hint-btn');
        if (hintBtn) {
          hintBtn.addEventListener('click', () => {
            const h = document.getElementById('landscape-hint');
            if (h) h.style.display = 'none';
          });
        }
      }

      toggleAudio() {
        if (!sound.ctx) {
          sound.init();
          this.domAudioBtn.innerHTML = '<span>&#128266;</span> SOUND: ON';
          this.domAudioBtn.classList.add('active');
        } else if (sound.ctx.state === 'suspended') {
          sound.ctx.resume();
          this.domAudioBtn.innerHTML = '<span>&#128266;</span> SOUND: ON';
          this.domAudioBtn.classList.add('active');
        } else {
          sound.ctx.suspend();
          this.domAudioBtn.innerHTML = '<span>&#128263;</span> SOUND: OFF';
          this.domAudioBtn.classList.remove('active');
        }
      }

      toggleBeastMode() {
        const isBeast = this.aircraft.toggleBeastMode();
        this.domBeastBtn.innerText = isBeast ? 'BEAST: ON' : 'BEAST: OFF';
        this.domBeastBtn.classList.toggle('beast-active', isBeast);
        sound.speakAlert(isBeast ? 'BEAST MODE ENGAGED' : 'STEALTH MODE');
      }

      toggleGraphics() {
        this.ultraGraphics = !this.ultraGraphics;
        this.domGfxBtn.innerText = this.ultraGraphics ? 'GFX: ULTRA' : 'GFX: BALANCED';
        this.domGfxBtn.classList.toggle('active', this.ultraGraphics);
      }

      toggleGear() {
        this.physics.gearDown = !this.physics.gearDown;
        this.domGearBtn.innerText = this.physics.gearDown ? 'GEAR: DOWN' : 'GEAR: UP';
        this.domGearBtn.classList.toggle('active', this.physics.gearDown);
      }

      toggleBay() {
        this.physics.bayOpen = !this.physics.bayOpen;
        this.domBayBtn.innerText = this.physics.bayOpen ? 'BAY: OPEN' : 'BAY: CLOSED';
        this.domBayBtn.classList.toggle('active', this.physics.bayOpen);
      }

      fireGun() {
        if (this.gunCooldown <= 0 && this.physics.ammo > 0) {
          this.combat.fireGun();
          this.physics.ammo--;
          this.gunCooldown = 0.05;
          this.domAmmo.innerText = this.physics.ammo;
        }
      }

      launchMissile() {
        if (this.physics.missilesLeft > 0 && !this.isLaunchingMissile) {
          this.isLaunchingMissile = true;
          this.physics.missilesLeft--;
          this.domMissiles.innerText = this.physics.missilesLeft;
          this.physics.bayOpen = true;

          setTimeout(() => {
            this.combat.launchMissile();
            setTimeout(() => {
              this.physics.bayOpen = false;
              this.isLaunchingMissile = false;
            }, 800);
          }, 200);
        }
      }

      deployFlares() {
        if (this.physics.flaresLeft > 0) {
          this.combat.dispenseFlares();
          this.physics.flaresLeft -= 2;
          this.domFlares.innerText = this.physics.flaresLeft;
        }
      }

      resetAircraft() {
        this.physics.reset();
        document.getElementById('master-warning').style.display = 'none';
        this.setCamera(0);
      }

      toggleHelp() {
        const modal = document.getElementById('help-modal');
        modal.classList.toggle('open');
      }

      setCamera(mode) {
        this.cameraMode = mode;
        const camBtns = document.querySelectorAll('.camera-switcher button');
        camBtns.forEach((btn, idx) => {
          btn.classList.toggle('active', idx === mode);
        });

        this.orbitControls.enabled = (mode === 3);

        // Pilot and Canopy visibility in cockpit view
        if (this.aircraft.pilotMesh) {
          this.aircraft.pilotMesh.visible = (mode !== 1);
        }
        if (this.aircraft.canopy) {
          this.aircraft.canopy.visible = (mode !== 1);
        }

        // Cockpit Acoustic Dampening
        sound.setCockpitMuffled(mode === 1);

        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.physics.quaternion);
        const up = new THREE.Vector3(0, 1, 0).applyQuaternion(this.physics.quaternion);
        const right = new THREE.Vector3(1, 0, 0).applyQuaternion(this.physics.quaternion);

        if (mode === 2) {
          this.flybyPos.copy(this.physics.position).add(forward.clone().multiplyScalar(400)).add(new THREE.Vector3(80, 25, 0));
        } else if (mode === 3) {
          this.orbitControls.target.copy(this.physics.position);
          this.camera.position.copy(this.physics.position)
            .add(forward.clone().multiplyScalar(11))
            .add(right.clone().multiplyScalar(14))
            .add(up.clone().multiplyScalar(4.2));
          this.orbitControls.update();
        }
      }

      cycleCamera() {
        const next = (this.cameraMode + 1) % 4;
        this.setCamera(next);
      }

      handleInputs(dt) {
        let pitch = this.touchPitch;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) pitch += 1.0;
        if (this.keys['KeyW'] || this.keys['ArrowUp']) pitch -= 1.0;
        this.physics.pitchInput = Math.max(-1.0, Math.min(1.0, pitch));

        let roll = this.touchRoll;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) roll -= 1.0;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) roll += 1.0;
        this.physics.rollInput = Math.max(-1.0, Math.min(1.0, roll));

        let yaw = this.touchYaw;
        if (this.keys['KeyQ']) yaw -= 1.0;
        if (this.keys['KeyE']) yaw += 1.0;
        this.physics.yawInput = yaw;

        if (this.keys['ShiftLeft'] || this.keys['ShiftRight'] || this.touchThrottleDelta > 0) {
          this.physics.throttle = Math.min(1.30, this.physics.throttle + 0.45 * dt);
        }
        if (this.keys['ControlLeft'] || this.keys['ControlRight'] || this.keys['KeyZ'] || this.touchThrottleDelta < 0) {
          this.physics.throttle = Math.max(0.0, this.physics.throttle - 0.45 * dt);
        }

        if (this.gunCooldown > 0) this.gunCooldown -= dt;
        if (this.keys['KeyF'] || this.touchFiringGun) {
          this.fireGun();
        }
      }

      updateCamera() {
        const jetPos = this.physics.position;
        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.physics.quaternion);
        const up = new THREE.Vector3(0, 1, 0).applyQuaternion(this.physics.quaternion);

        if (this.cameraMode === 0) {
          // Chase Cam
          const chaseDist = 13.5 + (this.physics.speedKnots / 700) * 5;
          const chaseHeight = 2.6 + Math.abs(this.physics.pitchInput) * 1.0;
          const targetCamPos = jetPos.clone()
            .sub(forward.clone().multiplyScalar(chaseDist))
            .add(up.clone().multiplyScalar(chaseHeight));

          this.camera.position.lerp(targetCamPos, 0.16);
          const lookTarget = jetPos.clone().add(forward.clone().multiplyScalar(30)).add(up.clone().multiplyScalar(0.6));
          this.camera.lookAt(lookTarget);

        } else if (this.cameraMode === 1) {
          // Cockpit / HMDS Cam
          const cockpitPos = jetPos.clone()
            .add(up.clone().multiplyScalar(1.02))
            .add(forward.clone().multiplyScalar(4.0));
          this.camera.position.copy(cockpitPos);
          const lookTarget = cockpitPos.clone().add(forward.clone().multiplyScalar(200)).add(up.clone().multiplyScalar(-0.02));
          this.camera.lookAt(lookTarget);

        } else if (this.cameraMode === 2) {
          // Flyby Cam
          this.camera.position.copy(this.flybyPos);
          this.camera.lookAt(jetPos);

        } else if (this.cameraMode === 3) {
          // Free Orbit Cam
          const prevTarget = this.orbitControls.target.clone();
          this.orbitControls.target.copy(jetPos);
          const delta = jetPos.clone().sub(prevTarget);
          this.camera.position.add(delta);
          this.orbitControls.update();
        }
      }

      updateGForceOverlay() {
        const overlay = document.getElementById('g-overlay');
        const g = this.physics.gForce;
        if (g > 5.5) {
          const blackIntensity = Math.min((g - 5.5) / 3.5, 0.95);
          overlay.style.background = `radial-gradient(circle, transparent 40%, rgba(0,0,0,${blackIntensity}) 90%)`;
        } else if (g < -1.5) {
          const redIntensity = Math.min(Math.abs(g + 1.5) / 2.5, 0.85);
          overlay.style.background = `radial-gradient(circle, transparent 40%, rgba(255,0,0,${redIntensity}) 90%)`;
        } else {
          overlay.style.background = 'transparent';
        }
      }

      animate() {
        requestAnimationFrame(() => this.animate());

        const now = performance.now();
        const dt = Math.min((now - this.lastTime) / 1000, 0.1);
        this.lastTime = now;

        this.handleInputs(dt);
        this.physics.update(dt);
        this.combat.update(dt);
        this.environment.update(dt);

        this.aircraft.pcd.update(this.physics, this.environment.targets, this.aircraft.beastMode);
        this.updateCamera();
        this.updateGForceOverlay();

        // Render via EffectComposer (HDR Bloom) or standard WebGLRenderer
        if (this.ultraGraphics && this.composer) {
          this.composer.render();
        } else {
          this.renderer.render(this.scene, this.camera);
        }

        this.hud.render(this.cameraMode, this.camera);

        // Throttle UI Updates (15 Hz)
        this.frameCount++;
        if (this.frameCount % 4 === 0) {
          this.domAirspeed.innerText = `${Math.round(this.physics.speedKnots)} KTS`;
          this.domMach.innerText = `M ${this.physics.mach.toFixed(2)}`;
          this.domThrottle.innerText = `${Math.round(this.physics.throttle * 100)} %`;
          this.domThrottleBar.style.width = `${Math.min(100, this.physics.throttle * 77)}%`;
          this.domGForce.innerText = `${(this.physics.gForce > 0 ? '+' : '')}${this.physics.gForce.toFixed(1)} G`;
          this.domAltitude.innerText = `${Math.round(this.physics.altitudeFt).toLocaleString()} FT`;
          this.domVVI.innerText = `${(this.physics.climbRateFpm > 0 ? '+' : '')}${Math.round(this.physics.climbRateFpm)} FPM`;
          this.domAoA.innerText = `${this.physics.aoaDeg.toFixed(1)} DEG`;
        }
      }
    }

    // Launch simulation on DOM load
    window.addEventListener('DOMContentLoaded', () => {
      window.simulationApp = new App();
    });
  </script>
</body>
</html>
""")

print("Successfully generated ultra high-fidelity simulation: " + output_path)
'''

with open(r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\build_simulation.py", "w", encoding="utf-8") as f:
    f.write(script_content)

print("Updated build_simulation.py with full ultra visual and plane upgrade architecture.")


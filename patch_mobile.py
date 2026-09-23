import os

build_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\build_simulation.py"

with open(build_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Global CSS to add touch-action: none and overscroll-behavior
old_global_css = """    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #02060a;
      font-family: 'Rajdhani', sans-serif;
      color: #e0f0ea;
    }"""

new_global_css = """    * {
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
      background: #02060a;
      font-family: 'Rajdhani', sans-serif;
      color: #e0f0ea;
      touch-action: none;
      overscroll-behavior: none;
    }"""

assert old_global_css in content, "old_global_css not found"
content = content.replace(old_global_css, new_global_css, 1)

# 2. Update Mobile Controls CSS
old_mobile_css = """    .mobile-controls {
      display: none;
      position: absolute;
      bottom: 75px;
      left: 20px;
      right: 20px;
      justify-content: space-between;
      pointer-events: none;
      z-index: 20;
    }

    .touch-stick-zone {
      width: 120px;
      height: 120px;
      background: rgba(0, 255, 119, 0.08);
      border: 2px dashed rgba(0, 255, 119, 0.4);
      border-radius: 50%;
      pointer-events: auto;
      position: relative;
    }

    .touch-knob {
      width: 44px;
      height: 44px;
      background: var(--hud-green);
      border-radius: 50%;
      position: absolute;
      top: calc(50% - 22px);
      left: calc(50% - 22px);
      box-shadow: 0 0 10px var(--hud-green);
      pointer-events: none;
    }

    .mobile-action-buttons {
      display: flex;
      flex-direction: column;
      gap: 12px;
      pointer-events: auto;
    }

    .touch-round-btn {
      width: 54px;
      height: 54px;
      border-radius: 50%;
      background: rgba(14, 25, 34, 0.9);
      border: 2px solid var(--hud-green);
      color: #fff;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 12px rgba(0, 255, 119, 0.3);
    }

    @media (max-width: 900px) {
      .mobile-controls { display: flex; }
      .side-gauge-cluster { min-width: 130px; padding: 8px 10px; }
      .gauge-value { font-size: 16px; }
      .top-bar { padding: 6px 10px; }
      .aircraft-badge { font-size: 15px; }
    }"""

new_mobile_css = """    .mobile-controls {
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
      transition: box-shadow 0.1s ease;
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

    .touch-round-btn.primary-msl:active {
      background: rgba(0, 229, 255, 0.35);
      transform: scale(0.93);
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

    @media (orientation: portrait) and (max-width: 900px) {
      .landscape-hint { display: flex; }
    }

    @media (max-width: 900px), (max-height: 520px) {
      .bottom-bar { display: none !important; }
      .side-gauge-cluster { display: none !important; }
      .mobile-controls { display: flex !important; }
      .top-bar {
        padding: 4px 8px;
        gap: 6px;
      }
      .aircraft-badge {
        font-size: 13px;
      }
      .badge-tag, .flight-status {
        display: none !important;
      }
      .top-controls {
        gap: 4px;
      }
      .hud-btn {
        padding: 4px 7px;
        font-size: 11px;
      }
    }"""

assert old_mobile_css in content, "old_mobile_css not found"
content = content.replace(old_mobile_css, new_mobile_css, 1)

# 3. Update HTML for Mobile Controls and Landscape Hint
old_mobile_html = """  <div class="mobile-controls">
    <div class="touch-stick-zone" id="touch-stick">
      <div class="touch-knob" id="touch-knob"></div>
    </div>
    <div class="mobile-action-buttons">
      <button class="touch-round-btn" id="touch-btn-gun">GUN</button>
      <button class="touch-round-btn" id="touch-btn-missile">MSL</button>
      <button class="touch-round-btn" id="touch-btn-flare">FLR</button>
    </div>
  </div>"""

new_mobile_html = """  <div id="landscape-hint" class="landscape-hint">
    <span>&#128260; ROTATE PHONE TO LANDSCAPE FOR BEST FLIGHT CONTROLS</span>
    <button id="close-hint-btn">&times;</button>
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
  </div>"""

assert old_mobile_html in content, "old_mobile_html not found"
content = content.replace(old_mobile_html, new_mobile_html, 1)

# 4. Update HUDDisplay responsive calculations for mobile screens
old_hud_render = """        const hudCenterY = (cameraMode === 0) ? this.cy - 40 : this.cy;

        // 1. Waterline Crosshair
        ctx.beginPath();
        ctx.moveTo(this.cx - 40, hudCenterY);
        ctx.lineTo(this.cx - 15, hudCenterY);
        ctx.lineTo(this.cx - 15, hudCenterY + 8);
        ctx.moveTo(this.cx + 2, hudCenterY);
        ctx.arc(this.cx, hudCenterY, 2, 0, Math.PI * 2);
        ctx.moveTo(this.cx + 15, hudCenterY + 8);
        ctx.lineTo(this.cx + 15, hudCenterY);
        ctx.lineTo(this.cx + 40, hudCenterY);
        ctx.stroke();

        // 2. Velocity Vector / Flight Path Marker (FPM)
        const fpmX = this.cx - this.physics.yawRate * 45;
        const fpmY = hudCenterY + this.physics.aoaDeg * 9;"""

new_hud_render = """        const isMobile = (this.width < 800 || this.height < 520);
        const hudCenterY = (cameraMode === 0) ? (isMobile ? this.cy - 20 : this.cy - 40) : this.cy;

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

        // 2. Velocity Vector / Flight Path Marker (FPM)
        const fpmScale = isMobile ? 6 : 9;
        const fpmX = this.cx - this.physics.yawRate * (isMobile ? 30 : 45);
        const fpmY = hudCenterY + this.physics.aoaDeg * fpmScale;"""

assert old_hud_render in content, "old_hud_render not found"
content = content.replace(old_hud_render, new_hud_render, 1)

# 5. Update Airspeed and Altitude boxes for mobile screen widths
old_hud_boxes = """        // 5. Airspeed & Altitude Ladders
        const spdX = this.cx - 240;
        ctx.strokeRect(spdX - 70, hudCenterY - 20, 80, 40);
        ctx.fillText(`${Math.round(this.physics.speedKnots)}`, spdX - 55, hudCenterY + 6);
        ctx.fillText(`M ${this.physics.mach.toFixed(2)}`, spdX - 55, hudCenterY + 35);

        const altX = this.cx + 240;
        ctx.strokeRect(altX - 10, hudCenterY - 20, 95, 40);
        ctx.fillText(`${Math.round(this.physics.altitudeFt)}`, altX + 5, hudCenterY + 6);
        ctx.fillText(`${(this.physics.climbRateFpm > 0 ? '+' : '')}${Math.round(this.physics.climbRateFpm)}`, altX + 5, hudCenterY + 35);

        ctx.fillText(`G: ${this.physics.gForce.toFixed(1)}`, this.cx - 240, hudCenterY + 80);
        ctx.fillText(`AoA: ${this.physics.aoaDeg.toFixed(1)}°`, this.cx - 240, hudCenterY + 105);"""

new_hud_boxes = """        // 5. Airspeed & Altitude Ladders (Auto-spaced for mobile and desktop)
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
        ctx.fillText(`AoA: ${this.physics.aoaDeg.toFixed(1)}°`, spdX - 70, hudCenterY + 92);"""

assert old_hud_boxes in content, "old_hud_boxes not found"
content = content.replace(old_hud_boxes, new_hud_boxes, 1)

# 6. Update App constructor to add touch state
old_app_ctor = """        this.keys = {};
        this.gunCooldown = 0;
        this.isLaunchingMissile = false;
        this.lastTime = performance.now();
        this.frameCount = 0;"""

new_app_ctor = """        this.keys = {};
        this.touchRoll = 0;
        this.touchPitch = 0;
        this.touchYaw = 0;
        this.touchThrottleDelta = 0;
        this.touchFiringGun = false;
        this.stickTouchId = null;

        this.gunCooldown = 0;
        this.isLaunchingMissile = false;
        this.lastTime = performance.now();
        this.frameCount = 0;"""

assert old_app_ctor in content, "old_app_ctor not found"
content = content.replace(old_app_ctor, new_app_ctor, 1)

# 7. Update handleInputs to combine keyboard and touch inputs
old_handle_inputs = """      handleInputs(dt) {
        let pitch = 0;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) pitch += 1.0;
        if (this.keys['KeyW'] || this.keys['ArrowUp']) pitch -= 1.0;
        this.physics.pitchInput = pitch;

        let roll = 0;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) roll -= 1.0;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) roll += 1.0;
        this.physics.rollInput = roll;

        let yaw = 0;
        if (this.keys['KeyQ']) yaw -= 1.0;
        if (this.keys['KeyE']) yaw += 1.0;
        this.physics.yawInput = yaw;

        if (this.keys['ShiftLeft'] || this.keys['ShiftRight']) {
          this.physics.throttle = Math.min(1.30, this.physics.throttle + 0.35 * dt);
        }
        if (this.keys['ControlLeft'] || this.keys['ControlRight'] || this.keys['KeyZ']) {
          this.physics.throttle = Math.max(0.0, this.physics.throttle - 0.35 * dt);
        }

        if (this.gunCooldown > 0) this.gunCooldown -= dt;
        if (this.keys['KeyF']) {
          this.fireGun();
        }
      }"""

new_handle_inputs = """      handleInputs(dt) {
        // Integrate keyboard + persistent mobile touch stick
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

        // Throttle control via keyboard OR mobile throttle buttons
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
      }"""

assert old_handle_inputs in content, "old_handle_inputs not found"
content = content.replace(old_handle_inputs, new_handle_inputs, 1)

# 8. Update setupUI touch handling with multi-touch tracking and throttle/gun/msl
old_stick_ui = """        const stickZone = document.getElementById('touch-stick');
        const knob = document.getElementById('touch-knob');
        let stickActive = false;

        const handleStick = (touch) => {
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
          this.physics.rollInput = dx / maxDist;
          this.physics.pitchInput = dy / maxDist;
        };

        stickZone.addEventListener('touchstart', (e) => {
          stickActive = true;
          handleStick(e.touches[0]);
        });
        window.addEventListener('touchmove', (e) => {
          if (stickActive) handleStick(e.touches[0]);
        });
        window.addEventListener('touchend', () => {
          stickActive = false;
          knob.style.transform = 'translate(0, 0)';
          this.physics.rollInput = 0;
          this.physics.pitchInput = 0;
        });

        document.getElementById('touch-btn-gun').addEventListener('click', () => this.fireGun());
        document.getElementById('touch-btn-missile').addEventListener('click', () => this.launchMissile());
        document.getElementById('touch-btn-flare').addEventListener('click', () => this.deployFlares());"""

new_stick_ui = """        // --- Multi-Touch Virtual Joystick Engine ---
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

          // Flight controls:
          // dx > 0 = Roll Right (+1), dx < 0 = Roll Left (-1)
          // dy > 0 = Pull stick back = Pitch UP (+1)
          // dy < 0 = Push stick forward = Pitch DOWN (-1)
          this.touchRoll = dx / maxDist;
          this.touchPitch = dy / maxDist;
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

        // Throttle Buttons (Hold to adjust engine thrust)
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

        // Camera Cycle Button for Mobile
        const btnCam = document.getElementById('touch-btn-cam');
        if (btnCam) {
          btnCam.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.cycleCamera();
          }, { passive: false });
          btnCam.addEventListener('click', () => this.cycleCamera());
        }

        // Close landscape hint
        const hintBtn = document.getElementById('close-hint-btn');
        if (hintBtn) {
          hintBtn.addEventListener('click', () => {
            const h = document.getElementById('landscape-hint');
            if (h) h.style.display = 'none';
          });
        }"""

assert old_stick_ui in content, "old_stick_ui not found"
content = content.replace(old_stick_ui, new_stick_ui, 1)

# 9. Audio unlock on any mobile touch
old_audio_listener = """        ['click', 'touchstart', 'keydown'].forEach((evt) => {
          window.addEventListener(evt, () => {
            if (sound.ctx && sound.ctx.state === 'suspended') sound.ctx.resume();
          }, { once: true });
        });"""

new_audio_listener = """        const unlockAudio = () => {
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
        });"""

assert old_audio_listener in content, "old_audio_listener not found"
content = content.replace(old_audio_listener, new_audio_listener, 1)

with open(build_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("patch_mobile.py: Applied all mobile responsive & multi-touch fixes successfully.")


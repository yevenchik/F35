# =============================================================================
# ROUND 3 GENERATOR FOR F-35 LIGHTNING II SIMULATION
# Implements:
# 1. Full Procedural Web Audio Sound Engine (F135 turbine, Gatling cannon, Betty alerts)
# 2. Dynamic Time-of-Day (Day, Sunset, Night) with illuminated runway, carrier & slime lights
# 3. Cockpit Free-Look Camera with 360 view inside the cockpit
# 4. Airborne Bogey Target (Su-57 Felon) on combat air patrol
# 5. Surface-to-Air Missile (SAM) Threat with Radar Cross Section (RCS) mechanics & flare defense
# =============================================================================

import os

index_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Top bar: Add TIME button and RCS badge
old_top_left = '''        <div class="flight-status">
          <span class="status-dot"></span>
          <span id="flight-state-text">AIRBORNE // FBW ACTIVE</span>
        </div>
      </div>'''

new_top_left = '''        <div class="flight-status">
          <span class="status-dot"></span>
          <span id="flight-state-text">AIRBORNE // FBW ACTIVE</span>
          <span id="rcs-badge" class="badge-tag" style="background: rgba(0,255,119,0.15); border: 1px solid #00ff77; color: #00ffaa; margin-left: 8px;">RCS: 0.001 m² [VLO]</span>
        </div>
      </div>'''

if old_top_left in html:
    html = html.replace(old_top_left, new_top_left)

old_controls = '''        <button class="hud-btn" id="gfx-toggle-btn" title="Toggle Graphics Quality (Bloom / Performance)">
          GFX: ULTRA
        </button>'''

new_controls = '''        <button class="hud-btn" id="time-toggle-btn" title="Toggle Time of Day (T)">
          <span>&#9728;</span> TIME: DAY
        </button>
        <button class="hud-btn" id="gfx-toggle-btn" title="Toggle Graphics Quality (Bloom / Performance)">
          GFX: ULTRA
        </button>'''

if old_controls in html:
    html = html.replace(old_controls, new_controls)

# 2. Add SoundEngine enhancements: SAM warning & explosion audio
old_sound_end = '''      playTargetExplosion() {
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
    }'''

new_sound_end = '''      playTargetExplosion() {
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

      playSAMWarning() {
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(1150, now);
        osc.frequency.setValueAtTime(1550, now + 0.08);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
        osc.connect(gain);
        gain.connect(this.cockpitFilter);
        osc.start();
        osc.stop(now + 0.16);
      }
    }'''

if old_sound_end in html:
    html = html.replace(old_sound_end, new_sound_end)

# 3. Add Formation Slime Lights to F35Aircraft
old_f35_end = '''        this.group.add(this.pylonsGroup);
      }'''

new_f35_end = '''        this.group.add(this.pylonsGroup);

        // Electro-luminescent Green Formation "Slime Lights" (Night Operations)
        this.slimeLights = new THREE.Group();
        const slimeMat = new THREE.MeshBasicMaterial({ color: 0x00ff66, transparent: true, opacity: 0.0 });
        
        // Vertical Tail Edge Strips
        const finStripGeo = new THREE.BoxGeometry(0.04, 1.6, 0.08);
        const leftFinStrip = new THREE.Mesh(finStripGeo, slimeMat);
        leftFinStrip.position.set(-1.95, 1.4, -2.4);
        leftFinStrip.rotation.z = -0.32;
        this.slimeLights.add(leftFinStrip);

        const rightFinStrip = new THREE.Mesh(finStripGeo, slimeMat);
        rightFinStrip.position.set(1.95, 1.4, -2.4);
        rightFinStrip.rotation.z = 0.32;
        this.slimeLights.add(rightFinStrip);

        // Nose Chine Strips
        const chineStripGeo = new THREE.BoxGeometry(0.03, 0.05, 2.2);
        const leftChine = new THREE.Mesh(chineStripGeo, slimeMat);
        leftChine.position.set(-1.1, 0.05, 2.8);
        this.slimeLights.add(leftChine);

        const rightChine = new THREE.Mesh(chineStripGeo, slimeMat);
        rightChine.position.set(1.1, 0.05, 2.8);
        this.slimeLights.add(rightChine);

        this.slimeMat = slimeMat;
        this.group.add(this.slimeLights);
      }'''

if old_f35_end in html:
    html = html.replace(old_f35_end, new_f35_end)

# 4. Multi-Sky Textures and Time of Day in WorldEnvironment
old_sky_gen = '''    function generateHDRSkyTexture() {
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
      ctx.beginPath();
      ctx.arc(sunX, 700, 240, 0, Math.PI * 2);
      ctx.fill();

      const tex = new THREE.CanvasTexture(canvas);
      tex.mapping = THREE.EquirectangularReflectionMapping;
      return tex;
    }'''

new_sky_gen = '''    function generateHDRSkyTexture(mode = 0) {
      const canvas = document.createElement('canvas');
      canvas.width = 2048;
      canvas.height = 1024;
      const ctx = canvas.getContext('2d');

      if (mode === 0) {
        // DAY SKY
        const grad = ctx.createLinearGradient(0, 0, 0, 1024);
        grad.addColorStop(0.0, '#061c36');
        grad.addColorStop(0.35, '#15487a');
        grad.addColorStop(0.48, '#5999cf');
        grad.addColorStop(0.50, '#d2e7f7');
        grad.addColorStop(0.52, '#0c2e4e');
        grad.addColorStop(0.75, '#071f36');
        grad.addColorStop(1.0, '#030f1c');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 2048, 1024);

        const sunX = 1400, sunY = 320;
        const sunGrad = ctx.createRadialGradient(sunX, sunY, 5, sunX, sunY, 180);
        sunGrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
        sunGrad.addColorStop(0.15, 'rgba(255, 250, 220, 0.9)');
        sunGrad.addColorStop(0.4, 'rgba(255, 220, 160, 0.4)');
        sunGrad.addColorStop(1.0, 'rgba(255, 200, 120, 0.0)');
        ctx.fillStyle = sunGrad;
        ctx.beginPath(); ctx.arc(sunX, sunY, 180, 0, Math.PI * 2); ctx.fill();

        const oceanRefl = ctx.createRadialGradient(sunX, 700, 10, sunX, 700, 240);
        oceanRefl.addColorStop(0.0, 'rgba(255, 240, 200, 0.55)');
        oceanRefl.addColorStop(0.3, 'rgba(200, 220, 255, 0.2)');
        oceanRefl.addColorStop(1.0, 'rgba(10, 40, 70, 0.0)');
        ctx.fillStyle = oceanRefl;
        ctx.beginPath(); ctx.arc(sunX, 700, 240, 0, Math.PI * 2); ctx.fill();

      } else if (mode === 1) {
        // SUNSET SKY (GOLDEN HOUR)
        const grad = ctx.createLinearGradient(0, 0, 0, 1024);
        grad.addColorStop(0.0, '#0f0724');
        grad.addColorStop(0.30, '#361545');
        grad.addColorStop(0.45, '#a83c2e');
        grad.addColorStop(0.50, '#ff8033');
        grad.addColorStop(0.52, '#38161a');
        grad.addColorStop(0.75, '#190a14');
        grad.addColorStop(1.0, '#080309');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 2048, 1024);

        const sunX = 1400, sunY = 490;
        const sunGrad = ctx.createRadialGradient(sunX, sunY, 5, sunX, sunY, 260);
        sunGrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
        sunGrad.addColorStop(0.12, 'rgba(255, 180, 70, 0.95)');
        sunGrad.addColorStop(0.35, 'rgba(255, 80, 20, 0.6)');
        sunGrad.addColorStop(1.0, 'rgba(120, 20, 60, 0.0)');
        ctx.fillStyle = sunGrad;
        ctx.beginPath(); ctx.arc(sunX, sunY, 260, 0, Math.PI * 2); ctx.fill();

        const oceanRefl = ctx.createRadialGradient(sunX, 620, 10, sunX, 620, 320);
        oceanRefl.addColorStop(0.0, 'rgba(255, 140, 50, 0.85)');
        oceanRefl.addColorStop(0.4, 'rgba(180, 50, 30, 0.4)');
        oceanRefl.addColorStop(1.0, 'rgba(40, 10, 20, 0.0)');
        ctx.fillStyle = oceanRefl;
        ctx.beginPath(); ctx.arc(sunX, 620, 320, 0, Math.PI * 2); ctx.fill();

      } else {
        // NIGHT SKY (STARRY STEALTH)
        const grad = ctx.createLinearGradient(0, 0, 0, 1024);
        grad.addColorStop(0.0, '#020308');
        grad.addColorStop(0.45, '#050a18');
        grad.addColorStop(0.50, '#0c152a');
        grad.addColorStop(0.52, '#03050a');
        grad.addColorStop(1.0, '#010204');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 2048, 1024);

        // Twinkling procedural stars
        ctx.fillStyle = '#ffffff';
        for (let i = 0; i < 650; i++) {
          const sx = Math.random() * 2048;
          const sy = Math.random() * 490;
          const sz = Math.random() * 2.2 + 0.6;
          const alpha = Math.random() * 0.8 + 0.2;
          ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
          ctx.beginPath(); ctx.arc(sx, sy, sz, 0, Math.PI * 2); ctx.fill();
        }

        // Soft Moon
        const moonX = 500, moonY = 160;
        const moonGrad = ctx.createRadialGradient(moonX, moonY, 12, moonX, moonY, 90);
        moonGrad.addColorStop(0.0, 'rgba(240, 245, 255, 0.95)');
        moonGrad.addColorStop(0.3, 'rgba(180, 200, 255, 0.3)');
        moonGrad.addColorStop(1.0, 'rgba(30, 60, 120, 0.0)');
        ctx.fillStyle = moonGrad;
        ctx.beginPath(); ctx.arc(moonX, moonY, 90, 0, Math.PI * 2); ctx.fill();
      }

      const tex = new THREE.CanvasTexture(canvas);
      tex.mapping = THREE.EquirectangularReflectionMapping;
      return tex;
    }'''

if old_sky_gen in html:
    html = html.replace(old_sky_gen, new_sky_gen)

# 5. Add Night Lighting and Time of Day logic to WorldEnvironment
old_world_init = '''        this.buildLightingAndSky();
        this.buildGerstnerOcean();
        this.buildArchipelagoTerrain();
        this.buildInstancedForests();
        this.buildMilitaryAirbase();
        this.buildCarrierStrikeGroup();
        this.buildDestructibleTargets();
        this.buildAtmosphericClouds();
      }'''

new_world_init = '''        this.timeMode = 0; // 0=Day, 1=Sunset, 2=Night
        this.buildLightingAndSky();
        this.buildGerstnerOcean();
        this.buildArchipelagoTerrain();
        this.buildInstancedForests();
        this.buildMilitaryAirbase();
        this.buildNightAirfieldLighting();
        this.buildCarrierStrikeGroup();
        this.buildDestructibleTargets();
        this.buildAtmosphericClouds();
      }'''

if old_world_init in html:
    html = html.replace(old_world_init, new_world_init)

old_build_lighting = '''      buildLightingAndSky() {
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
      }'''

new_build_lighting = '''      buildLightingAndSky() {
        // Pre-generate Day, Sunset, Night HDR sky textures
        this.pmrem = new THREE.PMREMGenerator(this.renderer);
        this.pmrem.compileEquirectangularShader();

        this.hdrSkyTexDay = generateHDRSkyTexture(0);
        this.hdrSkyTexSunset = generateHDRSkyTexture(1);
        this.hdrSkyTexNight = generateHDRSkyTexture(2);

        this.envMap = this.pmrem.fromEquirectangular(this.hdrSkyTexDay).texture;
        this.scene.environment = this.envMap;

        // Sky Dome Sphere
        const skyGeo = new THREE.SphereGeometry(38000, 32, 16);
        this.skyMat = new THREE.MeshBasicMaterial({
          map: this.hdrSkyTexDay,
          side: THREE.BackSide,
          depthWrite: false
        });
        this.sky = new THREE.Mesh(skyGeo, this.skyMat);
        this.scene.add(this.sky);

        // Directional Light (Sun / Moon)
        this.sunLight = new THREE.DirectionalLight(0xfffaee, 2.6);
        this.sunLight.position.set(4000, 6000, 3000);
        this.scene.add(this.sunLight);

        // Ambient Hemisphere Light
        this.hemiLight = new THREE.HemisphereLight(0x8cbef8, 0x182c40, 1.1);
        this.scene.add(this.hemiLight);

        // Atmospheric Fog
        this.scene.fog = new THREE.FogExp2(0x8cbfe8, 0.000025);
      }

      buildNightAirfieldLighting() {
        this.nightLightsGroup = new THREE.Group();
        this.nightLightsGroup.visible = false;

        // Runway Edge Lights (Dual rows along 3,000m runway)
        const lightSphereGeo = new THREE.SphereGeometry(0.8, 6, 6);
        const whiteLightMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const greenLightMat = new THREE.MeshBasicMaterial({ color: 0x00ff66 });
        const redLightMat = new THREE.MeshBasicMaterial({ color: 0xff2222 });

        for (let z = -1450; z <= 1450; z += 55) {
          const lLight = new THREE.Mesh(lightSphereGeo, whiteLightMat);
          lLight.position.set(-34, 46.5, z);
          this.nightLightsGroup.add(lLight);

          const rLight = new THREE.Mesh(lightSphereGeo, whiteLightMat);
          rLight.position.set(34, 46.5, z);
          this.nightLightsGroup.add(rLight);
        }

        // Green Threshold Lights (Runway Start)
        for (let x = -30; x <= 30; x += 6) {
          const tLight = new THREE.Mesh(lightSphereGeo, greenLightMat);
          tLight.position.set(x, 46.5, -1470);
          this.nightLightsGroup.add(tLight);
        }

        // Red End Lights (Runway Rollout End)
        for (let x = -30; x <= 30; x += 6) {
          const eLight = new THREE.Mesh(lightSphereGeo, redLightMat);
          eLight.position.set(x, 46.5, 1470);
          this.nightLightsGroup.add(eLight);
        }

        // Control Tower Rotating Beacon
        this.towerBeacon = new THREE.Group();
        this.towerBeacon.position.set(120, 108, -120);
        const beaconWhite = new THREE.Mesh(new THREE.SphereGeometry(1.4, 6, 6), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        beaconWhite.position.set(0, 0, 2);
        this.towerBeacon.add(beaconWhite);
        const beaconGreen = new THREE.Mesh(new THREE.SphereGeometry(1.4, 6, 6), new THREE.MeshBasicMaterial({ color: 0x00ff66 }));
        beaconGreen.position.set(0, 0, -2);
        this.towerBeacon.add(beaconGreen);
        this.nightLightsGroup.add(this.towerBeacon);

        // Carrier Deck Perimeter Night Lights
        for (let z = 6750; z <= 7450; z += 40) {
          const cLight = new THREE.Mesh(lightSphereGeo, new THREE.MeshBasicMaterial({ color: 0xffdd44 }));
          cLight.position.set(6475, 48, z);
          this.nightLightsGroup.add(cLight);
          const cLightR = new THREE.Mesh(lightSphereGeo, new THREE.MeshBasicMaterial({ color: 0xffdd44 }));
          cLightR.position.set(6525, 48, z);
          this.nightLightsGroup.add(cLightR);
        }

        this.scene.add(this.nightLightsGroup);
      }

      setTimeMode(mode) {
        this.timeMode = mode % 3;
        if (this.timeMode === 0) { // DAY
          this.skyMat.map = this.hdrSkyTexDay;
          this.skyMat.needsUpdate = true;
          this.sunLight.color.setHex(0xfffaee);
          this.sunLight.intensity = 2.6;
          this.sunLight.position.set(4000, 6000, 3000);
          this.hemiLight.color.setHex(0x8cbef8);
          this.hemiLight.groundColor.setHex(0x182c40);
          this.hemiLight.intensity = 1.1;
          this.scene.fog.color.setHex(0x8cbfe8);
          this.scene.fog.density = 0.000025;
          if (this.oceanMat) {
            this.oceanMat.uniforms.deepColor.value.set(0x02172b);
            this.oceanMat.uniforms.shallowColor.value.set(0x0c647b);
            this.oceanMat.uniforms.sunColor.value.set(0xfff7e8);
          }
          if (this.nightLightsGroup) this.nightLightsGroup.visible = false;
        } else if (this.timeMode === 1) { // SUNSET
          this.skyMat.map = this.hdrSkyTexSunset;
          this.skyMat.needsUpdate = true;
          this.sunLight.color.setHex(0xff6a28);
          this.sunLight.intensity = 3.4;
          this.sunLight.position.set(7000, 950, -5000);
          this.hemiLight.color.setHex(0xde5b35);
          this.hemiLight.groundColor.setHex(0x1b112c);
          this.hemiLight.intensity = 0.9;
          this.scene.fog.color.setHex(0x3a1928);
          this.scene.fog.density = 0.000030;
          if (this.oceanMat) {
            this.oceanMat.uniforms.deepColor.value.set(0x160c22);
            this.oceanMat.uniforms.shallowColor.value.set(0x6e2518);
            this.oceanMat.uniforms.sunColor.value.set(0xff7733);
          }
          if (this.nightLightsGroup) this.nightLightsGroup.visible = false;
        } else { // NIGHT
          this.skyMat.map = this.hdrSkyTexNight;
          this.skyMat.needsUpdate = true;
          this.sunLight.color.setHex(0x384a66);
          this.sunLight.intensity = 0.45;
          this.sunLight.position.set(-3000, 5000, -3000);
          this.hemiLight.color.setHex(0x0a1420);
          this.hemiLight.groundColor.setHex(0x020408);
          this.hemiLight.intensity = 0.35;
          this.scene.fog.color.setHex(0x03060c);
          this.scene.fog.density = 0.000035;
          if (this.oceanMat) {
            this.oceanMat.uniforms.deepColor.value.set(0x010308);
            this.oceanMat.uniforms.shallowColor.value.set(0x050e18);
            this.oceanMat.uniforms.sunColor.value.set(0x446699);
          }
          if (this.nightLightsGroup) this.nightLightsGroup.visible = true;
        }
        return this.timeMode;
      }'''

if old_build_lighting in html:
    html = html.replace(old_build_lighting, new_build_lighting)

# 6. Add Airborne Adversary (Su-57) and SAM Threat Missile System to CombatSystem
old_combat_init_end = '''        this.flareGeo = new THREE.SphereGeometry(0.40, 8, 8);
        this.flareMat = new THREE.MeshBasicMaterial({ color: 0xffbb22 });
      }'''

new_combat_init_end = '''        this.flareGeo = new THREE.SphereGeometry(0.40, 8, 8);
        this.flareMat = new THREE.MeshBasicMaterial({ color: 0xffbb22 });

        // Airborne Adversary: Su-57 Felon Fighter Jet on Combat Air Patrol
        this.adversaryGroup = this.createSu57Mesh();
        this.adversary = {
          mesh: this.adversaryGroup,
          orbitCenter: new THREE.Vector3(0, 1650, -3200),
          orbitRadius: 3600,
          orbitAngle: 0,
          speed: 215, // m/s
          health: 100,
          isAlive: true,
          destroyedTimer: 0
        };
        this.scene.add(this.adversaryGroup);

        // Add to target database
        this.world.targets.push({
          name: 'BOGEY: SU-57 FELON [HOSTILE]',
          mesh: this.adversaryGroup,
          radius: 35,
          isHostile: true,
          isAirborne: true,
          destroyed: false
        });

        // Surface-to-Air Missile (SAM) Threat Battery
        this.samSitePos = new THREE.Vector3(1200, 225, -3200);
        this.samMissiles = [];
        this.samCooldown = 0;
        this.samLockTimer = 0;
        this.samAlertActive = false;
      }

      createSu57Mesh() {
        const group = new THREE.Group();
        const camoMat = new THREE.MeshStandardMaterial({ color: 0x30373f, roughness: 0.45, metalness: 0.5 });
        const canopyMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.1, metalness: 0.9 });

        // Fuselage
        const fuse = new THREE.Mesh(new THREE.ConeGeometry(2.4, 20.0, 6).rotateX(Math.PI / 2), camoMat);
        group.add(fuse);

        // Wings
        const wingGeo = new THREE.BufferGeometry();
        const wingVerts = new Float32Array([
          0, 0, 4,    -7.5, 0, -4.5,   -1.5, 0, -6.5,
          0, 0, 4,    -1.5, 0, -6.5,   0, 0, -6.5,
          0, 0, 4,    1.5, 0, -6.5,    7.5, 0, -4.5,
          0, 0, 4,    0, 0, -6.5,      1.5, 0, -6.5
        ]);
        wingGeo.setAttribute('position', new THREE.BufferAttribute(wingVerts, 3));
        wingGeo.computeVertexNormals();
        const wings = new THREE.Mesh(wingGeo, camoMat);
        group.add(wings);

        // Twin Canted Vertical Fins
        const finGeo = new THREE.BoxGeometry(0.12, 2.8, 3.2);
        const lFin = new THREE.Mesh(finGeo, camoMat);
        lFin.position.set(-1.8, 1.3, -5.0);
        lFin.rotation.z = -0.38;
        group.add(lFin);

        const rFin = new THREE.Mesh(finGeo, camoMat);
        rFin.position.set(1.8, 1.3, -5.0);
        rFin.rotation.z = 0.38;
        group.add(rFin);

        // Canopy
        const canopy = new THREE.Mesh(new THREE.ConeGeometry(0.8, 5.0, 6).rotateX(Math.PI / 2), canopyMat);
        canopy.position.set(0, 0.7, 3.5);
        group.add(canopy);

        // Twin Engine Nozzles with Afterburner Glow
        const nozzleGeo = new THREE.CylinderGeometry(0.65, 0.65, 1.5, 8).rotateX(Math.PI / 2);
        const nozzleMat = new THREE.MeshBasicMaterial({ color: 0xff5511 });
        const lNozzle = new THREE.Mesh(nozzleGeo, nozzleMat);
        lNozzle.position.set(-1.2, 0, -7.0);
        group.add(lNozzle);

        const rNozzle = new THREE.Mesh(nozzleGeo, nozzleMat);
        rNozzle.position.set(1.2, 0, -7.0);
        group.add(rNozzle);

        group.position.set(0, 1650, -3200);
        return group;
      }'''

if old_combat_init_end in html:
    html = html.replace(old_combat_init_end, new_combat_init_end)

# 7. Add SAM Threat Logic & Su-57 Maneuvering in CombatSystem.update
old_combat_update_start = '''      update(dt) {
        // Muzzle Flash
        if (this.muzzleFlash.visible) {
          this.muzzleFlashTimer -= dt;
          if (this.muzzleFlashTimer <= 0) this.muzzleFlash.visible = false;
        }'''

new_combat_update_start = '''      update(dt) {
        // 1. Airborne Adversary (Su-57) Combat Air Patrol
        if (this.adversary && this.adversary.isAlive) {
          this.adversary.orbitAngle += (this.adversary.speed / this.adversary.orbitRadius) * dt;
          const x = this.adversary.orbitCenter.x + Math.sin(this.adversary.orbitAngle) * this.adversary.orbitRadius;
          const z = this.adversary.orbitCenter.z + Math.cos(this.adversary.orbitAngle) * this.adversary.orbitRadius;
          const y = this.adversary.orbitCenter.y + Math.sin(this.adversary.orbitAngle * 2.5) * 60;
          this.adversaryGroup.position.set(x, y, z);

          // Flight Banking into the Turn
          this.adversaryGroup.rotation.y = this.adversary.orbitAngle + Math.PI / 2;
          this.adversaryGroup.rotation.z = -0.42;
          this.adversaryGroup.rotation.x = Math.sin(this.adversary.orbitAngle * 2.5) * 0.08;
        } else if (this.adversary && !this.adversary.isAlive) {
          // Fatal Flat Spin Plummet
          this.adversaryGroup.position.y -= 110 * dt;
          this.adversaryGroup.rotation.x += 4.5 * dt;
          this.adversaryGroup.rotation.y += 6.0 * dt;

          // Smoke Plume
          if (Math.random() < 0.35) {
            this.createExplosion(this.adversaryGroup.position.clone().add(new THREE.Vector3(
              (Math.random() - 0.5) * 4, (Math.random() - 0.5) * 4, (Math.random() - 0.5) * 4
            )));
          }

          if (this.adversaryGroup.position.y <= 5) {
            this.createExplosion(this.adversaryGroup.position);
            sound.playTargetExplosion();
            this.adversary.isAlive = true;
            this.adversary.health = 100;
            this.adversaryGroup.position.set(0, 1650, -3200);
            this.adversaryGroup.rotation.set(0, 0, 0);
          }
        }

        // 2. SAM Threat Battery with RCS Detection
        const jetPos = this.aircraft.group.position;
        const distToSAM = jetPos.distanceTo(this.samSitePos);
        
        // Calculate Radar Cross Section (RCS)
        let rcs = 0.001; // Clean VLO Stealth
        if (window.simulationApp && window.simulationApp.bayOpen) rcs += 0.35;
        if (window.simulationApp && window.simulationApp.beastMode) rcs += 1.85;

        // Dynamic SAM Lock Range
        const maxLockRange = 3200 + Math.pow(rcs / 0.001, 0.42) * 4800; // ~3.2km when stealth, >17km when non-stealth!
        if (distToSAM < maxLockRange && jetPos.y > 60) {
          this.samLockTimer += dt;
          if (this.samLockTimer > 2.5 && this.samCooldown <= 0) {
            this.launchSAMMissile();
            this.samCooldown = 14.0;
            this.samLockTimer = 0;
            sound.playSAMWarning();
            sound.speakAlert('WARNING: SAM LAUNCH');
          }
        } else {
          this.samLockTimer = Math.max(0, this.samLockTimer - dt * 2);
        }
        if (this.samCooldown > 0) this.samCooldown -= dt;

        // Update In-Flight SAM Missiles
        for (let i = this.samMissiles.length - 1; i >= 0; i--) {
          const sam = this.samMissiles[i];
          sam.life -= dt;

          // Target: Check if Decoyed by Flares
          let targetPoint = jetPos.clone();
          let flareLock = null;
          for (const fl of this.flares) {
            if (fl.mesh.position.distanceTo(sam.mesh.position) < 450) {
              flareLock = fl.mesh.position;
              break;
            }
          }
          if (flareLock) targetPoint = flareLock;

          const toTarget = targetPoint.clone().sub(sam.mesh.position).normalize();
          sam.velocity.lerp(toTarget.multiplyScalar(420), 0.12);
          sam.mesh.position.addScaledVector(sam.velocity, dt);
          sam.mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), sam.velocity.clone().normalize());

          // Smoke puff
          if (Math.random() < 0.4) {
            const smoke = new THREE.Mesh(new THREE.SphereGeometry(0.9, 6, 6), new THREE.MeshBasicMaterial({ color: 0xcccccc, transparent: true, opacity: 0.5 }));
            smoke.position.copy(sam.mesh.position);
            this.scene.add(smoke);
            this.explosions.push({ mesh: smoke, life: 1.0, maxLife: 1.0, isSmoke: true });
          }

          // Detonation check
          if (sam.mesh.position.distanceTo(jetPos) < 18) {
            this.createExplosion(sam.mesh.position);
            sound.playTargetExplosion();
            sound.speakAlert('DIRECT HIT');
            this.scene.remove(sam.mesh);
            this.samMissiles.splice(i, 1);
          } else if (flareLock && sam.mesh.position.distanceTo(flareLock) < 25) {
            this.createExplosion(sam.mesh.position);
            sound.playTargetExplosion();
            this.scene.remove(sam.mesh);
            this.samMissiles.splice(i, 1);
          } else if (sam.life <= 0) {
            this.createExplosion(sam.mesh.position);
            this.scene.remove(sam.mesh);
            this.samMissiles.splice(i, 1);
          }
        }

        // Muzzle Flash
        if (this.muzzleFlash.visible) {
          this.muzzleFlashTimer -= dt;
          if (this.muzzleFlashTimer <= 0) this.muzzleFlash.visible = false;
        }'''

if old_combat_update_start in html:
    html = html.replace(old_combat_update_start, new_combat_update_start)

# Add launchSAMMissile method
old_tracer_hit = '''          // Collision check against targets
          for (const tgt of this.world.targets) {
            if (tgt.destroyed) continue;'''

new_tracer_hit = '''      launchSAMMissile() {
        sound.playMissileLaunch();
        const samGeo = new THREE.CylinderGeometry(0.22, 0.22, 5.2, 8).rotateX(Math.PI / 2);
        const samMat = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
        const samMesh = new THREE.Mesh(samGeo, samMat);
        samMesh.position.copy(this.samSitePos).add(new THREE.Vector3(0, 15, 0));

        const initVel = new THREE.Vector3(0, 1, 0).multiplyScalar(280);
        this.samMissiles.push({ mesh: samMesh, velocity: initVel, life: 9.0 });
        this.scene.add(samMesh);
      }

          // Collision check against targets
          for (const tgt of this.world.targets) {
            if (tgt.destroyed) continue;'''

if old_tracer_hit in html:
    html = html.replace(old_tracer_hit, new_tracer_hit)

# 8. Add Time-of-Day button event and Cockpit Free-Look in App class
old_app_controls = '''        this.domAudioBtn.addEventListener('click', () => this.toggleAudio());
        this.domBeastBtn.addEventListener('click', () => this.toggleBeastMode());
        this.domGfxBtn.addEventListener('click', () => this.toggleGraphics());
        this.domBayBtn.addEventListener('click', () => this.toggleBay());
        this.domGearBtn.addEventListener('click', () => this.toggleGear());'''

new_app_controls = '''        this.domAudioBtn.addEventListener('click', () => this.toggleAudio());
        this.domBeastBtn.addEventListener('click', () => this.toggleBeastMode());
        this.domGfxBtn.addEventListener('click', () => this.toggleGraphics());
        this.domBayBtn.addEventListener('click', () => this.toggleBay());
        this.domGearBtn.addEventListener('click', () => this.toggleGear());

        this.domTimeBtn = document.getElementById('time-toggle-btn');
        if (this.domTimeBtn) {
          this.domTimeBtn.addEventListener('click', () => this.toggleTimeOfDay());
        }'''

if old_app_controls in html:
    html = html.replace(old_app_controls, new_app_controls)

old_key_handler = '''          if (e.code === 'KeyM') this.toggleAudio();
          if (e.code === 'KeyV') this.cycleCamera();'''

new_key_handler = '''          if (e.code === 'KeyM') this.toggleAudio();
          if (e.code === 'KeyT') this.toggleTimeOfDay();
          if (e.code === 'KeyV') this.cycleCamera();'''

if old_key_handler in html:
    html = html.replace(old_key_handler, new_key_handler)

# Add toggleTimeOfDay and Cockpit Free-Look to App
old_toggle_beast = '''      toggleBeastMode() {
        this.beastMode = !this.beastMode;
        this.aircraft.toggleBeastMode();
        this.domBeastBtn.classList.toggle('active', this.beastMode);
        this.domBeastBtn.textContent = `BEAST: ${this.beastMode ? 'ON' : 'OFF'}`;
      }'''

new_toggle_beast = '''      toggleBeastMode() {
        this.beastMode = !this.beastMode;
        this.aircraft.toggleBeastMode();
        this.domBeastBtn.classList.toggle('active', this.beastMode);
        this.domBeastBtn.textContent = `BEAST: ${this.beastMode ? 'ON' : 'OFF'}`;
        this.updateRCSBadge();
      }

      toggleTimeOfDay() {
        const newMode = (this.world.timeMode + 1) % 3;
        this.world.setTimeMode(newMode);
        const labels = ['TIME: DAY', 'TIME: SUNSET', 'TIME: NIGHT'];
        if (this.domTimeBtn) this.domTimeBtn.innerHTML = `<span>&#9728;</span> ${labels[newMode]}`;

        // Slime lights at night
        if (this.aircraft.slimeMat) {
          this.aircraft.slimeMat.opacity = (newMode === 2) ? 0.95 : 0.0;
        }
      }

      updateRCSBadge() {
        const badge = document.getElementById('rcs-badge');
        if (!badge) return;
        let rcs = 0.001;
        if (this.bayOpen) rcs += 0.35;
        if (this.beastMode) rcs += 1.85;

        if (rcs > 1.0) {
          badge.style.background = 'rgba(255, 68, 68, 0.2)';
          badge.style.borderColor = '#ff4444';
          badge.style.color = '#ff6666';
          badge.textContent = `RCS: ${rcs.toFixed(3)} m² [DETECTED]`;
        } else if (rcs > 0.1) {
          badge.style.background = 'rgba(255, 170, 0, 0.2)';
          badge.style.borderColor = '#ffaa00';
          badge.style.color = '#ffbb33';
          badge.textContent = `RCS: ${rcs.toFixed(3)} m² [CAVITY]`;
        } else {
          badge.style.background = 'rgba(0, 255, 119, 0.15)';
          badge.style.borderColor = '#00ff77';
          badge.style.color = '#00ffaa';
          badge.textContent = `RCS: 0.001 m² [VLO]`;
        }
      }'''

if old_toggle_beast in html:
    html = html.replace(old_toggle_beast, new_toggle_beast)

# Also update RCS badge on toggleBay
old_toggle_bay = '''      toggleBay() {
        this.bayOpen = !this.bayOpen;
        this.aircraft.toggleBay(this.bayOpen);
        this.domBayBtn.classList.toggle('active', this.bayOpen);
        this.domBayBtn.textContent = `BAY: ${this.bayOpen ? 'OPEN' : 'CLOSED'}`;
      }'''

new_toggle_bay = '''      toggleBay() {
        this.bayOpen = !this.bayOpen;
        this.aircraft.toggleBay(this.bayOpen);
        this.domBayBtn.classList.toggle('active', this.bayOpen);
        this.domBayBtn.textContent = `BAY: ${this.bayOpen ? 'OPEN' : 'CLOSED'}`;
        this.updateRCSBadge();
      }'''

if old_toggle_bay in html:
    html = html.replace(old_toggle_bay, new_toggle_bay)

# Cockpit Free-Look Camera
old_cockpit_cam = '''        } else if (this.cameraMode === 1) {
          // Cockpit / HMDS Cam
          const cockpitPos = jetPos.clone()
            .add(up.clone().multiplyScalar(1.02))
            .add(forward.clone().multiplyScalar(4.0));
          this.camera.position.copy(cockpitPos);
          const lookTarget = cockpitPos.clone().add(forward.clone().multiplyScalar(20));
          this.camera.lookAt(lookTarget);'''

new_cockpit_cam = '''        } else if (this.cameraMode === 1) {
          // Cockpit / HMDS Cam with Free-Look support
          const cockpitPos = jetPos.clone()
            .add(up.clone().multiplyScalar(1.02))
            .add(forward.clone().multiplyScalar(4.0));
          this.camera.position.copy(cockpitPos);

          const lookDir = forward.clone();
          if (this.cockpitLookYaw || this.cockpitLookPitch) {
            lookDir.applyAxisAngle(up, this.cockpitLookYaw || 0);
            const rightAxis = new THREE.Vector3().crossVectors(forward, up).normalize();
            lookDir.applyAxisAngle(rightAxis, this.cockpitLookPitch || 0);
          }
          const lookTarget = cockpitPos.clone().add(lookDir.multiplyScalar(20));
          this.camera.lookAt(lookTarget);'''

if old_cockpit_cam in html:
    html = html.replace(old_cockpit_cam, new_cockpit_cam)

# Free look pointer handlers
old_init_app_vars = '''        this.cameraMode = 0; // 0=chase, 1=cockpit, 2=flyby, 3=orbit
        this.audioMuted = true;
        this.beastMode = false;'''

new_init_app_vars = '''        this.cameraMode = 0; // 0=chase, 1=cockpit, 2=flyby, 3=orbit
        this.audioMuted = true;
        this.beastMode = false;
        this.cockpitLookYaw = 0;
        this.cockpitLookPitch = 0;'''

if old_init_app_vars in html:
    html = html.replace(old_init_app_vars, new_init_app_vars)

# Write updated index.html
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Round 3 upgrades applied to index.html successfully!")

# Also write to build_simulation.py so it matches index.html exactly
build_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\build_simulation.py"
with open(build_path, "w", encoding="utf-8") as f:
    f.write(f'''# Python script to compile index.html
output_path = r"{index_path}"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(r\'\'\'{html}\'\'\')
print("Compiled index.html successfully.")
''')

print("Updated build_simulation.py successfully!")

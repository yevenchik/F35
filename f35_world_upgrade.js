/**
 * ============================================================================
 * F-35 LIGHTNING II FLIGHT SIMULATOR - UPGRADED WORLD & FLEET SYSTEM
 * Procedural Archipelago, Military Airbase Complex & Carrier Strike Group
 * ============================================================================
 * 
 * Components included:
 * 1. ProceduralArchipelago: Multi-octave Perlin fractal heightmap with
 *    biome elevation zones (beaches, lush valleys, rocky cliffs, mountain ridges)
 *    and flat airbase plateau blending.
 * 2. MilitaryAirbase: 10,000 ft Runway 36L/18R with precision markings,
 *    dynamic 4-light PAPI glide slope indicator, complete taxiway network with
 *    blue edge and green centerline lights, Hardened Aircraft Shelters (HAS),
 *    Control Tower with rotating dual-beam beacon, Surveillance Radar, and SAM battery.
 * 3. CarrierStrikeGroup: CVN Supercarrier with angled flight deck, 4 catapults,
 *    blast deflectors, 4 arresting wires, island superstructure, plus two
 *    Arleigh Burke-class Aegis Guided Missile Destroyers in tactical escort formation.
 * 4. TargetSystem: Interactive destructible naval drone target vessels and mountain
 *    radar station bunkers with hit detection, explosive fireballs, rising smoke plumes,
 *    and combat status notifications.
 * 5. UpgradedOceanAtmosphere: Dynamic water with specular glints, atmospheric sky,
 *    and drifting multi-layer volumetric cloud puffs.
 * 6. UpgradedWorldEnvironment: Master orchestrator seamlessly drop-in compatible
 *    with the F-35 simulation loop.
 */

// --- Fast Procedural Perlin / Fractal Noise Engine ---
class ProceduralNoise {
  constructor(seed = 1337) {
    this.p = new Uint8Array(512);
    const permutation = new Uint8Array(256);
    for (let i = 0; i < 256; i++) permutation[i] = i;
    // Fisher-Yates shuffle with seed
    let s = seed;
    for (let i = 255; i > 0; i--) {
      s = (s * 16807 + 3) % 2147483647;
      const j = s % (i + 1);
      const tmp = permutation[i];
      permutation[i] = permutation[j];
      permutation[j] = tmp;
    }
    for (let i = 0; i < 512; i++) {
      this.p[i] = permutation[i & 255];
    }
  }

  fade(t) {
    return t * t * t * (t * (t * 6 - 15) + 10);
  }

  lerp(t, a, b) {
    return a + t * (b - a);
  }

  grad(hash, x, y) {
    const h = hash & 7;
    const u = h < 4 ? x : y;
    const v = h < 4 ? y : x;
    return ((h & 1) ? -u : u) + ((h & 2) ? -2.0 * v : 2.0 * v);
  }

  noise(x, y) {
    const X = Math.floor(x) & 255;
    const Y = Math.floor(y) & 255;
    const xf = x - Math.floor(x);
    const yf = y - Math.floor(y);

    const u = this.fade(xf);
    const v = this.fade(yf);

    const aa = this.p[this.p[X] + Y];
    const ab = this.p[this.p[X] + Y + 1];
    const ba = this.p[this.p[X + 1] + Y];
    const bb = this.p[this.p[X + 1] + Y + 1];

    const x1 = this.lerp(u, this.grad(aa, xf, yf), this.grad(ba, xf - 1, yf));
    const x2 = this.lerp(u, this.grad(ab, xf, yf - 1), this.grad(bb, xf - 1, yf - 1));
    return (this.lerp(v, x1, x2) + 1.0) * 0.5; // normalized 0..1
  }

  fbm(x, y, octaves = 6, lacunarity = 2.0, persistence = 0.48) {
    let total = 0;
    let frequency = 1;
    let amplitude = 1;
    let maxValue = 0;
    for (let i = 0; i < octaves; i++) {
      total += this.noise(x * frequency, y * frequency) * amplitude;
      maxValue += amplitude;
      amplitude *= persistence;
      frequency *= lacunarity;
    }
    return total / maxValue;
  }
}

// Global noise instance
const worldNoise = new ProceduralNoise(48291);

// --- 1. PROCEDURAL ARCHIPELAGO & MOUNTAINS ---
class ProceduralArchipelago {
  constructor(scene) {
    this.scene = scene;
    this.size = 42000;
    this.segments = 240;
    this.airbasePlateauY = 22.0;

    // Island centers: [cx, cz, radius, maxAltitude, ridgeScale]
    this.islands = [
      { cx: 0, cz: -2000, r: 4800, maxH: 380, steep: 1.1 },      // Airbase island
      { cx: -7200, cz: -6500, r: 5500, maxH: 980, steep: 1.8 }, // North-West Alpine Range
      { cx: 6800, cz: -4200, r: 5200, maxH: 740, steep: 1.5 },  // East Radar Peaks
      { cx: -5400, cz: 4800, r: 4000, maxH: 520, steep: 1.3 },   // South-West Atoll & Bunkers
      { cx: 4200, cz: 4500, r: 3200, maxH: 260, steep: 1.0 }    // Fleet Approach Island
    ];

    this.buildTerrainMesh();
  }

  // Pure heightmap function queryable anywhere (for physics, AI, placement)
  getHeight(x, z) {
    // Airbase plateau boundary blending
    const abDistX = Math.abs(x - 0);
    const abDistZ = Math.abs(z - (-2000));
    
    // Core flat runway / taxiway zone: X within 380m, Z within 1900m
    if (abDistX < 380 && abDistZ < 1900) {
      return this.airbasePlateauY;
    }

    // Smooth transition boundary for airfield tarmac perimeter
    let airbaseBlend = 0;
    const abRadius = Math.hypot(abDistX * 1.5, abDistZ * 0.4);
    if (abRadius < 1800) {
      airbaseBlend = Math.cos((abRadius / 1800) * (Math.PI / 2));
      airbaseBlend = Math.pow(airbaseBlend, 2);
    }

    // Calculate natural archipelago elevation
    let rawHeight = 0;
    for (let i = 0; i < this.islands.length; i++) {
      const isl = this.islands[i];
      const dist = Math.hypot(x - isl.cx, z - isl.cz);
      if (dist < isl.r) {
        const falloff = Math.cos((dist / isl.r) * (Math.PI / 2));
        const nx = (x + 20000) * 0.00018;
        const nz = (z + 20000) * 0.00018;
        
        let detail = worldNoise.fbm(nx * isl.steep, nz * isl.steep, 5, 2.05, 0.48);
        // Ridgeline sharpness / chiseled crests
        detail = Math.pow(detail, 1.45);

        const h = falloff * isl.maxH * (0.35 + 0.65 * detail);
        if (h > rawHeight) rawHeight = h;
      }
    }

    // Blend natural terrain with the level airbase plateau
    let finalH = rawHeight * (1.0 - airbaseBlend) + this.airbasePlateauY * airbaseBlend;

    // Ocean waterline threshold
    if (finalH < 0.5) finalH = -2.0; // submerged coastal shelf

    return finalH;
  }

  buildTerrainMesh() {
    const geo = new THREE.PlaneGeometry(this.size, this.size, this.segments, this.segments);
    geo.rotateX(-Math.PI / 2);

    const pos = geo.attributes.position;
    const vertexCount = pos.count;
    const colors = new Float32Array(vertexCount * 3);

    // Color palettes for biome altitude zones
    const colBeach = new THREE.Color(0xd0be8d);    // Sandy coastal beach
    const colValley = new THREE.Color(0x38612b);   // Lush green lowland grass
    const colHighGrass = new THREE.Color(0x4d6836); // Subalpine plateau
    const colRock = new THREE.Color(0x636868);      // Steep granite / slate
    const colSnow = new THREE.Color(0xdce5ed);      // Chiseled alpine snow crest
    const colTarmacGround = new THREE.Color(0x283827); // Compacted turf around base

    const tempCol = new THREE.Color();

    for (let i = 0; i < vertexCount; i++) {
      const vx = pos.getX(i);
      const vz = pos.getZ(i);
      const vy = this.getHeight(vx, vz);
      pos.setY(i, vy);

      // Procedural biome coloring based on altitude and airfield proximity
      const abDist = Math.hypot(vx - 0, vz - (-2000));
      if (abDist < 1200 && vy >= this.airbasePlateauY - 1.0 && vy <= this.airbasePlateauY + 1.0) {
        tempCol.copy(colTarmacGround);
      } else if (vy <= 8.0) {
        // Coastal beach & sandy fringe
        const t = Math.max(0, vy / 8.0);
        tempCol.lerpColors(colBeach, colValley, t);
      } else if (vy < 140.0) {
        // Lush valleys
        const t = (vy - 8.0) / (140.0 - 8.0);
        tempCol.lerpColors(colValley, colHighGrass, t);
      } else if (vy < 480.0) {
        // Rocky slopes & mountain flanks
        const t = (vy - 140.0) / (480.0 - 140.0);
        tempCol.lerpColors(colHighGrass, colRock, t);
      } else {
        // High mountain peaks & snow
        const t = Math.min(1.0, (vy - 480.0) / 360.0);
        tempCol.lerpColors(colRock, colSnow, t);
      }

      colors[i * 3 + 0] = tempCol.r;
      colors[i * 3 + 1] = tempCol.g;
      colors[i * 3 + 2] = tempCol.b;
    }

    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.computeVertexNormals();

    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.88,
      metalness: 0.05,
      flatShading: false
    });

    this.mesh = new THREE.Mesh(geo, mat);
    this.mesh.receiveShadow = true;
    this.scene.add(this.mesh);
  }
}

// --- 2. MILITARY AIRBASE COMPLEX ---
class MilitaryAirbase {
  constructor(scene, terrainY = 22.0) {
    this.scene = scene;
    this.baseY = terrainY;
    this.group = new THREE.Group();
    this.group.position.set(0, this.baseY, -2000);

    this.papiLights = [];
    this.beaconGroup = null;
    this.radarDish = null;

    this.buildMainRunway();
    this.buildRunwayMarkings();
    this.buildPAPIApproachLights();
    this.buildTaxiwayNetwork();
    this.buildHardenedAircraftShelters();
    this.buildControlTower();
    this.buildSurveillanceRadarSite();
    this.buildSAMMissileBattery();

    this.scene.add(this.group);
  }

  buildMainRunway() {
    // 10,000 ft Runway (3,200 m length x 64 m width)
    const runwayGeo = new THREE.PlaneGeometry(64, 3200);
    runwayGeo.rotateX(-Math.PI / 2);

    // Concrete runway material with realistic tarmac texture
    const runwayCanvas = document.createElement('canvas');
    runwayCanvas.width = 512;
    runwayCanvas.height = 512;
    const ctx = runwayCanvas.getContext('2d');
    ctx.fillStyle = '#23272b';
    ctx.fillRect(0, 0, 512, 512);

    // Weathering, asphalt seams & tire rubber touchdown deposits
    ctx.fillStyle = '#1c1f22';
    for (let i = 0; i < 400; i++) {
      ctx.fillRect(Math.random() * 512, Math.random() * 512, 4 + Math.random() * 12, 2 + Math.random() * 4);
    }
    const runwayTex = new THREE.CanvasTexture(runwayCanvas);
    runwayTex.wrapS = THREE.RepeatWrapping;
    runwayTex.wrapT = THREE.RepeatWrapping;
    runwayTex.repeat.set(4, 40);

    const runwayMat = new THREE.MeshStandardMaterial({
      map: runwayTex,
      roughness: 0.8,
      metalness: 0.1
    });

    const runwayMesh = new THREE.Mesh(runwayGeo, runwayMat);
    runwayMesh.position.set(0, 0.15, 0);
    this.group.add(runwayMesh);

    // Asphalt blast pads at runway overruns
    const blastPadGeo = new THREE.PlaneGeometry(64, 120);
    blastPadGeo.rotateX(-Math.PI / 2);
    const blastPadMat = new THREE.MeshStandardMaterial({ color: 0x1a1c1e, roughness: 0.9 });
    
    const padNorth = new THREE.Mesh(blastPadGeo, blastPadMat);
    padNorth.position.set(0, 0.14, -1660);
    this.group.add(padNorth);

    const padSouth = new THREE.Mesh(blastPadGeo, blastPadMat);
    padSouth.position.set(0, 0.14, 1660);
    this.group.add(padSouth);
  }

  buildRunwayMarkings() {
    const whiteMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      polygonOffset: true,
      polygonOffsetFactor: -4,
      polygonOffsetUnits: -4
    });

    // 1. Centerline dashed lines: 30m length, 20m gap, 3.2m width
    const dashGeo = new THREE.PlaneGeometry(3.2, 30);
    dashGeo.rotateX(-Math.PI / 2);
    for (let z = -1400; z <= 1400; z += 50) {
      const dash = new THREE.Mesh(dashGeo, whiteMat);
      dash.position.set(0, 0.22, z);
      this.group.add(dash);
    }

    // 2. Continuous runway boundary edge stripes (width 1.2m)
    const edgeGeo = new THREE.PlaneGeometry(1.2, 3000);
    edgeGeo.rotateX(-Math.PI / 2);
    const edgeL = new THREE.Mesh(edgeGeo, whiteMat);
    edgeL.position.set(-30, 0.22, 0);
    this.group.add(edgeL);

    const edgeR = new THREE.Mesh(edgeGeo, whiteMat);
    edgeR.position.set(30, 0.22, 0);
    this.group.add(edgeR);

    // 3. Threshold Piano Keys (Runway 36L North and Runway 18R South)
    const keyGeo = new THREE.PlaneGeometry(2.4, 45);
    keyGeo.rotateX(-Math.PI / 2);
    for (let x = -26; x <= 26; x += 3.8) {
      if (Math.abs(x) < 2) continue; // centerline opening
      // South end (Runway 36L threshold)
      const keyS = new THREE.Mesh(keyGeo, whiteMat);
      keyS.position.set(x, 0.22, 1550);
      this.group.add(keyS);

      // North end (Runway 18R threshold)
      const keyN = new THREE.Mesh(keyGeo, whiteMat);
      keyN.position.set(x, 0.22, -1550);
      this.group.add(keyN);
    }

    // 4. Touchdown Zone (TDZ) Markings (pairs of 3 rectangular bars)
    const tdzGeo = new THREE.PlaneGeometry(1.8, 24);
    tdzGeo.rotateX(-Math.PI / 2);
    const tdzDistances = [150, 300, 450, 600, 750];
    tdzDistances.forEach(d => {
      // South approach
      for (let side of [-14, 14]) {
        for (let b = -2.5; b <= 2.5; b += 2.5) {
          const bar = new THREE.Mesh(tdzGeo, whiteMat);
          bar.position.set(side + b, 0.22, 1500 - d);
          this.group.add(bar);
        }
      }
      // North approach
      for (let side of [-14, 14]) {
        for (let b = -2.5; b <= 2.5; b += 2.5) {
          const bar = new THREE.Mesh(tdzGeo, whiteMat);
          bar.position.set(side + b, 0.22, -1500 + d);
          this.group.add(bar);
        }
      }
    });

    // 5. Runway Edge Lights
    const lightBulbGeo = new THREE.SphereGeometry(0.7, 6, 6);
    const whiteBulbMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const amberBulbMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 });
    const greenBulbMat = new THREE.MeshBasicMaterial({ color: 0x00ff44 });
    const redBulbMat = new THREE.MeshBasicMaterial({ color: 0xff1122 });

    for (let z = -1580; z <= 1580; z += 60) {
      let bulbMat = whiteBulbMat;
      if (Math.abs(z) > 1520) bulbMat = (z > 0) ? greenBulbMat : redBulbMat;
      else if (Math.abs(z) > 1100) bulbMat = amberBulbMat; // caution zone last 600m

      const l1 = new THREE.Mesh(lightBulbGeo, bulbMat);
      l1.position.set(-33, 0.6, z);
      this.group.add(l1);

      const l2 = new THREE.Mesh(lightBulbGeo, bulbMat);
      l2.position.set(33, 0.6, z);
      this.group.add(l2);
    }
  }

  buildPAPIApproachLights() {
    // 4-Light PAPI system on port side (West) at Touchdown Aiming Point (Z = 1200)
    // Real PAPI transitions: >3.5 deg = 4 White, 3.2 deg = 3W 1R, 3.0 deg = 2W 2R (On Path), 2.8 deg = 1W 3R, <2.5 deg = 4 Red
    this.papiGroup = new THREE.Group();
    this.papiGroup.position.set(-42, 0.4, 1200);

    const housingGeo = new THREE.BoxGeometry(2.2, 1.2, 1.8);
    const housingMat = new THREE.MeshStandardMaterial({ color: 0xd98218 }); // Aviation orange box

    const lampGeo = new THREE.CylinderGeometry(0.45, 0.45, 0.3, 12);
    lampGeo.rotateX(Math.PI / 2);

    for (let i = 0; i < 4; i++) {
      const box = new THREE.Mesh(housingGeo, housingMat);
      box.position.set(-i * 3.5, 0.6, 0);
      this.papiGroup.add(box);

      // Facing south toward landing aircraft (approach heading 360)
      const lampMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const lamp = new THREE.Mesh(lampGeo, lampMat);
      lamp.position.set(-i * 3.5, 0.6, 0.95);
      this.papiGroup.add(lamp);

      // Store reference and threshold angle (nominally: 3.5, 3.2, 2.8, 2.5 degrees)
      this.papiLights.push({
        mesh: lamp,
        targetAngle: 3.5 - i * 0.33, // degrees
        isWhite: true
      });
    }

    this.group.add(this.papiGroup);
  }

  updatePAPI(viewerPos) {
    // Calculate vertical glide slope angle from viewer position to touchdown point
    // PAPI world position: group position + papiGroup position
    const papiWorldZ = this.group.position.z + 1200;
    const papiWorldY = this.group.position.y;
    const distZ = viewerPos.z - papiWorldZ; // distance out on approach

    if (distZ <= 20) return; // aircraft passed touchdown point

    const altDiff = viewerPos.y - papiWorldY;
    const slopeDeg = (Math.atan2(altDiff, distZ) * 180) / Math.PI;

    for (let i = 0; i < this.papiLights.length; i++) {
      const light = this.papiLights[i];
      const shouldBeWhite = slopeDeg >= light.targetAngle;
      if (shouldBeWhite !== light.isWhite) {
        light.isWhite = shouldBeWhite;
        light.mesh.material.color.setHex(shouldBeWhite ? 0xffffff : 0xff1e1e);
      }
    }
  }

  buildTaxiwayNetwork() {
    // Parallel taxiway: 3,000m long, 24m wide, 110m East of runway
    const taxiwayGeo = new THREE.PlaneGeometry(24, 3000);
    taxiwayGeo.rotateX(-Math.PI / 2);
    const taxiwayMat = new THREE.MeshStandardMaterial({ color: 0x1f2327, roughness: 0.85 });

    const parTaxi = new THREE.Mesh(taxiwayGeo, taxiwayMat);
    parTaxi.position.set(110, 0.12, 0);
    this.group.add(parTaxi);

    // Connecting high-speed exit links (angled at 45 deg and 90 deg)
    const connectorPositionsZ = [-1400, -700, 0, 700, 1400];
    const connGeo = new THREE.PlaneGeometry(24, 110);
    connGeo.rotateX(-Math.PI / 2);
    connGeo.rotateY(Math.PI / 2);

    connectorPositionsZ.forEach(cz => {
      const conn = new THREE.Mesh(connGeo, taxiwayMat);
      conn.position.set(55, 0.13, cz);
      this.group.add(conn);
    });

    // Main flight line apron & tarmac staging area (350m x 250m)
    const apronGeo = new THREE.PlaneGeometry(280, 500);
    apronGeo.rotateX(-Math.PI / 2);
    const apron = new THREE.Mesh(apronGeo, taxiwayMat);
    apron.position.set(240, 0.11, -200);
    this.group.add(apron);

    // Taxiway Centerline Markings (Bright yellow stripe)
    const yellowStripeMat = new THREE.MeshBasicMaterial({
      color: 0xffcc00,
      polygonOffset: true,
      polygonOffsetFactor: -3,
      polygonOffsetUnits: -3
    });

    const taxYellowGeo = new THREE.PlaneGeometry(0.8, 2980);
    taxYellowGeo.rotateX(-Math.PI / 2);
    const taxYellow = new THREE.Mesh(taxYellowGeo, yellowStripeMat);
    taxYellow.position.set(110, 0.2, 0);
    this.group.add(taxYellow);

    // Hold Short Bar (Double solid / double dashed bar at runway entrances)
    connectorPositionsZ.forEach(cz => {
      const holdBarGeo = new THREE.PlaneGeometry(18, 1.2);
      holdBarGeo.rotateX(-Math.PI / 2);
      const holdBar = new THREE.Mesh(holdBarGeo, yellowStripeMat);
      holdBar.position.set(40, 0.21, cz);
      this.group.add(holdBar);
    });

    // Taxiway Edge Lights (Elevated blue lights) & Centerline Green Lights
    const blueBulbMat = new THREE.MeshBasicMaterial({ color: 0x0066ff });
    const greenBulbMat = new THREE.MeshBasicMaterial({ color: 0x00ff66 });
    const bulbGeo = new THREE.SphereGeometry(0.5, 6, 6);

    for (let z = -1480; z <= 1480; z += 50) {
      // Blue edge lights lining parallel taxiway
      const bLeft = new THREE.Mesh(bulbGeo, blueBulbMat);
      bLeft.position.set(96, 0.5, z);
      this.group.add(bLeft);

      const bRight = new THREE.Mesh(bulbGeo, blueBulbMat);
      bRight.position.set(124, 0.5, z);
      this.group.add(bRight);

      // Green centerline guide lights
      const gCenter = new THREE.Mesh(bulbGeo, greenBulbMat);
      gCenter.position.set(110, 0.25, z);
      this.group.add(gCenter);
    }
  }

  buildHardenedAircraftShelters() {
    // 4 Hardened Aircraft Shelters (HAS / TAB-VEE revetments) with arched concrete roofs
    const archRadius = 18;
    const archLength = 50;
    const archGeo = new THREE.CylinderGeometry(archRadius, archRadius, archLength, 24, 1, true, 0, Math.PI);
    archGeo.rotateZ(Math.PI / 2);
    archGeo.rotateY(Math.PI / 2);

    const concreteMat = new THREE.MeshStandardMaterial({
      color: 0x51565c,
      roughness: 0.9,
      metalness: 0.1,
      side: THREE.DoubleSide
    });

    // Earth revetment berm covering top of shelter
    const earthMat = new THREE.MeshStandardMaterial({ color: 0x33442a, roughness: 0.95 });

    const shelterZ = [-420, -320, -220, -120];
    shelterZ.forEach((sz, idx) => {
      const shelterGroup = new THREE.Group();
      shelterGroup.position.set(360, 0, sz);

      // Main concrete arched roof
      const arch = new THREE.Mesh(archGeo, concreteMat);
      arch.position.y = 0;
      shelterGroup.add(arch);

      // Rear heavy concrete blast deflection wall
      const backWallGeo = new THREE.CircleGeometry(archRadius, 24, 0, Math.PI);
      backWallGeo.rotateY(Math.PI / 2);
      const backWall = new THREE.Mesh(backWallGeo, concreteMat);
      backWall.position.set(archLength / 2, 0, 0);
      shelterGroup.add(backWall);

      // Earth camouflage cover on exterior
      const bermGeo = new THREE.CylinderGeometry(archRadius + 2.2, archRadius + 2.2, archLength - 4, 16, 1, true, 0, Math.PI);
      bermGeo.rotateZ(Math.PI / 2);
      bermGeo.rotateY(Math.PI / 2);
      const berm = new THREE.Mesh(bermGeo, earthMat);
      berm.position.set(0, 0.3, 0);
      shelterGroup.add(berm);

      // Taxi spur connecting shelter to apron
      const spurGeo = new THREE.PlaneGeometry(archLength + 30, 24);
      spurGeo.rotateX(-Math.PI / 2);
      const spurMat = new THREE.MeshStandardMaterial({ color: 0x212529, roughness: 0.85 });
      const spur = new THREE.Mesh(spurGeo, spurMat);
      spur.position.set(-20, 0.12, 0);
      shelterGroup.add(spur);

      this.group.add(shelterGroup);
    });
  }

  buildControlTower() {
    const towerGroup = new THREE.Group();
    towerGroup.position.set(220, 0, 250);

    // Concrete shaft base
    const baseGeo = new THREE.CylinderGeometry(7, 10, 48, 8);
    const baseMat = new THREE.MeshStandardMaterial({ color: 0x6e747b, roughness: 0.8 });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.y = 24;
    towerGroup.add(base);

    // Observation cab support ring
    const ringGeo = new THREE.CylinderGeometry(14, 8, 4, 8);
    const ring = new THREE.Mesh(ringGeo, baseMat);
    ring.position.y = 50;
    towerGroup.add(ring);

    // Hexagonal glass cab
    const cabGeo = new THREE.CylinderGeometry(13.5, 11, 8, 8);
    const cabMat = new THREE.MeshStandardMaterial({
      color: 0x113322,
      roughness: 0.1,
      metalness: 0.9,
      transparent: true,
      opacity: 0.85
    });
    const cab = new THREE.Mesh(cabGeo, cabMat);
    cab.position.y = 56;
    towerGroup.add(cab);

    // Tower roof & antenna mast
    const roofGeo = new THREE.ConeGeometry(14, 3, 8);
    const roof = new THREE.Mesh(roofGeo, baseMat);
    roof.position.y = 61.5;
    towerGroup.add(roof);

    const mastGeo = new THREE.CylinderGeometry(0.3, 0.6, 16, 6);
    const mast = new THREE.Mesh(mastGeo, new THREE.MeshStandardMaterial({ color: 0x222222 }));
    mast.position.y = 70;
    towerGroup.add(mast);

    // Rotating Dual-Beam Airport Beacon (Alternating Green & White lights)
    this.beaconGroup = new THREE.Group();
    this.beaconGroup.position.set(0, 64, 0);

    const greenBeamMat = new THREE.MeshBasicMaterial({ color: 0x00ff44 });
    const whiteBeamMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const beaconBulbGeo = new THREE.SphereGeometry(1.2, 8, 8);

    const bGreen = new THREE.Mesh(beaconBulbGeo, greenBeamMat);
    bGreen.position.set(0, 0, 1.8);
    this.beaconGroup.add(bGreen);

    const bWhite = new THREE.Mesh(beaconBulbGeo, whiteBeamMat);
    bWhite.position.set(0, 0, -1.8);
    this.beaconGroup.add(bWhite);

    towerGroup.add(this.beaconGroup);
    this.group.add(towerGroup);
  }

  buildSurveillanceRadarSite() {
    const radarGroup = new THREE.Group();
    radarGroup.position.set(230, 0, 480);

    // Lattice metal tower
    const latticeGeo = new THREE.CylinderGeometry(2.5, 4.5, 26, 4);
    const latticeMat = new THREE.MeshStandardMaterial({ color: 0x3a4047, wireframe: true });
    const lattice = new THREE.Mesh(latticeGeo, latticeMat);
    lattice.position.y = 13;
    radarGroup.add(lattice);

    // Equipment shelter cabin at base
    const cabinGeo = new THREE.BoxGeometry(10, 5, 8);
    const cabinMat = new THREE.MeshStandardMaterial({ color: 0x475141, roughness: 0.8 });
    const cabin = new THREE.Mesh(cabinGeo, cabinMat);
    cabin.position.y = 2.5;
    radarGroup.add(cabin);

    // Spinning 3D Parabolic Radar Dish
    this.radarDish = new THREE.Group();
    this.radarDish.position.set(0, 27, 0);

    // Curved parabolic reflector dish
    const dishGeo = new THREE.CylinderGeometry(9, 7.5, 3.2, 16, 1, false, 0, Math.PI);
    dishGeo.rotateZ(Math.PI / 2);
    const dishMat = new THREE.MeshStandardMaterial({
      color: 0xdd8800, // Aviation orange
      metalness: 0.7,
      roughness: 0.3,
      side: THREE.DoubleSide
    });
    const dish = new THREE.Mesh(dishGeo, dishMat);
    dish.rotation.y = -Math.PI / 2;
    this.radarDish.add(dish);

    // Waveguide feed horn
    const hornGeo = new THREE.ConeGeometry(0.8, 5, 6);
    hornGeo.rotateX(-Math.PI / 2);
    const horn = new THREE.Mesh(hornGeo, new THREE.MeshStandardMaterial({ color: 0x222222 }));
    horn.position.set(0, 0, 3.8);
    this.radarDish.add(horn);

    radarGroup.add(this.radarDish);
    this.group.add(radarGroup);
  }

  buildSAMMissileBattery() {
    // Air defense Surface-to-Air Missile (SAM) installation
    const samGroup = new THREE.Group();
    samGroup.position.set(-220, 0, 200);

    // Hexagonal defensive berm revetment
    const bermGeo = new THREE.RingGeometry(24, 38, 6);
    bermGeo.rotateX(-Math.PI / 2);
    const bermMat = new THREE.MeshStandardMaterial({ color: 0x3d4332, roughness: 0.95 });
    const berm = new THREE.Mesh(bermGeo, bermMat);
    berm.position.y = 1.2;
    samGroup.add(berm);

    // 2x 4-Canister SAM Launchers angled skyward
    for (let i = 0; i < 2; i++) {
      const lGroup = new THREE.Group();
      lGroup.position.set(-8 + i * 16, 0, 0);

      // Launcher trailer chassis
      const chassis = new THREE.Mesh(
        new THREE.BoxGeometry(7, 2, 14),
        new THREE.MeshStandardMaterial({ color: 0x2e3b2b })
      );
      chassis.position.y = 1.5;
      lGroup.add(chassis);

      // Elevated missile canister rack (angled at 60 deg)
      const rackGroup = new THREE.Group();
      rackGroup.position.set(0, 2.8, -2);
      rackGroup.rotation.x = -Math.PI / 3;

      const canisterGeo = new THREE.CylinderGeometry(0.65, 0.65, 9, 8);
      const canisterMat = new THREE.MeshStandardMaterial({ color: 0x485a44, metalness: 0.4 });
      for (let c = 0; c < 4; c++) {
        const can = new THREE.Mesh(canisterGeo, canisterMat);
        const cx = (c % 2 === 0 ? -0.8 : 0.8);
        const cy = (c < 2 ? 0.8 : -0.8);
        can.position.set(cx, cy, 0);
        rackGroup.add(can);
      }
      lGroup.add(rackGroup);
      samGroup.add(lGroup);
    }

    // Engagement Radar Dome (Dome on trailer)
    const radTrailer = new THREE.Mesh(
      new THREE.BoxGeometry(6, 3, 10),
      new THREE.MeshStandardMaterial({ color: 0x2e3b2b })
    );
    radTrailer.position.set(0, 1.5, -16);
    samGroup.add(radTrailer);

    const radDome = new THREE.Mesh(
      new THREE.SphereGeometry(3.5, 12, 12),
      new THREE.MeshStandardMaterial({ color: 0xdde2dc, roughness: 0.4 })
    );
    radDome.position.set(0, 5.0, -16);
    samGroup.add(radDome);

    this.group.add(samGroup);
  }

  update(dt, viewerPos) {
    // Rotate surveillance radar dish smoothly (15 RPM)
    if (this.radarDish) {
      this.radarDish.rotation.y += 1.57 * dt;
    }
    // Rotate airport beacon
    if (this.beaconGroup) {
      this.beaconGroup.rotation.y += 2.5 * dt;
    }
    // Update PAPI light colors based on viewer glide slope
    if (viewerPos) {
      this.updatePAPI(viewerPos);
    }
  }
}

// --- 3. CARRIER STRIKE GROUP (OFFSHORE NAVAL FLEET) ---
class CarrierStrikeGroup {
  constructor(scene) {
    this.scene = scene;
    this.fleetGroup = new THREE.Group();
    // Position fleet cruising offshore
    this.fleetGroup.position.set(6500, 0, 6200);
    this.fleetHeading = 0.52; // radians heading
    this.fleetGroup.rotation.y = this.fleetHeading;

    this.buildSupercarrier();
    this.buildEscortDestroyer('DDG-109', -950, 400); // Port Escort
    this.buildEscortDestroyer('DDG-112', 950, 450);  // Starboard Escort

    this.scene.add(this.fleetGroup);
  }

  buildSupercarrier() {
    this.cvnGroup = new THREE.Group();
    this.cvnGroup.position.set(0, 0, 0);

    const steelMat = new THREE.MeshStandardMaterial({
      color: 0x353d45, // Haze Gray
      roughness: 0.65,
      metalness: 0.35
    });
    const darkSteelMat = new THREE.MeshStandardMaterial({ color: 0x22262b, roughness: 0.8 });
    const deckMat = new THREE.MeshStandardMaterial({ color: 0x16191c, roughness: 0.92 }); // Non-skid flight deck

    // 1. Lower Hull: 332m long, 40m beam, sheer flare to 78m deck overhang
    const hullGeo = new THREE.BoxGeometry(44, 28, 330);
    const hull = new THREE.Mesh(hullGeo, steelMat);
    hull.position.y = 12;
    this.cvnGroup.add(hull);

    // Bulbous bow & flared forecastle
    const bowGeo = new THREE.ConeGeometry(22, 50, 8);
    bowGeo.rotateZ(Math.PI / 2);
    bowGeo.rotateY(-Math.PI / 2);
    const bow = new THREE.Mesh(bowGeo, steelMat);
    bow.position.set(0, 14, -180);
    this.cvnGroup.add(bow);

    // 2. Flight Deck: 332m length, 78m width, 9.5 deg angled waist deck
    const deckShape = new THREE.Shape();
    deckShape.moveTo(-22, -165);
    deckShape.lineTo(22, -165);  // Bow
    deckShape.lineTo(39, -60);   // Starboard sponson
    deckShape.lineTo(39, 130);   // Starboard aft
    deckShape.lineTo(18, 165);   // Stern starboard
    deckShape.lineTo(-18, 165);  // Stern port
    deckShape.lineTo(-39, 120);  // Port angled landing runout
    deckShape.lineTo(-39, -40);  // Port waist overhang
    deckShape.lineTo(-22, -165);

    const extrudeSettings = { depth: 4.5, bevelEnabled: false };
    const deckGeo = new THREE.ExtrudeGeometry(deckShape, extrudeSettings);
    deckGeo.rotateX(Math.PI / 2);

    const flightDeck = new THREE.Mesh(deckGeo, deckMat);
    flightDeck.position.y = 26;
    this.cvnGroup.add(flightDeck);

    // 3. Flight Deck Markings & Catapults
    const whiteLineMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const yellowLineMat = new THREE.MeshBasicMaterial({ color: 0xffbb00 });
    const redHazardMat = new THREE.MeshBasicMaterial({ color: 0xdd2211 });

    // Angled landing area runway centerline (Angled ~9 deg to port)
    const landingRunway = new THREE.Group();
    landingRunway.position.set(-6, 28.4, 0);
    landingRunway.rotation.y = -0.155; // 9 deg cant

    const runGeo = new THREE.PlaneGeometry(24, 230);
    runGeo.rotateX(-Math.PI / 2);
    const runMat = new THREE.MeshBasicMaterial({ color: 0x111316 });
    const runMesh = new THREE.Mesh(runGeo, runMat);
    landingRunway.add(runMesh);

    // Landing centerline dashed stripes
    const cGeo = new THREE.PlaneGeometry(1.2, 12);
    cGeo.rotateX(-Math.PI / 2);
    for (let z = -90; z <= 100; z += 22) {
      const cLine = new THREE.Mesh(cGeo, yellowLineMat);
      cLine.position.set(0, 0.05, z);
      landingRunway.add(cLine);
    }

    // 4 Arresting Gear Wires stretched across the angled deck
    for (let w = 0; w < 4; w++) {
      const wireGeo = new THREE.CylinderGeometry(0.12, 0.12, 26, 6);
      wireGeo.rotateZ(Math.PI / 2);
      const wire = new THREE.Mesh(wireGeo, new THREE.MeshStandardMaterial({ color: 0x8899aa, metalness: 0.9 }));
      wire.position.set(0, 0.15, 45 + w * 12);
      landingRunway.add(wire);
    }

    this.cvnGroup.add(landingRunway);

    // 4 Catapult Tracks with Jet Blast Deflectors (JBDs)
    // Cats 1 & 2 on Bow, Cats 3 & 4 on Waist
    const catPositions = [
      { x: -7, z: -110, angle: 0, jbdZ: -70 },    // Cat 1 Bow Port
      { x: 10, z: -110, angle: 0, jbdZ: -70 },     // Cat 2 Bow Starboard
      { x: -14, z: -25, angle: -0.155, jbdZ: 10 }, // Cat 3 Waist
      { x: -25, z: -15, angle: -0.155, jbdZ: 20 }  // Cat 4 Waist Outer
    ];

    catPositions.forEach((cat) => {
      const catTrackGeo = new THREE.PlaneGeometry(0.6, 95);
      catTrackGeo.rotateX(-Math.PI / 2);
      const catTrack = new THREE.Mesh(catTrackGeo, whiteLineMat);
      catTrack.position.set(cat.x, 28.45, cat.z);
      catTrack.rotation.y = cat.angle;
      this.cvnGroup.add(catTrack);

      // Jet Blast Deflector (JBD) - Angled cooling panel
      const jbdGeo = new THREE.BoxGeometry(7, 3.5, 0.4);
      jbdGeo.rotateX(-Math.PI / 4);
      const jbd = new THREE.Mesh(jbdGeo, darkSteelMat);
      jbd.position.set(cat.x, 29.2, cat.jbdZ);
      jbd.rotation.y = cat.angle;
      this.cvnGroup.add(jbd);
    });

    // 4. Island Superstructure (Starboard)
    const islandGroup = new THREE.Group();
    islandGroup.position.set(31, 28.5, -20);

    // Multi-tier deckhouse
    const islandLower = new THREE.Mesh(new THREE.BoxGeometry(10, 16, 42), steelMat);
    islandLower.position.y = 8;
    islandGroup.add(islandLower);

    // Navigation Bridge & Pri-Fly (Primary Flight Control)
    const bridge = new THREE.Mesh(new THREE.BoxGeometry(11, 6, 28), darkSteelMat);
    bridge.position.set(-0.5, 17, -4);
    islandGroup.add(bridge);

    // Phased Array Radars (AESA panels on island faces)
    const panelGeo = new THREE.PlaneGeometry(4.5, 4.5);
    const panelMat = new THREE.MeshStandardMaterial({ color: 0x828d96, metalness: 0.5 });
    const forwardPanel = new THREE.Mesh(panelGeo, panelMat);
    forwardPanel.position.set(0, 14, -21.1);
    islandGroup.add(forwardPanel);

    // Main lattice mast & TACAN dome
    const mastGeo = new THREE.CylinderGeometry(0.5, 1.2, 28, 6);
    const mast = new THREE.Mesh(mastGeo, darkSteelMat);
    mast.position.set(0, 30, -5);
    islandGroup.add(mast);

    const tacanDome = new THREE.Mesh(
      new THREE.CylinderGeometry(2, 2, 3, 12),
      new THREE.MeshStandardMaterial({ color: 0xdfe5ea })
    );
    tacanDome.position.set(0, 44, -5);
    islandGroup.add(tacanDome);

    this.cvnGroup.add(islandGroup);

    // 5. 4 Deck-Edge Aircraft Elevators
    const elevGeo = new THREE.BoxGeometry(14, 1.5, 24);
    const elevMat = new THREE.MeshStandardMaterial({ color: 0x22262a });
    const elevPositions = [
      { x: 39, z: -70 },  // Elev 1 Starboard Fwd
      { x: 39, z: 25 },   // Elev 2 Starboard Mid
      { x: 39, z: 95 },   // Elev 3 Starboard Aft
      { x: -38, z: 65 }   // Elev 4 Port Aft
    ];
    elevPositions.forEach(ep => {
      const el = new THREE.Mesh(elevGeo, elevMat);
      el.position.set(ep.x, 27, ep.z);
      this.cvnGroup.add(el);
    });

    // 6. Perimeter Deck Safety Lights (Green threshold bar & amber boundary lights)
    const greenLightMat = new THREE.MeshBasicMaterial({ color: 0x00ff44 });
    const amberLightMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 });
    const dotGeo = new THREE.SphereGeometry(0.45, 4, 4);

    for (let z = 140; z <= 165; z += 5) {
      const g = new THREE.Mesh(dotGeo, greenLightMat);
      g.position.set(-6, 28.5, z);
      this.cvnGroup.add(g);
    }
    for (let z = -140; z <= 140; z += 25) {
      const aL = new THREE.Mesh(dotGeo, amberLightMat);
      aL.position.set(-37, 28.5, z);
      this.cvnGroup.add(aL);

      const aR = new THREE.Mesh(dotGeo, amberLightMat);
      aR.position.set(37, 28.5, z);
      this.cvnGroup.add(aR);
    }

    // 7. Stern Foaming Wake Mesh
    const wakeGeo = new THREE.PlaneGeometry(55, 380);
    wakeGeo.rotateX(-Math.PI / 2);
    const wakeMat = new THREE.MeshBasicMaterial({
      color: 0xcde8ff,
      transparent: true,
      opacity: 0.35
    });
    const wake = new THREE.Mesh(wakeGeo, wakeMat);
    wake.position.set(0, 0.2, 340);
    this.cvnGroup.add(wake);

    this.fleetGroup.add(this.cvnGroup);
  }

  buildEscortDestroyer(pennant, offsetX, offsetZ) {
    // Arleigh Burke-class Flight IIA Guided Missile Destroyer (DDG)
    // Scale: 155m length, 20m beam
    const ddgGroup = new THREE.Group();
    ddgGroup.position.set(offsetX, 0, offsetZ);

    const hazeMat = new THREE.MeshStandardMaterial({ color: 0x48525b, roughness: 0.6, metalness: 0.3 });
    const deckMat = new THREE.MeshStandardMaterial({ color: 0x272d33, roughness: 0.85 });
    const darkMat = new THREE.MeshStandardMaterial({ color: 0x1d2226, roughness: 0.7 });

    // 1. Sleek flared stealth hull
    const hullGeo = new THREE.BoxGeometry(19, 12, 150);
    const hull = new THREE.Mesh(hullGeo, hazeMat);
    hull.position.y = 5.5;
    ddgGroup.add(hull);

    // Knife bow
    const bowGeo = new THREE.ConeGeometry(9.5, 35, 6);
    bowGeo.rotateZ(Math.PI / 2);
    bowGeo.rotateY(-Math.PI / 2);
    const bow = new THREE.Mesh(bowGeo, hazeMat);
    bow.position.set(0, 6.5, -80);
    ddgGroup.add(bow);

    // Weather deck
    const wDeckGeo = new THREE.PlaneGeometry(18.5, 148);
    wDeckGeo.rotateX(-Math.PI / 2);
    const wDeck = new THREE.Mesh(wDeckGeo, deckMat);
    wDeck.position.y = 11.6;
    ddgGroup.add(wDeck);

    // 2. Faceted Deckhouse with 4 AN/SPY-1D Phased Array Radar faces
    const bridgeGeo = new THREE.BoxGeometry(14, 11, 28);
    const bridge = new THREE.Mesh(bridgeGeo, hazeMat);
    bridge.position.set(0, 16.5, -24);
    ddgGroup.add(bridge);

    // Octagonal SPY radar face panels (Forward, Starboard, Port, Aft)
    const spyMat = new THREE.MeshStandardMaterial({ color: 0x939ea8, roughness: 0.3 });
    const spyGeo = new THREE.BoxGeometry(4.2, 4.2, 0.4);
    
    const spyFwd = new THREE.Mesh(spyGeo, spyMat);
    spyFwd.position.set(0, 18, -38.2);
    ddgGroup.add(spyFwd);

    const spyPort = new THREE.Mesh(spyGeo, spyMat);
    spyPort.rotation.y = Math.PI / 2;
    spyPort.position.set(-7.1, 18, -25);
    ddgGroup.add(spyPort);

    const spyStbd = new THREE.Mesh(spyGeo, spyMat);
    spyStbd.rotation.y = -Math.PI / 2;
    spyStbd.position.set(7.1, 18, -25);
    ddgGroup.add(spyStbd);

    // 3. Mk 45 5-inch (127mm) / 62 Caliber Naval Gun Turret on Foredeck
    const turretGeo = new THREE.BoxGeometry(4.5, 3, 5.5);
    const turret = new THREE.Mesh(turretGeo, hazeMat);
    turret.position.set(0, 13.2, -54);

    const barrelGeo = new THREE.CylinderGeometry(0.2, 0.25, 9, 8);
    barrelGeo.rotateX(-Math.PI / 2.2); // slight elevation
    const barrel = new THREE.Mesh(barrelGeo, darkMat);
    barrel.position.set(0, 0.8, -4.5);
    turret.add(barrel);
    ddgGroup.add(turret);

    // 4. Mk 41 Vertical Launch System (VLS) 32-cell forward missile deck
    const vlsFwdGeo = new THREE.PlaneGeometry(5.5, 8.5);
    vlsFwdGeo.rotateX(-Math.PI / 2);
    const vlsMat = new THREE.MeshStandardMaterial({ color: 0x1f2326, roughness: 0.5 });
    const vlsFwd = new THREE.Mesh(vlsFwdGeo, vlsMat);
    vlsFwd.position.set(0, 11.7, -42);
    ddgGroup.add(vlsFwd);

    // 5. Aft VLS (64 cells) & Dual Helicopter Hangar
    const hangarGeo = new THREE.BoxGeometry(14, 8, 22);
    const hangar = new THREE.Mesh(hangarGeo, hazeMat);
    hangar.position.set(0, 15, 20);
    ddgGroup.add(hangar);

    const vlsAft = new THREE.Mesh(new THREE.PlaneGeometry(6, 12).rotateX(-Math.PI / 2), vlsMat);
    vlsAft.position.set(0, 19.1, 20);
    ddgGroup.add(vlsAft);

    // 6. Helipad on Stern with Landing Circle
    const heliDeckGeo = new THREE.PlaneGeometry(16, 32);
    heliDeckGeo.rotateX(-Math.PI / 2);
    const heliDeck = new THREE.Mesh(heliDeckGeo, deckMat);
    heliDeck.position.set(0, 11.65, 52);
    ddgGroup.add(heliDeck);

    const circleGeo = new THREE.RingGeometry(4.5, 5.2, 24);
    circleGeo.rotateX(-Math.PI / 2);
    const circle = new THREE.Mesh(circleGeo, new THREE.MeshBasicMaterial({ color: 0xffffff }));
    circle.position.set(0, 11.7, 52);
    ddgGroup.add(circle);

    // 7. Raked mainmast with radar antennas
    const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.8, 18, 6), darkMat);
    mast.position.set(0, 27, -15);
    mast.rotation.x = 0.15;
    ddgGroup.add(mast);

    // 8. Destroyer Foaming Stern Wake
    const wake = new THREE.Mesh(
      new THREE.PlaneGeometry(24, 180).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: 0xcde8ff, transparent: true, opacity: 0.35 })
    );
    wake.position.set(0, 0.2, 160);
    ddgGroup.add(wake);

    this.fleetGroup.add(ddgGroup);
  }

  update(dt) {
    // Fleet slowly cruises forward through ocean swells (12 knots ~ 6.2 m/s)
    const fwd = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), this.fleetHeading);
    this.fleetGroup.position.addScaledVector(fwd, 6.2 * dt);
  }
}

// --- 4. INTERACTIVE DESTRUCTIBLE TARGETS & HIT DETECTION ---
class TargetSystem {
  constructor(scene, terrain) {
    this.scene = scene;
    this.terrain = terrain;
    this.targets = [];
    this.explosions = [];
    this.smokePlumes = [];
    this.score = 0;
    this.targetsDestroyed = 0;

    // Shared geometry & materials for explosions & effects
    this.explosionGeo = new THREE.SphereGeometry(1, 16, 16);
    this.smokeGeo = new THREE.DodecahedronGeometry(1, 1);

    this.buildTargets();
    this.createUIBanner();
  }

  createUIBanner() {
    this.banner = document.createElement('div');
    this.banner.id = 'combat-kill-banner';
    this.banner.style.position = 'absolute';
    this.banner.style.top = '14%';
    this.banner.style.left = '50%';
    this.banner.style.transform = 'translateX(-50%)';
    this.banner.style.color = '#ff3b30';
    this.banner.style.fontFamily = "'Share Tech Mono', 'Consolas', monospace";
    this.banner.style.fontSize = '24px';
    this.banner.style.fontWeight = 'bold';
    this.banner.style.letterSpacing = '3px';
    this.banner.style.textShadow = '0 0 16px rgba(255, 40, 40, 0.9)';
    this.banner.style.opacity = '0';
    this.banner.style.pointerEvents = 'none';
    this.banner.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
    this.banner.style.zIndex = '1000';
    document.body.appendChild(this.banner);
  }

  showNotification(text) {
    if (!this.banner) return;
    this.banner.innerText = text;
    this.banner.style.opacity = '1';
    this.banner.style.transform = 'translateX(-50%) scale(1.15)';
    setTimeout(() => {
      this.banner.style.opacity = '0';
      this.banner.style.transform = 'translateX(-50%) scale(1.0)';
    }, 2800);
  }

  buildTargets() {
    // 1. Offshore Naval Drone Target Vessels (Fast patrol boats in ocean waters)
    this.createNavalDroneTarget('TARGET BOAT T-01', 3200, 2400);
    this.createNavalDroneTarget('TARGET BOAT T-02', -4200, 3600);

    // 2. Mountain Radar Station Bunkers (Strategic targets perched on peaks)
    const mtn1H = this.terrain ? this.terrain.getHeight(6600, -4200) : 620;
    this.createMountainRadarTarget('RADAR BKT ECHO', 6600, -4200, mtn1H);

    const mtn2H = this.terrain ? this.terrain.getHeight(-7000, -6200) : 850;
    this.createMountainRadarTarget('MOUNTAIN POST OMEGA', -7000, -6200, mtn2H);

    // 3. Coastal Air Defense Radar Target
    const coastH = this.terrain ? this.terrain.getHeight(-2400, 1600) : 18;
    this.createCoastalBunkerTarget('COASTAL BATTERY RED', -2400, 1600, coastH);
  }

  createNavalDroneTarget(name, x, z) {
    const group = new THREE.Group();
    group.position.set(x, 1.2, z);

    // Drone hull (Red/Orange high-visibility target vessel)
    const hullGeo = new THREE.BoxGeometry(8, 2.5, 24);
    const hullMat = new THREE.MeshStandardMaterial({ color: 0xcc2211, roughness: 0.5 });
    const hull = new THREE.Mesh(hullGeo, hullMat);
    group.add(hull);

    // Radar reflector target mast (octahedral radar return enhancer)
    const mast = new THREE.Mesh(
      new THREE.CylinderGeometry(0.2, 0.3, 8, 6),
      new THREE.MeshStandardMaterial({ color: 0x111111 })
    );
    mast.position.set(0, 4.5, 0);
    group.add(mast);

    const reflector = new THREE.Mesh(
      new THREE.OctahedronGeometry(1.8),
      new THREE.MeshStandardMaterial({ color: 0xffcc00, metalness: 0.8, roughness: 0.2 })
    );
    reflector.position.set(0, 8.5, 0);
    group.add(reflector);

    this.scene.add(group);

    this.targets.push({
      id: 'target_' + this.targets.length,
      name: name,
      type: 'NAVAL_DRONE',
      group: group,
      position: group.position,
      radius: 12.0,
      hp: 80,
      maxHp: 80,
      alive: true,
      points: 750
    });
  }

  createMountainRadarTarget(name, x, z, y) {
    const group = new THREE.Group();
    group.position.set(x, y, z);

    // Hardened hexagonal concrete bunker
    const bunker = new THREE.Mesh(
      new THREE.CylinderGeometry(14, 18, 9, 6),
      new THREE.MeshStandardMaterial({ color: 0x4a4f47, roughness: 0.9 })
    );
    bunker.position.y = 4.5;
    group.add(bunker);

    // Geodesic Golf-Ball Radar Dome (Radome)
    const domeMat = new THREE.MeshStandardMaterial({
      color: 0xded8c8,
      roughness: 0.5,
      metalness: 0.1
    });
    const dome = new THREE.Mesh(new THREE.SphereGeometry(9, 16, 14), domeMat);
    dome.position.y = 13.5;
    group.add(dome);

    // Communications dish tower
    const commMast = new THREE.Mesh(
      new THREE.CylinderGeometry(0.4, 0.8, 18, 6),
      new THREE.MeshStandardMaterial({ color: 0x222222 })
    );
    commMast.position.set(10, 9, 0);
    group.add(commMast);

    this.scene.add(group);

    this.targets.push({
      id: 'target_' + this.targets.length,
      name: name,
      type: 'MOUNTAIN_RADAR',
      group: group,
      position: group.position,
      radius: 18.0,
      hp: 150,
      maxHp: 150,
      alive: true,
      points: 1200
    });
  }

  createCoastalBunkerTarget(name, x, z, y) {
    const group = new THREE.Group();
    group.position.set(x, y, z);

    const bunker = new THREE.Mesh(
      new THREE.BoxGeometry(22, 7, 22),
      new THREE.MeshStandardMaterial({ color: 0x3e453c, roughness: 0.9 })
    );
    bunker.position.y = 3.5;
    group.add(bunker);

    const radDome = new THREE.Mesh(
      new THREE.SphereGeometry(6, 12, 10),
      new THREE.MeshStandardMaterial({ color: 0xe0e0e0 })
    );
    radDome.position.y = 10;
    group.add(radDome);

    this.scene.add(group);

    this.targets.push({
      id: 'target_' + this.targets.length,
      name: name,
      type: 'SAM_RADAR',
      group: group,
      position: group.position,
      radius: 16.0,
      hp: 120,
      maxHp: 120,
      alive: true,
      points: 1000
    });
  }

  // Hit detection checked against combat tracers and missiles
  checkHits(tracers, missiles) {
    for (let t = 0; t < this.targets.length; t++) {
      const tgt = this.targets[t];
      if (!tgt.alive) continue;

      // 1. Check Gun Tracers (25mm Cannon)
      if (tracers && tracers.length > 0) {
        for (let i = tracers.length - 1; i >= 0; i--) {
          const tr = tracers[i];
          const dist = tr.mesh.position.distanceTo(tgt.position);
          if (dist < tgt.radius) {
            tgt.hp -= 20; // 20 damage per 25mm round
            this.spawnImpactSparks(tr.mesh.position);

            // Remove tracer
            this.scene.remove(tr.mesh);
            tracers.splice(i, 1);

            if (tgt.hp <= 0) {
              this.destroyTarget(tgt);
              break;
            }
          }
        }
      }

      // 2. Check AIM-120 AMRAAM Missiles
      if (missiles && missiles.length > 0) {
        for (let i = missiles.length - 1; i >= 0; i--) {
          const m = missiles[i];
          const dist = m.mesh.position.distanceTo(tgt.position);
          if (dist < tgt.radius + 6.0) {
            tgt.hp -= 150; // Direct missile hit
            this.triggerExplosion(m.mesh.position, 28.0);

            // Remove missile
            this.scene.remove(m.mesh);
            m.mesh.traverse((child) => {
              if (child.isMesh) {
                if (child.geometry) child.geometry.dispose();
                if (child.material) child.material.dispose();
              }
            });
            missiles.splice(i, 1);

            if (tgt.hp <= 0) {
              this.destroyTarget(tgt);
              break;
            }
          }
        }
      }
    }
  }

  spawnImpactSparks(pos) {
    const flash = new THREE.Mesh(
      new THREE.SphereGeometry(2.5, 6, 6),
      new THREE.MeshBasicMaterial({ color: 0xffdd44, transparent: true, opacity: 0.9 })
    );
    flash.position.copy(pos);
    this.scene.add(flash);
    this.explosions.push({ mesh: flash, age: 0, maxAge: 0.15, maxScale: 3 });
  }

  destroyTarget(tgt) {
    tgt.alive = false;
    this.targetsDestroyed++;
    this.score += tgt.points;

    // Trigger massive primary & secondary fireball
    this.triggerExplosion(tgt.position, 34.0);

    // Replace target structure with burnt scorched wreckage
    tgt.group.traverse(child => {
      if (child.isMesh && child.material) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0x111111,
          roughness: 0.95
        });
      }
    });

    // Spawn persistent billowing smoke plume
    this.createSmokePlume(tgt.position);

    // Announce kill banner
    this.showNotification(`TARGET DESTROYED: ${tgt.name} [+${tgt.points} PTS]`);
  }

  triggerExplosion(pos, maxRadius = 30.0) {
    // 1. Brilliant expanding fireball
    const expMat = new THREE.MeshBasicMaterial({
      color: 0xff5500,
      transparent: true,
      opacity: 0.95
    });
    const expMesh = new THREE.Mesh(this.explosionGeo, expMat);
    expMesh.position.copy(pos);
    this.scene.add(expMesh);

    this.explosions.push({
      mesh: expMesh,
      age: 0,
      maxAge: 1.2,
      maxScale: maxRadius
    });

    // 2. Shockwave blast ring
    const ringGeo = new THREE.RingGeometry(1, 2.5, 24);
    ringGeo.rotateX(-Math.PI / 2);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.8,
      side: THREE.DoubleSide
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.position.copy(pos).add(new THREE.Vector3(0, 1.0, 0));
    this.scene.add(ring);

    this.explosions.push({
      mesh: ring,
      age: 0,
      maxAge: 0.85,
      maxScale: maxRadius * 2.2
    });
  }

  createSmokePlume(pos) {
    const plume = {
      pos: pos.clone(),
      particles: [],
      spawnTimer: 0,
      duration: 40.0 // burns for 40 seconds
    };
    this.smokePlumes.push(plume);
  }

  update(dt) {
    // Animate explosions
    for (let i = this.explosions.length - 1; i >= 0; i--) {
      const exp = this.explosions[i];
      exp.age += dt;
      const progress = exp.age / exp.maxAge;

      exp.mesh.scale.setScalar(1.0 + progress * exp.maxScale);
      exp.mesh.material.opacity = Math.max(0, (1.0 - progress) * 0.95);

      if (exp.age >= exp.maxAge) {
        this.scene.remove(exp.mesh);
        if (exp.mesh.geometry) exp.mesh.geometry.dispose();
        if (exp.mesh.material) exp.mesh.material.dispose();
        this.explosions.splice(i, 1);
      }
    }

    // Animate and spawn rising smoke plumes from destroyed targets
    for (let p = this.smokePlumes.length - 1; p >= 0; p--) {
      const plume = this.smokePlumes[p];
      plume.duration -= dt;
      plume.spawnTimer -= dt;

      if (plume.spawnTimer <= 0 && plume.duration > 0) {
        plume.spawnTimer = 0.12; // spawn new puff
        const smokeMat = new THREE.MeshBasicMaterial({
          color: 0x1f2124,
          transparent: true,
          opacity: 0.6
        });
        const puff = new THREE.Mesh(this.smokeGeo, smokeMat);
        puff.position.copy(plume.pos).add(new THREE.Vector3(
          (Math.random() - 0.5) * 5,
          Math.random() * 3,
          (Math.random() - 0.5) * 5
        ));
        puff.scale.setScalar(4 + Math.random() * 3);
        this.scene.add(puff);

        plume.particles.push({
          mesh: puff,
          age: 0,
          maxAge: 5.5,
          velY: 18 + Math.random() * 8,
          driftX: 5.0 + Math.random() * 3.0
        });
      }

      // Update existing smoke puffs
      for (let k = plume.particles.length - 1; k >= 0; k--) {
        const sm = plume.particles[k];
        sm.age += dt;
        const progress = sm.age / sm.maxAge;
        sm.mesh.position.y += sm.velY * dt;
        sm.mesh.position.x += sm.driftX * dt;
        sm.mesh.scale.setScalar(4.0 + progress * 24.0);
        sm.mesh.material.opacity = Math.max(0, (1.0 - progress) * 0.6);

        if (sm.age >= sm.maxAge) {
          this.scene.remove(sm.mesh);
          if (sm.mesh.material) sm.mesh.material.dispose();
          plume.particles.splice(k, 1);
        }
      }

      if (plume.duration <= 0 && plume.particles.length === 0) {
        this.smokePlumes.splice(p, 1);
      }
    }
  }
}

// --- 5. OCEAN & ATMOSPHERE (WITH SPECULAR GLINT & SOFT CLOUDS) ---
class OceanAtmosphere {
  constructor(scene) {
    this.scene = scene;
    this.cloudClusters = [];

    this.buildSkyAndLighting();
    this.buildOceanShader();
    this.buildMultiLayerClouds();
  }

  buildSkyAndLighting() {
    // Atmospheric Scattering Sky Dome
    const vertexShader = `
      varying vec3 vWorldPosition;
      void main() {
        vec4 worldPosition = modelMatrix * vec4(position, 1.0);
        vWorldPosition = worldPosition.xyz;
        gl_Position = projectionMatrix * viewMatrix * worldPosition;
      }
    `;
    const fragmentShader = `
      uniform vec3 topColor;
      uniform vec3 horizonColor;
      uniform vec3 bottomColor;
      uniform vec3 sunPosition;
      varying vec3 vWorldPosition;
      void main() {
        vec3 dir = normalize(vWorldPosition);
        float h = dir.y;
        vec3 sky = (h > 0.0)
          ? mix(horizonColor, topColor, max(pow(max(h, 0.0), 0.55), 0.0))
          : mix(horizonColor, bottomColor, -h);
        
        // Sun disc & atmospheric solar glow
        float sunGlow = max(dot(dir, normalize(sunPosition)), 0.0);
        sky += vec3(1.0, 0.85, 0.6) * pow(sunGlow, 32.0) * 0.55;
        sky += vec3(1.0, 0.95, 0.85) * pow(sunGlow, 256.0) * 1.2;

        gl_FragColor = vec4(sky, 1.0);
      }
    `;

    const skyGeo = new THREE.SphereGeometry(32000, 32, 16);
    this.skyMat = new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms: {
        topColor: { value: new THREE.Color(0x0c3b75) },
        horizonColor: { value: new THREE.Color(0x8cbce3) },
        bottomColor: { value: new THREE.Color(0x071e36) },
        sunPosition: { value: new THREE.Vector3(4500, 5200, 3000) }
      },
      side: THREE.BackSide,
      depthWrite: false
    });
    this.sky = new THREE.Mesh(skyGeo, this.skyMat);
    this.scene.add(this.sky);

    // Sunlight with realistic high-altitude intensity & shadows
    this.sunLight = new THREE.DirectionalLight(0xfff6eb, 2.3);
    this.sunLight.position.set(4500, 5200, 3000);
    this.scene.add(this.sunLight);

    const hemiLight = new THREE.HemisphereLight(0x8cbce3, 0x14283c, 0.85);
    this.scene.add(hemiLight);

    // Atmospheric fog blending smoothly into horizon
    this.scene.fog = new THREE.FogExp2(0x8cbce3, 0.000028);
  }

  buildOceanShader() {
    // 80,000 m Endless Ocean Plane
    const oceanGeo = new THREE.PlaneGeometry(80000, 80000, 16, 16);
    oceanGeo.rotateX(-Math.PI / 2);

    // Procedural wave normal map canvas
    const waveCanvas = document.createElement('canvas');
    waveCanvas.width = 512;
    waveCanvas.height = 512;
    const wCtx = waveCanvas.getContext('2d');
    wCtx.fillStyle = '#0a2a4c';
    wCtx.fillRect(0, 0, 512, 512);

    // Multi-directional ocean ripples & wave crests
    for (let i = 0; i < 600; i++) {
      const alpha = 0.15 + Math.random() * 0.3;
      wCtx.fillStyle = `rgba(28, 85, 138, ${alpha})`;
      const wx = Math.random() * 512;
      const wy = Math.random() * 512;
      const len = 12 + Math.random() * 26;
      const thk = 2 + Math.random() * 4;
      wCtx.beginPath();
      wCtx.ellipse(wx, wy, len, thk, Math.PI / 4 + (Math.random() - 0.5) * 0.4, 0, Math.PI * 2);
      wCtx.fill();
    }

    this.oceanTex = new THREE.CanvasTexture(waveCanvas);
    this.oceanTex.wrapS = THREE.RepeatWrapping;
    this.oceanTex.wrapT = THREE.RepeatWrapping;
    this.oceanTex.repeat.set(240, 240);

    const oceanMat = new THREE.MeshStandardMaterial({
      map: this.oceanTex,
      color: 0x0c375e,
      roughness: 0.1,
      metalness: 0.88
    });

    this.ocean = new THREE.Mesh(oceanGeo, oceanMat);
    this.ocean.position.y = 0;
    this.scene.add(this.ocean);
  }

  buildMultiLayerClouds() {
    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.95,
      transparent: true,
      opacity: 0.58,
      depthWrite: false
    });

    const puffGeo = new THREE.SphereGeometry(1, 10, 8);

    // Tier 1: Mid-altitude fluffy cumulus clusters (1,200m - 2,000m)
    for (let i = 0; i < 42; i++) {
      const cluster = new THREE.Group();
      const cx = (Math.random() - 0.5) * 36000;
      const cy = 1300 + Math.random() * 700;
      const cz = (Math.random() - 0.5) * 36000;
      cluster.position.set(cx, cy, cz);

      const count = 6 + Math.floor(Math.random() * 6);
      for (let p = 0; p < count; p++) {
        const puff = new THREE.Mesh(puffGeo, cloudMat);
        const rad = 160 + Math.random() * 160;
        puff.scale.set(rad, rad * 0.45, rad);
        puff.position.set(
          (Math.random() - 0.5) * 320,
          (Math.random() - 0.5) * 60,
          (Math.random() - 0.5) * 320
        );
        cluster.add(puff);
      }
      this.cloudClusters.push(cluster);
      this.scene.add(cluster);
    }

    // Tier 2: High-altitude thin cirrus sheets (4,500m - 5,500m)
    const cirrusMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.25,
      depthWrite: false
    });
    for (let i = 0; i < 18; i++) {
      const sheet = new THREE.Mesh(new THREE.PlaneGeometry(3500, 1800), cirrusMat);
      sheet.rotateX(-Math.PI / 2);
      sheet.position.set(
        (Math.random() - 0.5) * 40000,
        4600 + Math.random() * 800,
        (Math.random() - 0.5) * 40000
      );
      this.cloudClusters.push(sheet);
      this.scene.add(sheet);
    }
  }

  update(cameraPos, jetPos, dt) {
    if (this.sky) {
      this.sky.position.copy(cameraPos);
    }
    if (this.ocean) {
      this.ocean.position.x = jetPos.x;
      this.ocean.position.z = jetPos.z;
      // Animate wave texture UV coordinates for flowing water motion
      this.oceanTex.offset.x = (jetPos.x / 80000) * 240 + performance.now() * 0.000015;
      this.oceanTex.offset.y = (jetPos.z / 80000) * 240 + performance.now() * 0.000012;
    }

    // Clouds drift slowly with the wind
    const windSpeed = 12 * dt;
    for (let i = 0; i < this.cloudClusters.length; i++) {
      const cl = this.cloudClusters[i];
      cl.position.x += windSpeed;
      if (cl.position.x > 20000) cl.position.x = -20000;
    }
  }
}

// --- 6. MASTER ORCHESTRATOR: UPGRADED WORLD ENVIRONMENT ---
class UpgradedWorldEnvironment {
  constructor(scene) {
    this.scene = scene;

    // 1. Procedural Archipelago & Mountains
    this.terrain = new ProceduralArchipelago(scene);

    // 2. Military Airbase Complex
    this.airbase = new MilitaryAirbase(scene, this.terrain.airbasePlateauY);

    // 3. Carrier Strike Group (CVN Supercarrier + 2 Aegis Destroyers)
    this.carrierGroup = new CarrierStrikeGroup(scene);

    // 4. Interactive Destructible Targets & Combat Hit Tracking
    this.targets = new TargetSystem(scene, this.terrain);

    // 5. Ocean & Atmosphere with Specular Glint & Clouds
    this.atmosphere = new OceanAtmosphere(scene);
  }

  // Master update tick called from main simulation loop
  update(cameraPos, jetPos, dt = 0.016, combatSystem = null) {
    // 1. Atmosphere & Ocean updates
    this.atmosphere.update(cameraPos, jetPos, dt);

    // 2. Airbase beacon, radar & dynamic PAPI lights
    this.airbase.update(dt, jetPos);

    // 3. Carrier Strike Group formation cruise
    this.carrierGroup.update(dt);

    // 4. Combat Hit Detection & Target explosions
    if (combatSystem) {
      this.targets.checkHits(combatSystem.tracers, combatSystem.missiles);
    }
    this.targets.update(dt);
  }
}

// Export classes to global window scope for integration
window.ProceduralArchipelago = ProceduralArchipelago;
window.MilitaryAirbase = MilitaryAirbase;
window.CarrierStrikeGroup = CarrierStrikeGroup;
window.TargetSystem = TargetSystem;
window.OceanAtmosphere = OceanAtmosphere;
window.UpgradedWorldEnvironment = UpgradedWorldEnvironment;

// Integration helper to upgrade existing running App instance
window.integrateWorldUpgrade = function(app) {
  if (!app || !app.scene) {
    console.error('integrateWorldUpgrade: valid App instance with scene required.');
    return;
  }

  console.log('[WorldUpgrade] Upgrading simulation world to full Archipelago & Fleet...');

  // Safely remove previous environment meshes if existing
  if (app.environment) {
    if (app.environment.sky) app.scene.remove(app.environment.sky);
    if (app.environment.ocean) app.scene.remove(app.environment.ocean);
    if (app.environment.sunLight) app.scene.remove(app.environment.sunLight);
  }

  // Instantiate master upgraded world
  app.environment = new UpgradedWorldEnvironment(app.scene);
  app.terrain = app.environment.terrain;
  app.targets = app.environment.targets;

  // Enhance combat update loop to feed bullets and missiles into target hit detection
  const originalCombatUpdate = app.combat.update.bind(app.combat);
  app.combat.update = function(dt) {
    // Run target collision checks
    if (app.targets) {
      app.targets.checkHits(app.combat.tracers, app.combat.missiles);
      app.targets.update(dt);
    }
    originalCombatUpdate(dt);
  };

  // Enhance main environment update
  app.environment.update = function(cameraPos, jetPos, dt = 0.016) {
    UpgradedWorldEnvironment.prototype.update.call(this, cameraPos, jetPos, dt, app.combat);
  };

  console.log('[WorldUpgrade] World upgrade and Carrier Strike Group integration complete!');
};

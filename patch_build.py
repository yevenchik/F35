import os

build_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\build_simulation.py"

with open(build_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update terrain elevation logic
old_terrain = """          let elev = (n1 + n2 + n3 + 150) * islandMask;

          // Flatten runway airbase area
          if (Math.abs(x) < 260 && Math.abs(z + 2000) < 1800) {
            elev = 35.8;
          } else if (islandMask < 0.05) {
            elev = -75.0; // Submerged deep seabed (prevents water z-fighting)
          } else if (elev < 1.5) {
            elev = -40.0 * (1.0 - Math.max(0, elev / 1.5));
          }

          pos.setY(i, elev);

          // Biome vertex coloring
          if (elev < 0.5) {
            color.setHex(0x0a2238); // Underwater reef / ocean trench
          } else if (elev < 10) {
            color.setHex(0xdcc79c); // Golden sand beach
          } else if (elev < 170) {
            color.setHex(0x2d5a28); // Lush green valley
          } else if (elev < 330) {
            color.setHex(0x454e47); // Rocky granite slopes
          } else {
            color.setHex(0xf0f5fa); // Snow dusting on mountain peaks
          }"""

new_terrain = """          // Raised landmass base elevation that smoothly descends into ocean
          const landBase = (islandMask > 0.08) ? (160 * Math.pow(islandMask, 0.75)) : -55;
          let elev = landBase + (n1 + n2 + n3) * islandMask;

          // Flatten runway airbase area
          if (Math.abs(x) < 260 && Math.abs(z + 2000) < 1800) {
            elev = 35.8;
          } else if (islandMask <= 0.08) {
            elev = -65.0; // Deep ocean seabed
          } else if (elev < 1.0) {
            elev = -35.0 * (1.0 - Math.max(0, elev / 1.0));
          }

          pos.setY(i, elev);

          // Biome vertex coloring
          if (elev < 0.5) {
            color.setHex(0x0c2540); // Deep ocean seabed
          } else if (elev < 12) {
            color.setHex(0xdcc79c); // Golden sand beach
          } else if (elev < 170) {
            color.setHex(0x2d5a28); // Lush green valley
          } else if (elev < 330) {
            color.setHex(0x454e47); // Rocky granite slopes
          } else {
            color.setHex(0xf0f5fa); // Snow dusting on mountain peaks
          }"""

assert old_terrain in content, "old_terrain not found"
content = content.replace(old_terrain, new_terrain, 1)

# Update Cockpit Cam position
old_cam = """        } else if (this.cameraMode === 1) {
          // Cockpit / HMDS Cam (Pilot Eye Level with Glare Shield & PCD Avionics)
          const cockpitPos = jetPos.clone()
            .add(up.clone().multiplyScalar(0.92))
            .add(forward.clone().multiplyScalar(2.7));
          this.camera.position.copy(cockpitPos);
          const lookTarget = cockpitPos.clone().add(forward.clone().multiplyScalar(200)).add(up.clone().multiplyScalar(-0.05));
          this.camera.lookAt(lookTarget);"""

new_cam = """        } else if (this.cameraMode === 1) {
          // Cockpit / HMDS Cam (Framed directly through HUD forward windscreen)
          const cockpitPos = jetPos.clone()
            .add(up.clone().multiplyScalar(1.02))
            .add(forward.clone().multiplyScalar(4.0));
          this.camera.position.copy(cockpitPos);
          const lookTarget = cockpitPos.clone().add(forward.clone().multiplyScalar(200)).add(up.clone().multiplyScalar(-0.02));
          this.camera.lookAt(lookTarget);"""

assert old_cam in content, "old_cam not found"
content = content.replace(old_cam, new_cam, 1)

with open(build_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("patch_build.py: Applied terrain and cockpit camera refinements successfully.")


import os

build_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\build_simulation.py"

with open(build_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix flipped nose cone and pitot position
old_nose = """        // 1. Nose Radome & Continuous Chine Forebody
        const noseGeo = new THREE.ConeGeometry(0.9, 3.8, 8);
        noseGeo.rotateX(-Math.PI / 2);
        noseGeo.scale(1.15, 0.65, 1.0);
        const nose = new THREE.Mesh(noseGeo, this.bodyMaterial);
        nose.position.set(0, 0.1, 6.2);
        m.add(nose);

        // Pitot boom
        const pitot = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.03, 0.8, 6), this.darkAccentMaterial);
        pitot.rotation.x = Math.PI / 2;
        pitot.position.set(0, 0.1, 8.2);
        m.add(pitot);"""

new_nose = """        // 1. Nose Radome & Continuous Chine Forebody (Properly oriented forward +Z)
        const noseGeo = new THREE.ConeGeometry(0.9, 3.8, 8);
        noseGeo.rotateX(Math.PI / 2); // Point sharp tip forward along +Z
        noseGeo.scale(1.15, 0.65, 1.0);
        const nose = new THREE.Mesh(noseGeo, this.bodyMaterial);
        nose.position.set(0, 0.1, 6.2);
        m.add(nose);

        // Pitot boom protruding from sharp radome tip
        const pitot = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.03, 0.8, 6), this.darkAccentMaterial);
        pitot.rotation.x = Math.PI / 2;
        pitot.position.set(0, 0.1, 8.4);
        m.add(pitot);"""

assert old_nose in content, "old_nose not found"
content = content.replace(old_nose, new_nose, 1)

# 2. Upgrade CombatSystem tracers & muzzle flash
old_combat = """        this.tracerGeo = new THREE.CylinderGeometry(0.12, 0.12, 3.2, 6).rotateX(Math.PI / 2);
        this.tracerMat = new THREE.MeshBasicMaterial({ color: 0xffeedd });

        this.flareGeo = new THREE.SphereGeometry(0.35, 8, 8);
        this.flareMat = new THREE.MeshBasicMaterial({ color: 0xffaa22 });

        this.explosionGeo = new THREE.SphereGeometry(18, 12, 12);
        this.explosionMat = new THREE.MeshBasicMaterial({ color: 0xff5500, transparent: true, opacity: 0.95 });
      }

      fireGun() {
        sound.playGunfire();
        const jetPos = this.aircraft.group.position;
        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.aircraft.group.quaternion);
        const up = new THREE.Vector3(0, 1, 0).applyQuaternion(this.aircraft.group.quaternion);
        const right = new THREE.Vector3(1, 0, 0).applyQuaternion(this.aircraft.group.quaternion);

        const gunPos = jetPos.clone()
          .add(right.clone().multiplyScalar(-1.1))
          .add(up.clone().multiplyScalar(0.45))
          .add(forward.clone().multiplyScalar(2.8));

        const tracer = new THREE.Mesh(this.tracerGeo, this.tracerMat);
        tracer.position.copy(gunPos);
        tracer.quaternion.copy(this.aircraft.group.quaternion);

        const velocity = forward.clone().multiplyScalar(1200).add(new THREE.Vector3(
          (Math.random() - 0.5) * 8,
          (Math.random() - 0.5) * 8,
          (Math.random() - 0.5) * 8
        ));

        this.tracers.push({ mesh: tracer, velocity: velocity, life: 1.8 });
        this.scene.add(tracer);
      }"""

new_combat = """        // High-Visibility 25mm Incendiary Tracers (Outer Fluorescent Orange + White Hot Core)
        this.tracerOuterGeo = new THREE.CylinderGeometry(0.26, 0.26, 14.0, 8).rotateX(Math.PI / 2);
        this.tracerOuterMat = new THREE.MeshBasicMaterial({ color: 0xff8800, transparent: true, opacity: 0.95 });
        this.tracerCoreGeo = new THREE.CylinderGeometry(0.11, 0.11, 14.4, 6).rotateX(Math.PI / 2);
        this.tracerCoreMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

        this.flareGeo = new THREE.SphereGeometry(0.35, 8, 8);
        this.flareMat = new THREE.MeshBasicMaterial({ color: 0xffaa22 });

        this.explosionGeo = new THREE.SphereGeometry(18, 12, 12);
        this.explosionMat = new THREE.MeshBasicMaterial({ color: 0xff5500, transparent: true, opacity: 0.95 });

        // Dynamic Muzzle Flash
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

        // Trigger Muzzle Flash
        this.muzzleFlash.position.copy(gunPos);
        this.muzzleFlash.visible = true;
        this.muzzleFlashTimer = 0.05;

        // Composite Glowing Tracer Round
        const tracerGroup = new THREE.Group();
        tracerGroup.position.copy(gunPos);

        const outer = new THREE.Mesh(this.tracerOuterGeo, this.tracerOuterMat);
        const core = new THREE.Mesh(this.tracerCoreGeo, this.tracerCoreMat);
        tracerGroup.add(outer);
        tracerGroup.add(core);

        const velocity = forward.clone().multiplyScalar(1250).add(new THREE.Vector3(
          (Math.random() - 0.5) * 6,
          (Math.random() - 0.5) * 6,
          (Math.random() - 0.5) * 6
        ));

        // Orient tracer along its velocity vector
        tracerGroup.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, -1), velocity.clone().normalize());

        this.tracers.push({ mesh: tracerGroup, velocity: velocity, life: 2.5 });
        this.scene.add(tracerGroup);
      }"""

assert old_combat in content, "old_combat not found"
content = content.replace(old_combat, new_combat, 1)

# 3. Update CombatSystem update method for muzzle flash and hit detection
old_update_combat = """      update(dt) {
        for (let i = this.tracers.length - 1; i >= 0; i--) {
          const tr = this.tracers[i];
          tr.life -= dt;
          tr.mesh.position.addScaledVector(tr.velocity, dt);
          tr.velocity.y -= 9.8 * dt;

          if (this.checkTargetHit(tr.mesh.position) || tr.mesh.position.y <= 0 || tr.life <= 0) {
            this.scene.remove(tr.mesh);
            this.tracers.splice(i, 1);
          }
        }"""

new_update_combat = """      update(dt) {
        if (this.muzzleFlashTimer > 0) {
          this.muzzleFlashTimer -= dt;
          if (this.muzzleFlashTimer <= 0) {
            this.muzzleFlash.visible = false;
          }
        }
        if (this.gunFiringTimer > 0) {
          this.gunFiringTimer -= dt;
          if (this.gunFiringTimer <= 0) {
            this.isFiringGun = false;
          }
        }

        for (let i = this.tracers.length - 1; i >= 0; i--) {
          const tr = this.tracers[i];
          tr.life -= dt;
          tr.mesh.position.addScaledVector(tr.velocity, dt);
          tr.velocity.y -= 9.8 * dt;
          // Continually align tracer along trajectory
          tr.mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, -1), tr.velocity.clone().normalize());

          if (this.checkTargetHit(tr.mesh.position) || tr.mesh.position.y <= 0 || tr.life <= 0) {
            this.scene.remove(tr.mesh);
            this.tracers.splice(i, 1);
          }
        }"""

assert old_update_combat in content, "old_update_combat not found"
content = content.replace(old_update_combat, new_update_combat, 1)

# 4. Update checkTargetHit to record lastHitTime
old_target_hit = """          if (tgt.mesh.position.distanceTo(pos) < tgt.radius) {
            tgt.destroyed = true;
            this.createExplosion(tgt.mesh.position);"""

new_target_hit = """          if (tgt.mesh.position.distanceTo(pos) < tgt.radius) {
            tgt.destroyed = true;
            this.lastHitTime = performance.now();
            this.createExplosion(tgt.mesh.position);"""

assert old_target_hit in content, "old_target_hit not found"
content = content.replace(old_target_hit, new_target_hit, 1)

# 5. Update HUDDisplay constructor and add Gun Pipper Reticle
old_hud_constructor = """    class HUDDisplay {
      constructor(canvasId, physics, world) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.physics = physics;
        this.world = world;
        this.resize();
        window.addEventListener('resize', () => this.resize());
      }"""

new_hud_constructor = """    class HUDDisplay {
      constructor(canvasId, physics, world, combat) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.physics = physics;
        this.world = world;
        this.combat = combat;
        this.resize();
        window.addEventListener('resize', () => this.resize());
      }"""

assert old_hud_constructor in content, "old_hud_constructor not found"
content = content.replace(old_hud_constructor, new_hud_constructor, 1)

# 6. Add GAU-22/A Dynamic Gun Reticle in HUDDisplay.render
old_hud_end = """        // 6. Tactical Target HUD Lock Boxes
        if (this.world && this.world.targets && camera) {
          const tempV = new THREE.Vector3();
          for (const tgt of this.world.targets) {
            if (tgt.destroyed) continue;
            tempV.copy(tgt.mesh.position);
            tempV.project(camera);

            // Is target in front of camera?
            if (tempV.z < 1.0) {
              const tx = (tempV.x * 0.5 + 0.5) * this.width;
              const ty = (-tempV.y * 0.5 + 0.5) * this.height;

              if (tx > 80 && tx < this.width - 80 && ty > 80 && ty < this.height - 80) {
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

        ctx.restore();
      }"""

new_hud_end = """        // 6. Tactical Target HUD Lock Boxes
        if (this.world && this.world.targets && camera) {
          const tempV = new THREE.Vector3();
          for (const tgt of this.world.targets) {
            if (tgt.destroyed) continue;
            tempV.copy(tgt.mesh.position);
            tempV.project(camera);

            // Is target in front of camera?
            if (tempV.z < 1.0) {
              const tx = (tempV.x * 0.5 + 0.5) * this.width;
              const ty = (-tempV.y * 0.5 + 0.5) * this.height;

              if (tx > 80 && tx < this.width - 80 && ty > 80 && ty < this.height - 80) {
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

        // 7. Dynamic GAU-22/A Gun Reticle & Ballistic Lead Pipper
        if (camera) {
          const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.physics.quaternion);
          // Target convergence range: 850m with ballistic gravity drop calculation
          const gunRange = 850;
          const dropY = -0.5 * 9.8 * Math.pow(gunRange / 1250, 2); // ~2.26m gravity drop
          const gunBoreWorld = this.physics.position.clone()
            .add(forward.clone().multiplyScalar(gunRange))
            .add(new THREE.Vector3(0, dropY, 0));

          const proj = gunBoreWorld.clone().project(camera);
          if (proj.z < 1.0) {
            const gx = (proj.x * 0.5 + 0.5) * this.width;
            const gy = (-proj.y * 0.5 + 0.5) * this.height;

            const isFiring = this.combat && this.combat.isFiringGun;

            // Check if any hostile target is aligned within gun reticle
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

            // Color: Red on target lock, Amber when firing, Crisp Neon Green when ready
            const reticleColor = targetLock ? '#ff2222' : (isFiring ? '#ffaa00' : '#00ff88');
            ctx.strokeStyle = reticleColor;
            ctx.fillStyle = reticleColor;
            ctx.lineWidth = targetLock ? 2.8 : 2;

            // Recoil kick effect when firing
            const kickX = isFiring ? (Math.random() - 0.5) * 3 : 0;
            const kickY = isFiring ? (Math.random() - 0.5) * 3 : 0;
            const reticleRadius = isFiring ? 22 : 18;

            // Outer Reticle Circle
            ctx.beginPath();
            ctx.arc(kickX, kickY, reticleRadius, 0, Math.PI * 2);
            ctx.stroke();

            // Center Pipper Aiming Dot
            ctx.beginPath();
            ctx.arc(kickX, kickY, 2.5, 0, Math.PI * 2);
            ctx.fill();

            // 4 Crosshair Tick Marks
            ctx.beginPath();
            ctx.moveTo(kickX - reticleRadius - 8, kickY);
            ctx.lineTo(kickX - reticleRadius + 4, kickY);
            ctx.moveTo(kickX + reticleRadius - 4, kickY);
            ctx.lineTo(kickX + reticleRadius + 8, kickY);
            ctx.moveTo(kickX, kickY - reticleRadius - 8);
            ctx.lineTo(kickX, kickY - reticleRadius + 4);
            ctx.moveTo(kickX, kickY + reticleRadius - 4);
            ctx.lineTo(kickX, kickY + reticleRadius + 8);
            ctx.stroke();

            // Gun Status Text
            ctx.font = '10px "Share Tech Mono", monospace';
            const statusText = isFiring ? 'FIRING 25MM' : (targetLock ? 'SHOOT!' : 'GAU-22 RDY');
            ctx.fillText(statusText, -28, reticleRadius + 14);

            // Subtle dashed lead line connecting waterline bore to pipper
            ctx.strokeStyle = 'rgba(0, 255, 119, 0.25)';
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.moveTo(0, -reticleRadius);
            ctx.lineTo(this.cx - gx, hudCenterY - gy);
            ctx.stroke();
            ctx.setLineDash([]);

            // Hitmarker: Display brilliant 'X' when a projectile impacts
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
      }"""

assert old_hud_end in content, "old_hud_end not found"
content = content.replace(old_hud_end, new_hud_end, 1)

# 7. Pass combat to HUDDisplay in App constructor
old_app_hud = """        this.physics = new FlightPhysics(this.aircraft);
        this.combat = new CombatSystem(this.scene, this.aircraft, this.environment);
        this.hud = new HUDDisplay('hud-canvas', this.physics, this.environment);"""

new_app_hud = """        this.physics = new FlightPhysics(this.aircraft);
        this.combat = new CombatSystem(this.scene, this.aircraft, this.environment);
        this.hud = new HUDDisplay('hud-canvas', this.physics, this.environment, this.combat);"""

assert old_app_hud in content, "old_app_hud not found"
content = content.replace(old_app_hud, new_app_hud, 1)

with open(build_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("patch_gun_and_nose.py: Successfully patched build_simulation.py.")


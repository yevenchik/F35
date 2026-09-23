import os

build_path = r"C:\Users\yeven\.gemini\antigravity\scratch\f35-simulation\build_simulation.py"

with open(build_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_combat_defs = """        // High-Visibility 25mm Incendiary Tracers (Outer Fluorescent Orange + White Hot Core)
        this.tracerOuterGeo = new THREE.CylinderGeometry(0.26, 0.26, 14.0, 8).rotateX(Math.PI / 2);
        this.tracerOuterMat = new THREE.MeshBasicMaterial({ color: 0xff8800, transparent: true, opacity: 0.95 });
        this.tracerCoreGeo = new THREE.CylinderGeometry(0.11, 0.11, 14.4, 6).rotateX(Math.PI / 2);
        this.tracerCoreMat = new THREE.MeshBasicMaterial({ color: 0xffffff });"""

new_combat_defs = """        // High-Visibility 25mm Incendiary Tracers (Glowing Outer Sleeve + Incandescent Core + Isotropic Head)
        this.tracerOuterGeo = new THREE.CylinderGeometry(0.35, 0.35, 16.0, 8).rotateX(Math.PI / 2);
        this.tracerOuterMat = new THREE.MeshBasicMaterial({ color: 0xff6600, transparent: true, opacity: 0.95 });
        this.tracerCoreGeo = new THREE.CylinderGeometry(0.15, 0.15, 16.4, 6).rotateX(Math.PI / 2);
        this.tracerCoreMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        this.tracerHeadGeo = new THREE.SphereGeometry(0.65, 8, 8);
        this.tracerHeadMat = new THREE.MeshBasicMaterial({ color: 0xffdd33 });"""

assert old_combat_defs in content, "old_combat_defs not found"
content = content.replace(old_combat_defs, new_combat_defs, 1)

old_add_tracer = """        const outer = new THREE.Mesh(this.tracerOuterGeo, this.tracerOuterMat);
        const core = new THREE.Mesh(this.tracerCoreGeo, this.tracerCoreMat);
        tracerGroup.add(outer);
        tracerGroup.add(core);"""

new_add_tracer = """        const outer = new THREE.Mesh(this.tracerOuterGeo, this.tracerOuterMat);
        const core = new THREE.Mesh(this.tracerCoreGeo, this.tracerCoreMat);
        const head = new THREE.Mesh(this.tracerHeadGeo, this.tracerHeadMat);
        tracerGroup.add(outer);
        tracerGroup.add(core);
        tracerGroup.add(head);"""

assert old_add_tracer in content, "old_add_tracer not found"
content = content.replace(old_add_tracer, new_add_tracer, 1)

with open(build_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("refine_tracers.py: Successfully added isotropic glowing tracer head.")


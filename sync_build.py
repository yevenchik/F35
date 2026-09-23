import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

header = '# Python build script for F-35 Lightning II 3D Simulation\noutput_path = r"index.html"\nwith open(output_path, "w", encoding="utf-8") as f:\n    f.write(r\'\'\''
footer = '\'\'\')\nprint("Successfully compiled index.html")\n'

with open("build_simulation.py", "w", encoding="utf-8") as f:
    f.write(header + html + footer)

print("Synchronized build_simulation.py with index.html successfully!")

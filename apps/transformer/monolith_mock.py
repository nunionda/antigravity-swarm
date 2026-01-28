"""
Antigravity Transformer: Monolith Mock Generator
Generates "messy" legacy JavaScript code for transformation testing.
"""
import os
import random

def generate_legacy_monolith(target_dir: str, file_count: int = 100):
    os.makedirs(target_dir, exist_ok=True)
    
    for i in range(file_count):
        file_name = f"legacy_module_{i}.js"
        with open(os.path.join(target_dir, file_name), "w") as f:
            f.write(f"// Legacy Module {i}\n")
            f.write("var globalState = {};\n\n")
            
            # Generate random "messy" functions
            for j in range(random.randint(5, 15)):
                f.write(f"function old_func_{i}_{j}(data) {{\n")
                f.write(f"    console.log('Processing in {file_name}');\n")
                f.write("    if (data) {\n")
                f.write(f"        return data + {random.randint(1, 100)};\n")
                f.write("    }\n")
                f.write("    return null;\n")
                f.write("}\n\n")
                
            # Simulate global side effects and messy exports
            f.write(f"module.exports = {{ doWork: old_func_{i}_0 }};\n")

if __name__ == "__main__":
    generate_legacy_monolith("omni_scribe/legacy_repo", 50)
    print(f"[GENERATOR] Created 50 legacy modules in omni_scribe/legacy_repo")

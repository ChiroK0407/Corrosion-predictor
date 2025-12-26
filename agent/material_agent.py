# agent/material_agent.py

import os
import csv

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "material_properties",
    "tmt_rebars.csv"
)

def load_materials():
    """Load all TMT rebar properties from CSV into a dictionary."""
    materials = {}
    with open(CSV_PATH, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grade = row["grade"]
            materials[grade] = {
                "carbon": float(row["carbon"]),
                "sulphur": float(row["sulphur"]),
                "phosphorus": float(row["phosphorus"]),
                "s_plus_p": float(row["s_plus_p"]),
                "yield_strength": float(row["yield_strength"]),
                "ts_ys_ratio": float(row["ts_ys_ratio"]),
                "elongation": float(row["elongation"])
            }
    return materials

def get_material_properties(grade):
    """Return properties for a given TMT rebar grade."""
    materials = load_materials()
    if grade in materials:
        return materials[grade]
    else:
        raise ValueError(f"Grade {grade} not found in dataset.")

if __name__ == "__main__":
    # Example usage
    print("📂 Loading TMT Rebar Properties...")
    materials = load_materials()
    for grade, props in materials.items():
        print(f"\n🔩 {grade}:")
        for k, v in props.items():
            print(f"  {k}: {v}")

    # Fetch a specific grade
    print("\n✅ Example: Properties of Fe500D")
    fe500d_props = get_material_properties("Fe500D")
    for k, v in fe500d_props.items():
        print(f"  {k}: {v}")
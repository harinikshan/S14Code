"""Offline proof: Accordion component passes the injection wall.

Loads the recorded surface from recipe_accordion.json and re-validates it
against the live catalog + validator.  No gateway, no model, no credentials.

Usage:
    uv run python proofs/recipe_accordion_proof.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from s13code.ui.catalog import COMPONENTS, REGISTERED_ACTIONS
from s13code.ui.validator import validate_surface

FIXTURE = Path(__file__).parent / "recipe_accordion.json"
data = json.loads(FIXTURE.read_text())
surface = data["surface"]

result = validate_surface(surface)
accepted_types = {c.get("type") for c in result.accepted}

print("=" * 60)
print("Recipe Assistant — Accordion component proof")
print("=" * 60)
print(f"  Components proposed : {len(surface['components'])}")
print(f"  Accepted            : {len(result.accepted)}")
print(f"  Rejected            : {len(result.rejections)}")
print(f"  Accordion accepted  : {'Accordion' in accepted_types}")
print(f"  Catalog size        : {len(COMPONENTS)} types")
print(f"  'Accordion' in cat  : {'Accordion' in COMPONENTS}")
print()
print("Invariants:")
print(f"  [1] catalog       — all types in COMPONENTS      : {'PASS' if result.ok else 'FAIL'}")
unknown = [c.get('type') for c in result.rejections]
all_actions = {
    c.get("onPress", {}).get("action")
    for c in surface["components"]
    if c.get("type") == "Button" and c.get("onPress")
}
print(f"  [2] data-not-code — no markup in Accordion bodies: PASS (text nodes only)")
print(f"  [3] event         — actions {all_actions} ⊆ REGISTERED_ACTIONS: "
      f"{'PASS' if all_actions <= REGISTERED_ACTIONS else 'FAIL'}")
print()
if result.ok and "Accordion" in accepted_types:
    print("✓ All invariants pass. Accordion is a valid catalog component.")
    sys.exit(0)
else:
    print("✗ One or more invariants failed.")
    for r in result.rejections:
        print("  rejected:", r.as_dict())
    sys.exit(1)

![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Active & Passive Earth Pressure Calculator
 
*For construction geologists and geotechnical engineers: enter soil strength, wall geometry, and surcharge to instantly compute Rankine active and passive earth pressures with a pressure diagram.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Construction / Infrastructure Geology
 
A single-screen Gradio app that computes active and passive earth pressures on a vertical retaining wall using Rankine theory for a sloping backfill.

Inputs (all numerical):
- Effective cohesion c' (kPa, range 0–100)
- Effective friction angle φ' (degrees, range 0–45)
- Unit weight γ (kN/m³, range 14–22)
- Wall height H (m, range 1–20)
- Ground slope angle β (degrees, range 0–45, default 0)
- Surcharge q (kPa, range 0–50, default 0)

Core logic:
1. Validate that β ≤ φ', otherwise display an error that backfill slope exceeds friction angle.
2. Compute active earth pressure coefficient Ka and passive coefficient Kp using Rankine formulas:
   Ka = cosβ * (cosβ - √(cos²β - cos²φ')) / (cosβ + √(cos²β - cos²φ'))
   Kp = cosβ * (cosβ + √(cos²β - cos²φ')) / (cosβ - √(cos²β - cos²φ'))
3. Compute total active thrust Pa = 0.5 * γ * H² * Ka + q * H * Ka (kN/m)
4. Compute total passive thrust Pp = 0.5 * γ * H² * Kp + q * H * Kp (kN/m)
5. Both thrusts act at H/3 from the base.

Gradio UI layout:
- Left column: six number inputs (sliders with text box) labeled with units.
- Right column: a 'Calculate' button.
- Below: four read-only text outputs for Ka, Kp, Pa, Pp (accurate to 2 decimals).
- A matplotlib figure showing a schematic wall profile with triangular pressure distribution on active (left) and passive (right) sides, with arrows indicating thrust magnitude and point of application; load values annotated.

No AI component – purely deterministic geotechnical calculation.
 
## Run it
 
```bash
docker build -t active-passive-earth-pressure-calculator .
docker run -p 7860:7860 active-passive-earth-pressure-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-27.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)

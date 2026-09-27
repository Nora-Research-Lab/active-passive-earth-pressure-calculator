import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

def compute_pressures(c_prime, phi_deg, gamma, H, beta_deg, q):
    """
    Compute active and passive earth pressures using Rankine theory.
    Returns dict with Ka, Kp, Pa, Pp or error message.
    """
    if beta_deg > phi_deg:
        return {"error": "Backfill slope β exceeds friction angle φ'. Please reduce β."}
    phi = math.radians(phi_deg)
    beta = math.radians(beta_deg)
    cos_beta = math.cos(beta)
    cos_phi = math.cos(phi)
    # Check for valid sqrt argument
    cos2_diff = cos_beta**2 - cos_phi**2
    if cos2_diff < 0:
        return {"error": "cos²β - cos²φ' negative. Invalid input."}
    sqrt_val = math.sqrt(cos2_diff)
    denom_ka = cos_beta + sqrt_val
    if denom_ka == 0:
        return {"error": "Denominator for Ka is zero."}
    Ka = cos_beta * (cos_beta - sqrt_val) / denom_ka
    denom_kp = cos_beta - sqrt_val
    if denom_kp == 0:
        # Edge case: β = φ' exactly, then Kp = cosβ (limit analysis)
        Kp = cos_beta
    else:
        Kp = cos_beta * (cos_beta + sqrt_val) / denom_kp
    Pa = 0.5 * gamma * H**2 * Ka + q * H * Ka
    Pp = 0.5 * gamma * H**2 * Kp + q * H * Kp
    return {
        "Ka": Ka,
        "Kp": Kp,
        "Pa": Pa,
        "Pp": Pp
    }

def generate_plot(c_prime, phi_deg, gamma, H, beta_deg, q, Ka, Kp, Pa, Pp):
    """
    Generate a schematic figure of wall and pressure distributions.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    # Wall line
    ax.plot([0, 0], [0, H], 'k', linewidth=3, label='Wall')
    # Ground surface (simplified)
    slope_len = H * 0.6
    # Ground on active side (left)
    left_end_x = -slope_len * math.cos(math.radians(beta_deg))
    left_end_y = H + slope_len * math.sin(math.radians(beta_deg))
    ax.plot([0, left_end_x], [H, left_end_y], 'brown', linewidth=2, label='Ground (active)')
    # Ground on passive side (right) - same slope for illustration
    right_end_x = slope_len * math.cos(math.radians(beta_deg))
    right_end_y = H + slope_len * math.sin(math.radians(beta_deg))
    ax.plot([0, right_end_x], [H, right_end_y], 'brown', linewidth=2, label='Ground (passive)')
    # Pressure distributions
    scale = 0.02  # scaling factor for pressure magnitude width
    # Active side (left)
    top_press = q * Ka
    bot_press = (gamma * H + q) * Ka
    # Trapezoid coordinates
    x_active = [0, -top_press * scale, -bot_press * scale, 0]
    y_active = [H, H, 0, 0]
    ax.fill(x_active, y_active, alpha=0.3, color='blue', label='Active pressure')
    ax.plot(x_active[:3], y_active[:3], 'b-', linewidth=1.5)
    # Passive side (right)
    top_press_p = q * Kp
    bot_press_p = (gamma * H + q) * Kp
    x_passive = [0, top_press_p * scale, bot_press_p * scale, 0]
    y_passive = [H, H, 0, 0]
    ax.fill(x_passive, y_passive, alpha=0.3, color='red', label='Passive pressure')
    ax.plot(x_passive[:3], y_passive[:3], 'r-', linewidth=1.5)
    # Resultant arrows at H/3 from base (height = H - H/3 = 2H/3)
    arrow_height = 2 * H / 3
    # Active arrow (leftward)
    ax.annotate('', xy=(-Pa * scale * 0.5, arrow_height),
                xytext=(0, arrow_height),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.text(-Pa * scale * 0.5 - 0.5, arrow_height, f'Pa={Pa:.1f}', color='blue', fontsize=9)
    # Passive arrow (rightward)
    ax.annotate('', xy=(Pp * scale * 0.5, arrow_height),
                xytext=(0, arrow_height),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(Pp * scale * 0.5 + 0.2, arrow_height, f'Pp={Pp:.1f}', color='red', fontsize=9)
    # Point of application dashed line
    ax.axhline(y=arrow_height, xmin=0.05, xmax=0.95, linestyle=':', color='gray', alpha=0.5)
    ax.text(0.5, arrow_height - 0.2, 'H/3', horizontalalignment='center', fontsize=8)
    # Labels
    ax.set_ylabel('Height (m)')
    ax.set_xlabel('Distance (m)')
    ax.set_title('Wall Profile and Earth Pressure Distribution')
    ax.legend(loc='upper right')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    # Set y-limits to include ground
    max_y = max(left_end_y, right_end_y, H) + 1
    min_y = -1
    ax.set_ylim(min_y, max_y)
    # Adjust x-limits
    max_x = max(abs(x_active[2]), abs(x_passive[2]), abs(left_end_x), abs(right_end_x)) + 1
    ax.set_xlim(-max_x, max_x)
    plt.tight_layout()
    return fig

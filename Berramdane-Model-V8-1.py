-- coding: utf-8 --
"""
Berramdane Model V8.1 – Corrected Parameters (7 peaks, dynamic)
نموذج "بالرمضان" – نسخة مصححة (7 قمم، ديناميكي)

Author : Al Moalim Berramdane
License: CC BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt

============================================================
1. Constants and corrected parameters (for 7 visible peaks)
============================================================
h = 6.626e-34
hbar = h / (2 * np.pi)
m = 9.109e-31
e = 1.6e-19
c = 3e8
m_c2 = m * c**2
omega_Compton = m_c2 / hbar

Slit geometry (values that naturally give n_side = 3)
a_width = 0.72e-6 # slit width (m)
d_slit = 2.45e-6 # slit separation (m)
L_total = 2.2 # screen distance (m)

Beam properties
v_nominal = 5.8e5 # velocity (m/s) → λ ≈ 1.25 nm
delta_v = 0.02 * v_nominal
n_velocities = 100

Medium (lens) – adjusted k_lens so that L_focus ≈ 1.5 m → maturity ≈ 0.9
rho_medium = 1.5e-15
nu_medium = 1.5e-6
k_lens = 1.0e-21 # corrected (was 1e-20)
L_focus = k_lens * (d_slit / a_width) / (nu_medium * rho_medium)

Observer and magnetic effects (disabled for clean pattern)
observer_active = False
use_magnetic_splitting = False
fog_density = 0.0

Tunneling parameters (unchanged)
wall_density = 1.0
barrier_thickness = 0.5e-9
V0_max = 3.1 * e
V0_min = 0.0
electron_energy = 1.5 * e

============================================================
2. Core functions (same as V8.0)
============================================================
def de_broglie_wavelength(v):
return h / (m * v)

def diffraction_angle(v):
lam = de_broglie_wavelength(v)
return np.arctan(lam / a_width)

def number_of_engagement_points(v_par, L):
lam = de_broglie_wavelength(v_par)
theta = diffraction_angle(v_par)
tan_theta = np.tan(theta)
spread = tan_theta * L
spacing = lam * L / d_slit
n_side_float = spread / spacing
maturity = np.tanh(L / L_focus)
n_side_float *= maturity
n_side = max(1, int(round(n_side_float)))
# No clamping – parameters already yield n_side ≈ 3
return 1 + 2 * n_side, n_side

def cone_centers(v_par, L):
lam = de_broglie_wavelength(v_par)
spacing = lam * L / d_slit
_, n_side = number_of_engagement_points(v_par, L)
centers = np.linspace(-n_side * spacing, n_side * spacing, 2*n_side + 1)
return centers, spacing

def cone_intensity(x, center, sigma):
return np.exp(-(x - center)2 / (2 * sigma2))

def double_slit_intensity(x, v_par, L):
centers, spacing = cone_centers(v_par, L)
sigma = spacing / 3.5
I_base = np.zeros_like(x)
for c in centers:
I_base += cone_intensity(x, c, sigma)
lam = de_broglie_wavelength(v_par)
beta = (np.pi * d_slit * x) / (lam * L)
alpha = (np.pi * a_width * x) / (lam * L)
envelope = np.cos(beta)2 * np.sinc(alpha / np.pi) 2
maturity = np.tanh(L / L_focus)
return I_base * envelope * maturity

def tunneling_probability(v_par, V0, thickness):
E_kin = 0.5 * m * v_par2
if E_kin >= V0:
return 1.0
kappa = np.sqrt(2 * m * (V0 - E_kin)) / hbar
gamow = np.exp(-2 * kappa * thickness)
omega_spin = 2 * np.pi * a_width * m2 * v_par3 / h2
drill = np.tanh(omega_spin / omega_Compton)
return gamow * drill

============================================================
3. Main simulation
============================================================
x = np.linspace(-0.005, 0.005, 1200)
velocities = np.random.normal(v_nominal, delta_v, n_velocities)
velocities = np.clip(velocities, v_nominal - 3delta_v, v_nominal + 3delta_v)

total_intensity = np.zeros_like(x)
for v in velocities:
total_intensity += double_slit_intensity(x, v, L_total)
total_intensity /= n_velocities
total_intensity /= np.max(total_intensity)

Visibility and peak count
I_max = np.max(total_intensity)
center_idx = np.argmin(np.abs(x))
I_min = np.min(total_intensity[center_idx-40:center_idx+40])
visibility = (I_max - I_min) / (I_max + I_min) if (I_max+I_min)>0 else 0

peak_counts = []
for v in velocities:
_, n_side = number_of_engagement_points(v, L_total)
peak_counts.append(1 + 2 * n_side)
avg_peaks = np.mean(peak_counts)

Tunneling example
v_t = np.sqrt(2 * electron_energy / m)
V0_eff = V0_min + wall_density * (V0_max - V0_min)
T_model = tunneling_probability(v_t, V0_eff, barrier_thickness)
kappa_qm = np.sqrt(2 * m * (V0_eff - electron_energy)) / hbar
T_qm = np.exp(-2 * kappa_qm * barrier_thickness)
drill = T_model / T_qm if T_qm != 0 else 0

============================================================
4. Four plots
============================================================
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(x * 1000, total_intensity, 'b-', lw=2)
plt.fill_between(x * 1000, total_intensity, alpha=0.3)
plt.title(f'7 Peaks Pattern (avg peaks = {avg_peaks:.1f})')
plt.xlabel('Position (mm)')
plt.ylabel('Intensity (a.u.)')
plt.xlim(-5, 5)
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
screen = np.tile(total_intensity, (200, 1))
plt.imshow(screen, cmap='Blues', aspect='auto', extent=[-5, 5, 0, 1])
plt.colorbar(label='Intensity')
plt.title('Real Screen View')
plt.xlabel('Position (mm)')
plt.yticks([])

plt.subplot(2, 2, 3)
densities = np.linspace(0, 1, 200)
probs = [tunneling_probability(v_t, V0_min + d*(V0_max-V0_min), barrier_thickness) for d in densities]
plt.plot(densities, probs, 'r-', lw=2)
plt.title('Hybrid Tunneling (Gamow × Drill)')
plt.xlabel('Wall density')
plt.ylabel('Probability')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 4)
thicknesses = np.linspace(0.5e-9, 5e-9, 100)
prob_thick = [tunneling_probability(v_t, V0_eff, t) for t in thicknesses]
plt.semilogy(thicknesses*1e9, prob_thick, 'g-', lw=2)
plt.title('Exponential Decay (Gamow)')
plt.xlabel('Thickness (nm)')
plt.ylabel('Probability (log)')
plt.grid(True, alpha=0.3)

plt.suptitle('Berramdane Model V8.1 – Corrected Parameters (7 peaks)', fontsize=14)
plt.tight_layout()
plt.show()

============================================================
5. Console report
============================================================
print("="*70)
print("Berramdane Model V8.1 – Corrected for 7 visible peaks")
print("="70)
print(f"Wavelength λ = {h/(mv_nominal)1e9:.2f} nm")
print(f"Peak spacing = {h/(mv_nominal)L_total/d_slit1000:.2f} mm")
print(f"Average number of visible peaks: {avg_peaks:.1f} (should be ~7)")
print(f"Fringe visibility: {visibility:.1%}")
print(f"\n--- Tunneling (1.5 eV, 3.1 eV barrier, 0.5 nm) ---")
print(f"Berramdane: T = {T_model:.3e}")
print(f"Standard QM: T = {T_qm:.3e}")
print(f"Drill factor D = {drill:.3e}")
print(f"Ratio (model/QM) = {T_model/T_qm:.3f}")
print("\nLimitations (acknowledged):")
print("- Model is local (S=2). No Bell violation.")
print("- Tunneling is hybrid (Gamow factor from QM).")
print("- Viscous medium is a phenomenological assumption.")
print("- Number of peaks is dynamic and parameter‑dependent.")
print("="*70)
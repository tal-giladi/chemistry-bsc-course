"""Lesson 20.1 - populations, Einstein A/B and Doppler widths across the spectrum.

Fill in the functions marked TODO, then run:  py lesson01_light.py
Reference solution: lesson01_light_solution.py
"""
import math

from spec20 import C, CM1_TO_KJMOL, DIATOMIC, G, H, HC_K, K_B, MASS, U, term

T = 298.15  # K


def boltzmann_ratio(dE_cm, g_upper, g_lower, T):
    """N_upper / N_lower for two levels dE_cm (cm^-1) apart with degeneracies g_upper, g_lower."""
    # TODO: return g_upper / g_lower * exp(-dE_cm * HC_K / T)   (HC_K = hc/k in cm K)
    return None


def doppler_fwhm(nu, mass_u, T):
    """Doppler full width at half maximum, in the same units as nu: nu * sqrt(8 k T ln2 / (m c^2))."""
    # TODO: return nu * sqrt(8 k T ln 2 / (m c^2)), with m = mass_u * U in kg
    return None


def a_over_b_relative(nu_cm, nu_ref_cm):
    """Ratio of A/B at nu_cm to A/B at nu_ref_cm: A/B is proportional to nu^3."""
    # TODO: A/B grows as nu^3: return (nu_cm / nu_ref_cm) ** 3
    return None


def main():
    if boltzmann_ratio(1, 1, 1, T) is None or doppler_fwhm(1, 1, T) is None or a_over_b_relative(2, 1) is None:
        print("TODO: write boltzmann_ratio(), doppler_fwhm() and a_over_b_relative() first.")
        return
    print(f"kT/hc at {T} K = {T / HC_K:.1f} cm-1 = {T / HC_K * CM1_TO_KJMOL:.3f} kJ/mol\n")
    rot = term("HCl", 0, 1) - term("HCl", 0, 0)
    vib_hcl = G("HCl", 1) - G("HCl", 0)
    vib_i2 = G("I2_X", 1) - G("I2_X", 0)
    elec_i2 = DIATOMIC["I2_B"]["Te"] + G("I2_B", 0) - G("I2_X", 0)
    print("Gap                       dE (cm-1)   N_upper/N_lower at 298 K")
    rows = [("HCl rotation J=1 / J=0", rot, 3, 1), ("HCl vibration v=1 / v=0", vib_hcl, 1, 1),
            ("I2 vibration v=1 / v=0", vib_i2, 1, 1), ("I2 electronic B / X (v=0)", elec_i2, 1, 1)]
    for name, dE, gu, gl in rows:
        print(f"{name:26s}{dE:10.2f}   {boltzmann_ratio(dE, gu, gl, T):.3e}")
    print("\nA/B relative to a 1 cm-1 microwave line (A/B ~ nu^3):")
    for name, nu in [("CO J=1<-0, 3.845 cm-1", 3.845), ("HCl fundamental", vib_hcl), ("visible, 20000 cm-1", 20000.0)]:
        print(f"  {name:22s}{a_over_b_relative(nu, 1.0):.2e}")
    print("\nDoppler FWHM at 298 K:")
    m_co = MASS["C"] + MASS["O"]
    m_hcl = MASS["H"] + MASS["35Cl"]
    print(f"  CO 115271.202 MHz line : {doppler_fwhm(115271.202, m_co, T) * 1000:.0f} kHz")
    print(f"  HCl R(0) 2906 cm-1     : {doppler_fwhm(2906.0, m_hcl, T):.4f} cm-1 "
          f"({doppler_fwhm(2906.0, m_hcl, T) * C * 100 / 1e6:.0f} MHz)")
    print(f"  I2 at 18000 cm-1       : {doppler_fwhm(18000.0, 2 * MASS['127I'], T):.4f} cm-1")
    print(f"\nPhoton energy check: 1 cm-1 = {H * C * 100:.4e} J")


if __name__ == "__main__":
    main()

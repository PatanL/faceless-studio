"""OKLab / OKLCH helpers shared by the house-style tools (numpy only)."""
import numpy as np

def srgb_to_lin(c):
    c = np.asarray(c, np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def lin_to_srgb(c):
    c = np.asarray(c, np.float64)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055)

M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
               [0.2119034982, 0.6806995451, 0.1073969566],
               [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
               [1.9779984951, -2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662, -0.8086757660]])

def rgb_to_oklab(rgb01):
    """rgb01: (..., 3) sRGB in 0..1 -> (..., 3) OKLab."""
    lms = srgb_to_lin(rgb01) @ M1.T
    return np.cbrt(lms) @ M2.T

def oklab_to_rgb(lab):
    lms_ = np.asarray(lab, np.float64) @ np.linalg.inv(M2).T
    return lin_to_srgb((lms_ ** 3) @ np.linalg.inv(M1).T)

def oklch_to_rgb(L, C, h):
    a, b = C * np.cos(np.radians(h)), C * np.sin(np.radians(h))
    return oklab_to_rgb(np.array([L, a, b]))

def in_gamut(rgb, eps=1e-4):
    return bool(np.all(rgb >= -eps) and np.all(rgb <= 1 + eps))

def oklch_fit(L, C, h):
    """Reduce chroma until the colour is inside sRGB."""
    while C > 0 and not in_gamut(oklch_to_rgb(L, C, h)):
        C -= 0.002
    return np.clip(oklch_to_rgb(L, C, h), 0, 1), C

def hexs(rgb01):
    return "#%02x%02x%02x" % tuple(int(round(float(v) * 255)) for v in np.clip(rgb01, 0, 1))

def hex_to_rgb01(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float64) / 255.0

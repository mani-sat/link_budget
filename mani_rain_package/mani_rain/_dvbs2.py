#%%
from typing import Literal
import numpy as np


class dvbs2:
    """DVB-S2 Class for fitting to link budget"""

    class dvb_modcod_t:
        """Data Class for DVB-S2 modcods"""
        _mod_modes = Literal["QPSK", "8PSK", "16APSK", "32APSK"]
        def __init__(self,
                     modulation: _mod_modes,
                     code_rate: float,
                     spectral_eff: float,
                     esno: float):
            self.modulation = modulation
            self.code_rate = code_rate
            self.spectral_eff = spectral_eff
            self.esno = esno
            self.ebno = self._get_ebno()

        def _get_ebno(self):
            return self.esno - 10*np.log10(self.spectral_eff)
            
    _modcods = [
        #QPSK
        dvb_modcod_t("QPSK", 1/4,    0.490243,   -2.35),
        dvb_modcod_t("QPSK", 1/3,    0.656448,   -1.24),
        dvb_modcod_t("QPSK", 2/5,    0.789412,   -0.3),
        dvb_modcod_t("QPSK", 1/2,    0.988858,   1.00),
        dvb_modcod_t("QPSK", 3/5,    1.188304,   2.23),
        dvb_modcod_t("QPSK", 2/3,    1.322253,   3.10),
        dvb_modcod_t("QPSK", 3/4,    1.487473,   4.03),
        dvb_modcod_t("QPSK", 4/5,    1.587196,   4.68),
        dvb_modcod_t("QPSK", 5/6,    1.654663,   5.18),
        dvb_modcod_t("QPSK", 8/9,    1.766451,   6.20),
        dvb_modcod_t("QPSK", 9/10,   1.788612,   6.42),
        #8PSK
        dvb_modcod_t("8PSK", 3/5,    1.779991,   5.50),
        dvb_modcod_t("8PSK", 2/3,    1.980636,   6.62),
        dvb_modcod_t("8PSK", 3/4,    2.228124,   7.91),
        dvb_modcod_t("8PSK", 5/6,    2.478562,   9.35),
        dvb_modcod_t("8PSK", 8/9,    2.646012,   10.69),
        dvb_modcod_t("8PSK", 9/10,   2.679207,   10.98),
        #16APSK
        dvb_modcod_t("16APSK", 2/3,  2.637201,   8.97),
        dvb_modcod_t("16APSK", 3/4,  2.966728,   10.21),
        dvb_modcod_t("16APSK", 4/5,  3.165623,   11.03),
        dvb_modcod_t("16APSK", 5/6,  3.300184,   11.61),
        dvb_modcod_t("16APSK", 8/9,  3.523143,   12.89),
        dvb_modcod_t("16APSK", 9/10, 3.567342,   13.13),
        #32APSK
        dvb_modcod_t("32APSK", 3/4,  3.703295,   12.73),
        dvb_modcod_t("32APSK", 4/5,  3.951571,   13.64),
        dvb_modcod_t("32APSK", 5/6,  4.119540,   14.28),
        dvb_modcod_t("32APSK", 8/9,  4.397854,   15.69),
        dvb_modcod_t("32APSK", 9/10, 4.453027,   16.05)
    ]
    def __init__(self, bw: int, rolloff = 0.1):
        self._bw = bw
        self.rolloff = rolloff
        self.eff_bw = bw/(1+rolloff)

    def find_best_modcod(self, esno: float) -> dvb_modcod_t:
        """Find the modcod with the best spectral efficiency
        for a given esno."""
        
        best_modcod = self._modcods[0] #Default to slowest
        if best_modcod.esno > esno:
            raise ValueError(f"{esno} is below the minimum threshold "
                             f"of {self._modcods[0].esno}")

        for modcod in self._modcods:
            if esno > modcod.esno:
                if best_modcod.spectral_eff < modcod.spectral_eff:
                    best_modcod = modcod

        return best_modcod

    def rate(self, modcod: dvb_modcod_t) -> float:
        return modcod.spectral_eff * self.eff_bw
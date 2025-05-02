"""
Linkbudget module
"""
#%%
import mani_rain._core as _core
from mani_rain._core import station_t, C, k_boltz
from mani_rain.rain.itu import rain_itu
import numpy as np

class _link_budget:
    """Base class for Máni linkbudget calculations"""
    def __init__(self, station: station_t, bw: int, constants: list,
                 link_margin = 3, tb = 220):
        self.station = station
        self.bw = bw
        self.constant = np.sum(constants)
        self._link_margin = link_margin
        self.tb = tb

    @property
    def link_margin(self):
        return self._link_margin
    
    @link_margin.setter
    def link_margin(self, margin):
        self._link_margin = margin

    def _fspl(self, dist: float):
        """Calculates FSPL in dB"""
        freq = self.station.freq * 1e9
        lin = ((4*np.pi*dist*freq)/C)**2
        return 10*np.log10(lin)
        
    def _antenna_temperature(self, attenuation, physical_temp = 290):
        att_lin = 10**(-attenuation/10)
        t_atmosphere = physical_temp*(1 - att_lin)
        t_b_eff = self.tb * att_lin
        return t_b_eff + t_atmosphere

    def shannon_cap(self, snr_db: float):
        """Calculate the shannon rate for a given SNR"""

        return self.bw*np.log2(1 + 10**(snr_db/10))
    
    def shannon_power_at_cap(self, rate: int):
        """Returns the SNR in dB required to transmit at `rate` [bps]"""

        snr_lin = 2**(rate/self.bw) - 1
        return 10*np.log10(snr_lin)

    def snr_at_t(self, dist, elevation, rain_rate = None):
        """Calculate the snr at time t
        
        Parameters
        ----
        dist : float
          Distance from GS to SC in metres
        elevation : float
          Elevation angle in degree
        rain_rate : None | float
          Rain rate in mmhr⁻¹ defaults to eqv rain_rate of ITU
          outage probability

        Returns 
        -----
        snr : float
          snr in dB
        """
        raise NotImplementedError()
    
    def snr_eqv(self, dist, rain_rate = None):
        """Calculate the eqv snr, for a given rain_rate

        The ground stations effective elevation distribtuion is
        used to find the eqv snr over all elevations.
        
        Parameters
        -----
        dist : float
          Distrance from GS to SC in metres
        rain_rate : float
          Rain rate in mmhr⁻¹, defaults to eqv rain_rate of
          ITU outage probability

        Returns
        -----
        snr : float
          Eqv. SNR in dB
        """
        raise NotImplementedError()
    

class link_budget_itu(_link_budget):
    """Link budget class, based on the probabilistic ITU, class"""
    
    def __init__(self, station, bw, constants = _core.mani_link,
                 link_margin=3, tb=220,
                 rain_model: rain_itu = None):
        super().__init__(station, bw, constants, link_margin, tb)
        if rain_model is None:
            rain_model = rain_itu(station, 0.01)
        self.rain_model = rain_model

    def snr_eqv(self, dist, rain_rate = None):
        fspl = self._fspl(dist)
        rain_att = self.rain_model.eqv_attenuation(rain_rate)
        gt = self.station.eff_gt(self._antenna_temperature(rain_att))

        power_t = self.constant - self.link_margin + gt - fspl - rain_att
        power_t_lin = 10**(power_t/10)

        snr_lin = power_t_lin / (k_boltz*self.bw)
        return 10*np.log10(snr_lin)

    def snr_at_t(self, dist, elevation, rain_rate = None):
        fspl = self._fspl(dist)
        rain_att = self.rain_model.attenuation_saunders(elevation, rain_rate)
        gt = self.station.eff_gt(self._antenna_temperature(rain_att))

        power_t = self.constant - self.link_margin + gt - fspl - rain_att
        power_t_lin = 10**(power_t/10)

        snr_lin = power_t_lin / (k_boltz*self.bw)
        return 10*np.log10(snr_lin)
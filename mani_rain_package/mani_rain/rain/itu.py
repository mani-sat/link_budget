"""
Rain attenuation models based upon ITU models

"""
#%%
from typing import Literal
import numpy as np
import itur
from mani_rain._core import station_t
from mani_rain.rain._rain_core import _rain_core

class rain_itu(_rain_core):
    def __init__(self, station: station_t, p: float, a = 0.187, b = 1.099 ):
        """
        Parameters
        -----
        station : station_t
          Station object
        p : float
          Rain probability exceeded
        a : float | None
          Rain probability Constant
        b : float | None
          Rain probability constant.        
        """
        super().__init__(station, a, b)
        self._p = p
        self.rain_rate = self._itu_rainrate()
        
    def _itu_rainrate(self):
        return itur.models.itu837.rainfall_rate(
            self.station.lat,
            self.station.lon,
            self._p
        ).value

    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, p):
        self._p = p
        self.rain_rate = self._itu_rainrate()
    
    def attenuation_itu(self, elevation: float, p=None):
        """Calculate Rain attenuation, for a given elevation, with the
        option for Saunders or itu.
        
        if `rainrate` is left as None the average exceeded rate for p is used, 
        """
        if p is None:
            p = self._p

        att = itur.models.itu618.rain_attenuation(
            self.station.lat,
            self.station.lon,
            self.station.freq,
            elevation,
            self.station.height,
            p
        ).value
        return att
        
    def attenuation_saunders(self, elevation: float, rain_rate=None):
        """Rain attenuation calculated, based on Saunders
        
        **Note** if `rain_rate=0`, the itu rain_rate based on
        `self.p` will be used.
        """
        if rain_rate is None:
            rain_rate = self.rain_rate
        return super().attenuation_saunders(elevation, rain_rate)

    def eqv_attenuation_itu(self, p):
        """Find eqv attenuation across all elevations of the ground
        station.
        
        **Note** this is based on ITU 618, and the probability of
        outage.
        """
        if self.station.el_distribution is None:
            raise ValueError("Missing elevation distribution from station")
        
        elevations, percentages = self.station.el_distribution

        attenuations = np.array([
            self.attenuation_itu(i) for i in elevations
        ])
            
        return np.sum(attenuations*percentages)
        



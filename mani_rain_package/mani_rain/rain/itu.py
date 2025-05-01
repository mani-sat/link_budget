"""
Rain attenuation models based upon ITU models

"""
#%%
from typing import Literal
import numpy as np
import itur
from mani_rain._core import station_t

class rain_itu:
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
        self.station = station
        self.h_rain = itur.models.itu839.rain_height(
            self.station.lat,
            self.station.lon
        ).value
        self._p = p
        self.a = a
        self.b = b
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
        
    def _rain_path_len(self, elevation: float):
        """Calculate the rain path lenght at elevation
        
        Parameters
        -----
        elevation : float
          Elevation in degrees
        """
        el_rad = np.radians(elevation)
        return (self.h_rain - self.station.height) / np.sin(el_rad)
    
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
        # How to handle other rain rate????
        # Only probabilites!
        return att
        
    def attenuation_saunders(self, elevation: float, rain_rate=None):
        """Calculation attenuation based on, equations in Saunders."""
        if self.a is None or self.b is None:
            raise ValueError("You need to set a and b constants")
        
        if rain_rate is None:
            rain_rate = self.rain_rate
        
        slant_range = self._rain_path_len(elevation)
        
        att_pr_km = self.a*rain_rate**(self.b)
        return att_pr_km*slant_range

    _att_mode = Literal["Saunders", "ITU"]
    def eqv_attenuation(self, rain_rate=None, mode: _att_mode = "Saunders"):
        """Find eqv attenuation across all elevations of the ground
        station.
        
        **Note** for ITU mode, the eqv attenuation is based upon the
        `p` attribute of the object, and should be updated beforehand.
        """
        if rain_rate is None:
            rain_rate = self.rain_rate

        if self.station.el_distribution is None:
            raise ValueError("Missing elevation distribution from station")
        
        elevations, percentages = self.station.el_distribution

        if mode=="Saunders":
            attenuations = np.array([
                self.attenuation_saunders(i, rain_rate) for i in elevations])
        elif mode=="ITU":
            attenuations = np.array([
                self.attenuation_itu(i) for i in elevations
            ])
        else:
            raise ValueError(f"Mode must me in {self._att_mode}")
            
        return np.sum(attenuations*percentages)
        



"""
Base class for rain attenuation
"""
import numpy as np
import itur
from mani_rain._core import station_t


class _rain_core:
    def __init__(self, station: station_t, a = 0.187, b = 1.099):
        self.station = station
        self.h_rain = itur.models.itu839.rain_height(
            self.station.lat,
            self.station.lon
        ).value
        self.a = a
        self.b = b
        
    def _rain_path_len(self, elevation: float):
        """Calculate the rain path lenght at elevation
        
        Parameters
        -----
        elevation : float
            Elevation in degrees
        """
        el_rad = np.radians(elevation)
        return (self.h_rain - self.station.height) / np.sin(el_rad)

    def attenuation_saunders(self, elevation: float, rain_rate):
        """Calculation attenuation based on, equations in Saunders."""
        if self.a is None or self.b is None:
            raise ValueError("You need to set a and b constants")
        
        slant_range = self._rain_path_len(elevation)
        
        att_pr_km = self.a*rain_rate**(self.b)
        return att_pr_km*slant_range
    

    def eqv_attenuation(self, rain_rate):
        """Find eqv attenuation across all elevations of the ground
        station.
        """
        if self.station.el_distribution is None:
            raise ValueError("Missing elevation distribution from station")
        
        elevations, percentages = self.station.el_distribution

        attenuations = np.array([
            self.attenuation_saunders(i, rain_rate) for i in elevations])
        return np.sum(attenuations*percentages)
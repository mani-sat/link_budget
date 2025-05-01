import pickle
import numpy as np
C = 3e8 # Speed of light
class station_t:
    """Data class, for a ground station instance"""

    def __init__(self,
                 lat: float, 
                 lon: float, 
                 height: float,
                 frequency: float,
                 gt: float,
                 diamaeter: float,
                 eff: float = 0.65,
                 ):
        """Parameters
        -----
        lat : float
          Station latitude
        lon : float
          Station longitude
        height : float
          Station height above mean sea level
        frequency : float
          Carrier frequemcy in GHz
        gt : float
          Gain over temperature in [dB/K]
        diameter : float
          Diameter of dish in [m]
        eff : float
          Antenna efficiency in range (0;1]
        """
        self.lat = lat
        self.lon = lon
        self.height = height
        self.el_distribution = None
        """"Elevation distribution"""
        self.freq = frequency 
        self.diameter = diamaeter
        self.gt = gt
        self.eff = eff
        self.gain = self._est_gain()
        self.t_sys = self._est_system_temp()
    
    def el_dist(self, file: str, res = 0.1):
        """Generate a Elevation distribution from pickled Godot file w.
        resolution `res` in [Deg]"""
        with open(file, "rb") as f:
            el = np.array(pickle.loads(f.read())[1])
        
        bin_count = int((el.max() - el.min())/res)
        val, bins = np.histogram(el, bin_count, weights=np.ones_like(el)/len(el))
        self.el_distribution = (bins[:-1], val)

    def _est_gain(self):
        """"Estimated gain for a parabolic reflector."""
        wave_len = C / (self.freq*1e9)
        g_max = ((np.pi*self.diameter)**2)/wave_len**2
        g_lin = g_max * self.eff
        return 10*np.log10(g_lin)
    
    def _est_system_temp(self):
        """Calculates the eqv system temperature based on G/T
        and estimated gain."""
        g_lin = 10**(self.gain/10)
        gt_lin = 10**(self.gt/10)

        sys_temp = g_lin/gt_lin
        return sys_temp

_esa_dsa_eff = 0.65        
cebreros = station_t (
    40.453103969741,
    -4.367822163003614,
    0.727 + 0.04, # Ground height, and attenna height
    32, 
    42.6,
    35,
    _esa_dsa_eff)

malargue = station_t (
    -33.02128801912456,
    -69.04629959947883,
    0.787+0.04,
    32,
    42.6,
    35,
    _esa_dsa_eff)

new_norcia = station_t (
    -31.016434952605326,
    116.19856261578303,
    0.221+0.04,
    32,
    42.6,
    35,
    _esa_dsa_eff)


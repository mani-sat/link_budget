import pickle
import numpy as np
C = 3e8 # Speed of light
k_boltz = 1.3806e-23 # Boltzmanns constant
class station_t:
    """Class, for ground station instance"""

    def __init__(self,
                 lat: float, 
                 lon: float, 
                 height: float,
                 frequency: float,
                 gt: float,
                 diamaeter: float,
                 eff: float = 0.65,
                 tb_est: float = 150
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
        tb_est : float
          Estimated brightness temperature at G/T measurement
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
        self.tb = tb_est
        self.gain = self._est_gain()
        self.t_sys = self._est_system_temp()
    
    def gen_el_dist(self, el_arr: np.ndarray = None,
                file: str = "", res = 0.1):
        """Generate a Elevation distribution from pickled Godot file w.
        resolution `res` in [Deg]"""

        if el_arr is None:
            if file == "":
                raise ValueError("Missing Data")
            with open(file, "rb") as f:
                el_arr = pickle.loads(f.read())
                
        bin_count = int((el_arr.max() - el_arr.min())/res)
        val, bins = np.histogram(el_arr, bin_count,
                                 weights=np.ones_like(el_arr)/len(el_arr))
        self.el_distribution = (bins[:-1], val)

    def _est_gain(self):
        """"Estimated gain for a parabolic reflector."""
        wave_len = C / (self.freq*1e9)
        g_max = ((np.pi*self.diameter)**2)/wave_len**2
        g_lin = g_max * self.eff
        return 10*np.log10(g_lin)
    
    def _est_system_temp(self):
        """Calculates the eqv system temperature based on G/T
        and estimated gain. The brightness temperature has been removed
        """
        g_lin = 10**(self.gain/10)
        gt_lin = 10**(self.gt/10)

        sys_temp = g_lin/gt_lin
        return sys_temp - self.tb
    
    def eff_gt(self, t_ant: float):
        """Calculates the equivalent G/T, for another brightness/
        antenna temperature"""
        g_lin = 10**(self.gain/10)
        t_sys = t_ant + self._est_system_temp()
        
        gt_eqv_lin = g_lin / t_sys
        return 10*np.log10(gt_eqv_lin)
        

_esa_dsa_eff = 0.65        
cebreros = station_t (
    40.453103969741,
    -4.367822163003614,
    0.727 + 0.04, # Ground height, and attenna height
    32, 
    55.8,
    35,
    _esa_dsa_eff)

malargue = station_t (
    -33.02128801912456,
    -69.04629959947883,
    0.787+0.04,
    32,
    55.8,
    35,
    _esa_dsa_eff)

new_norcia = station_t (
    -31.016434952605326,
    116.19856261578303,
    0.221+0.04,
    32,
    55.8,
    35,
    _esa_dsa_eff)

mani_link = [
    42.6, # dbi G_T
    10, #dBW p_t
    -1, # Gaseous Attenuation
    -0.5, # Other Attenuation, as pointing
]
"""Constant values in the mani to ground link"""
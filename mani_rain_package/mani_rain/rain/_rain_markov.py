import numpy as np
import mani_rain
from mani_rain.rain._rain_core import _rain_core

class markov_base:
    def __init__(self, model: np.ndarray, states: np.ndarray):
        self.state = 0
        self.states = states
        self.model = model
        self.s_range = np.arange(len(self.states))
        self.rng = np.random.default_rng()

    @staticmethod
    def from_file(model_path:str, states_path: str) -> "markov_base":
        """"Import model from external .npy files."""
        model = np.load(model_path)
        states = np.load(states_path)

        return markov_base(model, states)

    def draw_rain(self):
        """Draw next sample from the markov model
        
        Returns
        -----
        rain_rate_mmhr : float
            Rain rate in mmhr⁻¹
        """
        rain_state = self.rng.choice(self.s_range,
                                        p=self.model[self.state])
        
        self.state = rain_state
        rain_rate_mmhr = self.states[rain_state] * 60
        return rain_rate_mmhr

    


class markov_rain(_rain_core):
    def __init__(self, station, 
                 rain_model: markov_base,
                 a=0.187, b=1.099):
        super().__init__(station, a, b)
        self.rain_model = rain_model

    def attenuation_saunders(self, elevation, rain_rate = None):
        if rain_rate is None:
            rain_rate = self.rain_model.draw_rain()
        return super().attenuation_saunders(elevation, rain_rate)
    
    def eqv_attenuation(self, rain_rate = None):
        if rain_rate is None:
            rain_rate = self.rain_model.draw_rain()
            
        return super().eqv_attenuation(rain_rate)

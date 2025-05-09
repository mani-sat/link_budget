from ._rain_markov import markov_base, markov_rain

aau_model = markov_base.from_file(
    f"{__path__[0]}/models/aau_model.npy",
    f"{__path__[0]}/models/aau_states.npy"
)
nn_model = markov_base.from_file(
    f"{__path__[0]}/models/nn_model.npy",
    f"{__path__[0]}/models/nn_states.npy"
)
aau_ma_model = markov_base.from_file(
    f"{__path__[0]}/models/aau_ma_model.npy",
    f"{__path__[0]}/models/aau_ma_states.npy"
)




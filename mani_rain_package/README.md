# Mani rain package

The directory consist of the Python package used as a foundation for the rain, linkbugdet and data volume predictions for the Project.

To install the package run `pip install . `

## Structure

```
├── mani_rain
│   ├── rain
│   │   ├── models/
│   │   ├── __init__.py
│   │   ├── _rain_core.py
│   │   ├── _rain_markov.py
│   │   └── itu.py
│   ├── _core.py
│   ├── _dvbs2.py
│   ├── linkbugdet.py
│   └── __init__.py
├── examples
│   ├── ceb.ipynb
│   └── markov_model.ipynb
├── LICENSE
├── pyproject.toml
└── README.md 
```

The source code for the project are located in `mani_rain` split into different files.  
`mani_rain/rain` contains all files related to markov models and itu models. With `mani_rain/rain/models/` containing the pregenerated markov models for AAU and New Norcia.  
`exmaples` include usage example of itu and markov models.  


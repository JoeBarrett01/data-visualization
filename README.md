# Los Angeles County Sheriff Visualization

## Coding Requirements

1. Python-3
2. The below packages must be imported. 
3. The code must be ran from a terminal (such as VSCode, Powershell, Mac Terminal, etc) - Google colab as it does not fully support dash.
```
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import CubicSpline
```

## Data

Data has been made publicly available both in the repo for a csv and reading in a raw file shown below:

```
df = pd.read_csv(
    "https://raw.githubusercontent.com/JoeBarrett01/data-visualization/main/lancaster-contacts-data-store-2021-10-15.csv")
```

Data will be subset according to newdf. Further details on data collection for each variable are found in the [data dictionary](https://github.com/JoeBarrett01/data-visualization/blob/main/lancaster-contacts-data-dictionary-2021-10-15.csv).

## Running The Code

Run [visualization.py](https://github.com/JoeBarrett01/data-visualization/blob/main/visualization.py) with:
```
python3 visualization.py # if on mac
pipenv run python3 visualization.py #if using virtual environment
```

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.core.display import HTML, display
from math import ceil


def distplots(df, columns, hue=None, subplots_params=None):
    """
    :param df: Pandas DataFrame
    :param columns: list or string
        columns or column to visualize
    :param hue: list of string or string
    :param subplots_params: dictionary. Default: None
        parameters of plt.subplots()
    :return: None
        Draws sns.distplot
    """
    if isinstance(hue, str) or hue is None:
        hue = [hue]*len(columns)
    s_params = {
        'nrows': len(columns),
        'ncols': 1,
        'figsize': (15, len(columns) * 8)}
    if subplots_params is not None:
        s_params.update(subplots_params)
        if 'figsize' not in subplots_params:
            s_params['figsize'] = (s_params['nrows'] * 10, s_params['ncols'] * 8)

    fig, axis = plt.subplots(**s_params)
    display(HTML('<h1><B><center>' f"Distribution plots" "</span></h1>"))
    ax = axis.ravel()
    for idx, i in enumerate(columns):
        sns.histplot(x=i, data=df.dropna(subset=[i]), ax=ax[idx], hue=hue[idx])
        ax[idx].tick_params(labelsize=14)
        ax[idx].set_xlabel('')
        ax[idx].set_title(i, fontsize=23)
    plt.tight_layout()

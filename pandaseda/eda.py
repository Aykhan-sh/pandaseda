import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.core.display import HTML, display
from math import ceil
from typing import List, Tuple, Dict, AnyStr, Any, Union

class Describe:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.info = self.__desc(df)

    def __desc(self, df: pd.DataFrame) -> pd.DataFrame:
        desc = pd.DataFrame(
            {
                'dtypes': df.dtypes,
                'nunique': df.nunique(),
                "nans": df.isna().sum()
            }
        ).reset_index(level=0).merge(df.describe().T.reset_index(level=0), how='left').sort_values('nunique')
        return desc

    def display(self, sort: str='nunique') -> None:
        """Display function.
        
        :param sort: string
            Column to sort by
        :return: None
            Shows dataframe with information of every column
            
        """
        cm = sns.light_palette("gray", as_cmap=True)
        df = self.info.sort_values(by=sort)
        display(HTML('<h4><B><span style="padding-left: 30%";>' + f"shape {self.df.shape}" + "</span></h4>"))
        style1 = df.style.background_gradient(cmap=cm, subset=[sort])
        style2 = df.style.set_properties(**{'font-weight': 'bold'}, subset=['index'])
        style2.use(style1.export())
        display(style2)

    def countplot(self, nuniques: int, cols: int=2, hue: Union[str, List[int], None]=None, figsize: Tuple[int, int]=(10, 10), fontsize: int=14) -> None:  # TODO define out of the class
        display(HTML('<h1><B><center>' f"Countplots of data with less than {nuniques} unique values" "</span></h1>"))
        columns_for_counts = self.get_columns(number_of_nuniques=nuniques, mode='less')
        rows = ceil((len(columns_for_counts)) / cols)
        if figsize is None:
            figsize = (cols * 10, rows * 10)
        plt.figure(figsize=figsize)
        for i, (col) in enumerate(columns_for_counts):
            plt.subplot(rows, cols, i + 1)
            plt.title(col, fontdict={'size': 18})
            if hue is not None:
                if col == hue:
                    sns.countplot(x=col, data=self.df)
                else:
                    sns.countplot(x=col, data=self.df, hue=hue)
            else:
                sns.countplot(x=col, data=self.df)
            plt.xlabel('')
            plt.ylabel("count", fontsize=fontsize)
            plt.xticks(fontsize=fontsize)
            plt.yticks(fontsize=fontsize)

    def get_columns(self, number_of_nuniques: int=2, mode: str='equal') -> List:
        """Get Columns.
        
        :param number_of_nuniques:  one integer - number of unique values in column
        :param mode: string
            "less" - returns columns with number of unique values that is less than number_of_nuniques
            "equal" - returns columns with number of unique values that is equal to number_of_nuniques
            "more" - returns columns with number of unique values that is more than number_of_nuniques
        :return: returns array of columns with specific number of unique values
        
        """
        if mode not in ['less', 'more', 'equal']:
            raise Exception('mode must be one of: "less", "equal" or "more"')
        if mode == 'less':
            return self.info.loc[self.info['nunique'] < number_of_nuniques]['index'].values
        elif mode == 'more':
            return self.info.loc[self.info['nunique'] > number_of_nuniques]['index'].values
        elif mode == 'equal':
            return self.info.loc[self.info['nunique'] == number_of_nuniques]['index'].values


def correlation_heat_map(df: pd.DataFrame, figsize: Tuple=(10, 10), method: str='spearman') -> None:
    """Get correlation heatmap.
    
    :param df: Pandas DataFrame
    :param figsize: tuple
        size of the figure (x, y)
    :param method:  string. Default: "pearson"
        "method" parameter of pandas.Dataframe.corr function
        {"pearson", "kendall", "spearman"} or callable
    :return:
    
    """
    ax = sns.heatmap(df.corr(method=method), vmin=-1, vmax=1, annot=True)
    labels = [t.get_text() for t in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=30, horizontalalignment="right")
    sns.set(rc={'figure.figsize': figsize}, font_scale=1.4)


def correlation(df: pd.DataFrame, target: str, thresh: float=0.5, draw: bool=True, method: str='pearson', xlim: Tuple=(-1, 1)) -> List:
    """Get correlation.
    
    :param df: Pandas DataFrame
    :param target: string
        name of column to count correlation
    :param thresh: float [0.0, 1.0]. Default: 0.5
        show columns with absolute value of the score higher than threshold
    :param draw: bool. Default: True
        if True function will also draw barplot of correlation
    :param method: string. Default: "pearson"
        "method" parameter of pandas.Dataframe.corr function
        {"pearson", "kendall", "spearman"} or callable
    :param xlim: tuple of int. Default: (-1, 1)
        Limits for x axis.
        
    """
    cr = df.corrwith(df[target], method=method).sort_values()
    cr = cr[(cr < -thresh).values | (cr > thresh).values]
    cr = cr.loc[cr.index != target]
    if len(cr) == 0:
        return
    cr = cr.reset_index().rename({'index': 'variable', 0: 'score'}, axis=1)
    if draw:
        length = len(cr)
        plt.figure(figsize=(19, length * 2))
        sns.barplot(cr['score'], cr.variable)
        plt.xlim(*xlim)
        plt.title(f'{method} correlation with {target}', fontdict={'size': 30})
        plt.yticks(size=17);
        plt.xticks(size=17);
        plt.ylabel('');
        plt.xlabel('');
    return cr


def distplots(df: pd.DataFrame, columns: Union[str, List[int]], hue: Union[str, List[int], None]=None, subplots_params: Dict[Any, Any]=None) -> None:
    """Plot distplot.
    
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

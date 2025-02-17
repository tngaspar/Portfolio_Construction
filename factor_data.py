# functions to get data from factors

import pandas as pd

def get_factors(factor_list, start_date=None, end_date=None, ):
    """
    Gets data for factor(s) between 2 dates

    :param factor_list: list of factors names. Available factors:
        'SMB': Fama&French size factor;
        'HML': Fama&French value factor;
        'RMW': Fama&French profitability factor;
        'CMA': Fama&French investment factor;
        'Mkt-RF': Fama&French Market factor excess of risk free rate;
        'MOM': Momentum factor from Fama&French database;
        'BaB': Betting against Beta from AQR;
        'QMJ': Quality factor from AQR;
        'HML_Devil': Value factor with current market values from AQR;
        'UMD': Momentum factor from AQR
        Other factor from MSCI available
    :param start_date: first factor data date using datetime package format
    :param end_date: last factor data date using datetime package format
    :return: factor(s) data as pandas Dataframe
    """
    all_factors = pd.read_csv(r'Data\Factors\all_factors.csv', index_col=0).ffill()
    all_factors.index = pd.to_datetime(all_factors.index)

    if factor_list == ['all']:
        if start_date is None and end_date is None:
            r = all_factors
        else:
            r = all_factors.loc[start_date:end_date, :]
    elif not all(elem in all_factors.columns.values for elem in factor_list):
        print('Factor not found')
        print(factor_list)
        return
    else:
        if start_date is None and end_date is None:
            r = all_factors.loc[:, factor_list]
        else:
            r = all_factors.loc[start_date:end_date, factor_list]

    return r * 0.01

import pandas as pd
import stock_data
import factor_data
import statsmodels.api as sm
import numpy as np
from scipy.optimize import minimize
from dateutil.relativedelta import relativedelta
from alive_progress import alive_bar
from alive_progress import config_handler
config_handler.set_global(force_tty=True)

def get_loading_matrix(stocks, factors):
    # add case where dates dont match
    model = sm.OLS(stocks, factors).fit()
    parameters = model.params
    loading_matrix = pd.DataFrame(data=parameters.values, index=parameters.index, columns=stocks.columns).T

    return loading_matrix


def get_risk_contributions(asset_weights, stocks, factors):
    # add size debug
    x = asset_weights
    loadings_matrix = get_loading_matrix(stocks, factors)

    Sigma = stocks.cov().values
    # change Sigma based of results from OLS

    vol_x = np.sqrt(np.matmul(np.matmul(x, Sigma), x))

    Aplus = np.linalg.pinv(loadings_matrix)

    AT_x = np.matmul(loadings_matrix.values.T, x)
    Aplus_Sigma_x = np.matmul(np.matmul(Aplus, Sigma), x)

    risk_contributions = (AT_x * Aplus_Sigma_x) / vol_x
    #print(risk_contributions/vol_x)
    print(sum(x))
    return risk_contributions


def sigma_x(x, stock_returns):
    Sigma = stock_returns.cov().values
    vol_x = np.sqrt(np.matmul(np.matmul(x, Sigma), x))

    return vol_x


def weights_factor_risk_parity(stocks, factors, x0):
    
    n_stocks = stocks.shape[1]
    if x0 is None:
        x0 = np.ones(n_stocks) * 1 / n_stocks

    fun = lambda x: sum((get_risk_contributions(x, stocks, factors) / sigma_x(x, stock_returns=stocks) - 1 /
                         factors.shape[1]) ** 2)

    # constrains
    cons = [{'type': 'ineq', 'fun': lambda x: -sum(x) + 1},
            {'type': 'ineq', 'fun': lambda x: sum(x) - 1}]

    # bounds
    bounds = [(-1 / n_stocks, 1) for n in range(n_stocks)]

    res = minimize(fun, x0, method='SLSQP', bounds=bounds, constraints=cons, tol=0.00001, options={'disp': True})
    return res.x


def portfolio_weights_factor_risk_parity(tickers, factor_tickers, start_date, end_date, portfolio_rebalance_period):
    business_days_end_months = pd.date_range(start_date, end_date, freq=portfolio_rebalance_period)
    portfolio_weights = pd.DataFrame(index=business_days_end_months, columns=tickers)
    x0 = None
    with alive_bar(len(business_days_end_months)) as bar:
        for t in business_days_end_months:
            stocks = stock_data.get_daily_returns(tickers, t + relativedelta(months=-48), t)[1:]
            factors = factor_data.get_factors(factor_tickers, stocks.index[0], stocks.index[-1]) * 0.01
            print(stocks)
            print(factors)
            portfolio_weights.loc[t] = weights_factor_risk_parity(stocks, factors, x0)
            x0 = portfolio_weights.loc[t]
            bar()

    return portfolio_weights

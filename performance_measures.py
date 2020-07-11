# calculation for performance measures of portfolios are hosted here
import empyrical as ep
import stock_data as sdata
from scipy import stats
import pandas as pd


def performance_measures(portfolio_daily_returns, benchmark_returns=None, var_probability=0.05):
    # return pandas of all measures
    measures = {'Annualized Returns (CAGR)': annual_returns_cagr(portfolio_daily_returns),
                'Cumulative Returns': cumulative_returns(portfolio_daily_returns),
                'Annualized Volatility': annual_volatility(portfolio_daily_returns),
                'Sharpe Ratio': sharpe_ratio(portfolio_daily_returns),
                'Max Drawdown': max_drawdown(portfolio_daily_returns),
                'Calmar Ratio': calmar_ratio(portfolio_daily_returns),
                'Stability': stability(portfolio_daily_returns),
                'Skewness': skewness(portfolio_daily_returns),
                'Kurtosis': kurtosis(portfolio_daily_returns),
                'Daily Value at Risk (VaR)': value_at_risk(portfolio_daily_returns, var_probability),
                'Expected Shortfall': expected_shortfall(portfolio_daily_returns, var_probability),
                'Tail Ratio': tail_ratio(portfolio_daily_returns),
                'Alpha': alpha(portfolio_daily_returns, benchmark_returns),
                'Beta': beta(portfolio_daily_returns, benchmark_returns)
                }
    return pd.Series(measures)


def annual_returns_cagr(portfolio_daily_returns):
    return ep.annual_return(portfolio_daily_returns)


def cumulative_returns(portfolio_daily_returns):
    return ep.cum_returns_final(portfolio_daily_returns)


def annual_volatility(portfolio_daily_returns):
    return ep.annual_volatility(portfolio_daily_returns)


def sharpe_ratio(portfolio_daily_returns, risk_free=0):
    return ep.sharpe_ratio(portfolio_daily_returns)


def max_drawdown(portfolio_daily_returns):
    return ep.max_drawdown(portfolio_daily_returns)


def calmar_ratio(portfolio_daily_returns):
    return ep.calmar_ratio(portfolio_daily_returns)


def alpha(portfolio_daily_returns, benchmark_returns=None):
    if benchmark_returns is None:
        benchmark_returns = sdata.get_sp500_index_returns(portfolio_daily_returns.index[0],
                                                          portfolio_daily_returns.index[-1])
    return ep.alpha(portfolio_daily_returns, benchmark_returns)


def beta(portfolio_daily_returns, benchmark_returns=None):
    if benchmark_returns is None:
        benchmark_returns = sdata.get_sp500_index_returns(portfolio_daily_returns.index[0],
                                                          portfolio_daily_returns.index[-1])
    return ep.beta(portfolio_daily_returns, benchmark_returns)


def stability(portfolio_daily_returns):
    return ep.stability_of_timeseries(portfolio_daily_returns)


def skewness(portfolio_daily_returns):
    return stats.skew(portfolio_daily_returns)


def kurtosis(portfolio_daily_retuns):
    return stats.kurtosis(portfolio_daily_retuns)


def tail_ratio(portfolio_daily_returns):
    return ep.tail_ratio(portfolio_daily_returns)


def value_at_risk(portfolio_daily_returns, probability=0.05):
    return ep.value_at_risk(portfolio_daily_returns, probability)


def expected_shortfall(portfolio_daily_returns, probability):
    return ep.conditional_value_at_risk(portfolio_daily_returns, probability)

import os
os.chdir('../')

import datetime as dt
import importlib
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# ############### Import my scripts ###############
import stock_data
import risk_parity as rp
import factor_data
import factor_risk_parity as frp
import backtest_functions as bfunc
import equal_weight as ew
import factor_weight_parity as fwp
import performance_measures as perf



# Reload frequently changed scripts
importlib.reload(rp)
importlib.reload(factor_data)
importlib.reload(frp)
importlib.reload(bfunc)
importlib.reload(ew)
importlib.reload(fwp)
importlib.reload(perf)


# ############# chosing 4 factors to use
f_start_date = dt.date(1990, 12, 31)
f_end_date = dt.date(2004, 12, 31)

factors_cluster_1 = factor_data.get_factors(['CMA', 'HML_Devil'], f_start_date, f_end_date)
factors_cluster_2 = factor_data.get_factors(['BaB', 'RMW', 'QMJ'], f_start_date, f_end_date)

perf_measures = pd.concat([
    perf.performance_measures(factors_cluster_1['CMA']).rename('CMA'),
    perf.performance_measures(factors_cluster_1['HML_Devil']).rename('HML_Devil'),
    perf.performance_measures(factors_cluster_2['BaB']).rename('BaB'),
    perf.performance_measures(factors_cluster_2['RMW']).rename('RMW'),
    perf.performance_measures(factors_cluster_2['QMJ']).rename('QMJ')
    ], axis=1
)

perf_measures.round(2).to_csv(r'Implementation/factor_cluster_measures.csv')


# ############### Data gathering ###############
sp500 = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK',
         'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'AGN', 'ADS', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR',
         'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM',
         'AON', 'AOS', 'APA', 'AIV', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ARNC', 'ANET', 'AJG', 'AIZ', 'ATO', 'T', 'ADSK',
         'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BK', 'BAX', 'BDX', 'BRK-B', 'BBY', 'BIIB', 'BLK', 'BA',
         'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BF-B', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CPRI', 'CAH',
         'KMX', 'CCL', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHTR', 'CVX',
         'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO',
         'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'COTY',
         'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'FANG', 'DLR', 'DFS',
         'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'ETFC', 'EMN',
         'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR', 'EOG', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'EVRG',
         'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE',
         'FRC', 'FISV', 'FLT', 'FLIR', 'FLS', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'GPS',
         'GRMN', 'IT', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'GWW', 'HRB', 'HAL', 'HBI', 'HOG',
         'HIG', 'HAS', 'HCA', 'PEAK', 'HP', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HFC', 'HOLX', 'HD', 'HON', 'HRL',
         'HST', 'HPQ', 'HUM', 'HBAN', 'HII', 'IEX', 'IDXX', 'INFO', 'ITW', 'ILMN', 'IR', 'INTC', 'ICE', 'IBM', 'INCY',
         'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JKHY', 'J', 'JBHT', 'SJM', 'JNJ', 'JCI',
         'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KHC', 'KR', 'LB', 'LHX', 'LH',
         'LRCX', 'LW', 'LVS', 'LEG', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LYB', 'MTB',
         'M', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MKC', 'MXIM', 'MCD', 'MCK', 'MDT', 'MRK', 'MET',
         'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI',
         'MYL', 'NDAQ', 'NOV', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN',
         'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE',
         'ORCL', 'PCAR', 'PKG', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PM', 'PSX',
         'PNW', 'PXD', 'PNC', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO',
         'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTN', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP',
         'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SLG', 'SNA',
         'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR',
         'TGT', 'TEL', 'FTI', 'TFX', 'TXN', 'TXT', 'TMO', 'TIF', 'TJX', 'TSCO', 'TDG', 'TRV', 'TFC', 'TWTR', 'TSN',
         'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'VFC', 'VLO',
         'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VIAC', 'V', 'VNO', 'VMC', 'WRB', 'WAB', 'WMT', 'WBA', 'DIS',
         'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX',
         'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']
tickers = sp500

# portfolio investment period:
start_date = dt.date(2004, 12, 31)
end_date = dt.date(2019, 12, 31)

# remove NaN columns from investment universe to prevent errors:
p_tickers = stock_data.get_prices(tickers, start_date - dt.timedelta(days=365*4),
                                  start_date - dt.timedelta(days=365*4) + dt.timedelta(days=+5))
nan_cols = [i for i in p_tickers.columns if p_tickers[i].isnull().any()]
tickers = [eq for eq in tickers if eq not in nan_cols]


# Equal weights (long only):
ew_portfolio_weights = ew.portfolio_weights_ew(tickers, start_date, end_date, 'BM')
ew_daily_returns = bfunc.daily_returns_of_portfolio(ew_portfolio_weights)
ew_daily_returns.to_csv(r'Output\ew_daily_returns.csv')

# Factor Weight Parity:
factor_tickers = ['SMB', 'MOM', 'CMA', 'BaB']
fwp_portfolio_weights = fwp.portfolio_weights_factor_weight_parity(tickers, factor_tickers, start_date, end_date, 'BM')
fwp_daily_returns = bfunc.daily_returns_of_portfolio(fwp_portfolio_weights)
fwp_portfolio_weights.to_csv(r'Implementation\fwp_x_weights_4f.csv')
fwp_daily_returns.to_csv(r'Output\fwp_daily_returns.csv')

portfolios_perf_measures = pd.concat([
    perf.performance_measures(ew_daily_returns).rename('EW'),
    perf.performance_measures(fwp_daily_returns).rename('FWP')
    ], axis=1
)
portfolios_perf_measures.round(2).to_csv(r'Implementation\ew_and_fwp_performance measures.csv')

#plot here






# delete

factor_tickers2 = ['SMB', 'MOM', 'CMA', 'QMJ']
fwp_portfolio_weights2 = fwp.portfolio_weights_factor_weight_parity(tickers, factor_tickers2, start_date, end_date, 'BM')
fwp_daily_returns2 = bfunc.daily_returns_of_portfolio(fwp_portfolio_weights2)
fwp_daily_returns2.to_csv(r'Output\fwp_daily_returns.csv')

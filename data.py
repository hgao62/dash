# data.py
import pandas as pd
import numpy as np

def create_sample_data():
    dates = pd.date_range('2023-01-01', periods=12, freq='M')
    stocks = ['股票A', '股票B', '股票C', '股票D']
    df = pd.DataFrame()

    for stock in stocks:
        returns = np.random.normal(0.02, 0.05, size=len(dates))
        volumes = np.random.randint(1000, 10000, size=len(dates))
        prices = [100]
        for ret in returns:
            prices.append(prices[-1] * (1 + ret))
        prices = prices[1:]  # Remove initial price
        
        temp_df = pd.DataFrame({
            '日期': dates.strftime('%Y-%m'),
            '股票': stock,
            '收益率': returns,
            '交易量': volumes,
            '价格': prices
        })
        df = pd.concat([df, temp_df])
    
    return df

def calculate_stats(data):
    stats_df = data.groupby('股票').agg(
        平均收益率=('收益率', 'mean'),
        波动率=('收益率', 'std'),
        最大收益=('收益率', 'max'),
        最小收益=('收益率', 'min'),
        总交易量=('交易量', 'sum'),
        平均价格=('价格', 'mean')
    ).reset_index()

    # Formatting
    stats_df['平均收益率'] = stats_df['平均收益率'].map('{:.2%}'.format)
    stats_df['波动率'] = stats_df['波动率'].map('{:.2%}'.format)
    return stats_df
df = create_sample_data()
stats_df = calculate_stats(df)
import pandas as pd
from tqdm import tqdm
from eastmoney import f10

# 读取 CSV 文件，指定股票代码列的类型为 str
df = pd.read_csv('tdx_stocks.csv', dtype={'股票代码': str})

# 创建新的列来保存实际控制人的信息和实际控制人控股比例
df['实际控制人'] = ''
df['实际控制人控股比例'] = ''

# 对每一行进行迭代，使用tqdm显示进度
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        # 使用 shareholder_research 方法获取实际控制人的信息
        result = f10.shareholder_research(f"{row['交易所简码']}{row['股票代码']}")

        # 更新实际控制人的信息和实际控制人控股比例
        df.loc[index, '实际控制人'] = result['sjkzr'][0]['HOLDER_NAME']
        df.loc[index, '实际控制人控股比例'] = result['sjkzr'][0]['HOLD_RATIO']
    except Exception as e:
        print(f"An error occurred with the stock code: {row['股票代码']}. Error message: {e}")
        continue

# 保存新的 CSV 文件
df.to_csv('tdx_stocks_updated.csv', index=False)

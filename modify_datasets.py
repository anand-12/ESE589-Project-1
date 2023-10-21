import pandas as pd


file_path = "haberman.csv"
df = pd.read_csv(file_path)


for col_num, col_name in enumerate(df.columns, start=1):
    df[col_name] = "F" + str(col_num) + "-" + df[col_name].astype(str)


output_path = "haberman.csv"
df.to_csv(output_path, index=False)

import pandas as pd
import glob
import os

folder_path = 'C:/skn_17/web_crawling/crawling/csv/hyundai'

csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
# 파일 읽고 합치기
df_list = [pd.read_csv(file) for file in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

# 결과 저장
combined_df.to_csv('hyundai_all.csv', index=False)

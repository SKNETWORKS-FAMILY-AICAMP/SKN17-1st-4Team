import pandas as pd

df = pd.read_csv('kia_faq_all_final.csv')

df['기업명'] = '기아'
df['질문ID'] = ['Q' + str(i).zfill(3) for i in range(1, len(df) + 1)]

df = df[['기업명', '질문ID', '질문', '답변']]

df.to_csv('kia_faq_all_final_new.csv', index=False)
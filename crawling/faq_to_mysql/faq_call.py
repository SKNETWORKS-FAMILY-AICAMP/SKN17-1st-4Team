import pandas as pd

kia_csv = pd.read_csv('kia_faq_all_final_new.csv')
hyundai_csv = pd.read_csv('hyundai_all_new.csv')

kia_csv['question_id'] = 'K-' + kia_csv['질문ID'].astype(str)
hyundai_csv['question_id'] = 'H-' + hyundai_csv['질문ID'].astype(str)

kia_csv = kia_csv.rename(columns={
    '기업명': 'company_name',
    '질문': 'question',
    '답변': 'answer'
})

hyundai_csv = hyundai_csv.rename(columns={
    '기업명': 'company_name',
    '질문': 'question',
    '답변': 'answer'
})

kia_csv = kia_csv[['question_id', 'company_name', 'question', 'answer']]
hyundai_csv = hyundai_csv[['question_id', 'company_name', 'question', 'answer']]

faq_combined = pd.concat([kia_csv, hyundai_csv], ignore_index=True)

faq_combined.to_csv('company_faq_data.csv', index=False)
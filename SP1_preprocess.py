import pandas as pd

DATA_IN_PATH = "./datasets/"
ROW_DATA = "final.csv"
EN_DATA = "final_with_en_slogans.csv"
KO_DATA = "final_ko_slogan.csv"

eng = "[A-Za-z]"

row_df = pd.read_csv(DATA_IN_PATH + ROW_DATA)

row_df.dropna()
row_df.drop_duplicates(keep='first')
row_df.reset_index()

temp_df = row_df.copy()
temp_df["company"] = temp_df["company"].replace(
    "[-=+#/\:^$@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`'…》]", "", regex=True
)
temp_df["slogan"] = temp_df["slogan"].replace(
    "[-=+#/\:^$@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`'…》]", "", regex=True
)

row_df = temp_df
print(row_df)


# 영어 들어간 row만 선택
def select_rows_with_eng(target_df, target_text):
    temp_df = target_df.copy()
    temp_df = target_df[temp_df.slogan.str.contains(target_text)]
    temp_df.reset_index(drop=True, inplace=True)

    return temp_df

en_df = select_rows_with_eng(row_df, eng)
en_df.to_csv(DATA_IN_PATH + EN_DATA, encoding='utf-8-sig', index=None)


def delete_rows_with_eng(target_df, target_text):
    temp_df = target_df.copy()
    temp_df = target_df[
        ~temp_df.slogan.str.contains(target_text)
    ]  # 영어를 포함하지 않은 행만 남기기(not을 표현할때 ~ 사용)
    temp_df.reset_index(drop=True, inplace=True)

    return temp_df


ko_df = delete_rows_with_eng(row_df, eng)
ko_df.to_csv(DATA_IN_PATH + KO_DATA, encoding='utf-8-sig', index=None)

print(ko_df.head())

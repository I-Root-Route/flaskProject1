import pandas as pd
import numpy as np
import glob
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
path = BASE_DIR + '/uploads/*.csv'
test_file = glob.glob(path)
X_testset = pd.read_csv(test_file[0])
X_testset = X_testset.dropna(how="all", axis=1)
non_unique_columns = []
for column in X_testset.columns:
    if X_testset[column].nunique() == 1:
        non_unique_columns.append(column)

# print(X_testset["勤務地　市区町村コード"].value_counts())

non_unique_columns.extend(["土日祝のみ勤務",
                           "（派遣先）概要　勤務先名（漢字）",
                           "期間・時間　勤務開始日",
                           "仕事内容",
                           "勤務地　最寄駅1（駅名）",
                           "勤務地　最寄駅2（駅名）",
                           "（派遣先）概要　事業内容",
                           "動画ファイル名",
                           "（派遣先）職場の雰囲気",
                           "（紹介予定）待遇・福利厚生",
                           "期間･時間　備考",
                           "勤務地　備考",
                           "勤務地　最寄駅2（沿線名）",
                           "勤務地　都道府県コード",
                           "（派遣先）配属先部署　男女比　女",
                           "休日休暇(月曜日)",
                           "休日休暇(火曜日)",
                           "休日休暇(水曜日)",
                           "休日休暇(木曜日)",
                           "休日休暇(金曜日)",
                           "勤務地　最寄駅1（沿線名）",
                           "休日休暇　備考",
                           "給与/交通費　備考",
                           "勤務地　最寄駅2（駅からの交通手段）",
                           "学校・公的機関（官公庁）",
                           "勤務地　最寄駅1（駅からの交通手段）",
                           "勤務地　最寄駅1（分）",
                           "勤務地　最寄駅2（分）",
                           "（派遣先）配属先部署",
                           "経験者優遇",
                           "（紹介予定）年収・給与例",
                           "英語力を活かす",
                           "Excelのスキルを活かす",
                           "英語以外の語学力を活かす",
                           "PCスキル不要",
                           "お仕事のポイント（仕事PR）",
                           "休日休暇(日曜日)",
                           "休日休暇(土曜日)",
                           "シフト勤務",
                           "期間・時間　勤務時間",
                           "大量募集"
                           ])

# 平日の休日休暇をまとめる

X_testset["休日休暇(平日)"] = X_testset["休日休暇(月曜日)"] + \
                        X_testset["休日休暇(火曜日)"] + \
                        X_testset["休日休暇(水曜日)"] + \
                        X_testset["休日休暇(水曜日)"] + \
                        X_testset["休日休暇(木曜日)"] + \
                        X_testset["休日休暇(金曜日)"]

# X_dataset["休日休暇(土日)"] = X_dataset["休日休暇(土曜日)"] + X_dataset["休日休暇(日曜日)"]
# X_testset["休日休暇(土日)"] = X_testset["休日休暇(土曜日)"] + X_testset["休日休暇(日曜日)"]

X_testset = X_testset.drop(non_unique_columns, axis=1)

X_testset = pd.get_dummies(X_testset, columns=["（紹介予定）雇用形態備考"])

# お仕事名
key_words = ["未経験", "年収", "月", "週1", "週2", "週３", "週４", "正社員", "残業", "時", "定時", "退社", "円", "実働", "時給", "賞与"]
for index, row in enumerate(X_testset["お仕事名"].values):
    score = 0
    for i in range(len(key_words)):
        if key_words[i] in row:
            score += 1
    X_testset.loc[index, "お仕事名"] = score
X_testset["お仕事名"] = X_testset["お仕事名"].astype(int)

# (紹介予定) 休日休暇
X_testset["（紹介予定）休日休暇"] = X_testset["（紹介予定）休日休暇"].str[:1]
X_testset = pd.get_dummies(X_testset, columns=["（紹介予定）休日休暇"])

# (紹介予定) 入社時期
X_testset["（紹介予定）入社時期"] = X_testset["（紹介予定）入社時期"].str[:1]
X_testset = pd.get_dummies(X_testset, columns=["（紹介予定）入社時期"])
X_testset = X_testset.drop(["（紹介予定）入社時期_※"], axis=1)

# （派遣先）勤務先写真ファイル名

for index, row in enumerate(X_testset["（派遣先）勤務先写真ファイル名"].values):
    isfile = 0
    if row is not np.nan:
        isfile = 1
    X_testset.loc[index, "（派遣先）勤務先写真ファイル名"] = isfile
X_testset["（派遣先）勤務先写真ファイル名"] = X_testset["（派遣先）勤務先写真ファイル名"].astype(int)

# 応募資格
apply_keys = ["業界経験が必要", "短大", "大卒", "高卒", "専門"]
for index, row in enumerate(X_testset["応募資格"].values):
    difficulty = 0
    if apply_keys[0] in row:
        difficulty += 4
    elif apply_keys[1] in row:
        difficulty += 3
    elif apply_keys[2] in row:
        difficulty += 5
    elif apply_keys[3] in row:
        difficulty += 2
    elif apply_keys[4] in row:
        difficulty += 1
    else:
        difficulty += 0
    X_testset.loc[index, "応募資格"] = difficulty
X_testset["応募資格"] = X_testset["応募資格"].astype(int)

# Encoding
X_testset["勤務地　市区町村コード"] = X_testset["勤務地　市区町村コード"].map(
    {211: 1, 132: 2, 101: 3, 153: 4, 217: 5, 122: 1, 201: 2, 106: 3, 128: 4, 208: 5, 127: 6, 116: 7, 103: 8, 205: 9,
     102: 10})
X_testset["職種コード"] = X_testset["職種コード"].map(
    {22020: 0, 20810: 1, 20320: 2, 80310: 3, 20020: 4, 22030: 5, 20030: 6, 20040: 7, 22010: 8})

X_testset["会社概要　業界コード"] = X_testset["会社概要　業界コード"].map({30000: 1})
# X_dataset = pd.get_dummies(X_dataset, columns=["会社概要　業界コード"])

# Set Index
X_testset = X_testset.set_index(["お仕事No."])

X_testset.to_csv(BASE_DIR + '/processed/X_test_processed.csv')

"""
if __name__ == '__main__':
    # pd.set_option('display.max_rows', 200)
    # pd.set_option('display.max_columns', 200)
    # print(X_dataset.isnull().sum())
    # print(len(X_testset[X_testset["勤務地　市区町村コード_103"] == 1]))
    # print(X_testset.select_dtypes(include="object").columns)
    # print(X_testset["お仕事のポイント（仕事PR）"].value_counts())
    # X_dataset.to_csv('X_train_processed.csv')
    X_testset.to_csv('./processed/X_test_processed.csv')
"""
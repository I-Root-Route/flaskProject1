import xgboost as xgb
import pickle
import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
model = pickle.load(open("xgb_model.pickle", "rb"))

testset_X = pd.read_csv(BASE_DIR + '/processed/X_test_processed.csv')

testset_X = testset_X.drop("（紹介予定）雇用形態備考_アルバイト社員", axis=1)

test_X = testset_X.iloc[:, 1:].values

testset = xgb.DMatrix(test_X)
my_pred = pd.DataFrame()
my_pred["お仕事No."] = testset_X.iloc[:, 0]
my_pred["応募数 合計"] = model.predict(testset)
my_pred.to_csv(BASE_DIR + '/final_result/final_result.csv', index=False)



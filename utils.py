import pandas as pd

def get_test_data(file_path):
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")

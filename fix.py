import ast
import pandas as pd
from datasets import Dataset

def load_data(csv_path):
    print("loading data...")
    df = pd.read_csv("C:/Users/korry/Documents/flickr30k_rgb.csv").dropna().reset_index(drop=True)
    print("columns:", df.columns)
    print("shape (rows, cols):", df.shape)
    print("sample caption:", df["caption"][0])
    print("rgb length (first row):", len(eval(df["rgb_values"][0])))
    print("sample rgb values:", df["rgb_values"][0])

    # properly parse the RGB values if stored as string
    df["rgb_values"] = df["rgb_values"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # convert list to comma-separated string
    df["rgb_values"] = df["rgb_values"].apply(lambda x: ", ".join(map(str, x)))

    df["text"] = df["caption"] + " <RGB> " + df["rgb_values"]
    return Dataset.from_pandas(df[["text"]])

data = load_data("C:/Users/korry/Documents/flickr30k_rgb.csv")
print(data[0])

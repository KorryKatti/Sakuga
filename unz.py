import gzip
import shutil

with gzip.open(r"C:\Users\korry\Documents\flickr30k_rgb.csv.gz", "rb") as f_in:
    with open(r"C:\Users\korry\Documents\flickr30k_rgb.csv", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

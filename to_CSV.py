import csv
import gzip
from datasets import load_dataset
from PIL import Image
import numpy as np

# function to process a single image and return the rows for CSV
def process_image(sample):
    try:
        img = sample["image"].resize((96, 96))  # changed to 96x96
        rgb_matrix = np.array(img)
        flat_rgb = ",".join(f"{pixel[0]},{pixel[1]},{pixel[2]}" for row in rgb_matrix for pixel in row)
        captions = [sample[f"caption_{i}"] for i in range(5)]

        # generate a row for each caption
        rows = []
        for caption in captions if isinstance(captions, list) else [captions]:
            print(f"Processing: {caption[:60]}...")  # show first 60 chars of caption
            rows.append([caption, flat_rgb])
        return rows
    except Exception as e:
        print(f"Error processing image: {e}")
        return []

if __name__ == "__main__":
    # load the flickr30k dataset
    dataset = load_dataset("jxie/flickr8k")

    # open gzip csv file for writing
    with gzip.open(r"C:\Users\korry\Documents\flickr30k_rgb_96.csv.gz", "wt", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # write header
        header = ["caption", "rgb_values"]
        writer.writerow(header)

        # process images sequentially
        for i, sample in enumerate(dataset["test"]):
            rows = process_image(sample)
            for row in rows:
                writer.writerow(row)
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(dataset['test'])} images")

    print("CSV generation complete!")



# # import csv
# # from datasets import load_dataset
# # from PIL import Image
# # import numpy as np

# # # function to process a single image and return the rows for CSV
# # def process_image(sample):
# #     try:
# #         img = sample["image"].resize((512, 512))
# #         rgb_matrix = np.array(img)
# #         flat_rgb = [f"{pixel[0]},{pixel[1]},{pixel[2]}" for row in rgb_matrix for pixel in row]
# #         captions = sample["caption"]

# #         # generate a row for each caption
# #         rows = []
# #         for caption in captions if isinstance(captions, list) else [captions]:
# #             print(f"Processing: {caption[:60]}...")  # show first 60 chars of caption
# #             rows.append([caption] + flat_rgb)
# #         return rows
# #     except Exception as e:
# #         print(f"Error processing image: {e}")
# #         return []

# # if __name__ == "__main__":
# #     # load the flickr30k dataset
# #     dataset = load_dataset("nlphuji/flickr30k")

# #     # open csv file for writing
# #     with open("flickr30k_rgb.csv", "w", newline="") as csvfile:
# #         writer = csv.writer(csvfile)
# #         # write header
# #         header = ["caption"] + [f"r{i},g{i},b{i}" for i in range(512 * 512)]
# #         writer.writerow(header)

# #         # process images sequentially
# #         for i, sample in enumerate(dataset["test"]):
# #             rows = process_image(sample)
# #             for row in rows:
# #                 writer.writerow(row)
# #             if (i + 1) % 100 == 0:
# #                 print(f"Processed {i + 1}/{len(dataset['test'])} images")

# #     print("CSV generation complete!")

# # discarding this version since i realized a bit late that having too many columns might pose a problem in fine tuning

# import csv
# from datasets import load_dataset
# from PIL import Image
# import numpy as np

# # function to process a single image and return the rows for CSV
# def process_image(sample):
#     try:
#         img = sample["image"].resize((512, 512))
#         rgb_matrix = np.array(img)
#         flat_rgb = ",".join(f"{pixel[0]},{pixel[1]},{pixel[2]}" for row in rgb_matrix for pixel in row)
#         captions = sample["caption"]

#         # generate a row for each caption
#         rows = []
#         for caption in captions if isinstance(captions, list) else [captions]:
#             print(f"Processing: {caption[:60]}...")  # show first 60 chars of caption
#             rows.append([caption, flat_rgb])
#         return rows
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return []

# if __name__ == "__main__":
#     # load the flickr30k dataset
#     dataset = load_dataset("nlphuji/flickr30k")

#     # open csv file for writing
#     with open("flickr30k_rgb.csv", "w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         # write header
#         header = ["caption", "rgb_values"]
#         writer.writerow(header)

#         # process images sequentially
#         for i, sample in enumerate(dataset["test"]):
#             rows = process_image(sample)
#             for row in rows:
#                 writer.writerow(row)
#             if (i + 1) % 100 == 0:
#                 print(f"Processed {i + 1}/{len(dataset['test'])} images")

#     print("CSV generation complete!")

# so the thing is 30k images captioning is far too ehavy for my device hence i am watering it down to 8k

# import csv
# import gzip
# from datasets import load_dataset
# from PIL import Image
# import numpy as np

# # function to process a single image and return the rows for CSV
# def process_image(sample):
#     try:
#         img = sample["image"].resize((512, 512))
#         rgb_matrix = np.array(img)
#         flat_rgb = ",".join(f"{pixel[0]},{pixel[1]},{pixel[2]}" for row in rgb_matrix for pixel in row)
#         captions = captions = [sample[f"caption_{i}"] for i in range(5)]


#         # generate a row for each caption
#         rows = []
#         for caption in captions if isinstance(captions, list) else [captions]:
#             print(f"Processing: {caption[:60]}...")  # show first 60 chars of caption
#             rows.append([caption, flat_rgb])
#         return rows
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return []

# if __name__ == "__main__":
#     # load the flickr30k dataset
#     dataset = load_dataset("jxie/flickr8k")

#     # open gzip csv file for writing
#     with gzip.open(r"C:\Users\korry\Documents\flickr30k_rgb.csv.gz", "wt", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         # write header
#         header = ["caption", "rgb_values"]
#         writer.writerow(header)

#         # process images sequentially
#         for i, sample in enumerate(dataset["test"]):
#             rows = process_image(sample)
#             for row in rows:
#                 writer.writerow(row)
#             if (i + 1) % 100 == 0:
#                 print(f"Processed {i + 1}/{len(dataset['test'])} images")

#     print("CSV generation complete!")

# 512x512 is too much for my laptop so i am going to use  a lower version instead
# going with 128x128

# import csv
# import gzip
# from datasets import load_dataset
# from PIL import Image
# import numpy as np

# # function to process a single image and return the rows for CSV
# def process_image(sample):
#     try:
#         img = sample["image"].resize((128, 128))  # changed from 512x512 to 128x128
#         rgb_matrix = np.array(img)
#         flat_rgb = ",".join(f"{pixel[0]},{pixel[1]},{pixel[2]}" for row in rgb_matrix for pixel in row)
#         captions = [sample[f"caption_{i}"] for i in range(5)]

#         # generate a row for each caption
#         rows = []
#         for caption in captions if isinstance(captions, list) else [captions]:
#             print(f"Processing: {caption[:60]}...")  # show first 60 chars of caption
#             rows.append([caption, flat_rgb])
#         return rows
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return []

# if __name__ == "__main__":
#     # load the flickr30k dataset
#     dataset = load_dataset("jxie/flickr8k")

#     # open gzip csv file for writing
#     with gzip.open(r"C:\Users\korry\Documents\flickr30k_rgb_128.csv.gz", "wt", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         # write header
#         header = ["caption", "rgb_values"]
#         writer.writerow(header)

#         # process images sequentially
#         for i, sample in enumerate(dataset["test"]):
#             rows = process_image(sample)
#             for row in rows:
#                 writer.writerow(row)
#             if (i + 1) % 100 == 0:
#                 print(f"Processed {i + 1}/{len(dataset['test'])} images")

#     print("CSV generation complete!")

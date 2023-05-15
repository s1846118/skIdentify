import os
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil

# path1 - path to annotations folder, path2 - path to images folder 
def ttsplit(path1, path2):

    # List of annotations
    ann_files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1,f))]
    # List of photo filenames
    photos = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2,f))]

    # Create dict with image name as key and annotations as values
    image_anns = {}

    for img in photos:

        # UID for key/annotations
        uid = img.split('-')[0]

        image_anns[img] = []

        # Iterate through annotations and add to dict
        for i,ann in enumerate(ann_files):

            if uid in ann:
                image_anns[img].append(ann)

                # Remove image ann from list for faster runtime.
                if i == len(ann_files)-1:
                    ann_files = ann_files[:i]
                else:
                    ann_files = ann_files[:i] + ann_files[i+1:]

    # Train test split
    df = pd.DataFrame(image_anns.keys(),columns=['img_names'])
    train, test = train_test_split(df, test_size=0.1, random_state=42)

    print(image_anns)

    # Write to respective test, train folders
    for key in train['img_names']:
        # Adding image
        src_img = path2 + "/" + key
        dst_img = path2.split("/")[0] + '/train/' + key
        shutil.copy(src_img,dst_img)

        # Adding the XML annotations
        for ann in image_anns[key]:
            # Adding image
            src_img = path1 + "/" + ann
            dst_img = path1.split("/")[0] + '/train/' + ann
            shutil.copy(src_img,dst_img)

    # Write to respective test, train folders
    for key in test['img_names']:
        # Adding image
        src_img = path2 + "/" + key
        dst_img = path2.split("/")[0] + '/test/' + key
        shutil.copy(src_img,dst_img)

        # Adding the XML annotations
        for ann in image_anns[key]:
            # Adding image
            src_img = path1 + "/" + ann
            dst_img = path1.split("/")[0] + '/test/' + ann
            shutil.copy(src_img,dst_img)

if __name__ == '__main__':

    ttsplit('walkie-talkie-labeled/Annotations','walkie-talkie-labeled/images')
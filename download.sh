#!/bin/bash
if [ ! -d "./dataset" ]; then
  mkdir dataset
fi
if [ -f "./dataset/new-plant-diseases-dataset.zip" ]; then
  echo "File already exists. Skipping download."
  exit 0
fi
echo "Downloading new-plant-diseases-dataset.zip..."
curl -L -o ./dataset/new-plant-diseases-dataset.zip\
  https://www.kaggle.com/api/v1/datasets/download/vipoooool/new-plant-diseases-dataset
echo "Download complete. Unzipping..."
unzip -q ./dataset/new-plant-diseases-dataset.zip -d ./dataset
echo "Unzipping complete. Cleaning up..."
rm ./dataset/new-plant-diseases-dataset.zip
echo "Cleanup complete. Dataset is ready to use."
echo "Dataset structure:"
ls -R ./dataset
echo "Dataset downloaded and unzipped successfully."
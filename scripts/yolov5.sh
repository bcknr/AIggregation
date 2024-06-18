#!/bin/bash

# Globus our files to HPC Login, ssh cp to cbsugpu## workdir
git clone https://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@github.com/bcknr/AIggregation.git
cd ./AIggregation
git clone https://github.com/ultralytics/yolov5
cp ./train.yaml ./yolov5/train.yaml

# Train YOLOv5 on nest dataset
cd ./yolov5
pip install -r requirements.txt

python train.py --img=608 --epochs 300 --data train.yaml --weights yolov5m.pt --name AIggregation

# Predict across orthomosaic
cd ../

git clone https://github.com/obss/sahi.git
cd ./sahi

pip install -r requirements.txt
pip install -U scikit-image imagecodecs

sahi predict --slice_width 608 --slice_height 608 --overlap_height_ratio 0.1 --overlap_width_ratio 0.1 --model_confidence_threshold 0.25 --model_type yolov5 --source ../input/test_files/tile_test_nests.jpg --model_path ../yolov5/runs/train/AIggregation/weights/best.pt


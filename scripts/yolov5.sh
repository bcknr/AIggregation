#!/bin/bash

git clone https://github.com/ultralytics/yolov5
cp ./train.yaml ./yolov5/train.yaml

cd ./yolov5
pip install -r requirements.txt

python train.py --img=608 --epochs 2 --data train.yaml --weights yolov5s.pt
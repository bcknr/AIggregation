#!/bin/bash

git clone https://github.com/ultralytics/yolov5
cp ./train.yaml ./yolov5/train.yaml

cd ./yolov5
pip install -r requirements.txt wandb

# yolov5 defaults to batch=32. recommends starting with epoch=300
# I think we should run at minimum yolov5m 
python train.py --img=608 --epochs 300 --data train.yaml --weights yolov5m.pt
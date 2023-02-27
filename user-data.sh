#cloud-boothook
#!/bin/bash
cd /home/ubuntu
pip install boto3
git clone https://github.com/YashShelar007/CSE546-Project1.git
cp image_classification.py CSE546-Project1
cp imagenet-labels.json CSE546-Project1
cd CSE546-Project1
python3 app-tier.py
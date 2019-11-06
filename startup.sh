#! /bin/bash
git clone https://github.com/jameslsherman/ballet_auditions
cd ballet_auditions/
pip3 install -r requirements.txt
python3 schools.py
gsutil cp *.html gs://ballet_auditions
cd ..
rm -fr ballet_auditions
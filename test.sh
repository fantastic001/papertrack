#!/bin/bash 

python -m papertrack get --downloader simple --collector simple \
    --title "A consumption-investment model with state-dependent lower bound constraint on consumption" \
    --year 2021 \
    --author "Chonghu Guan" --author "Zuo Quan Xu" --author "Fahuai Yi" \
    --download-url https://arxiv.org/pdf/2109.06378.pdf \
    --field "Computer Science/Theory"

PAPERTRACK_ASK_ON_DEFAULT=1 python -m papertrack get --downloader simple --collector simple \
    --title "A consumption-investment model with state-dependent lower bound constraint on consumption" \
    --year 2021 \
    --author "Chonghu Guan" --author "Zuo Quan Xu" --author "Fahuai Yi" \
    --download-url https://arxiv.org/pdf/2109.06378.pdf 
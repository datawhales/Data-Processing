# ArXiv Papers Reference Dataset
ArXiv papers의 reference가 담긴 문장과 그 문장에 해당하는 reference를 pair 형태로 dataset을 만드는 코드입니다.

## Quick Start
You can quickly run the code or notebook by following steps:
- mkdir `data` directory then cd to `data` directory and download the source file `arXiv_src_2101_001.tar`
- unzip the data by running the following script
```bash
tar -xvf arXiv_src_2101_001.tar
```
- you will get `2101` directory
- cd to `2101` directory and to unzip all files in the directory, run the following script
```bash
for i in *.gz; do tar -zvxf "$i" --one-top-level ;done
```
- run the code or notebook

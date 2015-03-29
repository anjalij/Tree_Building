#!/usr/bin/env bash
python ./glycon.py 
dot -Tpng network.dot > network.png

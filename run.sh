#!/bin/bash
python main.py rules.txt
dot -Tpng network.dot > network.png

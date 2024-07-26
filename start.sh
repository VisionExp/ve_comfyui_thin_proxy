#!/usr/bin/env bash

echo $(date +%s) >| timestamp.txt

echo "Starting configuring custom nodes e.t.c"
python3 /comfyui/auto_configure.py

# Use libtcmalloc for better memory management
TCMALLOC="$(ldconfig -p | grep -Po "libtcmalloc.so.\d" | head -n 1)"
export LD_PRELOAD="${TCMALLOC}"

echo "Starting ComfyUI"
python3 /comfyui/main.py --cpu --listen




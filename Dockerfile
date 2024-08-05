# Use Nvidia CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base

# Prevents prompts from packages asking for user input during installation
ENV DEBIAN_FRONTEND=noninteractive
# Prefer binary wheels over source distributions for faster pip installations
ENV PIP_PREFER_BINARY=1
# Ensures output from python is printed immediately to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# Install Python, git and other necessary tools, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    git \
    wget \
    mc \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Clone ComfyUI repository and change working directory to ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /comfyui

WORKDIR /comfyui

# Install ComfyUI dependencies
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    && pip3 install --no-cache-dir xformers==0.0.21 \
    && pip3 install --no-cache-dir -r requirements.txt

# Clone additional repositories
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager.git /comfyui/custom_nodes/ComfyUI-Manager \
    && git clone https://github.com/VisionExp/ve_custom_comfyui_nodes.git /comfyui/custom_nodes/ve_custom_comfyui_nodes

# Install additional dependencies for ComfyUI-Manager
WORKDIR /comfyui/custom_nodes/ComfyUI-Manager
RUN pip3 install --no-cache-dir -r requirements.txt

# Set working directory back to root
WORKDIR /

# Add files
COPY timestamp.txt .
ADD start.sh ./
ADD checkpoints/ /comfyui/models/checkpoints
ADD auto_configure_thin.py /comfyui/

# Make start script executable
RUN chmod +x /start.sh

# Expose port
EXPOSE 8188

# Start the container
CMD /start.sh
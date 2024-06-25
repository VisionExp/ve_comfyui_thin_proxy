docker build --build-arg SKIP_DEFAULT_MODELS=1 -t deslancer/thin-comfy-server --platform linux/amd64 .
docker push deslancer/thin-comfy-server:latest
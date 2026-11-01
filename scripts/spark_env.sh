# Source ON the Spark before any studio work:  source ~/studio/app/scripts/spark_env.sh
# CPU only (never the GPU), Node 22 via nvm, static ffmpeg/yt-dlp, Python venv with kokoro/piper/faster-whisper.
export CUDA_VISIBLE_DEVICES=""
export PATH="$HOME/studio/bin:$PATH"
source ~/.nvm/nvm.sh >/dev/null 2>&1 && nvm use 22 >/dev/null 2>&1
source ~/studio/.venv/bin/activate
export STUDIO_PIPER_VOICES="$HOME/studio/models/piper"

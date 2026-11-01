#!/usr/bin/env bash
# Run ON the Spark (user space, no sudo). Idempotent.
# Installs: static ffmpeg/ffprobe (arm64), yt-dlp, Python venv ~/studio/.venv with
# CPU torch + kokoro (TTS) + faster-whisper (word timings). Node comes from nvm (v22).
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
S=~/studio; mkdir -p $S/bin $S/tmp $S/logs
cd $S/tmp
if [ ! -x $S/bin/ffmpeg ]; then
  wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz -O ffmpeg.tar.xz
  tar xf ffmpeg.tar.xz
  cp ffmpeg-*-arm64-static/ffmpeg ffmpeg-*-arm64-static/ffprobe $S/bin/
  rm -rf ffmpeg.tar.xz ffmpeg-*-arm64-static
fi
if [ ! -x $S/bin/yt-dlp ]; then
  wget -q https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux_aarch64 -O $S/bin/yt-dlp
  chmod +x $S/bin/yt-dlp
fi
$S/bin/ffmpeg -version | head -1
$S/bin/yt-dlp --version
if [ ! -d $S/.venv ]; then python3 -m venv $S/.venv; fi
P=$S/.venv/bin/pip
$P install -q -U pip wheel
$P install -q torch --index-url https://download.pytorch.org/whl/cpu
$P install -q "kokoro>=0.9.4" soundfile faster-whisper
$P install -q piper-tts || echo "piper-tts install failed (fallback only)"
$S/.venv/bin/python -c "import torch,kokoro,faster_whisper;print('torch',torch.__version__,'cuda?',torch.cuda.is_available())"

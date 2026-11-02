#!/usr/bin/env bash
# One-time setup on the Spark for the scored soundtrack (pipeline/audio/score.py). User space only, CPU only.
#   - FluidSynth 2.6.2 (LGPL-2.1) built from the official release tarball into ~/studio/opt/fluidsynth
#     (no audio drivers, no glib: osal=cpp11; cmake fetches the header-only gcem pinned by sha256)
#   - GeneralUser GS v2.0.3 SoundFont from its official repo at a pinned commit, checked against the sha256 that
#     pipeline/audio/config.SOUNDFONTS records (licence: pipeline/audio/LICENSES.md)
#   - pretty_midi, mido, pedalboard into ~/studio/.venv
# usage (on the Spark): bash ~/studio/app/scripts/spark_music_setup.sh
set -euo pipefail
S="$HOME/studio"
FS_VER=2.6.2
SF_COMMIT=684543d5e5efaef08d02be50dcda8d552478fa60
SF_SHA=9575028c7a1f589f5770fccc8cff2734566af40cd26ed836944e9a5152688cfe

if [ ! -e "$S/opt/fluidsynth/lib/libfluidsynth.so.3" ]; then
  mkdir -p "$S/src" && cd "$S/src"
  [ -d "fluidsynth-$FS_VER" ] || { curl -sSL -o "fluidsynth-$FS_VER.tar.gz" \
      "https://github.com/FluidSynth/fluidsynth/archive/refs/tags/v$FS_VER.tar.gz" && tar xzf "fluidsynth-$FS_VER.tar.gz"; }
  mkdir -p "fluidsynth-$FS_VER/build" && cd "fluidsynth-$FS_VER/build"
  nice -n 10 cmake .. -DCMAKE_INSTALL_PREFIX="$S/opt/fluidsynth" -DCMAKE_BUILD_TYPE=Release \
    -Denable-alsa=off -Denable-jack=off -Denable-dbus=off -Denable-pulseaudio=off -Denable-pipewire=off \
    -Denable-sdl3=off -Denable-readline=off -Denable-ladspa=off -Denable-network=off -Denable-oss=off \
    -Denable-systemd=off -Denable-libsndfile=off -Denable-openmp=off -Denable-signalsmith=off -Denable-midishare=off
  nice -n 10 make -j4 && make install
fi

SF="$S/models/soundfonts/GeneralUser-GS"
mkdir -p "$SF"
if [ ! -e "$SF/GeneralUser-GS.sf2" ]; then
  curl -sSL -o "$SF/GeneralUser-GS.sf2" "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/$SF_COMMIT/GeneralUser-GS.sf2"
  curl -sSL -o "$SF/LICENSE.txt" "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/$SF_COMMIT/documentation/LICENSE.txt"
fi
echo "$SF_SHA  $SF/GeneralUser-GS.sf2" | sha256sum -c -

source "$S/.venv/bin/activate"
nice -n 10 pip install -q pretty_midi mido pedalboard
cd "$S/app" && CUDA_VISIBLE_DEVICES="" python -c "from pipeline.audio import sf2; print('score renderer:', sf2.available())"

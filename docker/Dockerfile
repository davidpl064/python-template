# Base docker image
FROM ubuntu:24.04

# Install OS dependencies
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:ubuntu-toolchain-r/test && \
    apt-get update \
    && apt-get install -y --no-install-recommends \
    git python-dev \
    python3-gi python3-dev libpython3-dev python3-gst-1.0 python-gi-dev git python3-pip python3.8-dev libpython3.8-dev  \
    cmake wget g++ build-essential libssl-dev libglib2.0-dev libglib2.0-dev-bin libgstreamer1.0-dev \
    libtool m4 autoconf automake libgirepository1.0-dev libcairo2-dev python3-opencv \
    python3-numpy libgstrtspserver-1.0-0 gstreamer1.0-rtsp gobject-introspection \
    gir1.2-gst-rtsp-server-1.0 apt-transport-https ca-certificates locales \
    libeigen3-dev gcc-11 g++-11   gstreamer1.0-rts\
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    && apt install -y --no-install-recommends python3-opencv ffmpeg libavcodec-extra libopencv-dev libavutil-dev \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# Install uv
RUN apt-get update && \
    apt-get install -y git curl make && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY . /python_template

# Mount secrets with Nexus credentials
RUN --mount=type=secret,id=nexus-user,env=UV_INDEX_NEXUS_USERNAME \
    --mount=type=secret,id=nexus-pass,env=UV_INDEX_NEXUS_PASSWORD \
    cd /python_template && \
    uv pip install --system -e .

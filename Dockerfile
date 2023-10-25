FROM python:3.8-buster

RUN echo "deb https://mirrors.aliyun.com/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security/ buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends zip unzip libgl1-mesa-glx \
    && apt-get clean

WORKDIR /cloth_mask
COPY . /cloth_mask
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#RUN python3 download_models.py
RUN mkdir -p /root/.cache \
    && curl -o /root/.cache/carvekit.zip "http://mirrors.uat.enflame.cc/enflame.cn/maas/cloth_mask/carvekit.zip" \
    && unzip /root/.cache/carvekit.zip -d /root/.cache \
    && rm /root/.cache/carvekit.zip

ENTRYPOINT ["python3", "server.py"]
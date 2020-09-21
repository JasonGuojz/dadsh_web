FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-runtime

RUN apt-get update \
&& mkdir -p /usr/src/app \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Start the server
CMD ["gunicorn", "./src/predictor_app:app","-c","./gunicorn.conf.py"]
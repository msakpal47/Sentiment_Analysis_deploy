FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords
EXPOSE 80
CMD ["python", "app.py"]

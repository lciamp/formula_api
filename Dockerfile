FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP f1.py
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]

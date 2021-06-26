FROM tensorflow/tensorflow:2.3.1
ADD . /
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
FROM python:3
RUN pip install flask
RUN pip install flask-restful
RUN pip install requests
COPY ./custom_api_exception /custom_api_exception
COPY ./assets /assets
ADD ./resources.py /
ADD ./main.py /
EXPOSE 8080
CMD python ./main.py
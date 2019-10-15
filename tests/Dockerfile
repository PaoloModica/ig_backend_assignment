FROM python:3
RUN pip install flask
RUN pip install flask-restful
RUN pip install requests
COPY ./custom_api_exception /custom_api_exception
COPY ./assets /assets
COPY ./server /server
COPY ./tests /tests
ADD ./tester.py /
EXPOSE 8080
CMD python ./tester.py
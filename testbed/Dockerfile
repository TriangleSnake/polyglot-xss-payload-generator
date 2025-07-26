FROM tomcat:8-jdk8

WORKDIR /

RUN apt update && apt install -y ant git unzip&&\
    git clone https://github.com/google/firing-range.git &&\
    wget https://storage.googleapis.com/appengine-sdks/featured/appengine-java-sdk-1.9.92.zip &&\
    unzip appengine-java-sdk-1.9.92.zip && rm appengine-java-sdk-1.9.92.zip &&\
    mv appengine-java-sdk-1.9.92 /sdk

COPY ./build.xml /firing-range/build.xml

WORKDIR /firing-range

RUN mkdir -p lib &&\
    curl -Lo lib/servlet-api.jar https://repo1.maven.org/maven2/javax/servlet/servlet-api/2.5/servlet-api-2.5.jar

CMD ["ant","runserver"]
FROM python:3.7

RUN mkdir /code
WORKDIR /code

ARG JFROG_NPM_AUTH
ARG JFROG_NPM_EMAIL
ARG JFROG_NPM_PASSWORD
ARG JFROG_NPM_USERNAME
ARG JFROG_PASSWORD
ARG JFROG_USERNAME
ARG DJANGO_SETTINGS_MODULE


ENV JFROG_NPM_AUTH=$JFROG_NPM_AUTH
ENV JFROG_NPM_EMAIL=$JFROG_NPM_EMAIL
ENV JFROG_NPM_PASSWORD=$JFROG_NPM_PASSWORD
ENV JFROG_NPM_USERNAME=$JFROG_NPM_USERNAME
ENV JFROG_PASSWORD=$JFROG_PASSWORD
ENV JFROG_USERNAME=$JFROG_USERNAME
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
ENV SENTRY_AUTH_TOKEN=$SENTRY_AUTH_TOKEN
ENV SENTRY_ORG=$SENTRY_ORG

RUN wget https://s3-eu-west-1.amazonaws.com/ibconsole/util_scipts/codeship_artifactory.py
RUN apt-get -y update
RUN apt-get install -y mysql*
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install nodejs
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
RUN npm install -g apidoc@0.19.1
RUN npm install -g @sentry/cli --unsafe-perm
RUN pip install virtualenv virtualenvwrapper
RUN python codeship_artifactory.py

ADD requirements_test.txt requirements_test.txt
ADD requirements_lint.txt requirements_lint.txt
ADD requirements_dev.txt requirements_dev.txt
ADD requirements_deploy.txt requirements_deploy.txt
ADD requirements_db.txt requirements_db.txt
ADD requirements_project.txt requirements_project.txt
ADD requirements_lambda.txt requirements_lambda.txt
ADD requirements.txt requirements.txt

RUN virtualenv /_ib_venv
RUN /bin/bash -c "source /_ib_venv/bin/activate && pip install pip==20.1 setuptools==57.5.0"
RUN /bin/bash -c "source /_ib_venv/bin/activate && pip install -r requirements_lambda.txt"
RUN /bin/bash -c "source /_ib_venv/bin/activate && pip uninstall -y lambda-packages"
RUN /bin/bash -c "source /_ib_venv/bin/activate && pip install git+https://github.com/ib-devs/lambda-packages.git@master"

CMD ["/bin/bash"]

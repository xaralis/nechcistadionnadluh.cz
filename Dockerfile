FROM python:3.7-alpine as build

ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk add --no-cache \
    g++ \
    nodejs \
    nodejs-npm  \
    bash \
    git \
    openssh \
    postgresql-dev \
    freetype-dev \
    jpeg-dev \
    zlib-dev \
    build-base &&  \
    mkdir -p /build/wheels

# Install python requirements, collect as wheels and re-install
# later on in the `production` stage
COPY ./requirements.txt /build/wheels/
WORKDIR /build/wheels
RUN pip install -U pip && \
    pip wheel -r requirements.txt

# Install node-based requirements
WORKDIR /build
COPY ./package.json ./
RUN npm install

# Copy assets and build static file bundles
COPY ./webpack.config.js ./
COPY ./assets/ ./assets/
RUN ./node_modules/.bin/webpack --config webpack.config.js --mode production


FROM python:3.7-alpine as production

ENV PYTHONPATH /nsnd
ENV DJANGO_SETTINGS_MODULE nsnd.settings
ENV PATH "/home/nsnd/.local/bin:${PATH}"

# Create custom user to avoid running as a root
RUN addgroup -g 1001 nsnd && \
    adduser -D -u 1001 -G nsnd nsnd && \
    mkdir /nsnd && \
    chown nsnd:nsnd /nsnd

# Install dependencies
RUN apk add --no-cache \
    bash \
    git \
    postgresql-dev \
    build-base \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    openjpeg-dev \
    nginx \
    supervisor && \
    rm /etc/nginx/conf.d/default.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    mkdir /run/nginx

# Supervisor and Nginx configs
COPY ./docker/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY ./docker/nginx.conf /etc/nginx/conf.d/nsnd.conf

# Copy over collected wheels and build artifacts from build stage
COPY --from=build --chown=nsnd /build/wheels /wheels
COPY --from=build --chown=nsnd /build/assets /nsnd/assets
COPY --from=build --chown=nsnd /build/webpack-stats.json /nsnd/

# Copy over entrypoint file
COPY --chown=nsnd docker/entrypoint.sh /nsnd/

# Prepare media directory
RUN mkdir -p /media && chown nsnd:nsnd /media

USER nsnd
WORKDIR /nsnd

# Install wheels under user priviledges
RUN pip install -r /wheels/requirements.txt -f /wheels --user

# Rest of source files
COPY --chown=nsnd ./nsnd ./nsnd/
COPY --chown=nsnd ./thumbnails ./thumbnails/

# Collect static files
RUN mkdir /nsnd/static && \
    DEBUG=1 django-admin collectstatic --noinput --verbosity=0

USER root

# Get rid of useless files
RUN rm -rf /wheels && \
    rm -rf /home/nsnd/.cache/pip

EXPOSE 80

CMD ["sh", "./entrypoint.sh"]

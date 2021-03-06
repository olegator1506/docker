FROM php:7.4-fpm-alpine

EXPOSE 9000

# Install dev dependencies
RUN apk add --no-cache --virtual .build-deps \
    $PHPIZE_DEPS \
    curl-dev \
    imagemagick-dev \
    libtool \
    libxml2-dev \
    postgresql-dev \
    sqlite-dev 

# Install production dependencies
RUN apk add --no-cache \
    bash \
    curl \
    freetype-dev \
    g++ \
    gcc \
    git \
    icu-dev \
    icu-libs \
    imagemagick \
    libc-dev \
    libjpeg-turbo-dev \
    libpng-dev \
    libzip-dev \
    make \
    mysql-client \
    nodejs \
    nodejs-npm \
    oniguruma-dev \
    yarn \
    openssh-client \
    postgresql-libs \
    rsync \
    supervisor \
    zlib-dev \
    mc

# Install PECL and PEAR extensions
RUN pecl install \
    redis \
    imagick \
    xdebug 

# Enable PECL and PEAR extensions
RUN docker-php-ext-enable \
    redis \
    imagick \
    xdebug

# install LDAP extension
RUN apk add --no-cache ldb-dev libldap openldap-dev
RUN docker-php-ext-configure ldap
RUN docker-php-ext-install ldap


# Configure php extensions
RUN docker-php-ext-configure gd --with-freetype --with-jpeg

# Install php extensions
RUN docker-php-ext-install \
    bcmath \
    calendar \
    curl \
    exif \
    gd \
    iconv \
    intl \
    mbstring \
    pdo \
    pdo_mysql \
    pdo_pgsql \
    pdo_sqlite \
    pcntl \
    tokenizer \
    xml \
    zip




# Install composer
ENV COMPOSER_HOME /composer
ENV PATH ./vendor/bin:/composer/vendor/bin:$PATH
ENV COMPOSER_ALLOW_SUPERUSER 1
RUN curl -s https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin/ --filename=composer

# Install PHP_CodeSniffer
RUN composer global require "squizlabs/php_codesniffer=*"
# Install MySqlI php extension
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli


# Cleanup dev dependencies
RUN apk del -f .build-deps

#RUN rm -R /etc/php7
COPY files/IssuingCA01.crt /etc/ssl/certs/IssuingCA01.crt
COPY files/ldap.conf /etc/openldap/ldap.conf
COPY files/php-include-path.ini /usr/local/etc/php/conf.d/php-include-path.ini
CMD ["php-fpm","-F"]


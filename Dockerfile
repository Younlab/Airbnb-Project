FROM                python:3.6.5-slim
MAINTAINER          isoo7510@gmail.com

# pip install uwsgi
RUN                 apt -y update && apt -y dist-upgrade
RUN                 apt -y install build-essential
RUN                 apt -y install nginx supervisor

COPY                ./requirements.txt  /srv/
RUN                 pip install -r /srv/requirements.txt

# Production
ENV             BUILD_MODE              production
ENV             DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}

COPY            .   /srv/project

# 로그파일 기록 위한 폴더 생성
RUN             mkdir   /var/log/django

# Nginx 설정파일들 복사 및 enabled로 링크
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx.conf \
                        /etc/nginx/nginx.conf && \
                cp -f   /srv/project/.config/${BUILD_MODE}/nginx_app.conf \
                        /etc/nginx/sites-available && \
                rm -f   /etc/nginx/sites-enabled/* && \
                ln -sf  /etc/nginx/sites-available/nginx_app.conf \
                        /etc/nginx/sites-enabled/

# supervisor 설정 복사
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/supervisor.conf \
                        /etc/supervisor/conf.d/

# 7000번 포트 open
EXPOSE          7000

# supervisord 실행
CMD             supervisord -n
FROM ubuntu:latest
LABEL authors="mk"

ENTRYPOINT ["top", "-b"]
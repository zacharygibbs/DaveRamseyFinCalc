FROM node:20-slim AS build

RUN mkdir /mnt/node
WORKDIR /mnt/node

COPY ./DaveRamseyFinCalc /mnt/node/DaveRamseyFinCalc

RUN npx smui-theme template src/theme
#!/usr/bin/env bash

docker run -it \
       -e "SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID" \
       -e "SPOTIPY_CLIENT_SECRET=$SPOTIPY_CLIENT_SECRET" \
       -e "SPOTIPY_REDIRECT_URI=$SPOTIPY_REDIRECT_URI" \
       -e "OSP_USERNAME=$OSP_USERNAME" \
       -e "OSP_EMAIL=$OSP_EMAIL" \
       -e "OSP_PASSWORD=$OSP_PASSWORD" \
       osp:latest

#!/bin/sh
/wait-for-it.sh db:5432 -- uvicorn backend.main:app --host 0.0.0.0 --port 8000
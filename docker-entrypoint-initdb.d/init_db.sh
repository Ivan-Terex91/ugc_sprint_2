#!/bin/bash
set -e

psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE auth"

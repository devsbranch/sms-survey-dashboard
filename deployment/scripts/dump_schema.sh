#!/bin/bash

echo 'Dumping schema (without data) to ppcr-tralard.sql'
pg_dump -s ppcr-tralard > ../sql/ppcr-tralard.sql

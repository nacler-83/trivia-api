#!/bin/bash
dropdb trivia
createdb trivia
psql trivia < trivia.psql

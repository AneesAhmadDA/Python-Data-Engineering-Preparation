#!/bin/bash

echo "=================================="
echo "HDFS BASIC COMMAND PRACTICE"
echo "=================================="

echo "1. Checking HDFS root directory"

hdfs dfs -ls /

echo "2. Creating practice directory"

hdfs dfs -mkdir -p /learning

echo "3. Creating HDFS subdirectories"

hdfs dfs -mkdir -p /learning/input
hdfs dfs -mkdir -p /learning/output

echo "4. Listing HDFS directories"

hdfs dfs -ls -R /learning

echo "=================================="
echo "HDFS BASIC PRACTICE COMPLETED"
echo "=================================="
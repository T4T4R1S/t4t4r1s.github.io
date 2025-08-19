#!/bin/bash
read -p "Enter number of males: " m
read -p "Enter number of females:" f
total=$((f+m))
mp=$((100*m/total))
echo $mp

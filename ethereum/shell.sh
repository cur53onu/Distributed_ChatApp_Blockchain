#!/bin/bash
node compile.js
cp -r ./build/* ../JSON_Files/
node deploy.js

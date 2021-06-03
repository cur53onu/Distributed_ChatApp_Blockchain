#!/bin/bash
rm ./ethereum/build/*
node ./ethereum/compile.js
cp ./ethereum/build/* ./chatty/JSON_Files
node ./ethereum/deploy.js

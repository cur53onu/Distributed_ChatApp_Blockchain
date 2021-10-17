#!/bin/bash
node ./ethereum/compile.js
cp -r ./ethereum/build/* JSON_Files/
node ./ethereum/deploy.js

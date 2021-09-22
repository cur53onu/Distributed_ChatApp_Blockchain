#!/bin/bash
#docker
#node ./ethereum/compile.js
#p ./ethereum/build/* ./chatApp/JSON_Files
#node ./ethereum/deploy.js
#rm -r ../../ethereum/build
node ../../ethereum/compile.js
cp ../../ethereum/build/* ../JSON_Files
node ../../ethereum/deploy.js
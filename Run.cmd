@Echo off
title wallet checker V1.0.0 ITrebel.eth
Pushd "%~dp0"
:loop
node index.js
goto loop

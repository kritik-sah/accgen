@Echo off
title random wallet checker V1.0.0 ITrebel.eth
Pushd "%~dp0"
:loop
node random.js
goto loop

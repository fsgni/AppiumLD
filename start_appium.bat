@echo off
:: 设置 Android SDK 环境变量
set ANDROID_HOME=C:\Users\Administrator\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=C:\Users\Administrator\AppData\Local\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%ANDROID_HOME%\tools\bin

:: 先启动 ADB 服务
echo Starting ADB server...
adb kill-server
timeout /t 2 /nobreak > nul
adb start-server
timeout /t 2 /nobreak > nul

:: 启动 Appium 服务
echo Starting Appium Server...
appium -a 0.0.0.0 -p 4723 --allow-insecure chromedriver_autodownload --relaxed-security
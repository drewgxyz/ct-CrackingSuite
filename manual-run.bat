@echo off
pip3 install -r requirements.txt
pause
python proxy-scraper.py %*
pause
python resource-generator.py %*
pause
python config-maker.py %*
pause
python brute-force.py %*
pause
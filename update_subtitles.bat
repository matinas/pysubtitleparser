#bash

set folder="D:\MyFolder"
set filename="MySubs.srt"
set /A from_line=1
set /A to_line=1000
set /A shift_amount=3

cd C:\
cd ".\Users\Game Gear\Desktop"
py .\subtitle_parser.py %folder% %filename% %from_line% %to_line% %shift_amount%


#bash

set folder="D:\MyFolder"
set filename="MySubs.srt"
set /A from_line=1
set /A to_line=1000
set shift_amount=1

cd C:\
cd ".\Users\Desktop\pysubtitleparser\src"
py subtitle_parser.py %folder% %filename% %shift_amount% --start %from_line% --end %to_line%


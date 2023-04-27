@echo off
REM pip install .


WHERE fapelsystem_printModuleDir
IF %ERRORLEVEL% NEQ 0 (
	ECHO installing Fapelsystem module via pip
	REM ECHO pip install .
	pip install .
	REM pause
	REM exit 0
)

for /f %%i in ('fapelsystem_printModuleDir') do set INSTALLDIR=%%i
echo fapel system module installed in: %INSTALLDIR%

set CONFIGDIR=%AppData%\Fapelsystem
set SENDTODIR=%AppData%\Microsoft\Windows\SendTo



mkdir "%CONFIGDIR%"

copy "%INSTALLDIR%\fapel_system_template_windows.conf" "%CONFIGDIR%\fapel_system.conf"



call:link_module fapel_tagger.py 1-fapel-tagger.py
REM call:link_module fapel_counter.py 2-fapel-notice.py
call:link_counter notice 2-fapel-notice.py
call:link_counter ct 2-fapel-ct.py
REM call:link_module fapel_counter.py 6-fapel-ct.py
call:link_module fapel_search_not_tagged.py 5-fapel-search-not-tagged.py
REM search source file needs "find" cmd from linux => does not work on windows
REM call:link_module fapel_search_source_file.py 5-fapel-search-source-file.py
call:link_module fapel_search_tagged.py 4-fapel-search-tagged.py
call:link_module fapel_fap_set.py 3-fapel-fap-set.py
REM call:link_module openLink.sh 9-open-softlink-folder.sh
REM fapel exiles need a rewrite for windows
REM call:link_module fapel_exiles.py 9-fapel-exiles.py
call:link_module fapel_elo.py 9-fapel-elo.py

echo[


:choice
set /P c=Install fapelsystem basic directories [Y/N]?
if /I "%c%" EQU "Y" goto :createdirs
if /I "%c%" EQU "N" goto :donotcreatedirs
goto :choice


:createdirs



mkdir %UserProfile%\Documents\fapelsystem
mkdir %UserProfile%\Documents\fapelsystem\Tags
mkdir %UserProfile%\Documents\fapelsystem\Tags\.recycled
mkdir %UserProfile%\Documents\fapelsystem\Notice
mkdir %UserProfile%\Documents\fapelsystem\Tags\Ct
mkdir %UserProfile%\Documents\fapelsystem\Tags\Ct\Ct
REM touch ~/fapelsystem/Tags/Ct/Ct/.hide_button
REM touch ~/fapelsystem/Tags/Ct/Ct/.hide_child_buttons

REM echo "[fapxileForThisTag]" > ~/fapelsystem/Tags/Ct/Ct/.fapxile
REM echo "[fapxileForFapelsOfThisTag]" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
REM echo "[fapxileForSubTagsAndSubFapels]" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
REM	echo "ct" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
REM	echo "[excludedSubTags]" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile
REM	echo "Ct/Ct/0001" >> ~/fapelsystem/Tags/Ct/Ct/.fapxile


REM mkdir %UserProfile%\fapelsystem\Tags\Hoover_over_me_for_a_tip
mkdir "%UserProfile%\Documents\fapelsystem\Tags\Another Tag"

REM echo "[general]" > ~/fapelsystem/Tags/Hoover_over_me_for_a_tip/.taginfo
REM echo "tooltip='Create more Tags by simply creating directories under ~/fapelsystem/Tags'" >> ~/fapelsystem/Tags/Hoover_over_me_for_a_tip/.taginfo

mkdir %UserProfile%\Documents\fapelsystem\Elo
mkdir "%UserProfile%\Documents\fapelsystem\Search Results"
mkdir %UserProfile%\Documents\fapelsystem\Fapsets



:donotcreatedirs

pause








goto:eof



:link_module
copy "%INSTALLDIR%\%~1" "%INSTALLDIR%\%~1w"
create_shortcut_windows.vbs "%SENDTODIR%\%~2w.lnk" "%INSTALLDIR%\%~1w"
exit /B

:link_counter
copy "%INSTALLDIR%\fapel_counter.py" "%INSTALLDIR%\fapel_counter_%~1.pyw"
create_shortcut_windows.vbs "%SENDTODIR%\%~2w.lnk" "%INSTALLDIR%\fapel_counter_%~1.pyw"
exit /B

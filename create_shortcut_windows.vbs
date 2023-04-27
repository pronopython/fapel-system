set fs  = CreateObject("Scripting.FileSystemObject")
set ws  = WScript.CreateObject("WScript.Shell")
set arg = Wscript.Arguments

linkFile = arg(0)

set link = ws.CreateShortcut(linkFile)
    REM link.TargetPath = fs.BuildPath(ws.CurrentDirectory, arg(1))
	link.TargetPath = arg(1)
	if arg.count > 2 then
		link.Arguments = arg(2)
	end if
    link.Save
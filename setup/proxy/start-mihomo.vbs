Set ws = CreateObject("WScript.Shell")
Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set procs = wmi.ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'mihomo.exe'")
If procs.Count = 0 Then
  ws.Run """C:\Users\<用户名>\AppData\Local\mihomo\mihomo.exe"" -d ""C:\Users\<用户名>\AppData\Local\mihomo"" -f ""C:\Users\<用户名>\AppData\Local\mihomo\config.yaml""", 0, False
End If

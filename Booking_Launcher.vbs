Set WshShell = CreateObject("WScript.Shell")
' This starts the Streamlit server in the background (hidden)
WshShell.Run "cmd.exe /c python -m streamlit run app.py --server.headless true", 0
' Wait 5 seconds for the server to start
WScript.Sleep 5000
' Open the app in a "Clean" window (No browser tabs/address bar)
WshShell.Run "chrome.exe --app=http://localhost:8501"
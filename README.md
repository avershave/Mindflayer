# Ron

## GOAL:
+ Connect to MetasploitRPCClient
    - connectMsfRpcClient.py handles the connection to the client
    - createMsfRpcClient.py creates the client
+ Track open sessions
+ Find the vulnerabilities of the open sessions
    - These are dumped into a list which is dumped into a database
    - Could create an object in order to accomplish this?
+ Fire attacks at random sessions

## KNOWN
+ Metasploit creates its own database!
+ You are able to use this database to create a specific database

##LOOK INTO
+ Learning Metasploit from front to back
+ Metasploit RPCClient and MetasploitConsole need tob oth be open in order to execute?
+ Can Metasploit find vulnerabilities? Are they able to be parsed?
+ Using a database to track object values?
    - See if Metasploit just holds this data for you
        * More than likely due to the nature of the program
+ Does pyMetasploit track the list of possible working exploits for each session?
+ Refresh objects

## NOTES ON METASPLOIT
+ Exploits:
    - Options are different per exploit
        * Keyword "SET" for setting options
    - Able to load different payloads
    - Able to show targets
        * Able to execute exploits on multiple targets
    - Show info on exploit
+ Console:
    - You can use the console in pyMetasploit to run commands
        * What data structure does it output?
    - Search function
+ Auxiliary:
    - These scanners are used to find vulnerabilities
    - What data structure does it output?
+ Meterpreter:
    - What can you do post exploit in pyMetasploit?
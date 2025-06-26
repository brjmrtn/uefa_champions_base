# start.ps1
# Fija Java17 y activa el venv
$env:JAVA_HOME = ':\Users\borja.martin\java'
$env:Path      = "$env:JAVA_HOME\bin;$env:Path"
.\venv\Scripts\Activate.ps1

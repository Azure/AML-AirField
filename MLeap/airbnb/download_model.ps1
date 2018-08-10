[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -OutFile model\LICENSE             https://github.com/combust/mleap/raw/master/LICENSE
Invoke-WebRequest -OutFile model\airbnb.model.lr.zip https://github.com/combust/mleap/raw/master/mleap-benchmark/src/main/resources/models/airbnb.model.lr.zip
Invoke-WebRequest -OutFile model\airbnb.model.rf.zip https://github.com/combust/mleap/raw/master/mleap-benchmark/src/main/resources/models/airbnb.model.rf.zip

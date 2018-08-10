$ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest -OutFile model\inception-2015-12-05.tgz http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz

if (-not (Get-Command Expand-7Zip -ErrorAction Ignore)) {
    echo 'Need to install 7Zip4Powershell plugin to expand .tgz'
    Install-Module -Name 7Zip4Powershell 
}

Expand-7Zip model\inception-2015-12-05.tgz model\.
Expand-7Zip model\inception-2015-12-05.tar model\.

Remove-Item model\cropped_panda.jpg
Remove-Item model\inception-2015-12-05.tgz
Remove-Item model\inception-2015-12-05.tar

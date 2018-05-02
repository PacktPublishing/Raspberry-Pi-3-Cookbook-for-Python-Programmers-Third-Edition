function proxyenable {
# Define proxy settings
PROXY_ADDR="proxy.address.com:port"
# Login name (leave blank if not required):
LOGIN_USER="login_name"
# Login Password (leave blank to prompt):
LOGIN_PWD=
#If login specified - check for password
if [[ -z $LOGIN_USER ]]; then
  #No login for proxy
  PROXY_FULL=$PROXY_ADDR
else
  #Login needed for proxy Prompt for password -s option hides input
  if [[ -z $LOGIN_PWD ]]; then
    read -s -p "Provide proxy password (then Enter):" LOGIN_PWD
    echo
  fi
  PROXY_FULL=$LOGIN_USER:$LOGIN_PWD@$PROXY_ADDR
fi
#Web Proxy Enable: http_proxy or HTTP_PROXY environment variables
export http_proxy="http://$PROXY_FULL/"
export HTTP_PROXY=$http_proxy
export https_proxy="https://$PROXY_FULL/"
export HTTPS_PROXY=$https_proxy
export ftp_proxy="ftp://$PROXY_FULL/"
export FTP_PROXY=$ftp_proxy
#Remove info no longer needed from environment
unset LOGIN_USER LOGIN_PWD PROXY_ADDR PROXY_FULL
echo Proxy Enabled
}

function proxydisable {
#Disable proxy values, apt-get and get settings
unset http_proxy HTTP_PROXY https_proxy HTTPS_PROXY ftp_proxy FPT_PROXY
echo Proxy Disabled
}

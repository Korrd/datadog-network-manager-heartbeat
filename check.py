from datadog import initialize, api
from sys import argv as args
import netifaces
import subprocess

FLAG_DEBUG = ("--debug" in args)  # for debugging purposes

def main(args):

  # Get params and initialize datadog
  APP_KEY = getArgumentValue(args=args, flag="--app-key")
  API_KEY = getArgumentValue(args=args, flag="--api-key")
  EXPECTED_IP = getArgumentValue(args=args, flag="--target-ip")

  options = {
    "api_key": API_KEY,
    "app_key": APP_KEY,
  }
  initialize(**options)

  EVENT_TITLE = f"Network manager status at '{EXPECTED_IP}'"
  
  # Determine if network-manager is disconnected
  if not hasExpectedIpAddress(hostIp=EXPECTED_IP):
    # Smash it in the butt®
    restartNetworkManager()
    # Send restart event to datadog
    sendDatadogEvent(
        title=EVENT_TITLE, text=f"💥 '{EXPECTED_IP}' got its network-manager restarted", tags=[
        f"host_ip:'{EXPECTED_IP}'"], alert_type="error")
    if FLAG_DEBUG:
      print("🐶 Sending restart event to datadog!")
  else:
    if FLAG_DEBUG:
      print ("✅ All is well with the server")
      sendDatadogEvent(title=EVENT_TITLE, text=f"✅ '{EXPECTED_IP}' is working fine", tags=[
                       f"host_ip:'{EXPECTED_IP}'"], alert_type="info")

## ============================================================================
## Functions ==================================================================
## ============================================================================

### Sends an event to datadog
def sendDatadogEvent(title, text, tags, alert_type):
  api.Event.create(title=title, text=text, tags=tags, alert_type=alert_type)

### Gets an argument's value based on its flag and separator
def getArgumentValue(args, flag, separator="="):
    for element in args:
        if element.startswith(flag):
            return element.split(separator)[1]
    return ""  # Return empty if not found

### This function checks if the host machine got assigned the expected IP addr
### we don't care about more complex checks as the sever's IP is fixed
def hasExpectedIpAddress(hostIp):

  for iface in netifaces.interfaces():
    iface_details = netifaces.ifaddresses(iface)
    if netifaces.AF_INET in iface_details:
      ipAddress = iface_details[netifaces.AF_INET][0].get("addr")
      if ipAddress == hostIp:
        return True
  return False

def restartNetworkManager():
  if FLAG_DEBUG:
    print("❌ Restarting network-manager...")
  command = "service network-manager restart"
  proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

## ============================================================================
## Entrypoint --- ALWAYS PLACE AT EOF =========================================
## ============================================================================
if __name__ == "__main__":
    main(args)

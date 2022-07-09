## About this script

This custom datadog event checks if our home server has a private IP address. If it's not there, it restarts the network-manager service and emits a datadog event.

A niche fix created to tackle a pesky issue which I've been unable to solve otherwise: ubuntu's network-manager dies at random and kills network connectivity due to its temporary wifi card having a crap driver (which will soon be replaced by trusty, UTP cable) which dies every now and then and need a kick in the butt™.

Created by Victor M. Martin - 2022-07-09, while conquering Spain 🇪🇸 and bitching with his home server ~20.000 leagues away.

## Requirements

- Python 3
- Meant for `Ubuntu 20.04` or any ubuntu distro using network-manager
- Some python libraries, see [the requirements file](./requirements.txt)
  ```bash
    pip3 install -r requirements.txt
  ```

## Usage

Get datadog app and api keys from here: https://app.datadoghq.com/organization-settings/users, then replace placeholders with app and api keys, and the machine's expected IP address (note that `--debug` flag is optional: all it does it to print stuff to stdout for ease of debugging)

```bash
  check.py --app-key=<datadog_app_key> --api-key=<datadog_api_key> --target-ip=<server_private_ip> [--debug]
```

## Notes

This script requires root privileges, otherwise it'll be unable to restart the network-manager service.

# ocupado_plugin_ldap
LDAP plugin for the [ocupado tool](https://github.com/ashcrow/ocupado).

[![Build Status](https://api.travis-ci.org/ashcrow/ocupado_plugin_ldap.png)](https://travis-ci.org/ashcrow/ocupado_plugin_ldap/)

## Usage
Add the plugin to your configuration backend.


### ini
```ini
[plugin]
# ...
ocupado_plugin_ldap = LDAP

[ocupado_plugin_ldap]
uri = ldaps://127.0.0.1:389
base = ou=testing,dc=example,dc=org
filter = (cn=%s)
#user =
#passwd =
```

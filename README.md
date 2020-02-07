# overview

this is a python script to manipulate the power on an aviosys [ip power 9258](http://www.aviosys.com/products/9258.html) managed outlet.  this uses their lame HTTP interface in order to manipulate the outlet state.

this thing has an exceedingly crappy user interface, i don't recommend it to anyone except on pure basis of price.  this script simply wrappers some of the more annoying things associated with their HTTP interface.

# requirements

- written using python 3.7
- see the pipfile for more info re: requirements.

# configuration parameters

put your configuration parameters into `~/.config/botpower.cfg`. the format is [YAML](https://yaml.org). 

``` yaml
# admin is the default username from aviosys
username: admin
# '12345678' is the default password from aviosys. i'm assuming you've 
# changed this to somehing a bit more useful.
password: 12345678
# i'm using the requests library so it should behave reasonably here 
hostname: "10.0.0.x"
# note that the trailing '?' is important in the following.  this is the 
# CGI program they have running on this POS.  don't get clever here,
# they don't actually parse query parameters, so you have to craft the
# query string by hand in the script.
api_url: "/set.Cmdr?"
```

# operation 


**example(s)**

turn outlet #1 on.

``` text
% ./botpower.py -a on -o 1
outlet: 1
action: on
current outlet status
---------------------
outlet: 1 power: on
```

display the current state of the outlets.  note, that when the action is `display` we require but ignore the `-o` flag.

``` text
% ./botpower.py -a display -o 1
outlet: 1
action: display
current outlet status
---------------------
outlet: 1 power: on
outlet: 2 power: off
outlet: 3 power: off
outlet: 4 power: off
```

## mandatory arguments
```
-o, --outlet

outlet to manipulate, valid values are as follows:
single value from 1 - 4. 1 at a time.
all: execute the associated action on all ports

-a, --action

the action to effect upon an outlet. valid actions are as follows:

on  - turn the given outlet on
off - turn the given outlet off
display - display the current state of the outlets
```
## optional arguments

these will override your config file values.
```
-u, --username (default: admin)
-p, --password (default: 12345678) - this is factory default

-c, --config - alternate configuration file to use. 

```

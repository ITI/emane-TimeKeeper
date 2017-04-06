#
# Usage Instructions and Tips
#
# authors : Vignesh Babu
#


#Compilation:
```

	sudo make				# compiles TimeKeeper, scripts in lxc-command directory and the test files

```

#Running Tests:
```
	sudo make large_linear_enabled		# runs the large_linear test (emane-TimeKeeper/tests/large_linear/large_linear.py) with TimeKeeper Enabled. 
						# The Test file (emane-TimeKeeper/tests/large_linear/large_linear.py) has to be configured appropriately.

	sudo make large_linear_disabled		# runs the large_linear test (emane-TimeKeeper/tests/large_linear/large_linear.py) with TimeKeeper Disabled. 
						# The Test file (emane-TimeKeeper/tests/large_linear/large_linear.py) has to be configured appropriately.
```


#Running General Configurations:
```
	sudo python deploy.py <Options> <path to configuration files : node.conf and emane.conf>

	Options:
	--------
		-D	Disable TimeKeeper (enabled by default)

	If path to configuration files is not specified, the default path emane-Timekeeper/conf/ is used. It contains two default files node.conf and emane.conf 
	which have to be appropriately modified.
```

#Setting model parameters:
```
	Model parameters can be set by editing the xml files inside
	emane-Timekeeper/conf/models directory.

	-ieee80211abgmac.xml
	-rfpipe.xml
	-transvirtual.xml
	-universalphy.xml
```

# LinuxKernelScript
linux kernel generate patch and send patch script

# Usage
**1. how to use GeneratePatch.py?** <br/>
**First, write down commit msg.**    <br/>
commitmsg.info       <br/>
```
Use min instead of doing it manually		-> don't write prefix

Use min() to simplify code, there is no functional change.

Fixes: drivers/iio/poteionmeter/ad5272:73	 -> write down what file and line you have changed
Signed-off-by: William Dean <williamsukatube@gmail.com>
```
**Second, modify code and don't execute 'git add' command** <br/>
**Third, run scrpit as follows:**  <br/>
```
python2 GeneratePatch.py -b         // generate bugfix patch
python2 GeneratePatch.py            // generate cleanup patch
```

**2, how to use SendPathToCommunity.py?**  <br/>
**just run:** <br/>
```
python2 SendPathToCommunity.py <your_patch_file_name>
```

# Some Advice
**You need to run script at linux source code folder**, and this will work well :) <br/>
and if you have any problem, you can add a issue or feel free to contact me. <br/>

# stupid-bruter
[SDUBID](https://www.youtube.com/watch?v=m36LsyAJ8Gw) URL Path directory/file Bruter :grimacing:

Just an example. This code is not optimized (that's why it's called "stupid") and not ready to work hard because of the synchronous implementation in it. But, the idea of this project is to provide some basic structures of the simplest python project - what you need to use, how to use it, and so on. Use your imagination and rebuild it as you wish! 

You can implement your own classes with
```python3
class ThreadBruter(Bruter):
    ...

class MultiprocessingBruter(Bruter):
    ...

class AsyncBruter(Bruter):
    ...
```
Or you can rebuild all the things from the ground. 

## Run
Install the dependencies  
```bash
virtualenv -p python3 venv  
source venv/bin/activate  
pip3 install -r requirements  
```
Change the default host  
```python
class Values:
    HOST = "http://www.your_host_here.com/"
    LIMIT = None
```
Run
```bash
python3 main.py
```

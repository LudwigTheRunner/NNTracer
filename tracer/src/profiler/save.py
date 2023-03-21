from hashlib import md5
import CustomizedItem

numberType = [int, float, complex]
stringType = [str]
collectionType = [list, dict, tuple]
basicType = numberType + stringType + collectionType

def _optimizerHandler():
    pass

def _datasetHandler():
    pass

def _dataLoaderHandler():
    pass

def _neuralNetworkHandler(model) -> str:
    
    pass

def _scriptHandler():
    pass

def _codeFrameHandler():
    pass

def _instanceHandler():
    pass

def _classHandler():
    pass

def _functionHandler():
    pass

# TODO: get var name and var value turple
def _basicVarHandler(key, value, snapshot):
    pass

def add(**kwargs):
    snapshot = dict()
    for key, value in kwargs.keys():
        if type(value) in basicType:
            _basicVarHandler(key, value, snapshot)
        elif isinstance(value, CustomizedItem):
            value.__serialize()
        
if __name__ == '__main__':
    add(a=1, b=2, c='ff')
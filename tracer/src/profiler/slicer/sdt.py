import inspect, re
from pylint.lint import PyLinter
import hashlib, pickle
from collections import deque
# Create a PyLinter object
linter = PyLinter()

# Configure the linter as desired
linter.load_default_plugins() # Load the default pylint plugins
linter.options.disable = 'missing-docstring' # Disable the "missing-docstring" check
linter.options.enable = 'undefined-variable' # Enable the "undefined-variable" check
def __look_up_undefines(code):
   global linter
   results = linter.check(code)
   # Get the output as a string
   output_str = results.get_messages()
   # Get the array of undefined variables
   pattern = r"'(.+?)' is not defined"
   matches = re.findall(pattern, output_str)
   undefined_vars = list(set(matches))

   return undefined_vars


def __get_store_path(contents: bytes):
   md5_hash = hashlib.md5(contents)
   md5_str = md5_hash.hexdigest()
   base = '/Users/wgc/Project/NNTracer/.tmp/'
   return base + md5_str

def __resolve_sdt(obj, resolved: set, imports: set, assigns: set, defs: set) -> None:
   # if isinstance(object, (type(None), int, float, bool, str, bytes, bytearray, tuple, list, set, dict)):
   classque = deque([obj])
   while classque:
      value = classque.popleft()
      if isinstance(value, (type(None), int, float, bool, str, bytes, bytearray)):
         pass
      elif isinstance(value, (tuple, list, set)):
         for psbclass in value:
            classque.append(psbclass)
      elif isinstance(value, (dict)):
         for _, psbclass in dict:
            classque.append(psbclass)
      elif inspect.isclass(value) or inspect.isfunction(value):
         key = str(value)
         if key not in resolved:
            resolved.add(key)
            modulename = inspect.getmodule(value).__name__
            if modulename != '__main__':
               imports.add(f"import {modulename}\n")
            else:
               code = inspect.getsource(value)
               defs.add(code)
               obj = eval(var)
               for var in __look_up_undefines(code=code):
                  if isinstance(obj, (type(None), int, float, bool, str, bytes, bytearray)):
                     if var not in resolved:
                        resolved.add(var)
                        assigns.add(f"{var} = pickle.loads({pickle.dumps(obj, fix_imports=True)}, fix_imports=True)\n")
                  elif isinstance(obj, (tuple, list, set, dict)):
                     if var not in resolved:
                        resolved.add(var)
                        # further check its contents class/func deps
                        classque.append(obj)
                        assigns.add(f"{var} = pickle.loads({pickle.dumps(obj, fix_imports=True)}, fix_imports=True)\n")
                  elif inspect.isfunction(obj) or inspect.isclass(obj):
                     classque.append(obj)
                  # instance of a class
                  elif hasattr(obj, '__class__') and isinstance(obj, obj.__class__):
                     if var not in resolved:
                        resolved.add(var)
                        # further check its contents class/func deps
                        classque.append(obj)
                        assigns.add(f"{var} = pickle.loads({pickle.dumps(obj, fix_imports=True)}, fix_imports=True)\n")
                  else:
                     raise("Unexpected type during resolving class!")
      elif hasattr(value, '__class__') and isinstance(value, value.__class__):
         classque.append(value.__class__)
      else:
         raise("Unexpected type during snapshotting!")
   importStmt = ''.join(imports)
   assignStmt = ''.join(assigns)
   defStmt = ''.join(defs)
   return importStmt+'\n'+assignStmt+'\n'+defStmt

def snapshot(obj) -> None:
   obj_contents = pickle.dumps(obj, fix_imports=True)
   obj_pkl_path = __get_store_path(contents=object)
   with open(obj_pkl_path, 'wb') as f:
      f.write(obj_contents)
   sdtStmt = __resolve_sdt(obj=obj, resolved=set(), imports=set(), assigns=set(), defs=set())
   dpklStmt = \
f"""
snapshot = None
with open({obj_pkl_path}, 'rb') as f:
      global snapshot
      snapshot = pickle.load(f)
"""
   stmt_contents = sdtStmt + '\n' + dpklStmt
   with open(obj_pkl_path+'.de', 'w') as f:
      f.write(stmt_contents)
   


   












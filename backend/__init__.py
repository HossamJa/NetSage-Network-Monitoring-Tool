# Make backend a package and allow direct import of all its modules
import importlib

# Make 'features' available as a submodule of 'backend'
importlib.import_module('.features', __package__)

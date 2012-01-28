import os
import glob
import sys

import contrib

def get_module_processors(module):
    processor_names = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(module.__file__)+"/*.py")]
    processor_names.remove('__init__')
    processors = []

    for name in processor_names:
        processor_name = '.'.join(module.__name__.split('.') + [name])
        __import__(processor_name)

        processor = sys.modules[processor_name].Timeseries
        processors.append((name, processor, processor.get_title()))

    return processors

processors = get_module_processors(contrib)

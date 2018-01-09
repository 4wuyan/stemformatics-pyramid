"""
State-Saving
============

Functions to support saving instance state for pickling.

"""
import logging

log = logging.getLogger(__name__)


def saveToDict(obj):
    """Recursively construct a dictionary that encodes the instance state.  This will be
passed to __setstate___ (which calls simulateRestoreFromDict) when restoring the instance."""

    if hasattr(obj, '__dict__'):
        rd = dict()
        for tup in obj.__dict__.items():
            # log.debug('type(tup[1]) ' + str(type(tup[1])))
            if hasattr(tup[1], '__class__') and ((str(tup[1].__class__).find('sqlalchemy') < 0) or \
                                                         tup[1].__class__.__name__.startswith('Mapped')):
                rd[tup[0]] = saveToDict(tup[1])
        return rd

    else:
        return obj


def simulateRestoreFromDict(obj, sd):
    """Recursive function to restore dictionary (and sub-dicts) as attributes (and sub-attrs.)"""

    for tup in sd.items():
        # Excempt _common_name_map and it's kin since we really do use these as dicts, not attrs.
        if isinstance(tup[1], dict) and (not tup[0].endswith('_name_map')):
            new_obj = type(tup[0] + '_synth_object', (object,), {})()
            simulateRestoreFromDict(new_obj, tup[1])
        else:
            new_obj = tup[1]

        setattr(obj, tup[0], new_obj)

    return obj


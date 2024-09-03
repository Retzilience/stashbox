import sys

# Dependency check and import
try:
    import os
    import pickle
    import zlib
    from datetime import datetime, timedelta
except ImportError as e:
    missing_module = str(e).split()[-1]
    print(f"Error: Missing required module '{missing_module}'.")
    print(f"Please install it using `pip install {missing_module}` and try again.")
    sys.exit(1)

# Global default settings
_DEFAULT_EXPIRY_SECONDS = 60 * 60 * 24 * 60  # 60 days in seconds
_DEFAULT_PERSISTENCE = False
_DEFAULT_COMPRESSION = False
_DEFAULT_LOGGING = True
_STORAGE = {}
_STORAGE_LOG = {}
_CACHE_DIR = "./stashbox_cache"

# Utility functions
def _current_time():
    return datetime.now()

def _expiry_time(seconds):
    if seconds is None:
        return None
    try:
        expiry = _current_time() + timedelta(seconds=seconds)
        print(f"Setting expiry time: {expiry}")  # Debugging output
        return expiry
    except OverflowError:
        print(f"Error: The expiry time calculation overflowed with seconds={seconds}.")
        return None

def _is_expired(expiry):
    buffer = timedelta(milliseconds=100)  # Allow a 100 ms buffer to account for timing discrepancies
    if expiry:
        current_time = _current_time()
        print(f"Checking expiry time: Now={current_time}, Expiry={expiry}")  # Debugging output
        return current_time > (expiry + buffer)
    return False

def _get_file_path(name):
    return os.path.join(_CACHE_DIR, f"{name}.pkl")

def _save_to_disk(name, data, compress):
    if not os.path.exists(_CACHE_DIR):
        os.makedirs(_CACHE_DIR)
    with open(_get_file_path(name), 'wb') as f:
        if compress:
            f.write(zlib.compress(pickle.dumps(data)))
        else:
            pickle.dump(data, f)

def _load_from_disk(name, decompress):
    file_path = _get_file_path(name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            if decompress:
                return pickle.loads(zlib.decompress(f.read()))
            else:
                return pickle.load(f)
    raise ValueError(f"No data found for '{name}'.")

def _delete_from_disk(name):
    file_path = _get_file_path(name)
    if os.path.exists(file_path):
        os.remove(file_path)

def _log_storage(name, persistent, compress, expiry, log, operation):
    _STORAGE_LOG[name] = {
        'persistent': persistent,
        'compress': compress,
        'expiry': expiry,
        'logged': log,
        'operation': operation
    }

# Core functions
def stash(name, data, fmt=None, persist=None, comp=None, log=None, expiry=None):
    """Stashes data with the given name and optional parameters."""
    global _STORAGE
    persist = _DEFAULT_PERSISTENCE if persist is None else persist
    comp = _DEFAULT_COMPRESSION if comp is None else comp
    log = _DEFAULT_LOGGING if log is None else log
    expiry_seconds = _DEFAULT_EXPIRY_SECONDS if expiry is None else expiry
    
    # Correct expiry time calculation
    if expiry_seconds > 0:
        expiry = _expiry_time(expiry_seconds)
    else:
        expiry = None
    
    print(f"Stashing data: Name={name}, Persist={persist}, Expiry={expiry}")  # Debugging output
    
    if persist:
        _save_to_disk(name, data, comp)
    else:
        _STORAGE[name] = (data, expiry)

    if log or _DEFAULT_LOGGING:
        _log_storage(name, persist, comp, expiry, log, 'stash')

def fetch(name, fmt=None):
    """Fetches data stashed with the given name."""
    if name in _STORAGE:
        data, expiry = _STORAGE[name]
        if _is_expired(expiry):
            del _STORAGE[name]
            raise ValueError(f"Data for '{name}' has expired.")
        return data
    elif os.path.exists(_get_file_path(name)):
        log_info = _STORAGE_LOG.get(name, {})
        decompress = log_info.get('compress', False)
        expiry = log_info.get('expiry', None)

        # Check expiry before loading from disk
        if _is_expired(expiry):
            _delete_from_disk(name)
            del _STORAGE_LOG[name]
            raise ValueError(f"Persistent data for '{name}' has expired and has been deleted.")
        
        return _load_from_disk(name, decompress)
    else:
        raise ValueError(f"No data found for '{name}'.")

# Management functions
def list_all():
    """Lists all stashed slots and their details."""
    return _STORAGE_LOG

def info(name):
    """Retrieves detailed information about the data stashed under the given name."""
    if name in _STORAGE_LOG:
        return _STORAGE_LOG[name]
    raise ValueError(f"No stash info found for '{name}'.")

def delete(name):
    """Deletes the data stashed under the given name."""
    if name in _STORAGE:
        del _STORAGE[name]
    _delete_from_disk(name)
    if name in _STORAGE_LOG:
        del _STORAGE_LOG[name]

# Global configuration functions
def set_default_expiry(seconds):
    """Sets the default expiry time for all stashed data (in seconds)."""
    global _DEFAULT_EXPIRY_SECONDS
    _DEFAULT_EXPIRY_SECONDS = seconds

def set_default_persistence(persist):
    """Sets whether data is persistent by default."""
    global _DEFAULT_PERSISTENCE
    _DEFAULT_PERSISTENCE = persist

def set_default_compression(comp):
    """Sets whether data is compressed by default when stashed persistently."""
    global _DEFAULT_COMPRESSION
    _DEFAULT_COMPRESSION = comp

def set_default_logging(enabled):
    """Sets whether logging is enabled by default."""
    global _DEFAULT_LOGGING
    _DEFAULT_LOGGING = enabled

def log_status():
    """Returns the current global logging status."""
    return _DEFAULT_LOGGING

# Stashbox

Stashbox is a lightweight Python library designed for minimalistic data storage and retrieval. It allows you to easily stash (store) and fetch (retrieve) data with support for optional persistence, compression, expiry, and logging.

## Features

- **Simple API**: Stash and fetch data with concise, easy-to-understand commands.
- **Persistence**: Optionally persist data to disk, allowing it to survive program restarts.
- **Compression**: Reduce the storage size of your data with built-in compression.
- **Expiry**: Set an expiry time for stashed data, automatically removing it when it expires.
- **Logging**: Keep track of stashed operations with optional logging. On by default.

## Installation

You can install Stashbox using `pip`:

```bash
pip install stashbox
```

## Usage

### Basic Usage

```python
import stashbox

# Stash data
stashbox.stash('my_key', 'Hello, World!')

# Fetch data
data = stashbox.fetch('my_key')
print(data)  # Outputs: Hello, World!
```

### Advanced Usage

#### Stashing Data with Persistence

```python
stashbox.stash('my_key', 'Persistent Data', persist=True)
```

#### Fetching Data

```python
data = stashbox.fetch('my_key')
```

#### Setting Expiry for Data

```python
stashbox.stash('temporary_data', 'This will expire', expiry=3600)  # Expires in 1 hour
```

#### Compressing Data

```python
stashbox.stash('compressed_key', 'This data is compressed', comp=True)
```

#### Deleting Data

```python
stashbox.delete('my_key')
```

#### Listing All Stashed Data

```python
all_data = stashbox.list_all()
print(all_data)
```

#### Retrieving Metadata

```python
metadata = stashbox.info('my_key')
print(metadata)
```

#### Customizing Default Settings

```python
stashbox.set_default_expiry(86400)  # Default expiry to 1 day
stashbox.set_default_persistence(True)  # Enable persistence by default
stashbox.set_default_compression(True)  # Enable compression by default
stashbox.set_default_logging(False)  # Disables logging by default
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request on GitHub.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

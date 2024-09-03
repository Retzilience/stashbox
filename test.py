import stashbox

# Test basic stash and fetch
stashbox.stash('test_key', 'Hello from Stashbox!')
result = stashbox.fetch('test_key')
print(result)  # Should output: Hello from Stashbox!

# Test persistence
stashbox.stash('persistent_key', 'Persistent Data', persist=True)
persistent_result = stashbox.fetch('persistent_key')
print(persistent_result)  # Should output: Persistent Data

# Test listing all stashed data
all_stashes = stashbox.list_all()
print(all_stashes)  # Should show metadata for 'test_key' and 'persistent_key'

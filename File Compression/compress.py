import zlib
import base64

data = open('data.txt', 'r').read()

# Convert to bytes as zlib.compress expect the bytes
data_bytes = data.encode('utf-8')

# Data is compressed and returned a bytes object which is encoded by base64
compressed_data = base64.b64encode(zlib.compress(data_bytes, 9))
decoded_data = compressed_data.decode('utf-8')
print(compressed_data)

# Create a compressed file and write compressed data to the file
compressed_file = open('compressed.txt', 'w')
compressed_file.write(decoded_data)

# Decompress the compressed file content and read the data
decompressed_data = zlib.decompress(base64.b64decode(compressed_data))
print(decompressed_data)

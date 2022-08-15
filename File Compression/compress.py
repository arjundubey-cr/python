import zlib
import base64

data = open('data.txt', 'r').read()

# Convert to bytes as zlib.compress expect the bytes
data_bytes = bytes(data, 'utf-8')

# Data is compressed and returned a bytes object which is encoded by base64
compressed_data = base64.b64decode(zlib.compress(data_bytes, 9))
decoded_data = compressed_data.decode('utf-8')

compressed_file = open('compressed.text', 'w')
compressed_file.write(compressed_data)

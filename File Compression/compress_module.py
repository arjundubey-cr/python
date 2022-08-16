import zlib
import base64


def compress(input_file, output_file):
    file = open(input_file, 'r')
    data = file.read()
    file.close()

    # Convert to bytes as zlib.compress expect the bytes
    data_bytes = data.encode('utf-8')

    # Data is compressed and returned a bytes object which is encoded by base64
    compressed_data = base64.b64encode(zlib.compress(data_bytes, 9))

    # Decode the data using utf-8
    decoded_data = compressed_data.decode('utf-8')

    # Create a compressed file and write compressed data to the file
    compressed_file = open(output_file, 'w')
    compressed_file.write(decoded_data)


def decompress(input_file, output_file):
    data = open(input_file, 'r').read()
    encoded_data = data.encode('utf-8')
    decompressed_data = zlib.decompress(base64.b64decode(encoded_data))
    decoded_data = decompressed_data.decode('utf-8')

    file = open(output_file, 'w')
    file.write(decoded_data)
    file.close()


# compress('data.txt', 'comp.txt')
decompress('comp.txt', 'decomp.txt')

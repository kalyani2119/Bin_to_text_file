import binascii
import struct

# Define file paths
input_file = "env_txt/uboot.env"  # Replace with your uboot.env file path
output_file = "uboot_env.txt"  # Output text file

# Open and read the binary uboot.env file
with open(input_file, 'rb') as f:
    binary_data = f.read()

# Check if the file is empty
if not binary_data:
    print("Error: The uboot.env file is empty.")
    exit()

# Extract the CRC32 checksum (first 4 bytes)
crc32_stored = struct.unpack('<I', binary_data[:4])[0]  # Little-endian unsigned int
data = binary_data[4:]  # The rest is the environment data

# Calculate CRC32 of the data to verify integrity (optional)
computed_crc32 = binascii.crc32(data) & 0xFFFFFFFF
if crc32_stored != computed_crc32:
    print(f"Warning: CRC32 mismatch. Stored: {hex(crc32_stored)}, Computed: {hex(computed_crc32)}")
else:
    print("CRC32 check passed.")

# Decode the environment data (null-terminated key=value pairs)
env_text = ""
try:
    # Split the data by null bytes and process until double null (end of env)
    env_data = data.split(b'\x00')
    for entry in env_data:
        if not entry:  # Empty entry (double null) marks the end
            break
        # Decode as UTF-8, assuming text content
        env_text += entry.decode('utf-8') + '\n'
except UnicodeDecodeError:
    print("Error: Some data couldn’t be decoded as UTF-8. Dumping as raw bytes instead.")
    env_text = "Raw hex dump:\n" + binascii.hexlify(data).decode('ascii') + '\n'

# Save to a text file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(env_text)

print(f"Converted {input_file} to {output_file}")
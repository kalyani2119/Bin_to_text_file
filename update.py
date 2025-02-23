import binascii
import struct

# Define file paths
input_text_file = "env_txt/uboot_env.txt"  # Your modified text file
output_env_file = "env_txt/update_uboot.env"     # Output binary uboot.env file

# Read the text file
with open(input_text_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Prepare the environment data
env_data = b''
for line in lines:
    line = line.strip()  # Remove leading/trailing whitespace
    if line:  # Skip empty lines
        env_data += line.encode('utf-8') + b'\x00'  # Add null terminator after each entry

# Add double null terminator to mark the end
env_data += b'\x00'

# Calculate CRC32 checksum of the environment data
crc32_value = binascii.crc32(env_data) & 0xFFFFFFFF

# Combine CRC32 and data into final binary content
binary_content = struct.pack('<I', crc32_value) + env_data  # Little-endian CRC32

# Write to the uboot.env file
with open(output_env_file, 'wb') as f:
    f.write(binary_content)

print(f"Converted {input_text_file} back to {output_env_file}")
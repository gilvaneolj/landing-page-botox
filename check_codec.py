import struct
import sys

def get_mp4_codec(file_path):
    try:
        with open(file_path, 'rb') as f:
            while True:
                header = f.read(8)
                if len(header) < 8:
                    break
                size, type_ = struct.unpack('>I4s', header)
                type_ = type_.decode('latin1')
                
                if type_ == 'ftyp':
                    brand = f.read(4).decode('latin1')
                    return f"Type: {type_}, Brand: {brand}"
                
                # Skip to next atom
                if size == 1:
                    # 64-bit size
                    size = struct.unpack('>Q', f.read(8))[0]
                    f.seek(size - 16, 1)
                else:
                    f.seek(size - 8, 1)
    except Exception as e:
        return str(e)
    return "Unknown"

print(get_mp4_codec(r"c:\Users\joao_\OneDrive\Área de Trabalho\Landing Page\landing-page-botox\public\videos\video-institucional.mp4"))

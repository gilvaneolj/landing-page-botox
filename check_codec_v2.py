import struct
import os

def find_atom(f, target, end):
    while f.tell() < end:
        try:
            header = f.read(8)
            if len(header) < 8: break
            size, type_ = struct.unpack('>I4s', header)
            type_ = type_.decode('latin1')
            
            if size == 1:
                size = struct.unpack('>Q', f.read(8))[0]
                header_size = 16
            else:
                header_size = 8
            
            if type_ == target:
                return f.tell() + size - header_size
            
            if type_ in ['moov', 'trak', 'mdia', 'minf', 'stbl', 'stsd']:
                # Container atoms, recurse
                res = find_atom(f, target, f.tell() + size - header_size)
                if res: return res
            
            # Skip payload
            f.seek(size - header_size, 1)
        except:
            break
    return None

def get_codec(file_path):
    with open(file_path, 'rb') as f:
        f.seek(0, 2)
        end = f.tell()
        f.seek(0)
        
        # We need to find 'stsd' (Sample Description Box)
        # Hierarchy: moov -> trak -> mdia -> minf -> stbl -> stsd
        
        # Let's write a simple recursive scanner for these containers
        current_end = end
        
        # Scan for moov
        while f.tell() < current_end:
            header = f.read(8)
            if len(header) < 8: break
            size, type_ = struct.unpack('>I4s', header)
            type_ = type_.decode('latin1')
            
            if size == 1:
                size = struct.unpack('>Q', f.read(8))[0]
                payload_size = size - 16
            else:
                payload_size = size - 8
                
            if type_ == 'moov':
                # Found moov, search inside for trak -> ... -> stsd
                moov_end = f.tell() + payload_size
                return scan_for_stsd(f, moov_end)
            
            f.seek(payload_size, 1)
            
    return "moov not found"

def scan_for_stsd(f, end_pos):
    while f.tell() < end_pos:
        header = f.read(8)
        if len(header) < 8: break
        size, type_ = struct.unpack('>I4s', header)
        type_ = type_.decode('latin1')
        
        if size == 1:
            size = struct.unpack('>Q', f.read(8))[0]
            payload_size = size - 16
        else:
            payload_size = size - 8
            
        atom_end = f.tell() + payload_size
        
        if type_ == 'stsd':
            # Inside stsd:
            # 4 bytes version/flags
            # 4 bytes entry count
            # Then the codec atoms
            f.read(8) 
            codec_header = f.read(8)
            c_size, c_type = struct.unpack('>I4s', codec_header)
            return c_type.decode('latin1')
            
        if type_ in ['trak', 'mdia', 'minf', 'stbl']:
            res = scan_for_stsd(f, atom_end)
            if res: return res
            
        f.seek(atom_end)
        
    return None

print(get_codec(r"c:\Users\joao_\OneDrive\Área de Trabalho\Landing Page\landing-page-botox\public\videos\video-institucional.mp4"))

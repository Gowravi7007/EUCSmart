import hashlib
with open('C:\\Users\\gowra\\.gemini\\antigravity\\scratch\\antigravity_oem\\Antigravity.bin', 'rb') as f:
    h = hashlib.sha256(f.read()).hexdigest().upper()
with open('C:\\Users\\gowra\\.gemini\\antigravity\\scratch\\antigravity_oem\\hash.txt', 'w') as out:
    out.write(h)

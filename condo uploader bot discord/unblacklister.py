import random
import secrets
from lxml import etree

file = 'file.rbxlx'

# เปิดไฟล์ .rbxlx
try:
    doc = etree.parse(file)
except Exception as e:
    print(f"Error opening file: {e}")
    exit()

def uniqueId():
    print('UniqueId Unpatched')
    for el in doc.xpath("//UniqueId[@name='UniqueId']"):
        el.text = f'ILlmaijji{secrets.token_hex(110)}'
    save_file()

def referentt():
    print('Referent Unpatched')
    for el in doc.xpath("//Item[@referent]"):
        string = ''.join(random.choice('oijj') for _ in range(70))
        el.attrib['referent'] = f'Strijg{string}'
    save_file()

def assetId():
    print('AssetId Unpatched')
    for el in doc.xpath("//SourceAssetId[@name='SourceAssetId']"):
        el.text = f'-{secrets.token_hex(20)}'
    save_file()

# ฟังก์ชันบันทึกไฟล์
def save_file():
    try:
        with open(file, 'wb') as f:
            doc.write(f, pretty_print=True, xml_declaration=True, encoding="utf-8")
        print(f"File saved: {file}")
    except Exception as e:
        print(f"Error saving file: {e}")

# เรียกฟังก์ชันที่ต้องการ
uniqueId()
referentt()
assetId()

import hashlib
# import modulu
def sha256(text):
    # parametr text - funkci voláme s textovým řetězcem
    encoded_data = text.encode( 'utf-8' )
    # převede vstupní textový řetězec text na bajty pomocí kódování UTF-8
    # a uloží výsledek do proměnné
    hash_object = hashlib.sha256()
    # objekt se připraví pro výpočet SHA-256 hashe
    hash_object.update(encoded_data)
    # do objektu pomocí této metody přidáme kódovaná data
    hashed_data = hash_object.hexdigest()
    # metoda vrátí hash v textové podobě (hexadecimální reprezentace)
    return hashed_data
    # funkce vrátí zpracovaný řetězec
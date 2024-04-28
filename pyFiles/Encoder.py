import hashlib
def sha256(text):
    encoded_data = text.encode( 'utf-8' )

    hash_object = hashlib.sha256()

    hash_object.update( encoded_data )

    hashed_data = hash_object.hexdigest()

    return hashed_data
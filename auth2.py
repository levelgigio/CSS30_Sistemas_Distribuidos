from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

# random_seed = Random.new().read
#
# message = "To be signed".encode("utf-8")
# key = RSA.generate(1024, random_seed)
# h = SHA256.new(message)
# signature = pss.new(key).sign(h)
#
#
# # key = RSA.import_key(open('pubkey.der').read())
# # h = SHA256.new(message)
# verifier = pss.new(key.publickey())
# try:
#     verifier.verify(h, signature)
#     print( "The signature is authentic.")
# except (ValueError, TypeError):
#     print( "The signature is not authentic.")


# Criou-se uma semente randômica para gerar o par
# chave privada/pública.
random_seed = Random.new().read

# Posteriormente criou-se o par de chave privada/pública
# (gerada por Alice no exemplo).
keyPair = RSA.generate(1024, random_seed)
pubKey = keyPair.publickey()

# Dois textos foram usados. Um autêntico (gerado por Alice),
# sobre o qual a assinatura foi gerada, e um não-autentico
# (alterado na rede) sobre o qual iremos testar a assinatura
# para fins didáticos:
True_text = "Hello Bob"
True_text_encoded = True_text.encode("utf-8")
Fake_text = "Bye Bob"
Fake_text_encoded = Fake_text.encode("utf-8")
# A assinatura digital é então gerada usando o hash
# SHA256 aplicado ao conteúdo do texto
hashA = SHA256.new(True_text_encoded)
digitalSign = pss.new(keyPair).sign(hashA)
# signature = pss.new(key).sign(h)

print("Hash A:" + repr(hashA) + "\n")
print("Digital signature:" + repr(digitalSign) + "\n")

# O receptor da mensagem (Bob) recebe dois textos, e para
# analisar qual é o autentico irá usar a assinatura digital
# recebida. Primeiramente ele gera o hash SHA256 para cada
# um dos trechos de textos.
hashB = SHA256.new(True_text_encoded)
hashC = SHA256.new(Fake_text_encoded)

# Posteriormente ele utiliza a assinatura digital recebida
# para validar a autenticidade dos textos.
print("HashB :" + repr(hashB) + "\n")
print("HashC :" + repr(hashC) + "\n")


verifier = pss.new(pubKey)

try:
    verifier.verify(hashB, digitalSign)
    print("The signature is authentic.")
except (ValueError, TypeError):
    print("The signature is not authentic.")
try:
    verifier.verify(hashC, digitalSign)
    print("The signature is authentic.")
except (ValueError, TypeError):
    print("The signature is not authentic.")
# if pubKey.verify(hashB, digitalSign):
#     print("O texto autentico é " + True_text)
# elif pubKey.verify(hashB, digitalSign):
#     print("O texto autentico é " + Fake_text)
# else:
#     print("Nenhum dos textos é autentico")

# Finalmente, qual dos textos é o original de Alice!

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random


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
True_text = 'Hello Bob'
Fake_text = 'Bye Bob'

# A assinatura digital é então gerada usando o hash 
# SHA256 aplicado ao conteúdo do texto
hashA = SHA256.new(True_text.encode('utf-8')).digest()
digitalSign = keyPair.sign(hashA, '')

print("Hash A:" + repr(hashA) + "\n")
print("Digital signature:" + repr(digitalSign) + "\n")

# O receptor da mensagem (Bob) recebe dois textos, e para 
# analisar qual é o autentico irá usar a assinatura digital 
# recebida. Primeiramente ele gera o hash SHA256 para cada 
# um dos trechos de textos.
hashB = SHA256.new(True_text.encode('utf-8')).digest()
hashC = SHA256.new(Fake_text.encode('utf-8')).digest()

# Posteriormente ele utiliza a assinatura digital recebida 
# para validar a autenticidade dos textos.
print("HashB :" + repr(hashB) + "\n")
print("HashC :" + repr(hashC) + "\n")

if(pubKey.verify(hashB, digitalSign)):
    print("O texto autentico é " + True_text)
elif(pubKey.verify(hashB, digitalSign)):
    print("O texto autentico é " + Fake_text)
else:
    print("Nenhum dos textos é autentico")

# Finalmente, qual dos textos é o original de Alice!
from apps import encoder, decoder,sxtw_encoder, sxtw_decoder, aes_encoder, aes_decoder

str = "♦♥"
encode = encoder(str)
print("encoded: ", encode)
print("Lenght: ", len(encode))

decode = decoder(encode)
print("decoded: ", decode)

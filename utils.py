def fragmenta(mensagem : bytes):
    tamanho = len(mensagem)
    inteiro = tamanho // 50
    resto = tamanho % 50
    fragmentos = []
    if inteiro > 0:    
        for i in range(inteiro - 1):
            fragmentos.append(mensagem[i:50 * (i + 1)])
    if resto>0:
        fragmentos.append(mensagem[50*inteiro:])

    return fragmentos

def make_pack(fragmentos : list):
    



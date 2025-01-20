# Password Manager ----- Eye see you
import os, sys
import pyperclip

Show:bool = False
Size:int = 16
char_list:str = "abcdefghijklmnopqrstuvwxyz1234567890-+.,;/\\!@#$%&*()_=~{}[]"


# ---------------------- Main function
def __main__():	
	_isint = False
	while(_isint == False):
		try:
			chave: str = input("Digite sua senha numérica. Qualquer número serve:\n*o número não será salvo, então é importante memorizar.\n")
			if (int(chave) > 0):
				_isint = True
		except ValueError:
			_isint = False
	del(_isint)
	limpar()
	while True:
		inp: str = input("Digite o nome do APP sem caracteres especiais (/h para obter ajuda): ").lower()
		_comandos = comandos(inp)
		if(_comandos == 2):
			break
		elif(_comandos == 1):
			continue
		elif(_comandos == 0):
			pass
		else:
			print("Comando retornou um valor não indexado: ", _comandos)
			break
		if(inp.isalpha() == False):
			continue
		senha = gen_pass(chave, inp)
		if senha == -1:
			print(f"""
--------------------------------------
Erro ao gerar a senha. Nome do APP e/ou chave inválidos.
Prssione ENTER para sair
""")
			input()
			break
		pyperclip.copy(senha)
		if Show:
			limpar()
			print(f"Senha: {senha} ------ (copiada para área de transferência)\n")
		else:
			print(f"Senha: {senha[0:5]}*********** - (copiada para área de transferência)\n")
		del senha


# ---------------------- Comandos
def comandos(inp:str):
	global Show
	comandos = """
SHOW  |SHOWPASS |MOSTRAR  |VER |/S ---- Habilita impressão da senha na tela.
HIDE  |HIDEPASS |ESCONDER          ---- Desabilita a impressão da senha na tela.
HELP  |AJUDA    |/H                ---- Imprime a tela de ajuda.
QUIT  |SAIR     |LEAVE    |/Q |/L  ---- Finaliza o programa
CLEAR |CLS      |LIMPAR   |/C      ---- Limpa a tela
"""
	if inp in ("quit", "sair", "leave", "/q", "/l"):
		if input("Tem certeza? [S/N] ").lower() == "s":
			print("Saindo...")
			return 2
		else:
			return 1
	elif(inp in ("mostrar", "show", "ver", "showpass", "/s")):
		Show = True
		return 1
	elif(inp in ("esconder", "hide", "hidepass")):
		Show = False
		return 1
	elif(inp in ("help", "ajuda", "commands", "/h")):
		print(comandos)
		return 1
	elif(inp in ("clear", "limpar", "cls", "/c")):
		limpar()
		return 1
	return 0


# ---------------------- Password Generator
def gen_pass(key: str, appinp: str):
	try:
		appname = encrypt_name(key, appinp)
		senha: str = ""
		cont = 0
		for i in range(Size):
			if int(key[cont]) % 2:
				isup = True
			else:
				isup = False
			_num = i-1+(ord(appname[i].upper())-65)+int(key[cont])
			if _num < len(char_list):
				if i % 2:
					_char = char_list[_num]
				else:
					_char = char_list[-_num]
			else:
				if isup:
					_char = char_list[0]
				else:
					_char = char_list[len(char_list)-1]
			if isup:
				_char = _char.upper()
			senha += _char
			cont = (cont+1 if cont != len(key)-1 else 0)
		return senha
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		return -1



# ---------------------- App internal name
def encrypt_name(key, appinp):
	cur = 1
	cont = 0
	_app_name = appinp
	while(len(_app_name) < Size):
		if(len(_app_name) > 1):
			if(len(_app_name)-1 > int(key[cont])):
				_app_name += char_list[ord(_app_name[int(key[cont])].upper())+cur-65]
			else:
				_app_name += char_list[ord(_app_name[(-2)].upper())+cur-65]
		else:
			_app_name += _app_name
		cont = (cont+1 if cont != len(key)-1 else 0)
		cur += 1
	return _app_name


# ---------------------- CLS
def limpar():
	_ = os.system('cls')


if(__name__ == '__main__'):
	__main__()
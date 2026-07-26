class UsuarioController:
    def __init__(self, usuario_model):
        self.model = usuario_model

    def listar(self):
        return {"dados": self.model.get_all(), "sucesso": True}, 200

    def buscar(self, usuario_id):
        usuario = self.model.get_by_id(usuario_id)
        if usuario:
            return {"dados": usuario, "sucesso": True}, 200
        return {"erro": "Usuário não encontrado"}, 404

    def criar(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400
        nome = dados.get("nome", "")
        email = dados.get("email", "")
        senha = dados.get("senha", "")
        if not nome or not email or not senha:
            return {"erro": "Nome, email e senha são obrigatórios"}, 400
        usuario_id = self.model.create(nome, email, senha)
        return {"dados": {"id": usuario_id}, "sucesso": True}, 201

    def login(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400
        email = dados.get("email", "")
        senha = dados.get("senha", "")
        if not email or not senha:
            return {"erro": "Email e senha são obrigatórios"}, 400
        usuario = self.model.login(email, senha)
        if usuario:
            return {"dados": usuario, "sucesso": True, "mensagem": "Login OK"}, 200
        return {"erro": "Email ou senha inválidos", "sucesso": False}, 401

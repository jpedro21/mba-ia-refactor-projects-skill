from config.settings import VALID_CATEGORIES


class ProdutoController:
    def __init__(self, produto_model):
        self.model = produto_model

    def listar(self):
        return {"dados": self.model.get_all(), "sucesso": True}, 200

    def buscar(self, produto_id):
        produto = self.model.get_by_id(produto_id)
        if produto:
            return {"dados": produto, "sucesso": True}, 200
        return {"erro": "Produto não encontrado", "sucesso": False}, 404

    def criar(self, dados):
        error = self._validate_produto_data(dados)
        if error:
            return {"erro": error}, 400
        produto_id = self.model.create(
            dados["nome"], dados.get("descricao", ""),
            dados["preco"], dados["estoque"], dados.get("categoria", "geral"),
        )
        return {"dados": {"id": produto_id}, "sucesso": True, "mensagem": "Produto criado"}, 201

    def atualizar(self, produto_id, dados):
        if not self.model.get_by_id(produto_id):
            return {"erro": "Produto não encontrado"}, 404
        error = self._validate_produto_data(dados)
        if error:
            return {"erro": error}, 400
        self.model.update(
            produto_id, dados["nome"], dados.get("descricao", ""),
            dados["preco"], dados["estoque"], dados.get("categoria", "geral"),
        )
        return {"sucesso": True, "mensagem": "Produto atualizado"}, 200

    def deletar(self, produto_id):
        if not self.model.get_by_id(produto_id):
            return {"erro": "Produto não encontrado"}, 404
        self.model.delete(produto_id)
        return {"sucesso": True, "mensagem": "Produto deletado"}, 200

    def buscar_filtrado(self, termo, categoria, preco_min, preco_max):
        resultados = self.model.search(termo, categoria, preco_min, preco_max)
        return {"dados": resultados, "total": len(resultados), "sucesso": True}, 200

    def _validate_produto_data(self, dados):
        if not dados:
            return "Dados inválidos"
        for field in ("nome", "preco", "estoque"):
            if field not in dados:
                return f"{field.capitalize()} é obrigatório"
        if dados["preco"] < 0:
            return "Preço não pode ser negativo"
        if dados["estoque"] < 0:
            return "Estoque não pode ser negativo"
        if len(dados["nome"]) < 2:
            return "Nome muito curto"
        if len(dados["nome"]) > 200:
            return "Nome muito longo"
        categoria = dados.get("categoria", "geral")
        if categoria not in VALID_CATEGORIES:
            return f"Categoria inválida. Válidas: {VALID_CATEGORIES}"
        return None

from config.settings import (
    VALID_ORDER_STATUSES,
    DISCOUNT_TIER_HIGH, DISCOUNT_TIER_MEDIUM, DISCOUNT_TIER_LOW,
    DISCOUNT_RATE_HIGH, DISCOUNT_RATE_MEDIUM, DISCOUNT_RATE_LOW,
)


class PedidoController:
    def __init__(self, pedido_model):
        self.model = pedido_model

    def criar(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400
        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])
        if not usuario_id:
            return {"erro": "Usuario ID é obrigatório"}, 400
        if not itens:
            return {"erro": "Pedido deve ter pelo menos 1 item"}, 400
        resultado = self.model.create(usuario_id, itens)
        if "erro" in resultado:
            return {"erro": resultado["erro"], "sucesso": False}, 400
        return {"dados": resultado, "sucesso": True, "mensagem": "Pedido criado com sucesso"}, 201

    def listar_por_usuario(self, usuario_id):
        return {"dados": self.model.get_by_usuario(usuario_id), "sucesso": True}, 200

    def listar_todos(self):
        return {"dados": self.model.get_all(), "sucesso": True}, 200

    def atualizar_status(self, pedido_id, dados):
        novo_status = dados.get("status", "") if dados else ""
        if novo_status not in VALID_ORDER_STATUSES:
            return {"erro": "Status inválido"}, 400
        self.model.update_status(pedido_id, novo_status)
        return {"sucesso": True, "mensagem": "Status atualizado"}, 200

    def relatorio_vendas(self):
        discount_tiers = {
            "high": DISCOUNT_TIER_HIGH,
            "medium": DISCOUNT_TIER_MEDIUM,
            "low": DISCOUNT_TIER_LOW,
            "rate_high": DISCOUNT_RATE_HIGH,
            "rate_medium": DISCOUNT_RATE_MEDIUM,
            "rate_low": DISCOUNT_RATE_LOW,
        }
        return {"dados": self.model.relatorio_vendas(discount_tiers), "sucesso": True}, 200

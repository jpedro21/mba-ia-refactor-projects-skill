class PedidoModel:
    def __init__(self, db):
        self.db = db

    def _build_pedido_with_items(self, rows):
        pedidos = {}
        for row in rows:
            pid = row["pedido_id"] if "pedido_id" in row.keys() else row["id"]
            if pid not in pedidos:
                pedidos[pid] = {
                    "id": pid,
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": [],
                }
            if row["produto_id"]:
                pedidos[pid]["itens"].append({
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"] or "Desconhecido",
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"],
                })
        return list(pedidos.values())

    def create(self, usuario_id, itens):
        cursor = self.db.cursor()
        total = 0

        for item in itens:
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            if produto is None:
                return {"erro": f"Produto {item['produto_id']} não encontrado"}
            if produto["estoque"] < item["quantidade"]:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            total += produto["preco"] * item["quantidade"]

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total),
        )
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute("SELECT preco FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"]),
            )

        self.db.commit()
        return {"pedido_id": pedido_id, "total": total}

    def get_by_usuario(self, usuario_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT p.id as pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
                   ip.produto_id, ip.quantidade, ip.preco_unitario, pr.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = ip.produto_id
            WHERE p.usuario_id = ?
        """, (usuario_id,))
        return self._build_pedido_with_items(cursor.fetchall())

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT p.id as pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
                   ip.produto_id, ip.quantidade, ip.preco_unitario, pr.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = ip.produto_id
        """)
        return self._build_pedido_with_items(cursor.fetchall())

    def update_status(self, pedido_id, novo_status):
        cursor = self.db.cursor()
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
        self.db.commit()
        return True

    def relatorio_vendas(self, discount_tiers):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(total) FROM pedidos")
        faturamento = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
        pendentes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
        aprovados = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
        cancelados = cursor.fetchone()[0]

        desconto = 0
        if faturamento > discount_tiers["high"]:
            desconto = faturamento * discount_tiers["rate_high"]
        elif faturamento > discount_tiers["medium"]:
            desconto = faturamento * discount_tiers["rate_medium"]
        elif faturamento > discount_tiers["low"]:
            desconto = faturamento * discount_tiers["rate_low"]

        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": round(faturamento, 2),
            "desconto_aplicavel": round(desconto, 2),
            "faturamento_liquido": round(faturamento - desconto, 2),
            "pedidos_pendentes": pendentes,
            "pedidos_aprovados": aprovados,
            "pedidos_cancelados": cancelados,
            "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
        }

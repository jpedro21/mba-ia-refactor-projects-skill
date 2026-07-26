class UsuarioModel:
    def __init__(self, db):
        self.db = db

    def _row_to_dict(self, row, include_password=False):
        data = {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "tipo": row["tipo"],
            "criado_em": row["criado_em"],
        }
        if include_password:
            data["senha"] = row["senha"]
        return data

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usuarios")
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def get_by_id(self, usuario_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def login(self, email, senha):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "nome": row["nome"],
                "email": row["email"],
                "tipo": row["tipo"],
            }
        return None

    def create(self, nome, email, senha, tipo="cliente"):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, tipo),
        )
        self.db.commit()
        return cursor.lastrowid

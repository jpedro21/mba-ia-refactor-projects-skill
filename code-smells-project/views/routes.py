from flask import jsonify, request
from controllers.produto_controller import ProdutoController
from controllers.usuario_controller import UsuarioController
from controllers.pedido_controller import PedidoController


def register_routes(app, produto_ctrl, usuario_ctrl, pedido_ctrl):
    @app.route("/produtos", methods=["GET"])
    def listar_produtos():
        body, status = produto_ctrl.listar()
        return jsonify(body), status

    @app.route("/produtos/busca", methods=["GET"])
    def buscar_produtos():
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria", None)
        preco_min = float(request.args.get("preco_min")) if request.args.get("preco_min") else None
        preco_max = float(request.args.get("preco_max")) if request.args.get("preco_max") else None
        body, status = produto_ctrl.buscar_filtrado(termo, categoria, preco_min, preco_max)
        return jsonify(body), status

    @app.route("/produtos/<int:id>", methods=["GET"])
    def buscar_produto(id):
        body, status = produto_ctrl.buscar(id)
        return jsonify(body), status

    @app.route("/produtos", methods=["POST"])
    def criar_produto():
        body, status = produto_ctrl.criar(request.get_json())
        return jsonify(body), status

    @app.route("/produtos/<int:id>", methods=["PUT"])
    def atualizar_produto(id):
        body, status = produto_ctrl.atualizar(id, request.get_json())
        return jsonify(body), status

    @app.route("/produtos/<int:id>", methods=["DELETE"])
    def deletar_produto(id):
        body, status = produto_ctrl.deletar(id)
        return jsonify(body), status

    @app.route("/usuarios", methods=["GET"])
    def listar_usuarios():
        body, status = usuario_ctrl.listar()
        return jsonify(body), status

    @app.route("/usuarios/<int:id>", methods=["GET"])
    def buscar_usuario(id):
        body, status = usuario_ctrl.buscar(id)
        return jsonify(body), status

    @app.route("/usuarios", methods=["POST"])
    def criar_usuario():
        body, status = usuario_ctrl.criar(request.get_json())
        return jsonify(body), status

    @app.route("/login", methods=["POST"])
    def login():
        body, status = usuario_ctrl.login(request.get_json())
        return jsonify(body), status

    @app.route("/pedidos", methods=["POST"])
    def criar_pedido():
        body, status = pedido_ctrl.criar(request.get_json())
        return jsonify(body), status

    @app.route("/pedidos", methods=["GET"])
    def listar_todos_pedidos():
        body, status = pedido_ctrl.listar_todos()
        return jsonify(body), status

    @app.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])
    def listar_pedidos_usuario(usuario_id):
        body, status = pedido_ctrl.listar_por_usuario(usuario_id)
        return jsonify(body), status

    @app.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])
    def atualizar_status_pedido(pedido_id):
        body, status = pedido_ctrl.atualizar_status(pedido_id, request.get_json())
        return jsonify(body), status

    @app.route("/relatorios/vendas", methods=["GET"])
    def relatorio_vendas():
        body, status = pedido_ctrl.relatorio_vendas()
        return jsonify(body), status

    @app.route("/")
    def index():
        return jsonify({
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "1.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            },
        })

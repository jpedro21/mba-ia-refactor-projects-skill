import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))

VALID_CATEGORIES = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
VALID_ORDER_STATUSES = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]

DISCOUNT_TIER_HIGH = 10000
DISCOUNT_TIER_MEDIUM = 5000
DISCOUNT_TIER_LOW = 1000
DISCOUNT_RATE_HIGH = 0.10
DISCOUNT_RATE_MEDIUM = 0.05
DISCOUNT_RATE_LOW = 0.02

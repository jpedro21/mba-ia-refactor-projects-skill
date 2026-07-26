function formatCurrency(value) {
    return `R$ ${value.toFixed(2)}`;
}

module.exports = { formatCurrency };

require('dotenv').config();

module.exports = {
    port: parseInt(process.env.PORT || '3000', 10),
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || '',
    dbPath: process.env.DB_PATH || ':memory:',
};

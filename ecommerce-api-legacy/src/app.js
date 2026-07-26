const express = require('express');
const { port } = require('./config/settings');
const { createDatabase, initDb } = require('./database');
const { registerRoutes } = require('./views/routes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();
app.use(express.json());

const db = createDatabase();
initDb(db).then(() => {
    registerRoutes(app, db);
    app.use(errorHandler);

    app.listen(port, () => {
        console.log(`LMS API rodando na porta ${port}...`);
    });
}).catch(err => {
    console.error('Failed to initialize database:', err);
    process.exit(1);
});

module.exports = app;

const checkoutController = require('../controllers/checkoutController');
const reportController = require('../controllers/reportController');
const userController = require('../controllers/userController');

function registerRoutes(app, db) {
    app.post('/api/checkout', async (req, res, next) => {
        try {
            const result = await checkoutController.processCheckout(db, req.body);
            if (typeof result.body === 'string') {
                res.status(result.status).send(result.body);
            } else {
                res.status(result.status).json(result.body);
            }
        } catch (err) {
            next(err);
        }
    });

    app.get('/api/admin/financial-report', async (req, res, next) => {
        try {
            const result = await reportController.getFinancialReport(db);
            res.status(result.status).json(result.body);
        } catch (err) {
            next(err);
        }
    });

    app.delete('/api/users/:id', async (req, res, next) => {
        try {
            const result = await userController.deleteUser(db, req.params.id);
            res.status(result.status).send(result.body);
        } catch (err) {
            next(err);
        }
    });
}

module.exports = { registerRoutes };

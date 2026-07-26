const enrollmentModel = require('../models/enrollmentModel');

async function getFinancialReport(db) {
    const report = await enrollmentModel.getFinancialReport(db);
    return { status: 200, body: report };
}

module.exports = { getFinancialReport };

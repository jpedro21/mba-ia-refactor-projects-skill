const courseModel = require('../models/courseModel');
const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const { paymentGatewayKey } = require('../config/settings');

async function processCheckout(db, body) {
    const { usr: name, eml: email, pwd: password, c_id: courseId, card: cardNumber } = body;

    if (!name || !email || !courseId || !cardNumber) {
        return { status: 400, body: 'Bad Request' };
    }

    const course = await courseModel.findActiveById(db, courseId);
    if (!course) {
        return { status: 404, body: 'Curso não encontrado' };
    }

    const status = cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
    if (status === 'DENIED') {
        return { status: 400, body: 'Pagamento recusado' };
    }

    let user = await userModel.findByEmail(db, email);
    let userId;

    if (!user) {
        userId = await userModel.createUser(db, name, email, password || '123456');
    } else {
        userId = user.id;
    }

    const enrollmentId = await enrollmentModel.createEnrollment(db, userId, courseId);
    await enrollmentModel.createPayment(db, enrollmentId, course.price, status);
    await enrollmentModel.logAudit(db, `Checkout curso ${courseId} por ${userId}`);

    return { status: 200, body: { msg: 'Sucesso', enrollment_id: enrollmentId } };
}

module.exports = { processCheckout };

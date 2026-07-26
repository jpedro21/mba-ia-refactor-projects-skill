const { dbRun, dbGet, dbAll } = require('../database');

async function createEnrollment(db, userId, courseId) {
    const result = await dbRun(db, "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [userId, courseId]);
    return result.lastID;
}

async function createPayment(db, enrollmentId, amount, status) {
    return dbRun(db, "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [enrollmentId, amount, status]);
}

async function logAudit(db, action) {
    return dbRun(db, "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);
}

async function getFinancialReport(db) {
    const courses = await dbAll(db, "SELECT * FROM courses");
    const report = [];

    for (const course of courses) {
        const courseData = { course: course.title, revenue: 0, students: [] };
        const enrollments = await dbAll(db, "SELECT * FROM enrollments WHERE course_id = ?", [course.id]);

        for (const enr of enrollments) {
            const user = await dbGet(db, "SELECT name, email FROM users WHERE id = ?", [enr.user_id]);
            const payment = await dbGet(db, "SELECT amount, status FROM payments WHERE enrollment_id = ?", [enr.id]);

            if (payment && payment.status === 'PAID') {
                courseData.revenue += payment.amount;
            }
            courseData.students.push({
                student: user ? user.name : 'Unknown',
                paid: payment ? payment.amount : 0,
            });
        }
        report.push(courseData);
    }
    return report;
}

module.exports = { createEnrollment, createPayment, logAudit, getFinancialReport };

const { dbGet } = require('../database');

async function findActiveById(db, courseId) {
    return dbGet(db, "SELECT * FROM courses WHERE id = ? AND active = 1", [courseId]);
}

module.exports = { findActiveById };

const crypto = require('crypto');
const { dbRun, dbGet } = require('../database');

async function findByEmail(db, email) {
    return dbGet(db, "SELECT id FROM users WHERE email = ?", [email]);
}

async function createUser(db, name, email, password) {
    const hash = hashPassword(password);
    const result = await dbRun(db, "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [name, email, hash]);
    return result.lastID;
}

async function deleteUser(db, id) {
    await dbRun(db, "DELETE FROM enrollments WHERE user_id = ?", [id]);
    await dbRun(db, "DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)", [id]);
    return dbRun(db, "DELETE FROM users WHERE id = ?", [id]);
}

function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

module.exports = { findByEmail, createUser, deleteUser, hashPassword };

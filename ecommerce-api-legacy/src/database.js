const sqlite3 = require('sqlite3').verbose();
const { dbPath } = require('./config/settings');

function createDatabase() {
    return new sqlite3.Database(dbPath);
}

function dbRun(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.run(sql, params, function (err) {
            if (err) reject(err);
            else resolve({ lastID: this.lastID, changes: this.changes });
        });
    });
}

function dbGet(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) reject(err);
            else resolve(row);
        });
    });
}

function dbAll(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.all(sql, params, (err, rows) => {
            if (err) reject(err);
            else resolve(rows);
        });
    });
}

async function initDb(db) {
    await dbRun(db, "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)");
    await dbRun(db, "CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)");
    await dbRun(db, "CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)");
    await dbRun(db, "CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)");
    await dbRun(db, "CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)");

    const userCount = await dbGet(db, "SELECT COUNT(*) as count FROM users");
    if (userCount.count === 0) {
        await dbRun(db, "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", ['Leonan', 'leonan@fullcycle.com.br', '123']);
        await dbRun(db, "INSERT INTO courses (title, price, active) VALUES (?, ?, ?)", ['Clean Architecture', 997.00, 1]);
        await dbRun(db, "INSERT INTO courses (title, price, active) VALUES (?, ?, ?)", ['Docker', 497.00, 1]);
        await dbRun(db, "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [1, 1]);
        await dbRun(db, "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [1, 997.00, 'PAID']);
    }
}

module.exports = { createDatabase, dbRun, dbGet, dbAll, initDb };

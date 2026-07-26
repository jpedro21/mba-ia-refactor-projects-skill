const userModel = require('../models/userModel');

async function deleteUser(db, id) {
    await userModel.deleteUser(db, id);
    return { status: 200, body: 'Usuário deletado com sucesso.' };
}

module.exports = { deleteUser };

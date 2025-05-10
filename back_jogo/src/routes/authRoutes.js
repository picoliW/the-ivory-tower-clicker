const express = require("express");
const router = express.Router();
const pool = require("../config/dbConfig");

router.post("/register", async (req, res) => {
  const { email, password, confirmPassword } = req.body;

  if (!email || !password || !confirmPassword) {
    return res.status(400).json({
      success: false,
      message: "Todos os campos são obrigatórios",
    });
  }

  if (password !== confirmPassword) {
    return res.status(400).json({
      success: false,
      message: "As senhas não coincidem",
    });
  }

  try {
    const [existingUsers] = await pool.query(
      "SELECT * FROM users WHERE email = ?",
      [email]
    );

    if (existingUsers.length > 0) {
      return res.status(400).json({
        success: false,
        message: "Email já cadastrado",
      });
    }

    const [result] = await pool.query(
      "INSERT INTO users (email, password) VALUES (?, ?)",
      [email, password]
    );

    res.status(201).json({
      success: true,
      message: "Registro realizado com sucesso",
      userId: result.insertId,
    });
  } catch (error) {
    console.error("Erro no registro:", error);
    res.status(500).json({
      success: false,
      message: "Erro no servidor ao registrar usuário",
    });
  }
});

module.exports = router;

const express = require("express");
const router = express.Router();
const pool = require("../config/dbConfig");

router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({
      success: false,
      message: "Email e senha são obrigatórios",
    });
  }

  try {
    const [users] = await pool.query("SELECT * FROM users WHERE email = ?", [
      email,
    ]);

    if (users.length === 0) {
      return res.status(404).json({
        success: false,
        message: "Account not found",
      });
    }

    const user = users[0];
    if (user.password !== password) {
      return res.status(401).json({
        success: false,
        message: "Account not found",
      });
    }

    const [playerData] = await pool.query(
      "SELECT * FROM player_data WHERE user_id = ?",
      [user.id]
    );

    let data;
    if (playerData.length === 0) {
      const [result] = await pool.query(
        "INSERT INTO player_data (user_id) VALUES (?)",
        [user.id]
      );
      data = {
        damage: 1,
        gold: 0,
        gold_per_second: 0,
        floor: 1,
        dash_unlocked: false,
      };
    } else {
      data = playerData[0];
    }

    res.status(200).json({
      success: true,
      message: "Login realizado com sucesso",
      user: {
        id: user.id,
        email: user.email,
      },
      playerData: data,
    });
  } catch (error) {
    console.error("Erro no login:", error);
    res.status(500).json({
      success: false,
      message: "Erro no servidor ao fazer login",
    });
  }
});

router.post("/save-player-data", async (req, res) => {
  const { userId, damage, gold, gold_per_second, floor, dash_unlocked } =
    req.body;

  try {
    await pool.query(
      `UPDATE player_data 
       SET damage = ?, gold = ?, gold_per_second = ?, floor = ?, dash_unlocked = ?
       WHERE user_id = ?`,
      [damage, gold, gold_per_second, floor, dash_unlocked, userId]
    );

    res.status(200).json({
      success: true,
      message: "Player data saved successfully",
    });
  } catch (error) {
    console.error("Error saving player data:", error);
    res.status(500).json({
      success: false,
      message: "Error saving player data",
    });
  }
});

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

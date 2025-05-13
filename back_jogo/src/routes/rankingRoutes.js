const express = require("express");
const router = express.Router();
const pool = require("../config/dbConfig");

router.get("/players-ranking", async (req, res) => {
  try {
    const query = `
      SELECT u.nickname, p.gold, u.id
      FROM users u
      JOIN player_data p ON u.id = p.user_id
      ORDER BY p.gold DESC
      LIMIT 10
    `;

    const [players] = await pool.query(query);

    res.json({ success: true, players });
  } catch (error) {
    console.error("Erro ao buscar ranking:", error);
    res.status(500).json({
      success: false,
      message: "Erro ao buscar ranking de jogadores",
      error: error.message,
    });
  }
});

module.exports = router;

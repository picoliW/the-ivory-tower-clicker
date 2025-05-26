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
        movespeed: 1,
        dps: 0,
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
  const {
    userId,
    damage,
    gold,
    gold_per_second,
    floor,
    dash_unlocked,
    movespeed,
    dps,
  } = req.body;

  try {
    await pool.query(
      `UPDATE player_data 
       SET damage = ?, gold = ?, gold_per_second = ?, floor = ?, dash_unlocked = ?, movespeed = ?, dps = ?
       WHERE user_id = ?`,
      [
        damage,
        gold,
        gold_per_second,
        floor,
        dash_unlocked,
        movespeed,
        dps,
        userId,
      ]
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
  const { nickname, email, password, confirmPassword } = req.body;

  if (!nickname || !email || !password || !confirmPassword) {
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
      "INSERT INTO users (nickname, email, password) VALUES (?, ?, ?)",
      [nickname, email, password]
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

router.get("/achievements/:userId", async (req, res) => {
  try {
    const userId = req.params.userId;

    const [achievements] = await pool.query(
      `
      SELECT 
        a.*,
        ua.unlocked,
        ua.completed
      FROM achievements a
      LEFT JOIN user_achievements ua ON a.id = ua.achievement_id AND ua.user_id = ?
    `,
      [userId]
    );

    res.status(200).json({
      success: true,
      achievements,
    });
  } catch (error) {
    console.error("Error fetching achievements:", error);
    res.status(500).json({
      success: false,
      message: "Error fetching achievements",
    });
  }
});

router.post("/claim-achievement", async (req, res) => {
  try {
    const { userId, achievementId } = req.body;

    const [result] = await pool.query(
      `
      UPDATE user_achievements 
      SET completed = TRUE 
      WHERE user_id = ? AND achievement_id = ? AND unlocked = TRUE AND completed = FALSE
    `,
      [userId, achievementId]
    );

    if (result.affectedRows === 0) {
      return res.status(400).json({
        success: false,
        message: "Achievement not found or not eligible for claiming",
      });
    }

    const [achievement] = await pool.query(
      "SELECT reward FROM achievements WHERE id = ?",
      [achievementId]
    );

    await pool.query(
      "UPDATE player_data SET gold = gold + ? WHERE user_id = ?",
      [achievement[0].reward, userId]
    );

    res.status(200).json({
      success: true,
      message: "Achievement claimed successfully",
      reward: achievement[0].reward,
    });
  } catch (error) {
    console.error("Error claiming achievement:", error);
    res.status(500).json({
      success: false,
      message: "Error claiming achievement",
    });
  }
});

router.post("/check-achievements", async (req, res) => {
  try {
    const { userId, playerData } = req.body;

    const [achievements] = await pool.query("SELECT * FROM achievements");
    const [player] = await pool.query(
      "SELECT * FROM player_data WHERE user_id = ?",
      [userId]
    );

    if (player.length === 0) {
      return res
        .status(404)
        .json({ success: false, message: "Player not found" });
    }

    const playerObj = player[0];
    const enemyData = {
      enemies_defeated: playerData.enemies_defeated || 0,
    };

    for (const achievement of achievements) {
      try {
        const conditionMet = evalAchievementCondition(
          achievement.condition_text,
          { ...playerObj, ...playerData },
          enemyData
        );

        if (conditionMet) {
          await pool.query(
            `INSERT INTO user_achievements (user_id, achievement_id, unlocked)
             VALUES (?, ?, TRUE)
             ON DUPLICATE KEY UPDATE unlocked = TRUE`,
            [userId, achievement.id]
          );
        }
      } catch (e) {
        console.error(`Error checking achievement ${achievement.id}:`, e);
      }
    }

    res.status(200).json({ success: true });
  } catch (error) {
    console.error("Error checking achievements:", error);
    res
      .status(500)
      .json({ success: false, message: "Error checking achievements" });
  }
});

function evalAchievementCondition(condition, player, enemyManager) {
  const evalGlobals = {
    player,
    enemy_manager: enemyManager,
    enemyManager: enemyManager,
  };

  for (const key in evalGlobals) {
    if (key.startsWith("_")) {
      delete evalGlobals[key];
    }
  }

  if (
    (condition.includes("enemy_manager") ||
      condition.includes("enemyManager")) &&
    !enemyManager
  ) {
    return false;
  }

  try {
    const evalFn = new Function(
      "player",
      "enemyManager",
      "enemy_manager",
      `return ${condition}`
    );
    return evalFn(player, enemyManager, enemyManager);
  } catch (e) {
    console.error("Error evaluating condition:", e);
    return false;
  }
}

module.exports = router;

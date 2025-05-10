const express = require("express");
const configureServer = require("./config/serverConfig");
const authRoutes = require("./routes/authRoutes");

const app = express();

configureServer(app);

app.use("/auth", authRoutes);

app.get("/", (req, res) => {
  res.send("Ta bombando");
});

module.exports = app;

const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const configureServer = (app) => {
  app.use(cors());
  app.use(bodyParser.json());
  app.use(bodyParser.urlencoded({ extended: true }));

  return app;
};

module.exports = configureServer;

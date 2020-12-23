const express = require('express');
const router = express.Router();

const authController = require("./auth");
const testController = require("./test");
const stockController = require("./stock");
const userController = require("./user");

router.use('/auth', authController);
router.use('/test', testController);
router.use('/stocks', stockController);
router.use('/users', userController);

module.exports = router;
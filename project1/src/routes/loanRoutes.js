const express = require("express");
const { createLoan, updateRepayment } = require("../controllers/loanController");
const router = express.Router();

router.post("/create", createLoan);
router.post("/repay", updateRepayment);

module.exports = router;

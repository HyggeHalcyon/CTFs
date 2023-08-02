const express = require("express");
const mongoose = require("mongoose");
const session = require("express-session");
const MongoStore = require("connect-mongo");
const path = require("path");
const fs = require("fs");
const {
    generatePDF,
    formatHTML
} = require("./pdf.js");
const {
    randomBytes,
    createHash
} = require("crypto");
const app = express();
const port = 3000;
// TODO: Configure loading from dotenv for production
const dbURI = "mongodb://dev:IHeardPassphrasesArePrettySecure@localhost/dev?authSource=admin&w=1";
app.use(express.json());
app.use(express.urlencoded({
    extended: false
}));
app.use(
    session({
        secret: randomBytes(32).toString("hex"),
        resave: false,
        saveUninitialized: true,
        store: MongoStore.create({
            mongoUrl: dbURI,
        }),
    })
);
app.use("/static", express.static(__dirname + "/assets"));
app.get("/", (req, res) => {
    return res.redirect("/login");
});
app.get("/api/products", async (req, res) => {
    if (!req.session.user) return res.json([]);
    const products = await mongoose.model("Product").find();
    return res.json(products);
});
app.get("/login", (req, res) => {
    if (req.session.user) return res.redirect("/stock");
    return res.sendFile(__dirname + "/templates/login.html");
});
app.post("/login", async (req, res) => {
    const {
        username,
        password
    } = req.body;
    if (!username || !password) return res.redirect("/login?error=login-error");
    // TODO: Implement hashing
    const user = await mongoose.model("User").findOne({
        username,
        password
    });
    if (!user) return res.redirect("/login?error=login-error");
    req.session.user = user.id;
    console.log(req.session);
    return res.redirect("/stock");
});
app.post("/api/order", async (req, res) => {
            if (!req.session.user) return res.json({});
        }
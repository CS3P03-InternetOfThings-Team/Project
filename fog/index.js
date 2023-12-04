import express from "express";
import multer from "multer";
import path from "path";
import { unlink } from "fs/promises";
import { getTextFromSpeech } from "./stt.js";

const app = express();
app.use(express.json({ limit: "1mb" }));

const handleFile = multer({ dest: path.join(process.cwd(), "uploads") });

app.use((req, res, next) => {
  console.log("Incoming Request:");
  console.log(`\tUser Agent: ${req.headers["user-agent"]}`);
  console.log(`\tIP: ${req.ip}`);
  next();
});

app.get("/", async (req, res) => {
  return res.status(200).json({ msg: "Hello World!" });
});

app.post("/uploads/audio", handleFile.single("audio"), async (req, res) => {
  const username = req.query.username;
  const timestamp = req.query.timestamp;
  const filePath = `./uploads/${req.file.filename}`;
  const audioText = await getTextFromSpeech({ filename: filePath });
  console.log(`\t\tFrom ${username} @ ${timestamp} seconds`);
  console.log(`\t\tDetected text: ${audioText}`);
  await unlink(filePath);
  return res.status(201).json({ msg: "Audio file uploaded successfully!" });
});

app.use((req, res, next) => {
  return res
    .status(404)
    .json({ msg: "Route not found. Did you type it correctly?" });
});

app.listen(3000, "0.0.0.0", () => {
  console.log(`Server listening at http://0.0.0.0:3000/`);
});

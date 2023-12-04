import type { NextApiRequest, NextApiResponse } from "next";
import nextConnect from "next-connect";
import refererMiddleware from "../__middlewares/referer";
import axios from "axios";

const handler = nextConnect();
handler.use(refererMiddleware);

export default handler.all(
  async (req: NextApiRequest, res: NextApiResponse) => {
    const api = `${process.env.IOT_API}/auth/session`;
    const token = req.headers.authorization;
    try {
      const { data, status } = await axios.get(
        api,
        {
          headers: {
            "Content-Type": "application/json",
            "Authorization": token
          },
        }
      );
      res.status(status).json(data);
    } catch (err: any) {
      console.log(err)
      res.status(err.response?.status || 500).json(err.response?.data);
    }
  }
);

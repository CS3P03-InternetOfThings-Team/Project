import type { NextApiRequest, NextApiResponse } from "next";
import nextConnect from "next-connect";
import refererMiddleware from "../__middlewares/referer";
import axios from "axios";

const handler = nextConnect();
handler.use(refererMiddleware);

export default handler.all(
  async (req: NextApiRequest, res: NextApiResponse) => {
    const api = `${process.env.IOT_API}/auth/user-login`;

    try {
      const { data, status } = await axios.post(
        api,
        req.body,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
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

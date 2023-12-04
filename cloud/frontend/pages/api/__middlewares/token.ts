import nextConnect from "next-connect";
import { NextApiRequest, NextApiResponse } from "next";

const tokenMiddleware = nextConnect();

tokenMiddleware.use(
  async (req: NextApiRequest, res: NextApiResponse, next) => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      res.status(401).json({ unauthorized: true });
    }
    req.headers['token'] = token? token : undefined;
    next();
  }
);

export default tokenMiddleware;

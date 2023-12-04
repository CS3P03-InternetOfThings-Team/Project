import nextConnect from "next-connect";
import { NextApiRequest, NextApiResponse } from "next";

const refererMiddleware = nextConnect();

refererMiddleware.use(
  async (req: NextApiRequest, res: NextApiResponse, next) => {
    // const allowedDomains = process.env.SS_ALLOWED_DOMAINS || "";

    // const referer = req.headers.referer;
    // if (
    //   !referer ||
    //   !allowedDomains.split(",").some((domain) => referer.includes(domain))
    // ) {
    //   res.status(401).json({ unauthorized: true });
    // }
    next();
  }
);

export default refererMiddleware;

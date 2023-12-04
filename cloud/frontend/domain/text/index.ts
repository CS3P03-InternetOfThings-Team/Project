import HttpContract from "../contracts/http.contract";

export interface IUseText {
  getTexts: (text: string, limit: number) => Promise<any>;
}

export const useText = (http: HttpContract): IUseText => {

  const getTexts = (text: string, limit=3) => {
    const req = {limit, text}
    return http.post("/api/text-storage/get-texts", req);
  };

  return {
    getTexts
  };
};

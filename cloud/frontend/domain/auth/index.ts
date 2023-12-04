import HttpContract from "../contracts/http.contract";
// import { registerData } from "./register.interface";

export interface IUseAuth {
  authenticate: (user: any) => Promise<any>;
  getSession: () => Promise<any>;
}

export const useAuth = (http: HttpContract): IUseAuth => {

  const getSession = () => {
    return http.post("/api/auth/get-session", {});
  };

  const authenticate = async (user: {email: string, password: string}) => {
    return http.post("/api/auth/authentication", {
      ...user,
    });
  };

  return {
    authenticate,
    getSession
  };
};

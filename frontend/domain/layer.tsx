
import React, { createContext, ReactNode, useContext, useEffect, useState } from "react";
import HttpContract from "./contracts/http.contract";
import { IUseAuth, useAuth as appAuthorization } from "./auth";
import { IUseText, useText  as appText } from "./text";


interface ApplicationDeps {
  http: HttpContract;
  children: ReactNode;
}

interface IApplicationContext {
  auth?: IUseAuth;
  text?: IUseText;
  session?: any;
}

const ApplicationContext = createContext<IApplicationContext>({});

const AppProvider = ({ http, children }: ApplicationDeps) => {
  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState(null);

  const auth = appAuthorization(http);
  const text = appText(http);


  const getSession = async () => {
   const tokenFound = localStorage.getItem('access_token');
   if (!tokenFound) {
    setLoading(false);
    return;
   }
   const { data, error } = await auth.getSession();
   if (error){
    setLoading(false);
    return;
   }
   setSession(data)
   setLoading(false)
  }

  useEffect(() => {
    getSession()
  }, [])

  return (
    <ApplicationContext.Provider
      value={{ auth, session, text }}
    >
      {  
        !loading && children 
      }
    </ApplicationContext.Provider>
  );
};

export const useSession = (): any => {
  const sesion = useContext(ApplicationContext).session;
  return sesion;
}

export const useAuth = (): IUseAuth => {
  const auth = useContext(ApplicationContext).auth;
  if (!auth) {
    throw new Error("You must use useAuth inside ApplicationContext!");
  }
  return auth;
};

export const useText = (): IUseText => {
  const text = useContext(ApplicationContext).text;
  if(!text){
    throw new Error("You must use useAuth inside ApplicationContext!");
  }
  return text;
}

// export const useApp = (): IUseApp => {
//   const app = useContext(ApplicationContext).app;
//   if (!app) {
//     throw new Error("You must use useAuth inside ApplicationContext!");
//   }
//   return app;
// };

// export const useDocs = (): IUseDocs => {
//   const docs = useContext(ApplicationContext).docs;
//   if (!docs) {
//     throw new Error("You must use useAuth inside ApplicationContext!");
//   }
//   return docs;
// };

// export const useLoading = (): IUseLoading => {
//   const load = useContext(ApplicationContext).load;
//   if (!load) {
//     throw new Error("You must use useLoading inside ApplicationContext!");
//   }
//   return load;
// };

// export const useModal = (size?: "xl" | "lg" | "sm"): modalControls => {
//   const modal = useContext(ApplicationContext).modal;
//   if (!modal) {
//     throw new Error("You must use useModal inside ApplicationContext!");
//   }
//   return modal;
// };

// export const useAlert = (): IUseAlert["createAlert"] => {
//   const alert = useContext(ApplicationContext).alert;
//   if (!alert) {
//     throw new Error("You must use useAlert inside ApplicationContext!");
//   }
//   return alert;
// };

export default AppProvider;

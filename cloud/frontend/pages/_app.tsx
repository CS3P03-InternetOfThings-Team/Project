import "../styles/globals.css";
import type { AppProps } from "next/app";
import JSX from "next";
import ThemeProviderWrapper from "../theme/ThemeProvider";
import AppProvider from "../domain/layer";
import { useRouter } from "next/router";
import HttpInstance from "../infraestructure/http/axios/index"

export default function App({ Component, pageProps }: AppProps): JSX.Element {
  const router = useRouter();

  const http = new HttpInstance("", {
    locale: router.locale || "es"
  });
  
  return (
    <AppProvider http={http}>
      <ThemeProviderWrapper>
        <Component {...pageProps} />;
      </ThemeProviderWrapper>
    </AppProvider>
  )
}

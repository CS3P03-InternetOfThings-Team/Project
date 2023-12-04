import HttpContract, {
  HttpResponseContract,
} from "../../../domain/contracts/http.contract";
import axios, { AxiosInstance } from "axios";

export default class httpAxiosInstance implements HttpContract {
  private axiosInstance: AxiosInstance;
  baseHeaders: object;

  constructor(url: string, extraHeader?: { [key: string]: string }) {
    const baseHeaders = { Accept: "application/json", ...extraHeader };
    this.baseHeaders = baseHeaders;
    this.axiosInstance = axios.create({
      baseURL: url,
      headers: baseHeaders,
    });

    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem("access_token");
        config.headers['Authorization'] = token? token : undefined;
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }

  public async get(
    path: string,
    headers?: object
  ): Promise<HttpResponseContract> {
    const { data } = await this.axiosInstance
      .get(path, headers)
      .catch(({ response }) => ({
        data: {
          status: response.status,
          error: response.data || response.statusText,
        },
      }));
    return data;
  }

  public async post(
    path: string,
    body: object,
    headers: object
  ): Promise<HttpResponseContract> {
    const response = await this.axiosInstance
      .post(path, body, headers)
      .catch(({ response }) =>
        response
          ? {
              status: response.status,
              error: response.data || response.statusText,
            }
          : { status: undefined, error: {} }
      );

    return response;
  }
}

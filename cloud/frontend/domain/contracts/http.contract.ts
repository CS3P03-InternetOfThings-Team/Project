export interface HttpResponseContract {
  data?: any;
  status: number;
  error?: any;
}

interface HttpContract {
  get(path: string, headers?: object): Promise<HttpResponseContract>;
  post(
    path: string,
    body: object,
    headers?: object
  ): Promise<HttpResponseContract>;
}

export default HttpContract;

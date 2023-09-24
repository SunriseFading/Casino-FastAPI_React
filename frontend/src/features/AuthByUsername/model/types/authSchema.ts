export interface AuthSchema {
  username: string;
  password: string;
  isLoading: boolean;
  error?: string;
}

export interface AuthResponse {
  id: string;
  access_token: string;
  username: string;
}

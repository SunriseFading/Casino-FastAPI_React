export interface AuthSchema {
  username: string;
  password: string;
  isLoading: boolean;
  error?: string;
}

export interface AuthResponse {
  id: string;
  accessToken: string;
  username: string;
}

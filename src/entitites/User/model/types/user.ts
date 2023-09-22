export interface User {
  id: string;
  username: string;
  tokens: Token;
}

export interface Token {
  accessToken: string;
  refreshToken: string;
}

export interface UserSchema {
  authData?: User;
}

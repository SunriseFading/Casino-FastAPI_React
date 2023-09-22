export interface User {
  id: string;
  username: string;
  accessToken: string
}

export interface UserSchema {
  authData?: User;
}

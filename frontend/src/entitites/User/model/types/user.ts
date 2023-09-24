export interface User {
  id: string;
  username: string;
  access_token: string
}

export interface UserSchema {
  authData?: User;
}

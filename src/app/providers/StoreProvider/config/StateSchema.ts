import { UserSchema } from 'entitites/User';
import { AuthSchema } from 'features/AuthByUsername';

export interface StateSchema {
  user: UserSchema;
  authForm?: AuthSchema;
}

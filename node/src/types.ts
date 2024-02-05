export interface User {
    identifier: string;
    email: string;
    verifiedEmail: boolean;
    displayName: string;
    roleNames: string[];
    password: string | null;
  }
  
export type APIUser = {
    loginId: string;
    email: string;
    displayName: string;
    verifiedEmail: boolean;
    hashedPassword?: {
        django: {
            hash: string;
        }
    }
}
  
export type UserResponse = {
    loginIds: string[];
    userId: string;
    name: string;
    email: string;
    phone: string;
    verifiedEmail: boolean;
    verifiedPhone: boolean;
    roleNames: string[];
    userTenants: string[];
    status: string;
    externalIds: string[];
    picture: string;
    test: boolean;
    customAttributes: Record<string, any>;
    createdTime: number;
    TOTP: boolean;
    SAML: boolean;
    OAuth: Record<string, any>;
    webauthn: boolean;
    password: boolean;
    ssoAppIds: string[];
    givenName: string;
    middleName: string;
    familyName: string;
};

export enum Status {
    enabled = 'enabled',
    disabled = 'disabled',
    invited = 'invited'
}
  
export type CreatedUserMap = {
    userId: string;
    email: string;
}  
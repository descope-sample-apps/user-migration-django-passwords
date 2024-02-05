import { APIUser, UserResponse, User, Status } from "./types";

const getBearer = () => {

  if (process.env.DESCOPE_PROJECT_ID === undefined) {
    throw new Error('DESCOPE_PROJECT_ID is not defined');
  }
  
  if (process.env.DESCOPE_MANAGEMENT_KEY === undefined) {
    throw new Error('DESCOPE_MANAGEMENT_KEY is not defined');
  }
  
  const bearer = `Bearer ${process.env.DESCOPE_PROJECT_ID}:${process.env.DESCOPE_MANAGEMENT_KEY}`;
  return bearer;
}
export const createUser = async (user: User) => {
    let body: APIUser = {
      loginId: user.email,
      email: user.email,
      displayName: user.displayName,
      verifiedEmail: user.verifiedEmail,
    }
  
    if (user.password) {
      body.hashedPassword = {
        django: {
          hash: user.password
        }
      }
    }
  
    try {
      const res = await fetch('https://api.descope.com/v1/mgmt/user/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': getBearer()
        },
        body: JSON.stringify(body)
      });
      
      const data = await res.json();
      if (data.errorCode) {
        console.error(data);
        return;
      }
      const createdUser: UserResponse = data.user;
      return createdUser;
    }
   catch (e) {
    console.error("Error creating user: ", e);
  }

}

export const updateUserStatus = async (loginId: string, status: Status) => {
  const body = {
    loginId,
    status
  }
  try {
    const res = await fetch('https://api.descope.com/v1/mgmt/user/update/status', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': getBearer()
      },
      body: JSON.stringify(body)
    });
    
    const data = await res.json();
    if (data.errorCode) {
      console.error(data);
      return;
    }
    const updateUser: UserResponse = data.user;
    return updateUser;
  }
  catch (e) {
    console.error("Error updating user status: ", e);
  }
}

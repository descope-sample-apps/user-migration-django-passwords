import fs from 'fs';
import * as csv from 'fast-csv';
import { CreatedUserMap, Status, User } from './types';
import { createUser, updateUserStatus } from './helpers';
import dotenv from 'dotenv';
dotenv.config();


function writeCSV(filePath: string, data: CreatedUserMap[]) {
  const ws = fs.createWriteStream(filePath);
  csv
    .write(data, { headers: true })
    .pipe(ws);
}

async function processCSV(filePath: string) {
  const importedMappedUsers: CreatedUserMap[] = [];

  const stream = fs.createReadStream(filePath).pipe(csv.parse({ headers: true }));
  for await (const data of stream) {
    data.verifiedEmail = data.verifiedEmail === 'TRUE';
    if (data.password === '') data.password = null;
    try {
        data.roleNames = JSON.parse(data.roleNames);
    } catch (error) {
        data.roleNames = [];
    }
    const user: User = data;
    try {
      const createdUser = await createUser(user);
      if (createdUser) {
        console.log("Created User:", createdUser)
        const createdUserMap: CreatedUserMap = {
          userId: createdUser.userId,
          email: createdUser.email
        }
        importedMappedUsers.push(createdUserMap);

        const updatedUser = await updateUserStatus(createdUser.email, Status.enabled);
        console.log("Updated User:", updatedUser);
      }
    } catch (error) {
      console.error("Error creating user: ", error);
    }
  }
  console.log("Mapped users:");
  console.log(importedMappedUsers);

  writeCSV('src/export/imported_users.csv', importedMappedUsers);
} 

processCSV('src/sample_exported_users.csv').catch(console.error);
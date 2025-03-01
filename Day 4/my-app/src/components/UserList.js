import React, { useEffect, useState } from "react";
import { getUsers } from "../api/userApi";
const UserList = ()  => {
 const [users, setUsers] = useState([]);
 useEffect( ()  => {
 const fetchUsers = async () => {
 const token = localStorage.getItem( "token");
 if (!token) {
 window.location.href = "/login";
 return;
 }
 try {
 const response = await getUsers(token);
 setUsers(response.data);
} catch (error) {
    console.error( "Failed to fetch users:", error);
    }
    };
    fetchUsers();
    }, []);
    return (
    <div>
    <h2>User List</h2>
    <ul>
    {users.map((user) => (
    <li key={user._id}>{user.name} - {user.email}</li>
    ))}
    </ul>
    </div>
    );
    };
    export default UserList;
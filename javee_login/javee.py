class LoginSystem:
    # Sample users stored in a dictionary (in a real system, this would be in a database)
    _users = {
        "admin": "admin123",
        "user1": "password1",
        "guest": "guestpass"
    }

    def login(self, username: str, password: str) -> bool:
        """
        Attempts to log in a user with given credentials
        Args:
            username: The username to check
            password: The password to verify
        Returns:
            bool: True if login is successful, False otherwise
        """
        # Check if inputs are valid
        if not username or not password or username.strip() == "" or password.strip() == "":
            print("Username and password cannot be empty")
            return False

        # Check if username exists and password matches
        if username in self._users and self._users[username] == password:
            print(f"Login successful! Welcome, {username}")
            return True

        # No match found
        print("Invalid username or password")
        return False

# Example usage
if __name__ == "__main__":
    login_system = LoginSystem()

    # Test cases
    login1 = login_system.login("admin", "admin123")  # Should succeed
    login2 = login_system.login("user1", "password1")  # Should succeed
    login3 = login_system.login("", "")              # Should fail
package System;

public class User {
    private final String UserName;
    private final String Password;

    public User(String UserName, String Password) {
        this.UserName = UserName;
        this.Password = Password;
    }
    public void Print() {
        System.out.println(UserName);
        System.out.println(Password);
    }
    public boolean Login() {
        return UserName.equals("root") && Password.equals("123456");
    }

    public boolean Register() {
        return !UserName.equals("root") && !Password.equals("123456");
    }
}

package System;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * 数据库常用操作
 */
public class DB{

    private Connection con;
    private boolean error;
    private String error_inf;

    /**
     * 构造函数
     * @param database 数据库
     *
     * */
    public DB(String database) {
        try {

            Class.forName("com.mysql.cj.jdbc.Driver");
            con = DriverManager.getConnection("jdbc:mysql://182.92.221.222:3306/" + database,"root", "CS1806se.");
            this.error = false;

        } catch (Exception e) {

            this.error = true;
            this.error_inf = e.getMessage();

        }

    }
    /**
     * 执行一个查询语句并返回结果
     * @return ArrayList<Map<String, String>>
     * @param sql sql语句
     * */
    public ArrayList<Map<String, String>> Select(String sql) {

        ArrayList<Map<String, String>> arr = new ArrayList<>();
        Statement stmt;
        ResultSet res;
        ResultSetMetaData rsmd;

        try {
            stmt = con.createStatement();
            res = stmt.executeQuery(sql);
            rsmd = res.getMetaData();
            //遍历结果集
            while (res.next()) {
                //System.out.println("结果集列数:" + rsmd.getColumnCount());
                Map<String, String> temp = new HashMap<>();
                for (int i = 1; i <= rsmd.getColumnCount(); i++) {
                    temp.put(rsmd.getColumnName(i), res.getString(i));
                }
                arr.add(temp);
            }
            res.close();
            stmt.close();
            this.error = false;
            return arr;

        } catch (Exception e) {
            this.error = true;
            this.error_inf = e.getMessage();
            return arr;
        }
    }
    /**
     * 执行一个更新语句并返回布尔值
     * @return boolean
     * @param sql sql语句
     * */
    public boolean Update(String sql) {

        Statement stmt;

        try {

            stmt = con.createStatement();
            stmt.executeUpdate(sql);
            stmt.close();
            this.error = false;

        } catch (Exception e) {
            this.error = true;
            this.error_inf = e.getMessage();
            return false;
        }
        return true;
    }
    public boolean Error() {
        return this.error;
    }
    public String ErrorInf() {
        return this.error_inf;
    }

    /**
     *上传图片文件
     * @param path 要上传的文件在本地的路径
     * @param filename 上传的文件以filename命名存储在数据库
     * @return boolean 上传是否成功
     */
    public boolean Upload_Picture(String path, String filename) {
        try {
            String sql = "insert into picture(filename, data) value(?, ?)";
            PreparedStatement ps = con.prepareStatement(sql);
            File picture = new File(path);
            FileInputStream stream = new FileInputStream(picture);
            ps.setBinaryStream(2, stream);
            ps.setString(1, filename);
            ps.executeUpdate();
            return true;
        } catch (SQLException | FileNotFoundException e) {
            this.error = true;
            this.error_inf = e.getMessage();
            return false;
        }
    }

    /**
     *上传音频文件
     * @param path 要上传的文件在本地的路径
     * @param filename 上传的文件以filename命名存储在数据库
     * @return boolean 上传是否成功
     */
    public boolean Upload_Audio(String path, String filename) {
        try {
            String sql = "insert into audio(filename, data) value(?, ?)";
            PreparedStatement ps = con.prepareStatement(sql);
            File audio = new File(path);
            FileInputStream stream = new FileInputStream(audio);
            ps.setBinaryStream(2, stream);
            ps.setString(1, filename);
            ps.executeUpdate();
            return true;
        } catch (SQLException | FileNotFoundException e) {
            this.error = true;
            this.error_inf = e.getMessage();
            return false;
        }
    }

    /**
     * 从数据库下载图片
     * @param filename 数据库中的文件名
     * @return InputStream 以二进制流形式返回
     */
    public InputStream Download_Picture(String filename) {
        InputStream istream = null;
        try {
            String sql = "select * from picture where filename = ?;";
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, filename);
            ps.executeQuery();
            ResultSet rs = ps.getResultSet();
            if (rs.next()) {
                istream = rs.getBinaryStream("data");
            }
        } catch (SQLException e) {
            System.out.println("下载错误:1");
            e.printStackTrace();
        }
        return istream;
    }

    /**
     * 从数据库下载音频
     * @param filename 数据库中的文件名
     * @return InputStream 以二进制流形式返回
     */
    public InputStream Download_Audio(String filename) {
        InputStream istream = null;
        try {
            String sql = "select * from audio where filename = ?;";
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, filename);
            ps.executeQuery();
            ResultSet rs = ps.getResultSet();
            if (rs.next()) {
                istream = rs.getBinaryStream("data");
            }
        } catch (SQLException e) {
            System.out.println("下载错误:1");
            e.printStackTrace();
        }
        return istream;
    }

    /**
     * 关闭连接
     */
    public void Close() {
        if (con != null) {
            try {
                con.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}

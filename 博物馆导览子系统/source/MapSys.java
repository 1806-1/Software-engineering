package Servlet;

import System.*;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.catalina.filters.ExpiresFilter;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Map;

@WebServlet("/MapSys")
public class MapSys extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        JSONObject JR = new JSONObject();
        DB ExhibitionDB = null;
        try {
            String MuseumName = request.getParameter("MuseumName");
            ExhibitionDB = new DB("MUSEUM");
            if (ExhibitionDB.Error()) {
                JR.put("STATUS", "001");
                JR.put("Error", "ExhibitionDB connection Error!");
                throw new Exception(JR.getString("Error"));
            }

            String sql = "select * from MUSEUM.overview where bwgname='" + MuseumName + "';";
            ArrayList<Map<String, String>> res = ExhibitionDB.Select(sql);
            System.out.println(res.size());
            if (res.size() != 1) {
                JR.put("STATUS", "002");
                JR.put("Error", "The number of Exhibition is not 1!");
                throw new Exception(JR.getString("Error"));
            }
            JR.put("exhname", res.get(0).get("exhname"));
            JR.put("photo", res.get(0).get("photo"));
            JR.put("museumName", res.get(0).get("museumName"));
            JR.put("time", res.get(0).get("time"));
            JR.put("introduction", res.get(0).get("introduction"));
            JR.put("id", res.get(0).get("id"));
            JR.put("jingwei", res.get(0).get("jingwei"));
            JR.put("STATUS", "0");
            JR.put("Error", "");


        } catch (Exception e) {
            System.out.println(e.getMessage());
        } finally {
            response.setHeader("Content-Type", "text/html;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");
            try (PrintWriter pw = response.getWriter()) {
                pw.write(JSON.toJSONString(JR));
            } catch (Exception e) {
                System.out.println("Unknown Error!");
            }
            if (ExhibitionDB != null) {
                ExhibitionDB.Close();
            }
            System.out.println("doGet !");
        }
    }
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) {
        JSONObject JR = new JSONObject();
        DB ExhibitionDB = null;
        try {
            String MuseumName = request.getParameter("MuseumName");
            ExhibitionDB = new DB("MUSEUM");
            if (ExhibitionDB.Error()) {
                JR.put("STATUS", "001");
                JR.put("Error", "ExhibitionDB connection Error!");
                throw new Exception(JR.getString("Error"));
            }

            String sql = "select * from MUSEUM.overview where bwgname='" + MuseumName + "';";
            ArrayList<Map<String, String>> res = ExhibitionDB.Select(sql);
            System.out.println(res.size());
            if (res.size() != 1) {
                JR.put("STATUS", "002");
                JR.put("Error", "The number of Exhibition is not 1!");
                throw new Exception(JR.getString("Error"));
            }
            JR.put("photo", res.get(0).get("photo"));
            JR.put("museumName", res.get(0).get("museumName"));
            JR.put("time", res.get(0).get("time"));
            JR.put("introduction", res.get(0).get("introduction"));
            JR.put("id", res.get(0).get("id"));
            JR.put("jingwei", res.get(0).get("jingwei"));
            JR.put("STATUS", "0");
            JR.put("Error", "");


        } catch (Exception e) {
            System.out.println(e.getMessage());
        } finally {
            response.setHeader("Content-Type", "text/html;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");
            try (PrintWriter pw = response.getWriter()) {
                pw.write(JSON.toJSONString(JR));
            } catch (Exception e) {
                System.out.println("Unknown Error!");
            }
            if (ExhibitionDB != null) {
                ExhibitionDB.Close();
            }
            System.out.println("doGet !");
        }
    }
}